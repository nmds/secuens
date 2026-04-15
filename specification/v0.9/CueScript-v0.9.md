# CueScript Technical Cue Notation

## Specification v0.9 (Public Draft)

**Status:** Public Draft  
**Date:** April 2026  
**License:** CC BY-ND 4.0

---

## Overview

**CueScript** is a technical cue notation syntax built on the Fountain screenplay format. It allows production coordinators, directors, and technical teams to embed standardized technical cues within readable scripts while maintaining full compatibility with Fountain-based tools and Final Draft.

CueScript is a universal format that works across any production context requiring technical notation: theatre, film, television, live events, broadcast, podcasts, and more. The same syntax serves different domains through specialized applications built on the open format.

### File Format

CueScript documents are plain UTF-8 text files. They can be created and edited in any text editor and are fully compatible with Fountain-based applications.

**File Extensions**

CueScript documents use one of two extensions:

- **`.fountain`** — Standard Fountain extension. Use when working within the Fountain ecosystem or sharing with screenwriters, directors, and actors. Opens in any Fountain-compatible application.

- **`.cuescript`** — CueScript-specific extension. Use when creating production-focused documents or working primarily in CueScript-aware tools. Signals that the file contains technical cue notation.

Both extensions contain identical content and are fully interchangeable. The choice of extension signals intent and default application behavior, not format differences.

> **Note:** CueScript tools may accept `.txt` files as input when the content conforms to CueScript syntax, but `.txt` is not a recognized CueScript file extension.

### Design Principles

1. **Fountain-Native** - Built on Fountain syntax; CueScript documents are valid Fountain documents
2. **Domain-Agnostic** - Universal format that works across theatre, film, live events, broadcast, and any production context
3. **Non-Invasive** - Doesn't interfere with screenplay writing or reading experience
4. **Progressive Enhancement** - Start simple, add detail as production develops
5. **Parser-Friendly** - Clear, unambiguous patterns for reliable automated processing
6. **Human-Readable** - Cues are immediately understandable without specialized tools
7. **Open & Extensible** - Custom cue types and metadata keys welcome; specialized tools can build on the open format

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
    - `CAMERA (shot 5)` - if CAMERA uses "shot", all CAMERA cues must use "shot"
    - `LIGHT (setup 3)` - if LIGHT uses "setup", all LIGHT cues must use "setup"
  - Default/recommended: `cue` for all types

- **NUMBER**: Cue identifier supporting insertions
  - **Pattern A (Letter suffix):** `[0-9]+[a-z]*`
    - Examples: `1`, `12`, `5a`, `23b`, `100`
    - Common practice: Insert 5a between 5 and 6
  - **Pattern B (Decimal):** `[0-9]+\.[0-9]+`
    - Examples: `1.5`, `2.5`, `10.5`
    - Alternative practice: Insert 5.5 between 5 and 6
  - **Pattern C (QLab-style prefixed):** `[A-Z][0-9]+[a-z]*`
    - Examples: `A1`, `V3`, `A5a`, `L12b`
    - Common in QLab workflows where cue type is embedded in the number
    - The letter prefix is part of the number, not the CUETYPE
  - **Note:** Choose ONE pattern per production. Mixing patterns within the same cue type may cause sorting confusion.
  - Combined patterns (e.g., `5.5a`) are not currently supported pending validation of real-world usage.

- **TRIGGER** _(optional)_: When/how the cue is triggered
  - Keywords: `on`, `after`, `with`
  - Formats:
    - `on "dialogue"` - Triggers on specific spoken words (**quotes required**)
    - `after 3s` - Triggers after a time delay
    - `with action` - Triggers simultaneously with an action
  - If omitted, cue trigger is implicit from context
  - Examples:
    - `on "Juliet"` - Trigger when actor says "Juliet"
    - `after 2s` - Trigger 2 seconds after previous cue/action
    - `with door slam` - Trigger simultaneously with door slam
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

# Mixed in same document (valid - different CUETYPES)
CAMERA (shot 12): Close-up
LIGHT (cue 5): Key from left
SOUND (take 3): Dialogue recording

# Invalid - inconsistent within same CUETYPE
CAMERA (shot 1): Wide
CAMERA (cue 2): Close    â† ERROR: CAMERA already uses "shot"
```

---

## Metadata (Optional Technical Details)

CueScript supports optional metadata for technical implementation. Metadata is added in square brackets before the colon:

```
CUETYPE (cue NUMBER) [key=value, key2=value2]: DESCRIPTION
```

### Standard Metadata Keys

CueScript defines common metadata keys that work across domains. **Custom keys are always allowed** - any production can define domain-specific metadata.

**Universal Timing & Control:**

- `duration` - How long the cue takes to execute (e.g., `5s`, `2m`, `45s`)
- `fade` - Fade/transition time (e.g., `3s`, `500ms`)
- `prewait` - Delay before cue starts (e.g., `1s`, `2s`)
- `postwait` - Delay after cue completes (e.g., `2s`)
- `warn` - Advance warning time for coordination (e.g., `30s`, `2m`)

**Common Technical Parameters:**

- `level` - Intensity/volume (e.g., `80%`, `0.5`, `-6dB`)
- `file` - Media file reference (e.g., `"thunder.wav"`, `"intro.mp4"`)
- `target` - Specific equipment/output (e.g., `"channel_5"`, `"cam2"`, `"speaker_left"`)
- `source` - Input source (e.g., `"mic3"`, `"playback"`, `"laptop"`)
- `type` - Variant or category (e.g., `"key"`, `"bounce"`, `"practical"`)

**Theatre-Specific Examples:**

- `curve` - Lighting fade curve (e.g., `"log"`, `"linear"`)
- `intensity` - Light level (e.g., `"full"`, `"50%"`)
- `position` - Followspot position (e.g., `"center_stage"`, `"downstage_left"`)

**Film-Specific Examples:**

- `lens` - Camera lens (e.g., `"50mm"`, `"wide"`)
- `angle` - Camera angle (e.g., `"low"`, `"high"`, `"dutch"`)
- `frame` - Shot framing (e.g., `"CU"`, `"MCU"`, `"WS"`, `"ECU"`)
- `movement` - Camera movement (e.g., `"tracking"`, `"dolly"`, `"handheld"`)
- `plate` - VFX plate type (e.g., `"green"`, `"blue"`, `"clean"`)
- `element` - VFX element (e.g., `"background"`, `"foreground"`)

**Live Event/Broadcast-Specific Examples:**

- `transition` - Transition type (e.g., `"cut"`, `"dissolve"`, `"wipe"`)
- `preset` - Equipment preset (e.g., `"wide_shot"`, `"single"`, `"panel"`)
- `template` - Graphics template (e.g., `"lower_third"`, `"bug"`, `"full_screen"`)
- `position` - Graphics position (e.g., `"lower_third"`, `"corner"`, `"center"`)
- `compression` - Audio compression (e.g., `"light"`, `"medium"`, `"heavy"`)
- `gate` - Audio gate threshold (e.g., `"-20dB"`)

**Documentation:**

- `note` - Internal notes/reminders (not shown to operators in cue sheets)

### Format Rules

**Time Values:**

- **Units MUST be specified** for numeric values
- **Valid units:** `s` (seconds), `m` (minutes), `ms` (milliseconds), `h` (hours)
- **Descriptive values also valid:** `slow`, `fast`, `instant`
- Examples: `fade=3s` âœ… `fade=slow` âœ… `fade=3` âŒ

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

**Phase 2: Rehearsal/Pre-Production Refinement**

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

- `warn=30s` tells parser to generate an advance notice 30 seconds before the cue
- No `warn` metadata = no advance notice needed (simple cues can execute immediately)
- Parser calculates placement based on script timing and trigger point

**Example - What a parser might generate:**

**Source:**

```
LX (cue 5) on "Juliet" [warn=30s, fade=3s]: Fade to blackout
```

**Generated calling script view:**

```
[~30 seconds before "Juliet" line]
â”Œâ”€ STANDBY: LX 5
â”‚
â”‚  ... script continues ...
â”‚
â””â”€ [On "Juliet"]
   LX (cue 5) GO â†’ Fade to blackout (3s fade)
```

**Not every cue needs advance warning.** Simple cues (like quick audio transitions or camera cuts) may not require `warn` metadata. Complex cues (like crane moves, scenic automation, or multi-source video setups) typically benefit from longer advance warnings.

---

## Common Cue Types

**CueScript does not restrict cue types.** Any uppercase identifier is valid. Productions define cue types based on their specific needs and workflows.

Below are common conventions from different production contexts. These are suggestions, not requirements.

### Theatre Productions Commonly Use:

| Type    | Full Name          | Description                          | Example                             |
| ------- | ------------------ | ------------------------------------ | ----------------------------------- |
| `LX`    | Lighting/Electrics | Lighting cues (UK/International)     | `LX (cue 10): Sunset fade`          |
| `LIGHT` | Lighting           | Lighting cues (US alternative)       | `LIGHT (cue 10): Sunset fade`       |
| `SQ`    | Sound              | Sound effects and audio playback     | `SQ (cue 1): Thunder crash`         |
| `SOUND` | Sound              | Sound cues (alternative)             | `SOUND (cue 1): Thunder crash`      |
| `MQ`    | Music              | Musical cues and underscoring        | `MQ (cue 2): Opening theme`         |
| `MUSIC` | Music              | Music cues (alternative)             | `MUSIC (cue 2): Opening theme`      |
| `FLY`   | Flys               | Fly system/flying scenery            | `FLY (cue 3): Bring in chandelier`  |
| `SPOT`  | Followspot         | Follow spotlight operation           | `SPOT (cue 7): Pick up JOHN`        |
| `AUTO`  | Automation         | Automated scenery, turntables, lifts | `AUTO (cue 4): Revolve 180 degrees` |
| `VIDEO` | Video              | Video playback                       | `VIDEO (cue 3): Display countdown`  |
| `PROJ`  | Projection         | Projection mapping                   | `PROJ (cue 5): Show title card`     |

### Film Productions Commonly Use:

| Type       | Full Name      | Description               | Example                                  |
| ---------- | -------------- | ------------------------- | ---------------------------------------- |
| `CAMERA`   | Camera         | Camera setup and movement | `CAMERA (cue 5): Dolly in on actor`      |
| `SHOT`     | Shot           | Individual shot notation  | `SHOT (cue 3a): Close-up, low angle`     |
| `LIGHT`    | Lighting       | Lighting setup            | `LIGHT (cue 2): Natural window light`    |
| `SOUND`    | Sound          | Sound recording notes     | `SOUND (cue 1): Boom from above`         |
| `VFX`      | Visual Effects | VFX elements and plates   | `VFX (cue 12): Green screen background`  |
| `STUNT`    | Stunt          | Stunt coordination        | `STUNT (cue 1): Car crash sequence`      |
| `MAKEUP`   | Makeup         | Makeup and prosthetics    | `MAKEUP (cue 3): Blood effect applied`   |
| `WARDROBE` | Wardrobe       | Costume changes           | `WARDROBE (cue 2): Hero switches jacket` |

### Live Events Commonly Use:

| Type       | Full Name | Description                  | Example                                |
| ---------- | --------- | ---------------------------- | -------------------------------------- |
| `VIDEO`    | Video     | Video switching and playback | `VIDEO (cue 5): Switch to camera 3`    |
| `CAMERA`   | Camera    | Camera selection             | `CAMERA (cue 2): Isolate speaker`      |
| `AUDIO`    | Audio     | Audio mixing and playback    | `AUDIO (cue 7): Mics up for panel`     |
| `GRAPHICS` | Graphics  | Lower thirds, titles         | `GRAPHICS (cue 1): Display guest name` |
| `LIGHTS`   | Lighting  | Stage lighting cues          | `LIGHTS (cue 4): Follow spot on host`  |
| `PLAYBACK` | Playback  | Media playback               | `PLAYBACK (cue 3): Roll intro video`   |

### Broadcast/Streaming Commonly Use:

| Type         | Full Name  | Description              | Example                                |
| ------------ | ---------- | ------------------------ | -------------------------------------- |
| `CAMERA`     | Camera     | Camera switching         | `CAMERA (cue 8): Cut to camera 2`      |
| `GRAPHICS`   | Graphics   | On-screen graphics       | `GRAPHICS (cue 3): Lower third - name` |
| `AUDIO`      | Audio      | Audio levels and sources | `AUDIO (cue 5): Fade music bed`        |
| `PLAYBACK`   | Playback   | Pre-recorded content     | `PLAYBACK (cue 1): Roll package`       |
| `TRANSITION` | Transition | Wipes, dissolves         | `TRANSITION (cue 2): Fade to black`    |

### Custom Cue Types

Productions can define any cue type that fits their workflow. Examples:

- `HAZE` - Atmospheric effects
- `PYRO` - Pyrotechnic effects
- `TRAP` - Stage trap operations
- `DRONE` - Drone camera shots
- `MIC` - Microphone cues
- `PRAC` - Practical effects
- `TALENT` - Talent/actor direction
- `CREW` - Crew position changes

**The format is completely open** - use whatever cue types make sense for your production.

---

## Software Compatibility

CueScript is designed to work with industry-standard screenplay software, including both Fountain-based editors and Final Draft.

**Important:** CueScript documents are valid Fountain documents. Any Fountain-compatible application can open and edit them. CueScript-aware tools add the ability to _recognize and process_ the technical cue notation, but the files remain fully compatible with standard Fountain parsers.

### Fountain Integration

CueScript leverages three Fountain syntax features:

#### 1. Action Lines (Visible Cues)

CueScript cues are written as standard Fountain action lines. Any Fountain parser will see them as regular action elements:

```fountain
John walks to the door.

SQ (cue 5): Door slams shut

He jumps back in surprise.
```

**Result:** Cue appears in formatted screenplay, visible to all readers.

**Fountain Compatibility:** A standard Fountain parser treats this as an action line. A CueScript-aware parser recognizes it as a technical cue.

#### 2. Forced Action (Guaranteed Visibility)

Use Fountain's `!` prefix to force a line to be treated as action:

```fountain
!SQ (cue 5): Door slams shut
```

**Use when:** You need to ensure the cue appears in formatted output even if it might otherwise be interpreted differently.

#### 3. Notes (Hidden Cues)

Use Fountain's note syntax `[[ ]]` for cues that should only be visible to technical staff:

```fountain
John walks to the door.

[[SQ (cue 1): Background ambience loop]]

SQ (cue 5): Door slams shut
```

**Result:** `cue 1` is parsed by CueScript tools but invisible in formatted screenplay. `cue 5` is visible to all readers.

**Use for:**

- Atmospheric/background cues that don't need to be in the reading script
- Technical notes for operators
- Cues that clutter the reading experience

### Final Draft Compatibility

CueScript works seamlessly with Final Draft, the industry-standard screenwriting software, through multiple workflows.

#### Basic Workflow (Recommended for Most Users)

Write CueScript cues as **Action elements** in Final Draft using standard CueScript syntax:

**In Final Draft:**

1. Create an Action element (press Enter after dialogue, or use Format menu)
2. Type your cue using CueScript syntax: `SQ (cue 5): Door slams shut`
3. Continue writing your script normally
4. When ready to manage cues, export as **"Text with Layout"** (.txt)
5. Import the exported text file into CueScript-compatible software

**Example in Final Draft:**

```
INT. MANSION - NIGHT

John enters cautiously.

[Action Element]
SQ (cue 2): Distant thunder

He approaches the door.

[Action Element]
SQ (cue 3): Door slams shut

[Action Element]
LX (cue 4): Lights flicker
```

**What exports:**

```
INT. MANSION - NIGHT

John enters cautiously.

SQ (cue 2): Distant thunder

He approaches the door.

SQ (cue 3): Door slams shut

LX (cue 4): Lights flicker
```

The exported text preserves CueScript syntax perfectly and can be parsed by any CueScript-compatible tool.

**Notes for Final Draft Users:**

- Cues appear as regular action lines in your script
- They're visible to all readers (directors, actors, crew)
- For hidden cues, use Final Draft's Notes feature (Insert â†’ Note), then write CueScript syntax inside the note
- Final Draft notes export with `[[double brackets]]`, which matches Fountain's hidden note syntax

#### Fountain Round-Trip Workflow

For users who work in both Final Draft and Fountain-based editors:

**Final Draft â†’ Fountain:**

1. Export Final Draft script as `.fdx` (File â†’ Save As â†’ Final Draft 8-13 (.fdx))
2. Convert to Fountain using:
   - **Highland** (Mac) - Import FDX, export as Fountain
   - **Fade In** - Can open FDX and save as Fountain
   - **Online converters** - Various web-based tools
3. Edit in Fountain editor (can use hidden `[[cues]]` syntax)
4. Import into CueScript tools

**Fountain â†’ Final Draft:**

1. Convert Fountain to FDX using the same tools
2. Import FDX into Final Draft
3. CueScript cues preserved as action elements
4. Continue editing in Final Draft

**Benefits of this workflow:**

- Full access to Fountain's hidden cue syntax `[[...]]`
- Work in whichever app suits the task
- No data loss between formats
- Leverage both ecosystems

#### Custom Elements Workflow (Advanced)

Power users who want visual distinction of cue types in Final Draft can create custom paragraph elements.

**Setup (one time per computer):**

1. In Final Draft: Format â†’ Elements â†’ New Element
2. Create custom elements for each cue type you use:
   - Name: "Sound Cue" (or "SQ")
   - Based on: Action
   - Customize appearance (color, font, etc.)
3. Repeat for Light Cue, Music Cue, etc.
4. Save as template for future projects

**Using Custom Elements:**

1. Type your cue: `SQ (cue 5): Door slams shut`
2. Apply custom element formatting
3. Cues visually distinct from regular action
4. Export as "Text with Layout" - syntax preserved

**Benefits:**

- Visual distinction in Final Draft
- Easier to scan for cues while writing
- Professional appearance
- Still exports as valid CueScript syntax

**Trade-offs:**

- Requires initial setup or template installation
- Custom elements don't transfer when sharing raw .fdx files
- More setup than basic workflow

#### Recommendations by User Type

**Production Coordinators & Technical Directors:**

- Use **Basic Workflow** - simple, works everywhere
- Or use **Fountain editors** directly (Highland, Slugline, etc.)

**Directors & Writers:**

- Use **Basic Workflow** in Final Draft
- Keep cues visible in script during planning/rehearsal
- Let production team add technical details later

**Technical Teams:**

- Use **Fountain editors** for maximum control
- Or import from Final Draft exports
- Add metadata during technical preparation phase

**Film Productions:**

- Use **Custom Elements Workflow** to distinguish camera, lighting, VFX cues
- Visual coding helps during script breakdown
- Export preserves all CueScript syntax

**Live Event/Broadcast Teams:**

- **Basic Workflow** often sufficient for rundowns
- Hidden cues `[[ ]]` for technical notes not needed by talent
- Metadata crucial for video switching and audio routing

---

## Complete Examples

### Theatre Production Example

```fountain
INT. HAUNTED MANSION - NIGHT

John enters cautiously. The floorboards creak under his feet.

[[SQ (cue 1) [file="ambience_mansion.wav", level=0.3, loop=true]: Background ambience]]

He pauses, listening.

SQ (cue 2) [level=-6dB]: Distant thunder

He approaches the large wooden door.

!SQ (cue 3) on door contact: Door slams shut

LX (cue 4) with door slam [duration=500ms]: Lights flicker

John spins around, startled.

MQ (cue 5) [prewait=1s, fade=2s]: Tension underscore begins

JOHN
Who's there?

[[SPOT (cue 6) [warn=30s, target=spot_1]: Isolate John center stage]]

No response. Only silence.

LX (cue 7) [fade=5s, warn=30s]: Slow fade to blackout

FADE OUT.
```

### Film Production Example

```fountain
EXT. CITY STREET - DAY

Traffic moves past. Sarah walks briskly down the sidewalk.

CAMERA (shot 1) [lens=35mm, movement=tracking]: Follow Sarah medium shot

She glances over her shoulder nervously.

CAMERA (shot 2) [lens=85mm, angle=low, frame=CU]: Close-up - Sarah's eyes

A black car pulls up alongside her.

SOUND (take 1) [note="Capture car approach separately"]: Car engine close-up

Sarah stops. The window rolls down.

CAMERA (shot 3) [lens=50mm, angle=interior]: Through car window to driver

MYSTERIOUS MAN
Get in.

LIGHT (setup 2) [type=bounce, direction=left]: Soften shadows on actor

Sarah hesitates, then opens the door.

VFX (cue 4) [plate=green, element=city_background]: Background replacement

FADE TO:
```

### Live Event Example

```fountain
CONFERENCE - MAIN STAGE

House lights dim. Audience settles.

LIGHTS (cue 1) [fade=3s, preset=stage_wash]: Stage lights up

VIDEO (cue 2) [source=playback, file="intro.mp4"]: Roll intro video

Music builds. Video ends.

AUDIO (cue 3) [fade=2s, source=playback]: Fade music bed

GRAPHICS (cue 4) [template=lower_third, duration=8s]: Display "KEYNOTE SPEAKER"

Speaker walks to center stage.

CAMERA (cue 5) [preset=single_shot, transition=dissolve]: Camera 2 - speaker medium

Applause. Speaker begins.

AUDIO (cue 6) [source=lav_mic, gate=-20dB]: Activate speaker microphone

SPEAKER
Thank you all for coming today.

GRAPHICS (cue 7) [template=presentation, source=laptop]: Display slide 1

Speaker gestures to screen.

CAMERA (cue 8) [preset=wide, speed=slow]: Pull back to wide shot

The presentation continues.
```

### Broadcast Example

```fountain
NEWSCAST - STUDIO A

Opening music plays.

PLAYBACK (cue 1) [file="news_open.mp4", audio=stereo]: Roll open

Graphics animate on screen.

GRAPHICS (cue 2) [template=news_open, duration=5s]: Animated title sequence

Music fades. Camera reveals anchor desk.

CAMERA (cue 3) [source=cam1, transition=dissolve, duration=1s]: Dissolve to anchor

AUDIO (cue 4) [fade=2s, level=-12dB]: Music bed under

Anchor looks to camera.

AUDIO (cue 5) [source=anchor_mic, compression=medium]: Anchor microphone hot

ANCHOR
Good evening. Our top story tonight...

GRAPHICS (cue 6) [template=over_shoulder, image="city_hall.jpg"]: OTS graphic

Anchor continues reading.

PLAYBACK (cue 7) [file="package_city.mp4", cue_point=timecode]: Roll package

Video package plays.

TRANSITION (cue 8) with package end [type=fade, duration=1s]: Fade to black

Back to studio.

CAMERA (cue 9) [source=cam1]: Cut to anchor
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

When cues are added during rehearsals/production, choose one of these approaches:

**Method A: Letter Suffixes** (Traditional)

```
SQ (cue 5): Original cue
SQ (cue 5a): Added during tech rehearsal
SQ (cue 5b): Added later
SQ (cue 6): Next original cue
```

**Sorting order:** 1, 1a, 1b, 2, 2a, 3, 3a, 3b, 3c, 4...

**Method B: Decimal Notation** (Alternative)

```
SQ (cue 5): Original cue
SQ (cue 5.5): Added during tech rehearsal
SQ (cue 5.7): Added later
SQ (cue 6): Next original cue
```

**Sorting order:** 1, 1.5, 2, 2.5, 3, 3.5, 4...

> Choose ONE insertion method per production and stick with it. Mixing letter suffixes and decimals within the same cue type creates sorting ambiguities. This follows standard theatre practice where cues are inserted during tech rehearsals without renumbering the entire show.

### Cross-Type Numbering

Each cue type maintains its own numbering sequence:

```
SQ (cue 1): ...
LX (cue 1): ...  â† Different type, can reuse number
SQ (cue 2): ...
LX (cue 2): ...
```

This is standard practice - "LX 5" and "SQ 5" are different cues.

---

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
11. **Handle plain text exports:** Parse text from both Fountain and Final Draft sources

A CueScript-compliant parser SHOULD:

1. **Detect custom cue types:** Recognize any uppercase word following the pattern
2. **Warn on duplicate numbers:** Flag duplicate cue numbers within the same type
3. **Warn on label inconsistency:** Flag when same CUETYPE uses different labels (e.g., `CAMERA (shot 1)` then `CAMERA (cue 2)`)
4. **Support common alternatives:** Recognize established abbreviation variants (LX/LIGHT, SQ/SOUND, MQ/MUSIC)
5. **Extract metadata:** Document title, acts, scenes from Fountain structure
6. **Validate metadata:** Check that time values include units
7. **Generate coordination cues:** Calculate advance warning timing from `warn` metadata
8. **Warn on mixed numbering:** Flag use of both letter and decimal insertions in same cue type (e.g., `5a` and `5.5` for the same CUETYPE)

A CueScript-compliant parser MAY:

1. **Suggest standardization:** Offer to normalize cue type naming
2. **Warn on gaps:** Identify missing numbers in sequences (optional - gaps are valid)
3. **Auto-number:** Suggest cue numbers for unnumbered technical actions
4. **Cross-reference:** Link repeated cue references in dialogue/action
5. **Export to production systems:** Generate cue sheets, calling scripts, control system workspaces (QLab, video switchers, etc.)
6. **Domain-specific features:** Implement workflows specific to theatre, film, broadcast, etc.

---

## Edge Cases

### Cue References in Text

When dialogue or action mentions a cue without defining it, don't parse as a cue:

```fountain
STAGE MANAGER
Stand by for sound cue 5.

â† Not parsed as a cue (missing colon and description)
```

### Mixed Case

Only uppercase CUETYPE is valid:

```fountain
sq (cue 1): Door slams      â† Invalid (not uppercase)
SQ (cue 1): Door slams      â† Valid
Sq (cue 1): Door slams      â† Invalid (mixed case)
```

### Missing Components

Core components required (type, number, description), triggers and metadata optional:

```fountain
SQ: Door slams              â† Invalid (missing cue number)
SQ (cue 5)                  â† Invalid (missing description)
(cue 5): Door slams         â† Invalid (missing cue type)
SQ (cue 5): Door slams      â† Valid (minimal form)
SQ (cue 5) on "exit": Door  â† Valid (with trigger)
SQ (cue 5) [level=-3dB]: Door â† Valid (with metadata)
```

### Whitespace

Parsers should be flexible with whitespace:

```fountain
SQ (cue 5): Door slams      â† Valid
SQ(cue 5): Door slams       â† Valid (no space before parenthesis)
SQ (cue  5): Door slams     â† Valid (extra space in number)
SQ  (cue 5):  Door slams    â† Valid (extra spaces)
```

### Trigger Formats

All these trigger formats are valid:

```fountain
LX (cue 5) on "Juliet": Fade    â† Dialogue trigger (quotes required)
LX (cue 5) after 3s: Fade       â† Time delay
LX (cue 5) with entrance: Fade  â† Action trigger
LX (cue 5): Fade                â† No trigger (implicit)
```

**Important:** Dialogue triggers (using `on`) MUST use quotes to distinguish them from descriptions that might start with "on". For example:

```
âœ… LX (cue 5) on "stage": Fade    â† Trigger on the word "stage"
âŒ LX (cue 5) on stage: Fade      â† Ambiguous - is "on stage" the description?
âœ… LX (cue 5): Fade on stage      â† Clear - "on stage" is part of description
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
  - Example: If `CAMERA (shot 1)` is used, `CAMERA (cue 2)` should trigger a warning
- **Numbering consistency:** Using both letter and decimal patterns in same cue type
  - Example: `LX (cue 5a)` and `LX (cue 6.5)` should trigger a warning
- Duplicate cue numbers within same type
- Mixing abbreviations (e.g., using both LX and LIGHT in same script)
- Very long descriptions (>150 characters - might indicate error)
- Unknown cue types (not in standard list) - informational only, not an error
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

- Choose one naming convention per production (e.g., LIGHT vs LX - pick one)
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

### Metadata Usage

- Don't add metadata until you know the values
- Simple cues often don't need metadata
- Complex cues benefit from detailed metadata
- Use `warn` metadata for cues requiring advance preparation

### Domain-Specific Tips

**Theatre:**

- Use `warn` for complex cues (fly, automation, scene changes)
- Hidden cues for continuous/atmospheric elements
- Visible cues for actions that affect actors

**Film:**

- Camera and lighting setups often need detailed metadata
- Cue numbers can reuse with revision letters (cue 1, cue 1a for additional takes)
- VFX cues should note plates, elements, compositing needs

**Live Events:**

- Video and camera cues benefit from transition metadata
- Audio cues should specify sources and routing
- Graphics cues should note templates and durations

**Broadcast:**

- Playback cues need file references and cue points
- Camera transitions should specify type and duration
- Audio cues should note levels and compression

---

## Version History

**v0.9 (Public Draft - April 2026)**

- Initial public specification
- Core syntax definition
- Domain-agnostic design
- Common cue type conventions across theatre, film, live events, and broadcast
- Optional trigger syntax (`on`, `after`, `with`)
- Optional metadata system `[key=value]`
- Timing rules (units required for numeric values)
- Standby/warning system via `warn` metadata
- Progressive enhancement workflow
- Fountain integration patterns
- Final Draft compatibility
- Based on production practices across multiple industries

---

## Future Considerations (v2.0+)

Features being considered for future versions:

- **Cue relationships:** Syntax for linked, simultaneous, or follow-on cues
- **Role-specific cues:** Tie cues to specific performers, crew positions, or equipment
- **Pre-production checklists:** Cue counts and readiness verification
- **Multi-language support:** Support for non-English productions
- **Extended trigger types:** More sophisticated trigger conditions and dependencies
- **Conditional cues:** Cues that fire based on conditions (alternate takes, live vs recorded, etc.)
- **Timeline integration:** Explicit timecode or time-based triggering
- **Multi-camera notation:** Specific syntax for multi-camera productions
- **Revision tracking:** Built-in change tracking and version control

---

## License

CueScript is an open specification. Implementations may use any license, but the specification itself is released under [CC BY-ND 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Reference Implementation

**QBook** is a macOS application and the reference implementation of CueScript, demonstrating how specialized tools can be built on the universal CueScript format. QBook parses CueScript documents and exports directly to QLab workspaces.

CueScript is an open format — implementations can serve any production domain. QBook focuses on theatre and live production workflows, but film, broadcast, and live event applications are equally valid uses of the specification.

For more information: https://github.com/nmds/cuescript

---

## Acknowledgments

CueScript draws from production practices across theatre, film, television, live events, and broadcast industries. Thanks to production coordinators, stage managers, assistant directors, technical directors, and crew members across all disciplines for establishing the conventions that inform this specification.

### Fountain

CueScript is built on **Fountain**, the open-source plain text markup language for screenwriting created by [John August](http://johnaugust.com), [Stu Maschwitz](http://prolost.com), and [Nima Yousefi](http://nimayousefi.com), with contributions from Martin Vilcans, Brett Terpstra, Jonathan Poritsky, Kent Tessman, and Clinton Torres.

Fountain's elegant approach to plain text screenplay formatting inspired CueScript's design principles: human-readable, portable, future-proof, and built on open standards.

Learn more about Fountain at [fountain.io](https://fountain.io)

### Compatible Software

CueScript is designed to work seamlessly with:

- **Fountain** - The open-source screenplay markup syntax (fountain.io)
- **Final Draft** - Industry-standard screenwriting software
- **Highland, Slugline, Fade In, Beat, and other Fountain-compatible editors**

The format is intentionally domain-agnostic, allowing specialized applications to serve specific production contexts while sharing a common foundation.

---

_CueScript Specification v0.9 (Public Draft)_  
_Last updated: April 2026_
