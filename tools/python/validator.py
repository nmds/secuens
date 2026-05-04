"""
Secuens Specification Validator — Test Cases (Python)
Version: 0.9.1
License: MIT

Validates that a Secuens parser correctly handles all cases defined
in the Secuens v0.9.1 specification. Run this against any parser
implementation to verify compliance.

Usage:
    python validator.py

Output:
    PASS — the parser behaved as expected
    FAIL — the parser returned an unexpected result

Each test case is labelled:
    VALID   — the parser MUST recognize this as a cue
    INVALID — the parser MUST NOT recognize this as a cue
    WARN    — the parser MUST parse this but SHOULD emit a warning

Exit code:
    0 — all tests passed
    1 — one or more tests failed

Note: validator.py expects parser.py to be in the same directory,
or adjust the path in sys.path.insert below.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from parser import SecuensParser


# ---------------------------------------------------------------------------
# Test Definition
# ---------------------------------------------------------------------------

class TestCase:
    def __init__(self, category, label, input_line, expect_cue=None, expect_warning_contains=None, description=""):
        self.category = category          # "VALID" | "INVALID" | "WARN"
        self.label = label
        self.input_line = input_line
        self.expect_cue = expect_cue      # dict of expected cue fields, or None
        self.expect_warning_contains = expect_warning_contains  # substring to find in warnings
        self.description = description


TEST_CASES = [

    # -------------------------------------------------------------------------
    # CORE SYNTAX — Valid forms
    # -------------------------------------------------------------------------

    TestCase("VALID", "minimal form",
        "SQ (cue 5): Door slams shut",
        expect_cue={"cue_type": "SQ", "label": "cue", "number": "5", "description": "Door slams shut"},
        description="Minimal valid cue — type, number, description"
    ),

    TestCase("VALID", "with trigger on",
        'LX (cue 12) on "Juliet": Fade to blackout',
        expect_cue={"cue_type": "LX", "trigger_keyword": "on", "trigger_value": '"Juliet"'},
        description="Dialogue trigger with quotes"
    ),

    TestCase("VALID", "with trigger after",
        "SQ (cue 3) after 2s: Thunder crash",
        expect_cue={"trigger_keyword": "after", "trigger_value": "2s"},
        description="Time delay trigger"
    ),

    TestCase("VALID", "with trigger with",
        "SQ (cue 3) with door slam: Crash",
        expect_cue={"trigger_keyword": "with", "trigger_value": "door slam"},
        description="Action trigger — free-form text"
    ),

    TestCase("VALID", "custom trigger keyword",
        "LX (cue 5) before curtain: Fade",
        expect_cue={"trigger_keyword": "before", "trigger_value": "curtain"},
        description="Custom trigger keyword — must be accepted"
    ),

    TestCase("VALID", "with metadata only",
        "LX (cue 5) [fade=3s]: Fade to blackout",
        expect_cue={"metadata": {"fade": "3s"}},
        description="Metadata without trigger"
    ),

    TestCase("VALID", "with trigger and metadata",
        'LX (cue 5) on "Juliet" [fade=3s, warn=30s]: Fade to blackout',
        expect_cue={"trigger_keyword": "on", "metadata": {"fade": "3s", "warn": "30s"}},
        description="Trigger + metadata — full cue"
    ),

    TestCase("VALID", "multiple metadata pairs",
        'SQ (cue 2) [file="thunder.wav", level=-3dB]: Thunder crash',
        expect_cue={"metadata": {"file": "thunder.wav", "level": "-3dB"}},
        description="Multiple metadata pairs with quoted string and dB value"
    ),

    TestCase("VALID", "metadata comma without space",
        "LX (cue 5) [fade=3s,level=80%]: Fade",
        expect_cue={"metadata": {"fade": "3s", "level": "80%"}},
        description="Comma without trailing space — MUST be accepted"
    ),

    TestCase("VALID", "hidden cue in boneyard",
        "[[SQ (cue 1) [file=\"ambience.wav\", loop=true]: Background ambience]]",
        expect_cue={"hidden": True, "cue_type": "SQ"},
        description="Fountain boneyard hidden cue"
    ),

    TestCase("VALID", "forced action prefix",
        "!SQ (cue 5): Door slams shut",
        expect_cue={"cue_type": "SQ", "description": "Door slams shut"},
        description="Fountain forced action prefix — must be stripped before parsing"
    ),

    # NUMBER patterns
    TestCase("VALID", "number pattern A — plain",
        "LX (cue 10): Lights up",
        expect_cue={"number": "10"},
        description="Pattern A: plain integer"
    ),

    TestCase("VALID", "number pattern A — letter suffix",
        "LX (cue 5a): Insert cue",
        expect_cue={"number": "5a"},
        description="Pattern A: letter suffix"
    ),

    TestCase("VALID", "number pattern A — multi-letter suffix",
        "LX (cue 5ab): Insert cue",
        expect_cue={"number": "5ab"},
        description="Pattern A: multi-letter suffix"
    ),

    TestCase("VALID", "number pattern B — decimal",
        "LX (cue 5.5): Insert cue",
        expect_cue={"number": "5.5"},
        description="Pattern B: decimal notation"
    ),

    TestCase("VALID", "number pattern C — prefixed",
        "LX (cue A5): Prefixed cue",
        expect_cue={"number": "A5"},
        description="Pattern C: uppercase prefix"
    ),

    TestCase("VALID", "number pattern C — prefixed with suffix",
        "LX (cue A5a): Prefixed with suffix",
        expect_cue={"number": "A5a"},
        description="Pattern C: uppercase prefix with letter suffix"
    ),

    # LABEL flexibility
    TestCase("VALID", "label: shot",
        "CAMERA (shot 3): Close-up on actor",
        expect_cue={"label": "shot"},
        description="CAMERA using 'shot' label"
    ),

    TestCase("VALID", "label: setup",
        "LIGHT (setup 2): Key from left",
        expect_cue={"label": "setup"},
        description="LIGHT using 'setup' label"
    ),

    TestCase("VALID", "label: take",
        "SOUND (take 1): Boom from above",
        expect_cue={"label": "take"},
        description="SOUND using 'take' label"
    ),

    TestCase("VALID", "label: q",
        "LX (q 7): Lights change",
        expect_cue={"label": "q"},
        description="Short label 'q'"
    ),

    # Whitespace flexibility
    TestCase("VALID", "no space before paren",
        "SQ(cue 5): Door slams",
        expect_cue={"cue_type": "SQ", "number": "5"},
        description="No space before opening parenthesis — valid"
    ),

    TestCase("VALID", "extra space inside parens",
        "SQ (cue  5): Door slams",
        expect_cue={"number": "5"},
        description="Extra space between LABEL and NUMBER — valid"
    ),

    TestCase("VALID", "extra spaces between components",
        "SQ  (cue 5):  Door slams",
        expect_cue={"description": "Door slams"},
        description="Extra spaces between components — valid"
    ),

    # Metadata value types
    TestCase("VALID", "descriptive time value unquoted",
        "LX (cue 5) [fade=slow]: Fade",
        expect_cue={"metadata": {"fade": "slow"}},
        description="Descriptive time value without quotes"
    ),

    TestCase("VALID", "descriptive time value quoted",
        'LX (cue 5) [fade="slow"]: Fade',
        expect_cue={"metadata": {"fade": "slow"}},
        description="Descriptive time value with quotes — both valid"
    ),

    TestCase("VALID", "boolean true",
        "SQ (cue 1) [loop=true]: Ambience",
        expect_cue={"metadata": {"loop": "true"}},
        description="Boolean true value"
    ),

    TestCase("VALID", "boolean false",
        "SQ (cue 1) [loop=false]: Ambience",
        expect_cue={"metadata": {"loop": "false"}},
        description="Boolean false value"
    ),

    TestCase("VALID", "level in percent",
        "LX (cue 1) [level=80%]: Fade",
        expect_cue={"metadata": {"level": "80%"}},
        description="Level as percentage"
    ),

    TestCase("VALID", "level in dB",
        "SQ (cue 1) [level=-6dB]: Sound",
        expect_cue={"metadata": {"level": "-6dB"}},
        description="Level in decibels"
    ),

    TestCase("VALID", "uppercase value preserved",
        "CAMERA (shot 1) [frame=CU]: Close-up",
        expect_cue={"metadata": {"frame": "CU"}},
        description="Uppercase metadata value preserved"
    ),

    TestCase("VALID", "mixed-case target preserved",
        "CAMERA (shot 1) [target=Cam2]: Switch",
        expect_cue={"metadata": {"target": "Cam2"}},
        description="Mixed-case metadata value preserved"
    ),

    TestCase("VALID", "time units — milliseconds",
        "LX (cue 1) [fade=500ms]: Snap",
        expect_cue={"metadata": {"fade": "500ms"}},
        description="Millisecond time unit"
    ),

    TestCase("VALID", "time units — hours",
        "SQ (cue 1) [duration=2h]: Long fade",
        expect_cue={"metadata": {"duration": "2h"}},
        description="Hour time unit"
    ),

    TestCase("VALID", "custom metadata key",
        "CAMERA (shot 1) [mykey=myvalue]: Custom",
        expect_cue={"metadata": {"mykey": "myvalue"}},
        description="Custom metadata keys always allowed"
    ),

    TestCase("VALID", "long cuetype",
        "GRAPHICS (cue 1): Display title",
        expect_cue={"cue_type": "GRAPHICS"},
        description="Multi-letter CUETYPE"
    ),

    # -------------------------------------------------------------------------
    # INVALID forms — must NOT be recognized as cues
    # -------------------------------------------------------------------------

    TestCase("INVALID", "lowercase cuetype",
        "sq (cue 1): Door slams",
        description="Lowercase CUETYPE — invalid"
    ),

    TestCase("INVALID", "mixed-case cuetype",
        "Sq (cue 1): Door slams",
        description="Mixed-case CUETYPE — invalid"
    ),

    TestCase("INVALID", "missing cue number",
        "SQ: Door slams",
        description="Missing (LABEL NUMBER) block — invalid"
    ),

    TestCase("INVALID", "missing cuetype",
        "(cue 5): Door slams",
        description="Missing CUETYPE — invalid"
    ),

    TestCase("INVALID", "label-number no space",
        "SQ (cue5): Door slams",
        description="No space between LABEL and NUMBER — invalid"
    ),

    TestCase("WARN", "dialogue trigger without quotes",
        "LX (cue 5) on Juliet: Fade",
        expect_cue={"cue_type": "LX"},
        expect_warning_contains=None,
        description="Unquoted dialogue trigger — ambiguous, spec says quotes MUST be used."
    ),

    TestCase("INVALID", "normal action line",
        "John walks to the door.",
        description="Plain text — not a cue"
    ),

    TestCase("INVALID", "cue reference in dialogue",
        "Stand by for sound cue 5.",
        description="Cue reference in text — not a cue definition"
    ),

    TestCase("INVALID", "missing colon",
        "SQ (cue 5) Door slams",
        description="Missing colon separator — invalid"
    ),

    # -------------------------------------------------------------------------
    # WARN — Valid cues that should generate warnings
    # -------------------------------------------------------------------------

    TestCase("WARN", "missing description",
        "LX (cue 5):",
        expect_cue={"cue_type": "LX", "number": "5", "description": ""},
        expect_warning_contains="Missing description",
        description="Parser MAY accept as placeholder, SHOULD warn"
    ),

    TestCase("WARN", "trigger keyword without value",
        "LX (cue 5) on: Fade",
        expect_warning_contains="no value",
        description="Trigger keyword without value — should warn"
    ),

    TestCase("WARN", "time value without units",
        "LX (cue 5) [fade=3]: Fade",
        expect_warning_contains="missing units",
        description="Numeric time value without units — MUST warn"
    ),

]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_tests(parser: SecuensParser) -> tuple[int, int, int]:
    passed = 0
    failed = 0
    skipped = 0

    print("Secuens Specification Validator — v0.9.1")
    print("=" * 60)
    print()

    for tc in TEST_CASES:
        result = parser.parse_text(tc.input_line)
        cues = result.cues
        warnings = result.warnings

        if tc.category == "VALID":
            if not cues:
                print(f"  ✗ FAIL [{tc.category}] {tc.label}")
                print(f"       Input: {tc.input_line}")
                print(f"       Expected: cue found")
                print(f"       Got: no cue parsed")
                failed += 1
                continue

            cue = cues[0]
            field_fail = False
            if tc.expect_cue:
                for field_name, expected_value in tc.expect_cue.items():
                    actual = getattr(cue, field_name, None)
                    if actual != expected_value:
                        print(f"  ✗ FAIL [{tc.category}] {tc.label}")
                        print(f"       Input: {tc.input_line}")
                        print(f"       Field '{field_name}': expected {expected_value!r}, got {actual!r}")
                        failed += 1
                        field_fail = True
                        break

            if not field_fail:
                print(f"  ✓ PASS [{tc.category}] {tc.label}")
                passed += 1

        elif tc.category == "INVALID":
            if cues:
                print(f"  ✗ FAIL [{tc.category}] {tc.label}")
                print(f"       Input: {tc.input_line}")
                print(f"       Expected: no cue")
                print(f"       Got: {cues[0]}")
                failed += 1
            else:
                print(f"  ✓ PASS [{tc.category}] {tc.label}")
                passed += 1

        elif tc.category == "WARN":
            if tc.expect_cue and not cues:
                print(f"  ✗ FAIL [{tc.category}] {tc.label}")
                print(f"       Input: {tc.input_line}")
                print(f"       Expected: cue + warning")
                print(f"       Got: no cue at all")
                failed += 1
                continue

            if tc.expect_warning_contains:
                warning_texts = [w.message.lower() for w in warnings]
                if any(tc.expect_warning_contains.lower() in w for w in warning_texts):
                    print(f"  ✓ PASS [{tc.category}] {tc.label}")
                    passed += 1
                else:
                    print(f"  ✗ FAIL [{tc.category}] {tc.label}")
                    print(f"       Input: {tc.input_line}")
                    print(f"       Expected warning containing: '{tc.expect_warning_contains}'")
                    print(f"       Got warnings: {[w.message for w in warnings]}")
                    failed += 1
            else:
                print(f"  ✓ PASS [{tc.category}] {tc.label}")
                passed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    print(f"Total: {len(TEST_CASES)} test cases")
    return passed, failed, skipped


def main():
    parser = SecuensParser()
    passed, failed, skipped = run_tests(parser)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
