# CueScript Technical Cue Notation
## Specification v0.9 (Public Draft)

**Status:** Public Draft — open for community feedback  
**Date:** January 2026  
**License:** CC BY-ND 4.0

---

## Overview

**CueScript** is a plain-text technical cue notation format for scripts, scores, and production documents. It allows production coordinators, directors, and technical teams to embed standardized technical cues within any readable text document.

CueScript works in any text editor, on any platform, without requiring specialized software. It is designed to be immediately readable by humans and reliably parseable by machines.

CueScript is a universal format that works across any production context requiring technical notation: theatre, film, television, live events, broadcast, podcasts, and more. The same syntax serves different domains through specialized applications built on the open format.

CueScript is inspired by Fountain, the plain-text screenplay format. CueScript documents are compatible with Fountain parsers and applications, though Fountain tooling is not required.

### File Format

**File Extensions:**

CueScript documents may use either extension:

- **`.fountain`** — Maximum compatibility with Fountain ecosystem  
  Opens in any Fountain-compatible application.  
  Recommended for screenplays with embedded cues.

- **`.cuescript`** — CueScript-specific extension  
  Signals CueScript-aware tooling.  
  Recommended for technical calling scripts and production-focused documents.

Both extensions contain identical UTF-8 text and are fully interchangeable. The choice of extension signals intent and default application behavior.

**Encoding:** UTF-8 text

**Choosing an Extension:**

Use `.fountain` when:
- Working in the Fountain ecosystem (Highland, Slugline, Beat, etc.)
- Sharing with screenwriters, directors, or actors
- Early in production process
- Maximum compatibility is priority

Use `.cuescript` when:
- Creating technical calling scripts for production
- Working primarily in CueScript-aware applications
- Signaling "this is a production document"
- Want CueScript tools to open by default

**Note:** Extensions are interchangeable — simply rename the file. The content format is identical.

**Example Workflows:**

Collaborative screenplay:
```
hamlet.fountain          ← Shared with creative team
```

Technical production:
```
calling_script.cuescript ← Used by stage managers, operators
```

Mixed use:
```
hamlet.fountain          ← Master screenplay
hamlet_tech.cuescript    ← Technical calling script derived from master
```

### Design Principles

1. **Human-Readable First** — Readable in any text editor, on any platform, without specialized software
2. **Domain-Agnostic** — Universal format across theatre, film, live events, broadcast, and any production context
3. **Non-Invasive** — Does not interfere with screenplay writing or reading experience
4. **Progressive Enhancement** — Start simple, add detail as production develops
5. **Parser-Friendly** — Clear, unambiguous patterns for reliable automated processing
6. **Open & Extensible** — Custom cue types and metadata keys welcome; specialized tools can build on the open format
7. **Fountain-Compatible** — Valid CueScript documents are valid Fountain documents

---

## Core Syntax

### Basic Cue Format

```
CUETYPE (LABEL NUMBER) TRIGGER: DESCRIPTION
```

**Components:**

- **CUETYPE**: Production element identifier (typically 2-6 uppercase letters)
  - Must be uppercase letters (A-Z) only
  - Single word, no spaces
  - Based on production discipline conventions
  - Examples: `LX`, `SOUND`, `CAMERA`, `VIDEO`, `AUDIO`

- **LABEL**: Descriptor for the cue identifier (typically "cue", "shot", "setup", "take")
  - Pattern: One or more lowercase letters `[a-z]+`
  - Common labels: `cue`, `shot`, `setup`, `take`, `q`
  - **Consistency rule:** Each CUETYPE must use the same LABEL throughout a document
  - Examples:
    - `CAMERA (shot 5)` — if CAMERA uses "shot", all CAMERA cues must use "shot"
    - `LIGHT (setup 3)` — if LIGHT uses "setup", all LIGHT cues must use "setup"
  - Default/recommended: `cue` for all types

- **NUMBER**: Cue identifier supporting insertions
  - **Pattern A (Letter suffix):** `[0-9]+[a-z]*`
    - Examples: `1`, `12`, `5a`, `23b`, `100`
    - Common practice: Insert `5a` between `5` and `6`
  - **Pattern B (Decimal):** `[0-9]+\.[0-9]+`
    - Examples: `1.5`, `2.5`, `10.5`
    - Alternative practice: Insert `5.5` between `5` and `6`
  - **Note:** Choose ONE pattern per production. Mixing patterns in the same cue sequence may cause sorting confusion.
  - Combined patterns (e.g., `5.5a`) are not currently supported pending validation of real-world usage.

- **TRIGGER** *(optional)*: When/how the cue is triggered
  - Keywords: `on`, `after`, `with`
  - Formats:
    - `on "dialogue"` — Triggers on specific spoken words (**quotes required**)
    - `after 3s` — Triggers after a time delay
    - `with action` — Triggers simultaneously with an action
  - If omitted, cue trigger is implicit from context
  - Examples:
    - `on "Juliet"` — Trigger when actor says "Juliet"
    - `after 2s` — Trigger 2 seconds after previous cue/action
    - `with door slam` — Trigger simultaneously with door slam
  - **Important:** Dialogue triggers MUST use quotes to avoid ambiguity with descriptions

- **DESCRIPTION**: Human-readable description of the cue action
  - Free-form text
  - Should describe what happens, not technical implementation details
  - Keep concise but clear

**Examples:**
```
# Theatre (using "cue")
SQ (cue 5): Door slams shut
LX (cue 12a) on "Juliet": Fade to blackout

# Film (using natural terminology)
CAMERA (shot 3): Close-up on John's face
LIGHT (setup 2a) after establishing: Key light from left
SOUND (take 1): Boom from above

# Live Events (using "cue")
VIDEO (cue 3) with speaker entrance: Switch to camera 2
AUDIO (cue 7): Fade music under speech

# Broadcast (using "cue")
GRAPHICS (cue 1): Display lower third - guest name
CAMERA (cue 5) on host question: Wide shot of panel

# Mixed in same document (valid — different CUETYPEs)
CAMERA (shot 12): Close-up
LIGHT (cue 5): Key from left
SOUND (take 3): Dialogue recording

# Invalid — inconsistent within same CUETYPE
CAMERA (shot 1): Wide
CAMERA (cue 2): Close    ← ERROR: CAMERA already uses "shot"
```

---

## Metadata (Optional Technical Details)

CueScript supports optional metadata for technical implementation. Metadata is added in square brackets before the colon:

```
CUETYPE (cue NUMBER) [key=value, key2=value2]: DESCRIPTION
```

### Standard Metadata Keys

CueScript defines common metadata keys that work across domains. **Custom keys are always allowed** — any production can define domain-specific metadata.

**Universal Timing & Control:**
- `duration` — How long the cue takes to execute (e.g., `5s`, `2m`, `45s`)
- `fade` — Fade/transition time (e.g., `3s`, `500ms`)
- `prewait` — Delay before cue starts (e.g., `1s`, `2s`)
- `postwait` — Delay after cue completes (e.g., `2s`)
- `warn` — Advance warning time for coordination (e.g., `30s`, `2m`)

**Common Technical Parameters:**
- `level` — Intensity/volume (e.g., `80%`, `0.5`, `-6dB`)
- `file` — Media file reference (e.g., `"thunder.wav"`, `"intro.mp4"`)
- `target` — Specific equipment/output (e.g., `"channel_5"`, `"cam2"`, `"speaker_left"`)
- `source` — Input source (e.g., `"mic3"`, `"playback"`, `"laptop"`)
- `type` — Variant or category (e.g., `"key"`, `"bounce"`, `"practical"`)

**Theatre-Specific Examples:**
- `curve` — Lighting fade curve (e.g., `"log"`, `"linear"`)
- `intensity` — Light level (e.g., `"full"`, `"50%"`)
- `position` — Followspot position (e.g., `"center_stage"`, `"downstage_left"`)

**Film-Specific Examples:**
- `lens` — Camera lens (e.g., `"50mm"`, `"wide"`)
- `angle` — Camera angle (e.g., `"low"`, `"high"`, `"dutch"`)
- `frame` — Shot framing (e.g., `"CU"`, `"MCU"`, `"WS"`, `"ECU"`)
- `movement` — Camera movement (e.g., `"tracking"`, `"dolly"`, `"handheld"`)
- `plate` — VFX plate type (e.g., `"green"`, `"blue"`, `"clean"`)
- `element` — VFX element (e.g., `"background"`, `"foreground"`)

**Live Event/Broadcast-Specific Examples:**
- `transition` — Transition type (e.g., `"cut"`, `"dissolve"`, `"wipe"`)
- `preset` — Equipment preset (e.g., `"wide_shot"`, `"single"`, `"panel"`)
- `template` — Graphics template (e.g., `"lower_third"`, `"bug"`, `"full_screen"`)
- `position` — Graphics position (e.g., `"lower_third"`, `"corner"`, `"center"`)
- `compression` — Audio compression (e.g., `"light"`, `"medium"`, `"heavy"`)
- `gate` — Audio gate threshold (e.g., `"-20dB"`)

**Documentation:**
- `note` — Internal notes/reminders (not shown to operators in cue sheets)

### Format Rules

**Time Values:**
- **Units MUST be specified** for numeric values
- **Valid units:** `s` (seconds), `m` (minutes), `ms` (milliseconds), `h` (hours)
- **Descriptive values also valid:** `slow`, `fast`, `instant`
- Examples: `fade=3s` ✅ `fade=slow` ✅ `fade=3` ❌

**Level/Intensity Values:**
- **Percentage:** `80%`, `50%`
- **Decimal:** `0.5`, `0.8`
- **Decibels:** `-6dB`, `-3dB`
- **Descriptive:** `full`, `half`, `dim`

**File Paths:**
- Use quotes if filename contains spaces: `file="my sound.wav"`
- No quotes needed for simple names: `file=thunder.wav`

**Boolean Values:**
- Use `true`/`false` or just the key name for true
- Examples: `loop=true`, `autofollow=false`

### Metadata Examples

**Theatre:**
```
LX (cue 5) [fade=3s]: Fade to blackout
SQ (cue 2) [file="thunder.wav", level=-3dB]: Thunder crash
FLY (cue 1) [warn=2m, duration=30s]: Bring in chandelier
SPOT (cue 7) [target=spot_1, level=80%]: Pick up JOHN
```

**Film:**
```
CAMERA (cue 12) [lens=50mm, angle=low]: Close-up on actor
LIGHT (cue 3) [type=key, direction=left, intensity=2k]: Key light
SOUND (cue 2) [boom=overhead, wind=reduce]: Dialogue recording
VFX (cue 8) [plate=green, element=background]: Composite shot
```

**Live Events:**
```
VIDEO (cue 3) [source=cam2, transition=cut]: Switch to speaker cam
AUDIO (cue 7) [fade=2s, level=-6dB]: Music under speech
GRAPHICS (cue 1) [duration=8s, position=lower_third]: Guest name
CAMERA (cue 5) [preset=wide, speed=slow]: Audience pan
```

**Broadcast:**
```
PLAYBACK (cue 1) [file="package_intro.mp4", audio=stereo]: Roll intro
CAMERA (cue 3) [transition=dissolve, duration=1s]: Dissolve to camera 2
GRAPHICS (cue 4) [template=bug, position=corner]: Network logo
AUDIO (cue 2) [source=mic3, gate=-20dB]: Talent microphone
```

**Descriptive values also valid:**
```
LX (cue 12) [fade=slow, target=downstage]: Warm glow
VIDEO (cue 8) [transition=fast]: Quick cut
AUDIO (cue 3) [level=full]: Music at full volume
```

### Progressive Enhancement Workflow

The power of optional metadata is that the same cue can evolve throughout production:

**Phase 1: Initial Writing/Planning**
```
LX (cue 5): Fade to blackout
CAMERA (cue 12): Close-up on actor's face
```
Just mark where cues happen. Readable by all stakeholders.

**Phase 2: Rehearsal/Pre-Production**
```
LX (cue 5) [fade=3s]: Fade to blackout
CAMERA (cue 12) [lens=50mm]: Close-up on actor's face
```
Add timing and technical decisions as they're made. Still readable.

**Phase 3: Technical Preparation/Production**
```
LX (cue 5) [fade=3s, warn=30s, target=all]: Fade to blackout
CAMERA (cue 12) [lens=50mm, angle=low, frame=CU]: Close-up on actor's face
```
Production team adds implementation details. Export-ready for control systems.

**Key principle:** A cue is valid at every stage. Add detail when needed, not before.

### Standby/Warning System

CueScript uses the `warn` metadata to indicate when production coordinators should give advance notice to operators:

```
LX (cue 5) on "Juliet" [warn=30s, fade=3s]: Fade to blackout
VIDEO (cue 12) [warn=1m]: Roll pre-recorded package
CAMERA (cue 8) [warn=15s]: Crane move to overhead
```

**How it works:**
- `warn=30s` tells a parser to generate an advance notice 30 seconds before the cue
- No `warn` metadata = no advance notice needed (simple cues can execute immediately)
- Parser calculates placement based on script timing and trigger point

**Example — what a parser might generate:**

Source:
```
LX (cue 5) on "Juliet" [warn=30s, fade=3s]: Fade to blackout
```

Generated calling script view:
```
[~30 seconds before "Juliet" line]
┌─ STANDBY: LX 5
│
│  ... script continues ...
│
└─ [On "Juliet"]
   LX (cue 5) GO → Fade to blackout (3s fade)
```

Not every cue needs advance warning. Simple cues may not require `warn` metadata. Complex cues (crane moves, scenic automation, multi-source video setups) typically benefit from longer advance warnings.

---

## Common Cue Types

**CueScript does not restrict cue types.** Any uppercase identifier is valid. Productions define cue types based on their specific needs and workflows.

Below are common conventions from different production contexts. These are suggestions, not requirements.

### Theatre Productions Commonly Use:

| Type | Full Name | Description | Example |
|------|-----------|-------------|---------|
| `LX` | Lighting/Electrics | Lighting cues (UK/International) | `LX (cue 10): Sunset fade` |
| `LIGHT` | Lighting | Lighting cues (US alternative) | `LIGHT (cue 10): Sunset fade` |
| `SQ` | Sound | Sound effects and audio playback | `SQ (cue 1): Thunder crash` |
| `SOUND` | Sound | Sound cues (alternative) | `SOUND (cue 1): Thunder crash` |
| `MQ` | Music | Musical cues and underscoring | `MQ (cue 2): Opening theme` |
| `MUSIC` | Music | Music cues (alternative) | `MUSIC (cue 2): Opening theme` |
| `FLY` | Flys | Fly system/flying scenery | `FLY (cue 3): Bring in chandelier` |
| `SPOT` | Followspot | Follow spotlight operation | `SPOT (cue 7): Pick up JOHN` |
| `AUTO` | Automation | Automated scenery, turntables, lifts | `AUTO (cue 4): Revolve 180 degrees` |
| `VIDEO` | Video | Video playback | `VIDEO (cue 3): Display countdown` |
| `PROJ` | Projection | Projection mapping | `PROJ (cue 5): Show title card` |

### Film Productions Commonly Use:

| Type | Full Name | Description | Example |
|------|-----------|-------------|---------|
| `CAMERA` | Camera | Camera setup and movement | `CAMERA (cue 5): Dolly in on actor` |
| `SHOT` | Shot | Individual shot notation | `SHOT (cue 3a): Close-up, low angle` |
| `LIGHT` | Lighting | Lighting setup | `LIGHT (cue 2): Natural window light` |
| `SOUND` | Sound | Sound recording notes | `SOUND (cue 1): Boom from above` |
| `VFX` | Visual Effects | VFX elements and plates | `VFX (cue 12): Green screen background` |
| `STUNT` | Stunt | Stunt coordination | `STUNT (cue 1): Car crash sequence` |
| `MAKEUP` | Makeup | Makeup and prosthetics | `MAKEUP (cue 3): Blood effect applied` |
| `WARDROBE` | Wardrobe | Costume changes | `WARDROBE (cue 2): Hero switches jacket` |

### Live Events Commonly Use:

| Type | Full Name | Description | Example |
|------|-----------|-------------|---------|
| `VIDEO` | Video | Video switching and playback | `VIDEO (cue 5): Switch to camera 3` |
| `CAMERA` | Camera | Camera selection | `CAMERA (cue 2): Isolate speaker` |
| `AUDIO` | Audio | Audio mixing and playback | `AUDIO (cue 7): Mics up for panel` |
| `GRAPHICS` | Graphics | Lower thirds, titles | `GRAPHICS (cue 1): Display guest name` |
| `LIGHTS` | Lighting | Stage lighting cues | `LIGHTS (cue 4): Follow spot on host` |
| `PLAYBACK` | Playback | Media playback | `PLAYBACK (cue 3): Roll intro video` |

### Broadcast/Streaming Commonly Use:

| Type | Full Name | Description | Example |
|------|-----------|-------------|---------|
| `CAMERA` | Camera | Camera switching | `CAMERA (cue 8): Cut to camera 2` |
| `GRAPHICS` | Graphics | On-screen graphics | `GRAPHICS (cue 3): Lower third - name` |
| `AUDIO` | Audio | Audio levels and sources | `AUDIO (cue 5): Fade music bed` |
| `PLAYBACK` | Playback | Pre-recorded content | `PLAYBACK (cue 1): Roll package` |
| `TRANSITION` | Transition | Wipes, dissolves | `TRANSITION (cue 2): Fade to black` |

### Custom Cue Types

Productions can define any cue type that fits their workflow. Examples:
- `HAZE` — Atmospheric effects
- `PYRO` — Pyrotechnic effects
- `TRAP` — Stage trap operations
- `DRONE` — Drone camera shots
- `MIC` — Microphone cues
- `PRAC` — Practical effects
- `TALENT` — Talent/actor direction
- `CREW` — Crew position changes

**The format is completely open** — use whatever cue types make sense for your production.

---

## Fountain Compatibility

CueScript documents are valid Fountain documents. This compatibility is intentional but not a dependency — CueScript works equally well as standalone plain text.

### Visible Cues (Action Lines)

Standard Fountain action lines. Visible in all Fountain-compatible applications:

```fountain
INT. STAGE - NIGHT

The storm builds.

SQ (cue 5): Thunder crash
LX (cue 6) [fade=3s]: Fade to blackout
```

### Hidden Cues (Fountain Notes)

Fountain note syntax `[[ ]]` creates cues that are hidden in clean reading views:

```fountain
The lovers meet at last.

[[LX (cue 12a) on "Juliet": Fade to warm special]]

ROMEO
But, soft! What light through yonder window breaks?
```

Hidden cues are useful for:
- Continuous/atmospheric cues that don't need to be visible in a reading script
- Technical notes for operators only
- Cues that would distract from the narrative flow

### Forced Action Lines

The `!` prefix forces Fountain to treat a line as action, useful if a cue line would otherwise be parsed as a character name or heading:

```fountain
!LX (cue 1): House lights up
```

### Final Draft Compatibility

CueScript works within Final Draft documents when cues are placed in action/description paragraphs. The syntax is identical; Fountain-specific features (hidden notes with `[[ ]]`, forced lines with `!`) are not available in Final Draft, but all other CueScript syntax works as written.

---

## Complete Examples

### Theatre Example

```fountain
HAMLET - ACT III, SCENE I - THE PALACE

A room in the castle. Dim lighting.

LX (cue 45) [fade=5s]: Fade up from blackout — dim interior
SQ (cue 22): Distant wind ambience begins

OPHELIA moves to center stage.

[[SQ (cue 23) on "To be" [warn=10s]: Subtle underscore begins]]

HAMLET
To be, or not to be, that is the question.

LX (cue 46) [fade=2s]: Isolate HAMLET in special
```

### Film Example

```fountain
EXT. CLIFFTOP - GOLDEN HOUR

CAMERA (shot 14) [lens=85mm, frame=MCU]: Medium close-up on SARAH
LIGHT (setup 6) [type=key, direction=left]: Sun as practical key
SOUND (take 1): Boom from above, wind filter on

SARAH looks out over the sea.

CAMERA (shot 14a) [lens=85mm, movement=slow_push]: Push in slowly
```

### Live Event Example

```fountain
ANNUAL CONFERENCE - MAIN STAGE

House music plays. Audience settles.

AUDIO (cue 1) [fade=2s, source=playback]: House music fade out
VIDEO (cue 1) [source=cam1, transition=cut]: Camera 1 wide stage
GRAPHICS (cue 1) [template=lower_third, duration=8s]: Display "KEYNOTE SPEAKER"

Speaker walks to center stage.

AUDIO (cue 2) [source=lav_mic, gate=-20dB]: Activate speaker microphone

SPEAKER
Thank you all for coming today.

GRAPHICS (cue 2) [template=presentation, source=laptop]: Display slide 1
```

---

## Cue Numbering Conventions

### Sequential Numbering
Cues are typically numbered sequentially within each type:
```
SQ (cue 1): ...
SQ (cue 2): ...
SQ (cue 3): ...
```

### Insertion Methods

When cues are added during rehearsals or production, choose one of these approaches:

**Method A: Letter Suffixes** (Traditional)
```
SQ (cue 5): Original cue
SQ (cue 5a): Added during tech rehearsal
SQ (cue 5b): Added later
SQ (cue 6): Next original cue
```
Sorting order: 1, 1a, 1b, 2, 2a, 3, 3a, 3b, 3c, 4...

**Method B: Decimal Notation** (Alternative)
```
SQ (cue 5): Original cue
SQ (cue 5.5): Added during tech rehearsal
SQ (cue 5.7): Added later
SQ (cue 6): Next original cue
```
Sorting order: 1, 1.5, 2, 2.5, 3, 3.5, 4...

Choose ONE method per production and stick with it. Mixing both patterns in the same cue sequence can create sorting ambiguities.

### Cross-Type Numbering
Each cue type maintains its own numbering sequence:
```
SQ (cue 1): ...
LX (cue 1): ...  ← Different type, can reuse number
SQ (cue 2): ...
LX (cue 2): ...
```

This is standard practice — "LX 5" and "SQ 5" are different cues.

---

## Parser Requirements

A CueScript-compliant parser MUST:

1. **Recognize the basic pattern:** `CUETYPE (LABEL NUMBER) [TRIGGER] [metadata]: DESCRIPTION`
2. **Support flexible labels:** Recognize any lowercase label (pattern `[a-z]+`)
3. **Support cue numbers:** Support both numbering patterns:
   - Pattern A: `[0-9]+[a-z]*` (letter suffix: `1`, `5a`, `23b`)
   - Pattern B: `[0-9]+\.[0-9]+` (decimal: `1.5`, `5.5`)
4. **Recognize standard cue types:** All abbreviated forms listed above
5. **Handle optional triggers:** Parse `on "text"`, `after 3s`, `with action` syntax
6. **Handle optional metadata:** Parse `[key=value]` format in square brackets
7. **Validate time units:** Require units (s, m, ms, h) for numeric time values
8. **Handle Fountain notes:** Parse cues within `[[ ]]` as hidden cues
9. **Preserve Fountain compatibility:** Not break existing Fountain parsing
10. **Case sensitivity:** CUETYPE must be uppercase, labels lowercase, cue numbers preserve case

A CueScript-compliant parser SHOULD:

1. **Detect custom cue types:** Recognize any uppercase word following the pattern
2. **Warn on duplicate numbers:** Flag duplicate cue numbers within the same type
3. **Warn on label inconsistency:** Flag when same CUETYPE uses different labels
4. **Support common alternatives:** Recognize established abbreviation variants (LX/LIGHT, SQ/SOUND, MQ/MUSIC)
5. **Validate metadata:** Check that time values include units
6. **Generate coordination cues:** Calculate advance warning timing from `warn` metadata
7. **Warn on mixed numbering:** Flag use of both letter and decimal insertions in same cue type

A CueScript-compliant parser MAY:

1. **Suggest standardization:** Offer to normalize cue type naming
2. **Warn on gaps:** Identify missing numbers in sequences (optional — gaps are valid)
3. **Auto-number:** Suggest cue numbers for unnumbered technical actions
4. **Export to production systems:** Generate cue sheets, calling scripts, control system workspaces
5. **Domain-specific features:** Implement workflows specific to theatre, film, broadcast, etc.

---

## Edge Cases

### Cue References in Text
When dialogue or action mentions a cue without defining it, don't parse as a cue:

```fountain
STAGE MANAGER
Stand by for sound cue 5.

← Not parsed as a cue (missing colon and description)
```

### Mixed Case
Only uppercase CUETYPE is valid:

```fountain
sq (cue 1): Door slams      ← Invalid (not uppercase)
SQ (cue 1): Door slams      ← Valid
Sq (cue 1): Door slams      ← Invalid (mixed case)
```

### Missing Components
Core components required (type, label, number, description), triggers and metadata optional:

```fountain
SQ: Door slams              ← Invalid (missing label and number)
SQ (cue 5)                  ← Invalid (missing description)
(cue 5): Door slams         ← Invalid (missing cue type)
SQ (cue 5): Door slams      ← Valid (minimal form)
SQ (cue 5) on "exit": Door  ← Valid (with trigger)
SQ (cue 5) [level=-3dB]: Door ← Valid (with metadata)
```

### Whitespace
Parsers should be flexible with whitespace:

```fountain
SQ (cue 5): Door slams      ← Valid
SQ(cue 5): Door slams       ← Valid (no space before parenthesis)
SQ (cue  5): Door slams     ← Valid (extra space in number)
SQ  (cue 5):  Door slams    ← Valid (extra spaces)
```

### Trigger Formats
All these trigger formats are valid:

```fountain
LX (cue 5) on "Juliet": Fade    ← Dialogue trigger (quotes required)
LX (cue 5) after 3s: Fade       ← Time delay
LX (cue 5) with entrance: Fade  ← Action trigger
LX (cue 5): Fade                ← No trigger (implicit)
```

**Important:** Dialogue triggers (using `on`) MUST use quotes to distinguish them from descriptions:
```
✅ LX (cue 5) on "stage": Fade    ← Trigger on the word "stage"
❌ LX (cue 5) on stage: Fade      ← Ambiguous
✅ LX (cue 5): Fade on stage      ← Clear — "on stage" is part of description
```

---

## Validation Rules

### Required
- Cue type must be present and uppercase
- Label must be present and lowercase letters only
- Cue number must match one of these patterns:
  - Letter suffix: `[0-9]+[a-z]*` (e.g., `1`, `5a`, `23b`)
  - Decimal: `[0-9]+\.[0-9]+` (e.g., `1.5`, `5.5`)
- Description must be present (non-empty after colon)
- Time values in metadata MUST include units (s, m, ms, h)
- Dialogue triggers MUST use quotes: `on "word"` not `on word`

### Recommended Warnings
- **Label consistency:** Each CUETYPE should use the same label throughout the document
- **Numbering consistency:** Using both letter and decimal patterns in same cue type
- Duplicate cue numbers within same type
- Mixing abbreviations (e.g., using both LX and LIGHT in same script)
- Very long descriptions (>150 characters — might indicate error)
- Unknown cue types (not in standard list) — informational only, not an error
- Time values without units in metadata

### Not Required
- Sequential numbering across entire script
- Starting from 1 (can start at any number)
- Continuous sequences (gaps are allowed and common)
- Using abbreviated forms (SOUND is as valid as SQ)
- Triggers on every cue (optional element)
- Metadata on every cue (optional element)

---

## Best Practices

### Consistency
- Choose one naming convention per production (e.g., LIGHT vs LX — pick one)
- Use consistent cue type names throughout the script
- Number cues sequentially within each discipline

### Clarity
- Keep descriptions concise but clear
- Describe the effect or result, not the technical implementation
- Use terminology your production team understands
- Save technical details for metadata

### Organization
- Use hidden cues `[[ ]]` for technical notes that shouldn't clutter the reading script
- Use visible cues for actions that all stakeholders need to see
- Group related cues near each other in the script

### Production Process
- Start with sequential numbers (1, 2, 3...)
- Add revision letters (5a, 5b) during production as needed
- Avoid renumbering entire sequences mid-production
- Add metadata progressively as decisions are made

---

## Version History

**v0.9 (Public Draft — January 2026)**
- First public release for community feedback
- Core syntax definition
- Domain-agnostic design
- Common cue type conventions across theatre, film, live events, and broadcast
- Optional trigger syntax (`on`, `after`, `with`)
- Optional metadata system `[key=value]`
- Timing rules (units required for numeric values)
- Standby/warning system via `warn` metadata
- Progressive enhancement workflow
- Fountain compatibility
- Final Draft compatibility

---

## Future Considerations (v1.0+)

Features being considered for future versions:

- **Cue relationships:** Syntax for linked, simultaneous, or follow-on cues
- **Role-specific cues:** Tie cues to specific performers, crew positions, or equipment
- **Multi-language support:** Support for non-English productions
- **Extended trigger types:** More sophisticated trigger conditions and dependencies
- **Conditional cues:** Cues that fire based on conditions (alternate takes, live vs recorded, etc.)
- **Timeline integration:** Explicit timecode or time-based triggering
- **Multi-camera notation:** Specific syntax for multi-camera productions
- **Revision tracking:** Built-in change tracking and version control

---

## License

CueScript is an open specification released under [CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/).

Implementations may use any license. The specification text may be freely shared and implemented with attribution, but may not be modified or republished in altered form.

---

## Acknowledgments

CueScript draws from production practices across theatre, film, television, live events, and broadcast industries. Thanks to production coordinators, stage managers, assistant directors, technical directors, and crew members across all disciplines for establishing the conventions that inform this specification.

### Fountain

CueScript is inspired by **Fountain**, the open plain-text markup language for screenwriting created by [John August](http://johnaugust.com), [Stu Maschwitz](http://prolost.com), and [Nima Yousefi](http://nimayousefi.com), with contributions from Martin Vilcans, Brett Terpstra, Jonathan Poritsky, Kent Tessman, and Clinton Torres.

Fountain's approach to plain-text document formatting — human-readable, portable, future-proof, and built on open standards — informed CueScript's design principles.

Learn more about Fountain at [fountain.io](https://fountain.io)

---

*CueScript Specification v0.9 (Public Draft)*  
*January 2026*
