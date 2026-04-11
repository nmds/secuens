# CueScript

**Plain-text technical cue notation for theatre, film, and live production.**

CueScript is an open format for embedding technical cues — lighting, sound, camera, video, and more — directly within scripts and production documents. It works in any text editor, on any platform, without specialized software.

---

## What it looks like

```
LX (cue 5) [fade=3s]: Fade to blackout
SQ (cue 6) on "exit": Door slams shut
CAMERA (shot 3) [lens=85mm, frame=MCU]: Close-up on Sarah
VIDEO (cue 2) with speaker entrance [transition=cut]: Switch to camera 2
```

Simple to read. Simple to write. Parseable by machines, legible to humans.

---

## Who it's for

- **Stage managers** annotating calling scripts
- **Directors** marking cues during script development
- **ADs and script supervisors** coordinating technical departments on set
- **Live event and broadcast directors** managing complex multi-department cues
- **Developers** building production tools that need an open, interoperable cue format

---

## How it works

A CueScript cue has four parts:

```
CUETYPE (LABEL NUMBER) TRIGGER: DESCRIPTION
```

| Part | Required | Example |
|------|----------|---------|
| `CUETYPE` | Yes | `LX`, `SOUND`, `CAMERA` |
| `(LABEL NUMBER)` | Yes | `(cue 5)`, `(shot 3a)` |
| `TRIGGER` | No | `on "Juliet"`, `after 2s` |
| `DESCRIPTION` | Yes | `Fade to blackout` |

Optional metadata adds technical detail without breaking readability:

```
LX (cue 5) [fade=3s, warn=30s]: Fade to blackout
```

Cues evolve with production — start minimal, add detail as decisions are made.

---

## Domain-agnostic

CueScript is not a theatre format or a film format. The same syntax serves any production context:

- **Theatre** — `LX`, `SQ`, `FLY`, `SPOT`, `AUTO`
- **Film** — `CAMERA`, `LIGHT`, `SOUND`, `VFX`, `STUNT`
- **Live events** — `VIDEO`, `AUDIO`, `GRAPHICS`, `PLAYBACK`
- **Broadcast** — `CAMERA`, `GRAPHICS`, `TRANSITION`, `PLAYBACK`
- **Any production** — define your own cue types freely

---

## Plain text, no dependencies

CueScript is UTF-8 text. It opens in:

- Any text editor (TextEdit, Notepad, Vim, VS Code...)
- Any Fountain-compatible application (Highland, Slugline, Beat, Fade In...)
- Final Draft (as action/description paragraphs)

CueScript is **inspired by Fountain** and is compatible with Fountain parsers. Fountain tooling is not required — CueScript works equally well as standalone plain text.

**File extensions:** `.cuescript` for production documents, `.fountain` for maximum Fountain ecosystem compatibility. Both contain identical text and are freely interchangeable.

---

## Specification

The full specification is in [`specification/CueScript-v0.9-draft.md`](specification/CueScript-v0.9-draft.md).

Current version: **v0.9 (Public Draft)**

The spec covers:
- Core syntax and all components
- Optional metadata system
- Cue numbering conventions
- Fountain compatibility patterns
- Parser requirements (MUST / SHOULD / MAY)
- Validation rules and edge cases
- Complete examples across theatre, film, live events, and broadcast

---

## Status

CueScript v0.9 is a **public draft open for community feedback**.

The format is stable enough to build on. Feedback before v1.0 is especially valuable — open an [Issue](https://github.com/meikr/cuescript/issues) to share your thoughts, report ambiguities, or propose additions.

---

## Contributing

Feedback is welcome via [GitHub Issues](https://github.com/meikr/cuescript/issues).

Useful contributions include:
- Ambiguities or gaps in the specification
- Real-world cue conventions not covered
- Domain-specific use cases (film, broadcast, live events)
- Parser implementation questions

CueScript is maintained by the [meikr](https://github.com/meikr) organization.

---

## License

The CueScript Specification is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

You are free to use, implement, and share the format with attribution. Implementations may use any license.
