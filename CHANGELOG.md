# Changelog

All notable changes to the Secuens specification are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.9.1] — Public Draft — April 2026

### Changed

- Added explicit author attribution: **Nicola Marra de Scisciolo**
- Renamed format: CueScript → **Secuens**
- File extension updated: `.cuescript` → `.secuens`
- Repository references updated: `github.com/nmds/secuens`
- Website references updated: `secuens.org`
- Minor editorial corrections throughout

---

## [0.9.0] — Public Draft — April 2026

Initial public release of the Secuens specification.

### Specification

- Core syntax: `CUETYPE (LABEL NUMBER) TRIGGER [METADATA]: DESCRIPTION`
- CUETYPE: uppercase identifier, any production department (`LX`, `CAMERA`, `AUDIO`, etc.)
- LABEL: flexible lowercase word per CUETYPE (`cue`, `shot`, `setup`, `take`, `q`, etc.)
- NUMBER: three supported patterns — letter suffix (`5a`), decimal (`5.5`), prefixed (`A5`)
- TRIGGER: optional keyword + value (`on "line"`, `after 3s`, `with entrance`)
- METADATA: optional `[key=value]` pairs for technical implementation details
- DESCRIPTION: human-readable plain language description

### Metadata System

- Standard keys defined: `duration`, `fade`, `prewait`, `postwait`, `warn`
- Common technical keys: `level`, `file`, `target`, `source`, `type`
- Domain-specific examples: theatre, film, live events, broadcast
- Time values require units (`s`, `m`, `ms`, `h`)
- Custom keys always permitted

### Trigger System

- Standard keywords: `on`, `after`, `with`
- Custom keywords permitted for domain-specific workflows
- Dialogue triggers require quotes: `on "Juliet"` not `on Juliet`
- Time triggers: `after 3s`, `after 500ms`
- Action triggers: `with entrance`, `with door slam`

### Standby/Warning System

- `warn` metadata key for advance preparation notices
- Parsers may generate coordination cues from `warn` values

### Domain Support

- Theatre: `LX`, `SQ`, `MQ`, `FLY`, `SPOT`, `AUTO`, `PROJ`
- Film: `CAMERA`, `LIGHT`, `SOUND`, `VFX` with `shot`/`setup`/`take` labels
- Live Events: `VIDEO`, `AUDIO`, `CAMERA`, `GRAPHICS`, `LIGHTS`, `PLAYBACK`
- Broadcast: `CAMERA`, `GRAPHICS`, `AUDIO`, `PLAYBACK`, `TRANSITION`

### Compatibility

- Fountain-compatible: cues render as action lines in Fountain applications
- Hidden cues via Fountain boneyard syntax: `[[LX (cue 1): ...]]`
- Forced visibility via Fountain prefix: `!SQ (cue 5): ...`
- Final Draft compatibility tested and confirmed

### Parser Requirements

- Full MUST / SHOULD / MAY requirements defined
- Formal regex patterns for each syntax component
- Validation rules and recommended warnings
- Edge cases documented

### Examples

- Theatre: basic scene, full musical act
- Film: exterior street scene with VFX and car interior
- Live Events: corporate conference multi-session
- Broadcast: evening newscast with packages and graphics

---

## Future

See [Future Considerations](specification/v0.9/Secuens-v0.9.1-DRAFT.md#future-considerations) in the spec for what's being explored for v1.0.
