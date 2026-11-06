# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Course materials for **14:125:444 Smart Prosthetics and Robotic Systems** (Rutgers BME senior elective, instructor Dr. Adam Gormley). It is mainly a documentation/content repo: outside `website/` and `CAD/` there is no build, lint, or test tooling. The root `.gitignore` is the stock Python template.

Students build a multi-axis robotic arm (Arduino + Python, machine vision via OpenCV/Roboflow, natural-language control via an LLM API). The course is being updated for **Spring 2027** (Tuesdays, 2–5 PM); see the note in `README.md`.

## Files

- `README.md` — syllabus: course description, format, 5-phase schedule, grading breakdown.
- `Assignments.md` — weekly assignment table (week, due date, topic, resources). Due dates are from the previous offering and need to be re-dated for each new semester.
- `arduino_motor_control_handout.md` — long-form handout for the Phase 1 motors module, with embedded Arduino C++ sketches and ASCII wiring diagrams.
- `inventory.md` — purchased-parts inventory from the Amazon order history, linked to the CAD parts, with per-arm counts and a 9-set count for 40 students (8 teams of 5 plus a spare set); §6 lists spares that are not in the CAD. `inventory.xlsx` is the counting sheet built from it (same rows, plus Actual count and To order columns); keep the two in step when items change.
- `CAD/` — text-to-cad project for the robotic arm (`CAD/README.md`: layout and how to print). `src/` holds the Python models (catalog in `CAD/src/README.md`), `tools/print_parts.py` builds print sets into `tmp/print/` from the configs in `print_configs/`, `STEP/` the generated outputs (committed so students can use them without cadgen), `STEP/imported/fusion/` the original Fusion 360 exports (belt drive arm, joints 1–2, two-stage 16:1 planetary gearbox) that serve as the replica reference, and `STEP/imported/vendor/` the step.parts downloads. Earlier Fusion 360 `.f3z` versions remain in git history.
- `CAD/docs/claude-code-guide.md` — user guide for preparing prints and editing parts with Claude Code (how the project works, example prompts); keep it in step with the print tool and the CAD rules below.
- `CAD/docs/assembly-guide.md` — illustrated, step-by-step guide to building the arm from parts (gearbox, base and joint 1, hinge and joint 2 so far). Its pictures in `CAD/docs/img/assembly/` come from `CAD/tools/render_assembly.py` and a step list per chapter in `CAD/tools/assembly_steps/` (`gearbox`, `joint1`, `joint2`; step numbers run through the whole guide); check a chapter with `CAD/checks/assembly_steps.py`. Re-render when a design change affects them.
- `website/` — course site (Astro static, same stack as the drug delivery site; `website/README.md`), deployed to GitHub Pages at https://gormleylab.github.io/AI-robotics-course/ by `.github/workflows/site.yml` on pushes to `main`. Its assembly page renders `CAD/docs/assembly-guide.md` directly, with TA review forms from `website/src/data/review-questions.json`; if a step is added, removed or renumbered, update that file too or the build fails. Returned review files name the TA: don't commit them, because this repo is public.
- `CAD/docs/design.md` — design documentation for the Fusion baseline: parts, interfaces, gear and belt data, issue log. `CAD/docs/migration-log.md` tracks the multi-session Fusion → text-to-cad migration; read its "Next session" section before continuing.

## CAD work (text-to-cad plugin)

The arm is being recreated as Python models with the text-to-cad `cad` skill (cadgen + build123d). Load that skill before any CAD work.

- Run Python through cadgen's pinned launcher, not the project `.venv`: `PYTHONPATH=src ~/.local/bin/cadgen +0.8.2 run ...`, from `CAD/` (the same for `cadgen +0.8.2 inspect|snapshot|export`). If 0.8.2 is not installed, run `uvx --no-config --managed-python --python 3.13 --from cadgen==0.8.2 cadgen doctor` once. The project pins 0.8.2 even where the text-to-cad plugin's skill names another version; move the pin as its own step, and compare every rebuilt STEP with the committed ones.
- Models keep `@step(out=...)`: every run rewrites that part's STEP, and an assembly's run rewrites its children's. An assembly composes a child as `child().shape`. The full arm's mechanism is build123d joints built from `full_arm/common.JOINTS` and `POSES` (mechanism states); pose a snapshot with `--pose pick`.
- Checks address parts by their 0.7 tree position (`#o1.12.9`) through `checks/scene.py` (`read_scene`, `resolve`, `leaves`), over cadgen's `read_step`.
- Every printed part gets an entry in `CAD/checks/fusion_map.json` and must pass `checks/compare_to_fusion.py --map checks/fusion_map.json` (bbox ±0.1 mm, volume ±0.5 %, symmetric difference ≤0.5 %). Helical gears need `"method": "sliced"` in their map entry: the 3D boolean always fails on their flanks. Gate slow parts in parallel, one process per `--only` filter.
- Replica first: recreated parts must match the Fusion STEP files. Model each subassembly in one clean frame that maps onto the Fusion assembly by a single transform (the gearbox does this; see `CAD/src/gearbox/common.py`), and compare with `"frame": "world"`. Don't fix the issues in `design.md` §8 during recreation; fix them later, one per commit.
- Print fits: every fit feature (bearing seat, printed shaft in a bearing, pin or bushing hole, hex socket, screw clearance) is sized from the part's own profile, `FIT = profile("<part>")` from `lib/tolerances.py` (`hole`, `shaft`, `hex_socket_r` with a `FIT` class; `FIT.m3_clear`, `FIT.insert_m3`, ...), never as a bare nominal number; a new printed part goes in `PARTS` and in `PRINTED` (with its count per arm) in `tools/print_parts.py`. Never edit `DEFAULT` (`FUSION`) or `PART_PROFILES` (empty) to print; the gate does not reliably catch a profile left switched. See `CAD/README.md` (Printing the parts) and `design.md` §6.
- Print sets: build them with `tools/print_parts.py` from a JSON config (notes, default profile, per-part profiles, adjusted or added profiles, parts to build), `~/.local/bin/cadgen +0.8.2 run tools/print_parts.py print_configs/<name>.json`. It writes STL + STEP + `manifest.json` + `print_list.txt` (a per-arm print checklist for students) to `tmp/print/<name>/` and never touches `STEP/` or the committed profiles. Configs validated with the fit coupon are committed in `CAD/print_configs/` (one per printer and material; `form4_grey_v5.json` is validated, `x1c_pla.json` not yet): use them as they are for that printer, and pass `--only` for single parts rather than editing them. When someone asks to print a part on a printer ("print a new planet gear on the Form 4"), list `print_configs/` and pick the config whose printer and material match. If the material isn't named and more than one config fits the printer, ask which material is loaded. If the only match isn't validated, or nothing matches, say so and offer the fit coupon before building arm parts. Report the config used and its `notes` (handling advice such as pressing bushings with a vise). Drafts and tuning go in `CAD/tmp/print/`; once a coupon validates a config, move it to `print_configs/` with the results in `notes`. When the user asks to change print parameters, edit the config, not `tolerances.py`.
- Assembly know-how (how a fit is assembled, tools, order of steps, results from test prints) goes in `design.md` §6 "Assembly notes (for the build guide)", the source for the arm's future build guide. Record it there when the user reports it, with the date and the printer and material.
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
