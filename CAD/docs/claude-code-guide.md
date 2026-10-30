# Working on the Arm with Claude Code

**14:125:444 Smart Prosthetics and Robotic Systems** — Dr. Adam Gormley

This guide covers preparing parts for printing and editing the arm's design,
with [Claude Code](https://claude.com/claude-code) doing the CAD work. You
describe what you want in plain language; Claude edits the Python models, builds
the parts, runs the checks and keeps the documentation up to date. The sections
below explain how the project is put together, so you know what to ask for, and
give example prompts you can copy.

**Contents**

1. [Setup](#1-setup)
2. [How the platform works](#2-how-the-platform-works)
3. [Preparing prints](#3-preparing-prints)
4. [Editing parts](#4-editing-parts)
5. [Looking at models](#5-looking-at-models)
6. [What Claude does and doesn't do on its own](#6-what-claude-does-and-doesnt-do-on-its-own)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Setup

You need:

- **Claude Code**, started in the repository folder (`AI-robotics-course/`).
  Claude reads `CLAUDE.md` there at the start of every session; it holds the
  project's rules, so you don't need to repeat them.
- **The text-to-cad plugin** for Claude Code. It gives Claude the `cad` skill
  (modelling and inspection), the CAD Viewer, and related skills such as
  `dfam-check` (printability), `gcode` (FDM slicing with OrcaSlicer) and
  `bambu-labs` (sending prints to the Bambu Lab printer).
- **cadgen 0.8.2**, the CAD engine the models run on. The project pins this
  version. Install it once:

  ```bash
  uvx --no-config --managed-python --python 3.13 --from cadgen==0.8.2 cadgen doctor
  ```

  This also writes the `cadgen` launcher to `~/.local/bin/` (`cadgen.cmd` on
  Windows). If Claude reports that cadgen is missing, ask it to run this.
- **For printing:** the lab has two printers.
  - **Formlabs Form 4** (resin, SLA) with Grey Resin V5: PreForm.
  - **Bambu Lab X1 Carbon** (FDM) with PLA: Bambu Studio or OrcaSlicer, and
    Bambu Connect if you want Claude to send prints to it.

> **First prompt to try:** *"Give me a tour of the CAD project: what parts
> there are, where they live, and which issues are still open."*

---

## 2. How the platform works

### Parts are Python programs

Every printed part is a short Python script in `CAD/src/` that builds the part
with [build123d](https://build123d.readthedocs.io). Dimensions are named
constants and parameters, not clicks in a GUI, so a change is an edit to the
script. Running a script regenerates the part's STEP file.

| Folder | What's in it |
|---|---|
| `CAD/src/joint12/` | Base box, J1 (waist) and the hinge |
| `CAD/src/gearbox/` | The two-stage 16:1 planetary gearbox on J2 (shoulder) |
| `CAD/src/belt_arm/` | One belt-drive arm segment; the arm uses two (J3 elbow, J4 wrist) |
| `CAD/src/full_arm/` | The whole arm with its four joints and named poses (`zero`, `reach`, `pick`, `folded`) |
| `CAD/src/purchased/` | Bearings, motors, screws and other bought parts, for fit and interference checks |
| `CAD/src/lib/` | Shared code: dimensions (`params.py`), gears, GT2 pulleys, and print fits (`tolerances.py`) |
| `CAD/STEP/` | The generated STEP files, committed so anyone can open them without cadgen |
| `CAD/checks/` | Verification scripts (comparison with the original Fusion design, interference, joint clearance) |
| `CAD/tools/print_parts.py` | Builds print-ready parts (section 3) |
| `CAD/docs/design.md` | The design record: parts, interfaces, gear and belt data, and the issue log |
| `CAD/tmp/` | Scratch space for experiments and print sets; git ignores it |

A part catalog with notes on each script is in [`CAD/src/README.md`](../src/README.md).

### The committed STEP files are the nominal design

The arm was first designed in Fusion 360 and then recreated in Python. The
committed STEP files keep Fusion's sizes: a bearing seat is exactly the
bearing's diameter, a pin hole exactly the pin's. That is the right reference
for design work, but printed as-is most fits would be too tight. **Don't print
from `CAD/STEP/`.** Print sets are built separately (section 3).

### Fit profiles

Each printing process needs its own allowance on every fit. `lib/tolerances.py`
groups the fit features into classes and holds a profile of allowances for
each process:

| Class | What it covers | `PLA_FDM` | `RESIN` |
|---|---|---|---|
| `press` | Bearings in printed seats, printed shafts in bearings, bushings and planet pins | 0.10 | 0.05 |
| `slip` | Parts that slide in by hand: dowel, M5 nut slot, washer recesses, motor shaft bore | 0.20 | 0.10 |
| `clearance` | M3 and M5 screw holes and slots | 0.2 | 0.1 |
| `hex_socket` | Female hexes, across flats | 0.25 | 0.15 |
| `insert_m3` / `insert_m5` | Threaded-insert hole diameters | Ø4.2 / Ø6.4 (heat-set) | Ø4.8 / Ø7.3 (epoxy-bonded) |

All values are in mm on the diameter. A third profile, `FUSION`, is all zeros;
it's what the committed files use. Gear teeth are deliberately not adjusted.
The full rules are in [design.md §6](design.md#6-fasteners-and-print-fits).

These presets are starting points. You tune them for your printer and material
with the **fit coupon**, a small plate with one of every fit.

### Checks

Claude verifies its work with scripts in `CAD/checks/`, and you can ask for any
of them by name or by purpose:

- **Fusion comparison** (`compare_to_fusion.py`): every printed part against
  the original Fusion part (size within 0.1 mm, volume within 0.5 %). Deliberate
  changes are recorded as departures, with the issue that caused them.
- **Interference** (`checks/inspect/interference.py`): parts that overlap in an
  assembly.
- **Joint clearance** (`joint_clearance.py`): turns a joint through a range of
  angles and reports collisions.
- **Printability** (the `dfam-check` skill): thin walls, overhangs and other
  process-specific problems in a mesh.

### The design record

[`design.md`](design.md) is the source of truth for the design. Every design
change updates it in the same commit. The sections you'll use most:

- **§5 Interface table**: the locked interfaces between subassemblies (axis
  positions, bolt patterns, hex sizes, the NEMA17 mount, the link interface).
  Changing one is a breaking change and Claude will call it out.
- **§6 Fasteners and print fits**: which features get which allowance.
- **§8 Issue log**: every known problem, with an ID (I‑1, I‑2, ...), severity,
  evidence, and how it was fixed or why it was accepted.

---

## 3. Preparing prints

### How a print set is built

`CAD/tools/print_parts.py` builds the parts at the fit profiles you choose and
writes them to `CAD/tmp/print/<name>/`. It never edits the committed profiles
and never writes to `CAD/STEP/`, so preparing prints can't change the design.
The settings live in a small JSON config, also in `CAD/tmp/print/`, which
Claude edits for you:

```json
{
  "default": "GREY_V5",
  "parts": {"wall": "TOUGH"},
  "profiles": {"GREY_V5": {"base": "RESIN", "press": 0.07},
               "TOUGH": {"base": "RESIN"}},
  "only": ["ring_gear", "planet_gear"]
}
```

- `default`: the profile for every part not listed in `parts`.
- `parts`: a different profile for particular parts. You can mix printers:
  each part sizes only its own features, so a resin gear in a PLA housing
  needs nothing extra.
- `profiles`: named profiles of your own, each starting from a preset (`base`)
  with any values changed. Naming one after the printer and material
  (`GREY_V5`) records the material in every part's manifest.
- `only`: which parts to build. Without it, every arm part is built.

Each part comes out as:

- an **STL**, meshed to 0.01 mm and checked to be closed, ready for the slicer;
- a **STEP** of the same part;
- an entry in **`manifest.json`**: the exact fit values used, how many to print
  per arm, the size and the volume.

Parts are centred on the origin with their base at z = 0, in the model's
orientation. Orient them in the slicer.

### Step 1: tune the fits with the coupon

Print the fit coupon in the material you'll use, then post-process it exactly
as you will the real parts (resin shrinks slightly in post-cure). Try every
feature with the real hardware: the 6805, 608 and 6801 bearings in their seats,
the Ø25 and Ø12 pegs in the 6805 and 6801 bores, the planet pin, bushing and
dowel holes, M3 and M5 screws, the M5 nut slot, the hex socket with a printed
`Pin`, and the threaded inserts. Then tell Claude what you found.

> *"I'm printing on a Form 4 in Grey Resin V5. Set up a print config for it and
> build the fit coupon."*

> *"Build the PLA fit coupon for the X1C."*

> *"The coupon results: the 608 bearing won't go in, the 6805 is a good press
> fit, the dowel falls through, and the M3 screws are tight. Adjust the profile
> and build a new coupon."*

> *"Make three coupons with press fits of 0.04, 0.06 and 0.08 so I can compare
> them side by side."*

Repeat until everything fits. The config then holds your tuned values.

### Step 2: build the parts

> *"Build the full arm from the Form 4 config."*

> *"Build just the gearbox parts."*

> *"Build the gears and pulleys for the Form 4 and everything else for the X1C
> in PLA."*

> *"Reprint the Wall in Tough 2000: give it its own profile and build only
> that part."*

> *"How much resin will one arm take, and which parts are the biggest?"*

Claude reports each part's profile, size, volume and the per-arm count, and
flags any mesh that isn't closed.

### Step 3: check printability (optional)

> *"Run a DfAM check on the resin print set and tell me about thin walls and
> anything that will need special orientation."*

### Step 4: slice and print

**Formlabs (PreForm).** Open the STLs in PreForm. On a Form 4 (build volume
200 × 125 × 210 mm) every part fits, but some only stand up or tilted:

| Part | Size (mm) | Placement |
|---|---|---|
| `Base`, `Top` (2 each per arm) | 240 × 80 | Tilted about 40–60° along the length; doesn't fit flat |
| `Box bottom`, `Box top` | 180 × 150 | On edge or tilted |
| Everything else | ≤ 121 | Any orientation |

- Keep supports off fit surfaces: bearing seats, shaft journals, gear teeth,
  hex sockets and mating faces.
- Where you can, point bearing-seat and bore axes up the build (Z), so they
  print round.
- Leave parts solid (no hollowing).
- Wash, dry fully, post-cure, then remove supports and sand the support marks.

**Bambu Lab X1C (FDM).** The build volume is 256 × 256 × 256 mm, so every part,
including the 240 mm `Base` and `Top`, fits flat. Claude can slice the STLs
with OrcaSlicer's built-in X1C profiles and open the result in Bambu Connect or
Bambu Studio. You pick the printer and start the print there; Claude never
starts a print itself.

> *"Slice the PLA print set for the X1C with a 0.4 mm nozzle, 0.2 mm layers and
> 4 walls, and open it in Bambu Studio."*

> *"Lay out both Base plates on one X1C build plate."*

- Lay plates flat, with bearing seats and bores pointing up (Z), so they print
  round.
- Use enough walls around heat-set insert holes for the inserts to grip
  (4 walls is a good start).
- Gears and pulleys print better on the Form 4: its finer layers give cleaner
  teeth.

### Threaded inserts

- **FDM (PLA):** heat-set the ruthex inserts with a soldering iron, as before.
- **Resin:** cured resin doesn't melt, so heat-set inserts don't work. The
  resin profiles size the holes for the same inserts bonded with slow-cure
  epoxy. Put the epoxy on the hole wall and thread a greased screw into the
  insert while it cures, so no glue gets into the threads.
- Two parts have thin walls around their insert holes in resin: the `Wall`
  (about 1.1 mm) and the ring gear (about 0.85 mm). Print them in a tough
  resin if a standard resin cracks there.

### How many of each part

One arm needs: 1 each of `box_bottom`, `box_top`, `hinge`, `coupling_shaft`,
`gt2_pulley_160t`, `ring_gear`, `back_cover`, `front_cover`, `nema17_mount`,
`input_shaft`, `carrier_stage1_output` and `carrier_stage2_output`; 2 each of
`carrier_plate`, `base`, `top`, `wall`, `dual_gt2_pulley`, `gt2_80_output` and
`output_block`; 4 each of `pin`, `spacer_5mm` and `spacer_15mm`; and 6
`planet_gear`. The manifest lists the same counts. Bought parts are in
[`inventory.md`](../../inventory.md).

---

## 4. Editing parts

### How an edit works

When you ask for a change, Claude:

1. reads the part's script and the relevant parts of `design.md`;
2. edits the script (or the shared constant in `lib/params.py` or a `common.py`,
   if several parts depend on it);
3. rebuilds the part and every assembly that contains it;
4. checks the result: a snapshot image, interference with neighbouring parts,
   joint clearance if the change could affect motion, and the Fusion
   comparison;
5. updates `design.md` (the part's description, §5 if an interface moved, §8 if
   it fixes or opens an issue) and re-renders any image in `docs/img/` the
   change made out of date;
6. tells you what changed and what the checks found, then commits only if you
   ask.

### Rules the project follows

These are in `CLAUDE.md`, so Claude applies them without being told. They're
here so you know why it may push back or ask a question.

- **One issue per commit.** Problems are logged in the issue log first and
  fixed one at a time, each fix in its own commit that names the issue.
- **Locked interfaces.** Changing anything in §5 (an axis position, a bolt
  pattern, the link interface, a hex size) breaks compatibility with other
  parts. Claude will say so and ask before going ahead.
- **Fits come from the profile.** A new bearing seat, pin hole, hex socket or
  screw hole is sized from the part's fit profile, never as a bare number, so
  it picks up the right allowance for each printer. A new printed part is
  registered in `lib/tolerances.py` and in the print tool's part list.
- **Departures are recorded.** A deliberate change from the original Fusion
  part is recorded in `checks/fusion_map.json` with the issue that caused it,
  so the comparison still passes.

### Example prompts

**Understanding the design**

> *"Explain how J2 works, from the motor to the coupling shaft."*

> *"What does the Wall hold, and which parts bolt to it?"*

> *"Which open issues are there, and which ones matter most for the next
> build?"*

**Small changes**

> *"Make the Wall rails 8 mm thick instead of 7, and check nothing else
> collides."*

> *"Add a 2 mm chamfer to the outside edges of the box top."*

> *"Move the J1 motor slot 3 mm further from the axis and tell me what that does
> to the belt length."* (The slot is locked interface IF‑3, so Claude will flag
> it as a breaking change and ask before editing.)

**Reporting and fixing problems**

> *"When we assembled the arm, the 160T pulley rubbed on the hinge. Log it as an
> issue with the evidence from the model."*

> *"The ring gear bulged at its heat-set inserts. Apply the remedy in I-23 to
> the next print set."*

> *"The idler jack screw hits the output block at −95°. What are the options
> for getting J3 to −100°?"*

**Checking motion and fit**

> *"Show me the arm in the pick pose."*

> *"Sweep J3 from −90° to +90° and list anything that collides."*

> *"Check the gearbox assembly for interference."*

**New parts**

> *"Design a mount for a USB camera on the wrist, using the link interface on
> the output block."*

For a new part, say what it must attach to and any hardware it carries.
Claude will look up purchasable parts (screws, bearings, motors) on step.parts
before modelling stand-ins, and ask about anything that changes the design
materially.

### Tips

- **Be specific about intent, not just numbers.** *"The belt is too slack after
  a week"* gives Claude more to work with than *"move the idler 2 mm"*, and it
  may find a better fix.
- **Ask for options before big changes.** *"What are the options, and what does
  each one break?"* gets you a comparison before anything is edited.
- **Edit, then print.** After a design change, build a new print set
  (section 3); the print tool always builds from the current models.
- **Exploratory work goes in `CAD/tmp/`.** Ask Claude to try something there
  first if you aren't sure you want it in the design.

---

## 5. Looking at models

- **CAD Viewer:** ask *"Show me the hinge"* or *"Open the print set's ring gear
  STL"*. Claude gives you a link that opens the model in your browser, where
  you can rotate it, pick faces and edges, and measure. The viewer refreshes
  when the file changes.
- **Referring to geometry:** in the viewer you can copy a reference to a face
  or edge (for example `.../hinge.step#o1.f12`) and paste it into your prompt:
  *"Make this face 2 mm thicker: `<reference>`."*
- **Snapshots:** Claude renders images to check its own work, and you can ask
  for one: *"Render the belt arm from above."*
- **Committed images:** `CAD/docs/img/` holds the images used in the docs; they
  are re-rendered when the design changes.

---

## 6. What Claude does and doesn't do on its own

| Claude does without asking | Claude asks first |
|---|---|
| Read files, run models and checks, render snapshots | Commit or push |
| Build print sets in `CAD/tmp/print/` and edit their configs | Change a locked interface (§5) |
| Write experiments in `CAD/tmp/` | Change the committed fit profiles in `lib/tolerances.py` |
| Restore committed STEP files that a rebuild rewrote, after checking the geometry is unchanged | Delete files outside `CAD/tmp/` |

It reports what it checked and what it didn't. If a check fails, or a step is
skipped, it says so.

---

## 7. Troubleshooting

| Symptom | What to do |
|---|---|
| *"cadgen is not installed"* | Run the `uvx ... cadgen doctor` command in [Setup](#1-setup), or ask Claude to. |
| The CAD Viewer link doesn't open | Ask Claude to start the viewer (`cadgen viewer --host 127.0.0.1 --json --detach`) and give you the link again. You can also open the STL in PreForm or any viewer directly. |
| `git status` shows many changed STEP files after a rebuild | Usually float noise (`2.2e-16` becoming `0`) or line endings. Ask Claude to compare the geometry with the committed files and restore them if nothing really changed. |
| A print-set run says *"MESH NOT CLOSED"* | Don't print that STL. Tell Claude the part's name; the model needs a look. |
| *"unknown profile"*, *"unknown parts"*, *"unknown fields"* | A typo in the print config. Ask Claude to fix it. |
| A resin part's fits are off but the coupon fitted | Check that the part had the same post-processing as the coupon, and that it was printed from the same config (the manifest records it). |
| Claude wants to change something you didn't ask for | Say no. It should stay within the request; anything else belongs in its own issue and commit. |

The project's history, session by session, is in
[`migration-log.md`](migration-log.md).
