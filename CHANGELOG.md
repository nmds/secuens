# Changelog

All notable changes to the CueScript specification will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased] — Editorial revision

### Changed
- File Format section rewritten: more concise, UTF-8 moved to opening line
- Fountain Integration heading hierarchy corrected (`###` → `####`)
- Duplicate Fountain compatibility note removed from Design Principles
- "Best Practices" subsection in Cue Numbering collapsed into inline note
- Production Coordination Context section removed (content moved to site documentation)
- License clarified: CC BY-ND 4.0 (was CC BY 4.0)

### Added
- Pattern C: QLab-style prefixed numbering (`A1`, `V3`, `A5a`)
- `.txt` note: accepted as parser input but not a recognized CueScript extension

### Fixed
- Reference Implementation updated: QMan → QBook, correct repository URL

---

## [v0.9] — January 2026 — Public Draft

First public release of the CueScript specification, open for community feedback.

### Included
- Core syntax: `CUETYPE (LABEL NUMBER) TRIGGER: DESCRIPTION`
- Domain-agnostic design (theatre, film, live events, broadcast)
- Optional trigger syntax (`on`, `after`, `with`)
- Optional metadata system (`[key=value]`)
- Timing rules (units required for numeric time values)
- Standby/warning system via `warn` metadata
- Cue numbering conventions (letter suffix and decimal patterns)
- Fountain compatibility
- Final Draft compatibility
- Parser requirements (MUST / SHOULD / MAY)
- Validation rules and edge cases
- Examples across theatre, film, and live events

---

*Older versions will be listed here as the spec evolves.*
