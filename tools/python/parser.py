"""
Secuens Reference Parser — Python
Version: 0.9
License: MIT (tool implementation; specification under CC BY-ND 4.0)

A minimal reference parser for the Secuens specification v0.9.
Demonstrates correct parsing logic for all spec components.

Usage:
    python parser.py script.secuens
    python parser.py script.fountain

    Or import and use programmatically:
    from parser import SecuensParser
    parser = SecuensParser()
    cues = parser.parse_file("script.secuens")
"""

import re
import sys
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class Cue:
    """Represents a parsed Secuens cue."""
    line_number: int
    raw: str
    cue_type: str                       # CUETYPE — e.g. "LX", "CAMERA"
    label: str                          # LABEL — e.g. "cue", "shot", "setup"
    number: str                         # NUMBER — e.g. "5", "5a", "5.5", "A5"
    description: str                    # DESCRIPTION — human-readable text
    trigger_keyword: Optional[str] = None   # TRIGGER keyword — e.g. "on", "after"
    trigger_value: Optional[str] = None     # TRIGGER value — e.g. '"Juliet"', "3s"
    metadata: dict = field(default_factory=dict)  # METADATA key-value pairs
    hidden: bool = False                # True if wrapped in [[ ]]


@dataclass
class ParseWarning:
    """A non-fatal warning from the parser."""
    line_number: int
    message: str
    raw: str


@dataclass
class ParseResult:
    """Result of parsing a Secuens document."""
    cues: list[Cue]
    warnings: list[ParseWarning]
    cue_types_seen: dict  # cuetype -> label used (for consistency checks)


# ---------------------------------------------------------------------------
# Regex Patterns
# ---------------------------------------------------------------------------

# Matches optional Fountain boneyard wrapper [[ ... ]]
BONEYARD_RE = re.compile(r'^\[\[(.*)\]\]$')

# Matches optional Fountain forced action prefix !
FORCED_ACTION_RE = re.compile(r'^!')

# Core cue pattern:
# CUETYPE (LABEL NUMBER) TRIGGER [METADATA]: DESCRIPTION
#
# Groups:
#   1: cuetype
#   2: label
#   3: number
#   4: trigger (optional, full "keyword value" string)
#   5: metadata block content (optional, inside [ ])
#   6: description
CUE_RE = re.compile(
    r'^([A-Z]+)'                        # CUETYPE: uppercase letters
    r'\s*\('                            # opening paren, optional whitespace
    r'([a-z]+)'                         # LABEL: lowercase word
    r'\s+'                              # required space between LABEL and NUMBER
    r'([A-Z]?[0-9]+(?:[a-z]*|(?:\.[0-9]+)))'  # NUMBER: patterns A, B, C
    r'\s*\)'                            # closing paren, optional whitespace
    r'(?:\s+([a-z]+\s+(?:"[^"]*"|[0-9]+(?:\.[0-9]+)?(?:s|m|ms|h)|[^"\[:\n][^\[:\n]*?)))?' # TRIGGER: keyword + (quoted|time|free-form non-dialogue)
    r'(?:\s*\[([^\]]*)\])?'            # METADATA: [key=value, ...] (optional)
    r'\s*:\s*'                          # colon separator
    r'(.*)'                             # DESCRIPTION
)

# Pattern to detect trigger keyword immediately before colon (no value)
TRIGGER_NO_VALUE_RE = re.compile(
    r'^([A-Z]+)\s*\([a-z]+\s+[^\)]+\)\s+([a-z]+)\s*(?:\[[^\]]*\])?\s*:'
)

# Metadata key=value pair pattern
METADATA_PAIR_RE = re.compile(r'([a-z]+)=((?:"[^"]*"|[^,\]]+))')

# Time value validation: must have units
TIME_KEYS = {'duration', 'fade', 'prewait', 'postwait', 'warn'}
TIME_VALUE_RE = re.compile(r'^[0-9]+(?:\.[0-9]+)?(s|m|ms|h)$')


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class SecuensParser:
    """
    Minimal Secuens v0.9 reference parser.

    Implements all MUST requirements from the specification.
    Implements key SHOULD requirements (warnings).
    """

    def parse_file(self, filepath: str) -> ParseResult:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return self.parse_lines(lines)

    def parse_text(self, text: str) -> ParseResult:
        return self.parse_lines(text.splitlines(keepends=True))

    def parse_lines(self, lines: list[str]) -> ParseResult:
        cues = []
        warnings = []
        cue_types_seen = {}  # cuetype -> label

        for line_number, raw_line in enumerate(lines, start=1):
            line = raw_line.rstrip('\n').rstrip('\r')

            # Check for Fountain boneyard (hidden cues)
            hidden = False
            boneyard_match = BONEYARD_RE.match(line)
            if boneyard_match:
                line = boneyard_match.group(1).strip()
                hidden = True

            # Strip forced action prefix
            line = FORCED_ACTION_RE.sub('', line)

            # Attempt to parse as a cue
            cue = self._parse_cue(line, line_number, raw_line.rstrip(), hidden, warnings)
            if cue:
                # Check label consistency (SHOULD warn)
                existing_label = cue_types_seen.get(cue.cue_type)
                if existing_label is None:
                    cue_types_seen[cue.cue_type] = cue.label
                elif existing_label != cue.label:
                    warnings.append(ParseWarning(
                        line_number=line_number,
                        message=(
                            f"Inconsistent label for {cue.cue_type}: "
                            f"previously used '{existing_label}', now '{cue.label}'"
                        ),
                        raw=raw_line.rstrip()
                    ))

                cues.append(cue)

        # Check for duplicate cue numbers within same CUETYPE (SHOULD warn)
        self._check_duplicates(cues, warnings)

        return ParseResult(cues=cues, warnings=warnings, cue_types_seen=cue_types_seen)

    def _parse_cue(self, line: str, line_number: int, raw: str, hidden: bool, warnings: list) -> Optional[Cue]:
        # Check for trigger-keyword-without-value pattern before main parse
        # e.g. "LX (cue 5) on: Fade" — keyword directly before colon
        kw_no_val = TRIGGER_NO_VALUE_RE.match(line)
        if kw_no_val:
            warnings.append(ParseWarning(
                line_number=line_number,
                message=f"Trigger keyword '{kw_no_val.group(2)}' has no value",
                raw=raw
            ))
            # Still attempt to parse the rest of the cue without the trigger

        match = CUE_RE.match(line)
        if not match:
            return None

        cue_type = match.group(1)
        label = match.group(2)
        number = match.group(3)
        trigger_raw = match.group(4)  # e.g. 'on "Juliet"' or 'after 3s' or None
        metadata_raw = match.group(5)  # content inside [ ] or None
        description = match.group(6).strip()

        # Parse trigger
        trigger_keyword = None
        trigger_value = None
        if trigger_raw:
            trigger_parts = trigger_raw.strip().split(None, 1)
            if len(trigger_parts) == 2:
                trigger_keyword = trigger_parts[0]
                trigger_value = trigger_parts[1]
            elif len(trigger_parts) == 1:
                # keyword without value — invalid per spec, but we warn rather than fail
                warnings.append(ParseWarning(
                    line_number=line_number,
                    message=f"Trigger keyword '{trigger_parts[0]}' has no value",
                    raw=raw
                ))

        # Parse metadata
        metadata = {}
        if metadata_raw:
            metadata, meta_warnings = self._parse_metadata(metadata_raw, line_number, raw)
            warnings.extend(meta_warnings)

        # Warn on empty description (SHOULD warn, MAY accept as placeholder)
        if not description:
            warnings.append(ParseWarning(
                line_number=line_number,
                message=f"{cue_type} (cue {number}): Missing description — treating as placeholder",
                raw=raw
            ))

        return Cue(
            line_number=line_number,
            raw=raw,
            cue_type=cue_type,
            label=label,
            number=number,
            description=description,
            trigger_keyword=trigger_keyword,
            trigger_value=trigger_value,
            metadata=metadata,
            hidden=hidden
        )

    def _parse_metadata(self, metadata_raw: str, line_number: int, raw: str) -> tuple[dict, list]:
        metadata = {}
        warnings = []

        for pair_match in METADATA_PAIR_RE.finditer(metadata_raw):
            key = pair_match.group(1)
            value = pair_match.group(2).strip()

            # Strip quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

            # Validate time units for time-related keys (MUST validate)
            if key in TIME_KEYS:
                if not TIME_VALUE_RE.match(value) and value not in ('slow', 'fast', 'instant'):
                    warnings.append(ParseWarning(
                        line_number=line_number,
                        message=f"Time value '{value}' for key '{key}' missing units (expected: s, m, ms, h)",
                        raw=raw
                    ))

            metadata[key] = value

        return metadata, warnings

    def _check_duplicates(self, cues: list[Cue], warnings: list[ParseWarning]):
        seen = {}  # (cuetype, number) -> line_number
        for cue in cues:
            key = (cue.cue_type, cue.number)
            if key in seen:
                warnings.append(ParseWarning(
                    line_number=cue.line_number,
                    message=(
                        f"Duplicate cue number: {cue.cue_type} {cue.label} {cue.number} "
                        f"(first seen at line {seen[key]})"
                    ),
                    raw=cue.raw
                ))
            else:
                seen[key] = cue.line_number


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python parser.py <file.secuens>")
        sys.exit(1)

    filepath = sys.argv[1]
    parser = SecuensParser()

    try:
        result = parser.parse_file(filepath)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Secuens Parser v0.9 — {filepath}")
    print(f"{'─' * 60}")
    print(f"Found {len(result.cues)} cue(s), {len(result.warnings)} warning(s)")
    print()

    # Print cues
    for cue in result.cues:
        hidden_marker = " [HIDDEN]" if cue.hidden else ""
        trigger_str = ""
        if cue.trigger_keyword:
            trigger_str = f" | trigger: {cue.trigger_keyword} {cue.trigger_value}"
        metadata_str = ""
        if cue.metadata:
            metadata_str = f" | metadata: {cue.metadata}"
        print(f"  Line {cue.line_number:4d}{hidden_marker}: {cue.cue_type} ({cue.label} {cue.number}){trigger_str}{metadata_str}")
        if cue.description:
            print(f"             → {cue.description}")

    # Print warnings
    if result.warnings:
        print()
        print("Warnings:")
        for w in result.warnings:
            print(f"  Line {w.line_number:4d}: ⚠ {w.message}")

    # Summary of cue types
    print()
    print("Cue Types:")
    for cue_type, label in sorted(result.cue_types_seen.items()):
        count = sum(1 for c in result.cues if c.cue_type == cue_type)
        print(f"  {cue_type:12s} ({label}) — {count} cue(s)")


if __name__ == "__main__":
    main()
