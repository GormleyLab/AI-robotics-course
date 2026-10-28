# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Course materials for **14:125:444 Smart Prosthetics and Robotic Systems** (Rutgers BME senior elective, instructor Dr. Adam Gormley). It is a documentation/content repo, not a software project: there is no build, lint, or test tooling. The `.gitignore` is the stock Python template, anticipating future Python code.

Students build a multi-axis robotic arm (Arduino + Python, machine vision via OpenCV/Roboflow, natural-language control via an LLM API). The course is being updated for **Spring 2027** (Tuesdays, 2–5 PM); see the note in `README.md`.

## Files

- `README.md` — syllabus: course description, format, 5-phase schedule, grading breakdown.
- `Assignments.md` — weekly assignment table (week, due date, topic, resources). Due dates are from the previous offering and need to be re-dated for each new semester.
- `arduino_motor_control_handout.md` — long-form handout for the Phase 1 motors module, with embedded Arduino C++ sketches and ASCII wiring diagrams.
- `inventory.md` — purchased-parts inventory from the Amazon order history, linked to the CAD parts, with per-arm counts and a 9-set count for 40 students (8 teams of 5 plus a spare set); §6 lists spares that are not in the CAD.
- `CAD/` — text-to-cad project for the robotic arm (`CAD/README.md`: layout and how to print). `src/` holds the Python models (catalog in `CAD/src/README.md`), `STEP/` the generated outputs (committed so students can use them without cadgen), `STEP/imported/fusion/` the original Fusion 360 exports (belt drive arm, joints 1–2, two-stage 16:1 planetary gearbox) that serve as the replica reference, and `STEP/imported/vendor/` the step.parts downloads. Earlier Fusion 360 `.f3z` versions remain in git history.
- `CAD/docs/design.md` — design documentation for the Fusion baseline: parts, interfaces, gear and belt data, issue log. `CAD/docs/migration-log.md` tracks the multi-session Fusion → text-to-cad migration; read its "Next session" section before continuing.

## CAD work (text-to-cad plugin)

The arm is being recreated as Python models with the text-to-cad `cad` skill (cadgen + build123d). Load that skill before any CAD work.

- Run Python through cadgen's pinned environment, not the project `.venv`: `PYTHONPATH=src uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.26 python ...`, from `CAD/`.
- Every printed part gets an entry in `CAD/checks/fusion_map.json` and must pass `checks/compare_to_fusion.py --map checks/fusion_map.json` (bbox ±0.1 mm, volume ±0.5 %, symmetric difference ≤0.5 %). Helical gears need `"method": "sliced"` in their map entry: the 3D boolean always fails on their flanks. Gate slow parts in parallel, one process per `--only` filter.
- Replica first: recreated parts must match the Fusion STEP files. Model each subassembly in one clean frame that maps onto the Fusion assembly by a single transform (the gearbox does this; see `CAD/src/gearbox/common.py`), and compare with `"frame": "world"`. Don't fix the issues in `design.md` §8 during recreation; fix them later, one per commit.
- Print fits: every fit feature (bearing seat, printed shaft in a bearing, pin or bushing hole, hex socket, screw clearance) is sized from the part's own profile, `FIT = profile("<part>")` from `lib/tolerances.py` (`hole`, `shaft`, `hex_socket_r` with a `FIT` class; `FIT.m3_clear`, `FIT.insert_m3`, ...), never as a bare nominal number; a new printed part goes in `PARTS`. Commit with `DEFAULT = FUSION` and an empty `PART_PROFILES`; the gate does not reliably catch a profile left switched. See `CAD/README.md` (Printing the parts) and `design.md` §6.
- Locked interfaces are listed in `design.md` §5. Changing one is a breaking change and must be called out.
- Every design change must update `CAD/docs/design.md` in the same commit: the affected part rows, interface table (§5), ratios and link lengths (§1), and issue log (§8, marking issues fixed with the commit that fixed them). If a change makes a snapshot in `CAD/docs/img/` out of date, re-render it.
- Exploratory scripts and snapshots go in `CAD/tmp/` (git-ignored); reusable checks go in `CAD/checks/`.

## Cross-file consistency

- The phase/week structure appears in both `README.md` (Class Schedule) and `Assignments.md` (Assignment Categories), and the two currently disagree (e.g., Phase 2 is Weeks 3–6 in the README but 3–7 in Assignments). Keep them in sync when editing either.
- Course number, instructor name, and course title are repeated in the header of each Markdown file.

## Arduino handout conventions

Target hardware is the **Arduino Uno Q** with **A4988** stepper drivers, **NEMA17** steppers, and an **MG996R** servo. Code examples build on each other and share a fixed pin map; new or revised examples should reuse it:

| Signal | Pin |
|--------|-----|
| `STEP_PIN` | 2 |
| `DIR_PIN` | 5 |
| `MS2_PIN` (quarter-step) | 4 |
| `LIMIT_SWITCH_PIN` | 7 |
| `SERVO_PIN` | 9 |
| `LED_PIN` | 13 |
| `POT_PIN` | A0 |

Pins are declared with `#define`. Step counts assume 200 steps/rev at full step and 800 steps/rev in quarter-step mode. Later sections use the `AccelStepper` and `Servo` libraries. The table of contents at the top uses GitHub anchor links, so renaming a section heading requires updating its TOC entry.
