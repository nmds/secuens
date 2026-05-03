# Secuens

**Plain-text technical cue notation for theatre, film, live events, and broadcast.**

> *Write the cue where the idea happens.*

---

Secuens is an open specification for embedding technical cues directly inside scripts, scores, and production documents — as readable plain text. No proprietary formats, no separate cue lists, no extra tools required to read.

A Secuens cue looks like this:

```
LX (cue 5) on "Juliet" [fade=3s]: Fade to blackout
CAMERA (shot 3) [lens=85mm, frame=CU]: Close-up on actor's face
AUDIO (cue 7) [fade=2s, level=-6dB]: Music under speech
```

That's it. Human-readable. Machine-parseable. Works in any text editor.

---

## Why Secuens

Production teams work from scripts. But technical cues live in separate systems — cue sheets, QLab workspaces, lighting desks, camera logs — disconnected from the creative document that drives the whole production.

Every time something changes, you update three documents.

Secuens fixes that by bringing the cue back where the idea lives: **in the text**.

---

## How It Works

A cue follows a consistent pattern:

```
CUETYPE (label NUMBER) TRIGGER [METADATA]: DESCRIPTION
```

- **CUETYPE** — the production department or element (`LX`, `SOUND`, `CAMERA`, `VIDEO`, `AUDIO`...)
- **label NUMBER** — the cue identifier (`cue 5`, `shot 3`, `setup 2a`)
- **TRIGGER** — optional: when it fires (`on "line"`, `after 3s`, `with entrance`)
- **METADATA** — optional: technical details (`[fade=3s, level=80%]`)
- **DESCRIPTION** — what happens, in plain language

Secuens files are plain UTF-8 text. They can be opened in any text editor or word processor. In Fountain-compatible applications, cues render as readable action lines — no plugins, no modifications required.

---

## Quick Examples

### Theatre

```secuens
INT. HAUNTED MANSION - NIGHT

John enters cautiously.

[[SQ (cue 1) [file="ambience.wav", loop=true]: Background ambience]]

SQ (cue 2) [level=-6dB]: Distant thunder

He approaches the door.

SQ (cue 3) on door contact: Door slams shut

LX (cue 4) with door slam [duration=500ms]: Lights flicker

LX (cue 7) [fade=5s, warn=30s]: Slow fade to blackout
```

### Film

```secuens
EXT. CITY STREET - DAY

CAMERA (shot 1) [lens=35mm, movement=tracking]: Follow Sarah medium shot

She glances over her shoulder.

CAMERA (shot 2) [lens=85mm, angle=low, frame=CU]: Close-up — Sarah's eyes

SOUND (take 1) [note="Capture separately"]: Car engine close-up

LIGHT (setup 2) [type=bounce, direction=left]: Soften shadows on actor
```

### Live Event

```secuens
LIGHTS (cue 1) [fade=3s, preset=stage_wash]: Stage lights up

VIDEO (cue 2) [source=playback, file="intro.mp4"]: Roll intro video

CAMERA (cue 5) [preset=single_shot, transition=dissolve]: Camera 2 — speaker

AUDIO (cue 6) [source=lav_mic, gate=-20dB]: Activate speaker mic
```

---

## File Extensions

- **`.secuens`** — Secuens-specific extension for production-focused documents
- **`.fountain`** — Use when working within the Fountain ecosystem or sharing with screenwriters and directors

Both extensions contain identical content and are fully interchangeable.

---

## Specification

The full specification lives in [`specification/v0.9/`](specification/v0.9/).

Current version: **v0.9.1 (Public Draft, April 2026)**

The spec covers:
- Complete syntax definition with formal patterns
- All cue components: CUETYPE, LABEL, NUMBER, TRIGGER, METADATA, DESCRIPTION
- Standard metadata keys for timing, levels, files, targets, and more
- Domain conventions: theatre, film, live events, broadcast
- Fountain compatibility patterns (action lines, forced action, hidden cues)
- Parser requirements (MUST / SHOULD / MAY)
- Validation rules and edge cases
- Complete production examples

---

## Examples

Real-world example files are in [`examples/`](examples/):

| File | Domain |
|------|--------|
| [`theatre-basic.secuens`](examples/theatre-basic.secuens) | Simple theatre scene |
| [`theatre-musical.secuens`](examples/theatre-musical.secuens) | Musical theatre, multi-department |
| [`film-shoot.secuens`](examples/film-shoot.secuens) | Film production with setup notation |
| [`live-event-conference.secuens`](examples/live-event-conference.secuens) | Corporate live event |
| [`broadcast-newscast.secuens`](examples/broadcast-newscast.secuens) | TV broadcast |

---

## Tools

### Parsers

- [`tools/parsers/`](tools/parsers/) — Reference parser implementations

### Validators

- [`tools/validators/`](tools/validators/) — Validator logic and test cases

### Known Implementations

See [secuens.org/implementations](https://www.secuens.org/implementations) for a current list of tools that support Secuens.

**QBook** is the reference implementation — a production-focused cue management application built on the Secuens format. Learn more at [secuens.org](https://www.secuens.org).

---

## Progressive Enhancement

Secuens is designed for production workflows. A cue is valid at any stage of detail:

```secuens
# During scripting — mark where it happens
LX (cue 5):

# During rehearsal — add the trigger and description
LX (cue 5) on "Juliet": Fade to blackout

# During tech — add full implementation detail
LX (cue 5) on "Juliet" [fade=3s, warn=30s, target=all]: Fade to blackout
```

---

## Contributing

Secuens is an open specification. Community input is welcome — especially from production practitioners across all domains.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

The Secuens specification is released under [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/).

You are free to read, implement, and share the specification. You may not publish modified versions of the specification itself.

Implementations — parsers, editors, tools built on Secuens — may use any license.

---

## Acknowledgments

Secuens draws from production practices across theatre, film, television, live events, and broadcast. Its plain-text philosophy was inspired by [Fountain](https://fountain.io), the open screenplay markup language.

The name *Secuens* comes from the Latin *sequens* — the sequence, the thing that follows — with the cue hidden inside.

---

*Secuens Specification v0.9.1 (Public Draft) — April 2026*  
*[secuens.org](https://www.secuens.org) · [github.com/meikr/secuens](https://github.com/meikr/secuens)*
