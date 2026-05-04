/**
 * Secuens Specification Validator — Test Cases (JavaScript)
 * Version: 0.9.1
 * License: MIT
 *
 * Validates that a Secuens parser correctly handles all cases defined
 * in the Secuens v0.9.1 specification. Run this against any parser
 * implementation to verify compliance.
 *
 * Usage (Node.js):
 *   node validator.js
 *
 * Usage (module):
 *   const { runTests } = require('./validator');
 *   const { SecuensParser } = require('./parser');
 *   const { passed, failed } = runTests(new SecuensParser());
 *
 * Output:
 *   PASS — the parser behaved as expected
 *   FAIL — the parser returned an unexpected result
 *
 * Each test case is labelled:
 *   VALID   — the parser MUST recognize this as a cue
 *   INVALID — the parser MUST NOT recognize this as a cue
 *   WARN    — the parser MUST parse this but SHOULD emit a warning
 *
 * Exit code:
 *   0 — all tests passed
 *   1 — one or more tests failed
 *
 * Note: validator.js expects parser.js to be in the same directory.
 */

'use strict';

// ---------------------------------------------------------------------------
// Test Cases
// ---------------------------------------------------------------------------

const TEST_CASES = [

  // -------------------------------------------------------------------------
  // CORE SYNTAX — Valid forms
  // -------------------------------------------------------------------------

  { category: "VALID", label: "minimal form",
    input: "SQ (cue 5): Door slams shut",
    expectCue: { cueType: "SQ", label: "cue", number: "5", description: "Door slams shut" },
    description: "Minimal valid cue — type, number, description" },

  { category: "VALID", label: "with trigger on",
    input: 'LX (cue 12) on "Juliet": Fade to blackout',
    expectCue: { cueType: "LX", triggerKeyword: "on", triggerValue: '"Juliet"' },
    description: "Dialogue trigger with quotes" },

  { category: "VALID", label: "with trigger after",
    input: "SQ (cue 3) after 2s: Thunder crash",
    expectCue: { triggerKeyword: "after", triggerValue: "2s" },
    description: "Time delay trigger" },

  { category: "VALID", label: "with trigger with",
    input: "SQ (cue 3) with door slam: Crash",
    expectCue: { triggerKeyword: "with", triggerValue: "door slam" },
    description: "Action trigger — free-form text" },

  { category: "VALID", label: "custom trigger keyword",
    input: "LX (cue 5) before curtain: Fade",
    expectCue: { triggerKeyword: "before", triggerValue: "curtain" },
    description: "Custom trigger keyword — must be accepted" },

  { category: "VALID", label: "with metadata only",
    input: "LX (cue 5) [fade=3s]: Fade to blackout",
    expectCue: { metadata: { fade: "3s" } },
    description: "Metadata without trigger" },

  { category: "VALID", label: "with trigger and metadata",
    input: 'LX (cue 5) on "Juliet" [fade=3s, warn=30s]: Fade to blackout',
    expectCue: { triggerKeyword: "on", metadata: { fade: "3s", warn: "30s" } },
    description: "Trigger + metadata — full cue" },

  { category: "VALID", label: "multiple metadata pairs",
    input: 'SQ (cue 2) [file="thunder.wav", level=-3dB]: Thunder crash',
    expectCue: { metadata: { file: "thunder.wav", level: "-3dB" } },
    description: "Multiple metadata pairs with quoted string and dB value" },

  { category: "VALID", label: "metadata comma without space",
    input: "LX (cue 5) [fade=3s,level=80%]: Fade",
    expectCue: { metadata: { fade: "3s", level: "80%" } },
    description: "Comma without trailing space — MUST be accepted" },

  { category: "VALID", label: "hidden cue in boneyard",
    input: '[[SQ (cue 1) [file="ambience.wav", loop=true]: Background ambience]]',
    expectCue: { hidden: true, cueType: "SQ" },
    description: "Fountain boneyard hidden cue" },

  { category: "VALID", label: "forced action prefix",
    input: "!SQ (cue 5): Door slams shut",
    expectCue: { cueType: "SQ", description: "Door slams shut" },
    description: "Fountain forced action prefix — must be stripped before parsing" },

  // NUMBER patterns
  { category: "VALID", label: "number pattern A — plain",
    input: "LX (cue 10): Lights up",
    expectCue: { number: "10" },
    description: "Pattern A: plain integer" },

  { category: "VALID", label: "number pattern A — letter suffix",
    input: "LX (cue 5a): Insert cue",
    expectCue: { number: "5a" },
    description: "Pattern A: letter suffix" },

  { category: "VALID", label: "number pattern A — multi-letter suffix",
    input: "LX (cue 5ab): Insert cue",
    expectCue: { number: "5ab" },
    description: "Pattern A: multi-letter suffix" },

  { category: "VALID", label: "number pattern B — decimal",
    input: "LX (cue 5.5): Insert cue",
    expectCue: { number: "5.5" },
    description: "Pattern B: decimal notation" },

  { category: "VALID", label: "number pattern C — prefixed",
    input: "LX (cue A5): Prefixed cue",
    expectCue: { number: "A5" },
    description: "Pattern C: uppercase prefix" },

  { category: "VALID", label: "number pattern C — prefixed with suffix",
    input: "LX (cue A5a): Prefixed with suffix",
    expectCue: { number: "A5a" },
    description: "Pattern C: uppercase prefix with letter suffix" },

  // LABEL flexibility
  { category: "VALID", label: "label: shot",
    input: "CAMERA (shot 3): Close-up on actor",
    expectCue: { label: "shot" },
    description: "CAMERA using 'shot' label" },

  { category: "VALID", label: "label: setup",
    input: "LIGHT (setup 2): Key from left",
    expectCue: { label: "setup" },
    description: "LIGHT using 'setup' label" },

  { category: "VALID", label: "label: take",
    input: "SOUND (take 1): Boom from above",
    expectCue: { label: "take" },
    description: "SOUND using 'take' label" },

  { category: "VALID", label: "label: q",
    input: "LX (q 7): Lights change",
    expectCue: { label: "q" },
    description: "Short label 'q'" },

  // Whitespace flexibility
  { category: "VALID", label: "no space before paren",
    input: "SQ(cue 5): Door slams",
    expectCue: { cueType: "SQ", number: "5" },
    description: "No space before opening parenthesis — valid" },

  { category: "VALID", label: "extra space inside parens",
    input: "SQ (cue  5): Door slams",
    expectCue: { number: "5" },
    description: "Extra space between LABEL and NUMBER — valid" },

  { category: "VALID", label: "extra spaces between components",
    input: "SQ  (cue 5):  Door slams",
    expectCue: { description: "Door slams" },
    description: "Extra spaces between components — valid" },

  // Metadata value types
  { category: "VALID", label: "descriptive time value unquoted",
    input: "LX (cue 5) [fade=slow]: Fade",
    expectCue: { metadata: { fade: "slow" } },
    description: "Descriptive time value without quotes" },

  { category: "VALID", label: "descriptive time value quoted",
    input: 'LX (cue 5) [fade="slow"]: Fade',
    expectCue: { metadata: { fade: "slow" } },
    description: "Descriptive time value with quotes — both valid" },

  { category: "VALID", label: "boolean true",
    input: "SQ (cue 1) [loop=true]: Ambience",
    expectCue: { metadata: { loop: "true" } },
    description: "Boolean true value" },

  { category: "VALID", label: "boolean false",
    input: "SQ (cue 1) [loop=false]: Ambience",
    expectCue: { metadata: { loop: "false" } },
    description: "Boolean false value" },

  { category: "VALID", label: "level in percent",
    input: "LX (cue 1) [level=80%]: Fade",
    expectCue: { metadata: { level: "80%" } },
    description: "Level as percentage" },

  { category: "VALID", label: "level in dB",
    input: "SQ (cue 1) [level=-6dB]: Sound",
    expectCue: { metadata: { level: "-6dB" } },
    description: "Level in decibels" },

  { category: "VALID", label: "uppercase value preserved",
    input: "CAMERA (shot 1) [frame=CU]: Close-up",
    expectCue: { metadata: { frame: "CU" } },
    description: "Uppercase metadata value preserved" },

  { category: "VALID", label: "mixed-case target preserved",
    input: "CAMERA (shot 1) [target=Cam2]: Switch",
    expectCue: { metadata: { target: "Cam2" } },
    description: "Mixed-case metadata value preserved" },

  { category: "VALID", label: "time units — milliseconds",
    input: "LX (cue 1) [fade=500ms]: Snap",
    expectCue: { metadata: { fade: "500ms" } },
    description: "Millisecond time unit" },

  { category: "VALID", label: "time units — hours",
    input: "SQ (cue 1) [duration=2h]: Long fade",
    expectCue: { metadata: { duration: "2h" } },
    description: "Hour time unit" },

  { category: "VALID", label: "custom metadata key",
    input: "CAMERA (shot 1) [mykey=myvalue]: Custom",
    expectCue: { metadata: { mykey: "myvalue" } },
    description: "Custom metadata keys always allowed" },

  { category: "VALID", label: "long cuetype",
    input: "GRAPHICS (cue 1): Display title",
    expectCue: { cueType: "GRAPHICS" },
    description: "Multi-letter CUETYPE" },

  // -------------------------------------------------------------------------
  // INVALID forms — must NOT be recognized as cues
  // -------------------------------------------------------------------------

  { category: "INVALID", label: "lowercase cuetype",
    input: "sq (cue 1): Door slams",
    description: "Lowercase CUETYPE — invalid" },

  { category: "INVALID", label: "mixed-case cuetype",
    input: "Sq (cue 1): Door slams",
    description: "Mixed-case CUETYPE — invalid" },

  { category: "INVALID", label: "missing cue number",
    input: "SQ: Door slams",
    description: "Missing (LABEL NUMBER) block — invalid" },

  { category: "INVALID", label: "missing cuetype",
    input: "(cue 5): Door slams",
    description: "Missing CUETYPE — invalid" },

  { category: "INVALID", label: "label-number no space",
    input: "SQ (cue5): Door slams",
    description: "No space between LABEL and NUMBER — invalid" },

  { category: "WARN", label: "dialogue trigger without quotes",
    input: "LX (cue 5) on Juliet: Fade",
    expectCue: { cueType: "LX" },
    expectWarningContains: null,
    description: "Unquoted dialogue trigger — ambiguous, spec says quotes MUST be used." },

  { category: "INVALID", label: "normal action line",
    input: "John walks to the door.",
    description: "Plain text — not a cue" },

  { category: "INVALID", label: "cue reference in dialogue",
    input: "Stand by for sound cue 5.",
    description: "Cue reference in text — not a cue definition" },

  { category: "INVALID", label: "missing colon",
    input: "SQ (cue 5) Door slams",
    description: "Missing colon separator — invalid" },

  // -------------------------------------------------------------------------
  // WARN — Valid cues that should generate warnings
  // -------------------------------------------------------------------------

  { category: "WARN", label: "missing description",
    input: "LX (cue 5):",
    expectCue: { cueType: "LX", number: "5", description: "" },
    expectWarningContains: "missing description",
    description: "Parser MAY accept as placeholder, SHOULD warn" },

  { category: "WARN", label: "trigger keyword without value",
    input: "LX (cue 5) on: Fade",
    expectWarningContains: "no value",
    description: "Trigger keyword without value — should warn" },

  { category: "WARN", label: "time value without units",
    input: "LX (cue 5) [fade=3]: Fade",
    expectWarningContains: "missing units",
    description: "Numeric time value without units — MUST warn" },

];

// ---------------------------------------------------------------------------
// Runner
// ---------------------------------------------------------------------------

function runTests(parser) {
  let passed = 0;
  let failed = 0;

  console.log("Secuens Specification Validator — v0.9.1");
  console.log("=".repeat(60));
  console.log();

  for (const tc of TEST_CASES) {
    const result = parser.parseText(tc.input);
    const { cues, warnings } = result;

    if (tc.category === "VALID") {
      if (!cues.length) {
        console.log(`  ✗ FAIL [${tc.category}] ${tc.label}`);
        console.log(`       Input: ${tc.input}`);
        console.log(`       Expected: cue found`);
        console.log(`       Got: no cue parsed`);
        failed++;
        continue;
      }

      const cue = cues[0];
      let fieldFail = false;

      if (tc.expectCue) {
        for (const [field, expected] of Object.entries(tc.expectCue)) {
          const actual = cue[field];
          const match = typeof expected === 'object'
            ? JSON.stringify(actual) === JSON.stringify(expected)
            : actual === expected;

          if (!match) {
            console.log(`  ✗ FAIL [${tc.category}] ${tc.label}`);
            console.log(`       Input: ${tc.input}`);
            console.log(`       Field '${field}': expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
            failed++;
            fieldFail = true;
            break;
          }
        }
      }

      if (!fieldFail) {
        console.log(`  ✓ PASS [${tc.category}] ${tc.label}`);
        passed++;
      }

    } else if (tc.category === "INVALID") {
      if (cues.length) {
        console.log(`  ✗ FAIL [${tc.category}] ${tc.label}`);
        console.log(`       Input: ${tc.input}`);
        console.log(`       Expected: no cue`);
        console.log(`       Got: ${JSON.stringify(cues[0])}`);
        failed++;
      } else {
        console.log(`  ✓ PASS [${tc.category}] ${tc.label}`);
        passed++;
      }

    } else if (tc.category === "WARN") {
      if (tc.expectCue && !cues.length) {
        console.log(`  ✗ FAIL [${tc.category}] ${tc.label}`);
        console.log(`       Input: ${tc.input}`);
        console.log(`       Expected: cue + warning`);
        console.log(`       Got: no cue at all`);
        failed++;
        continue;
      }

      if (tc.expectWarningContains) {
        const warningTexts = warnings.map(w => w.message.toLowerCase());
        const found = warningTexts.some(w => w.includes(tc.expectWarningContains.toLowerCase()));
        if (found) {
          console.log(`  ✓ PASS [${tc.category}] ${tc.label}`);
          passed++;
        } else {
          console.log(`  ✗ FAIL [${tc.category}] ${tc.label}`);
          console.log(`       Input: ${tc.input}`);
          console.log(`       Expected warning containing: '${tc.expectWarningContains}'`);
          console.log(`       Got warnings: ${JSON.stringify(warnings.map(w => w.message))}`);
          failed++;
        }
      } else {
        console.log(`  ✓ PASS [${tc.category}] ${tc.label}`);
        passed++;
      }
    }
  }

  console.log();
  console.log("=".repeat(60));
  console.log(`Results: ${passed} passed, ${failed} failed`);
  console.log(`Total: ${TEST_CASES.length} test cases`);

  return { passed, failed };
}

// ---------------------------------------------------------------------------
// CLI (Node.js only)
// ---------------------------------------------------------------------------

if (typeof require !== 'undefined' && require.main === module) {
  const { SecuensParser } = require('./parser');
  const parser = new SecuensParser();
  const { failed } = runTests(parser);
  process.exit(failed === 0 ? 0 : 1);
}

// ---------------------------------------------------------------------------
// Export
// ---------------------------------------------------------------------------

if (typeof module !== 'undefined') {
  module.exports = { runTests, TEST_CASES };
}
