# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Course materials for **14:125:444 Smart Prosthetics and Robotic Systems** (Rutgers BME senior elective, instructor Dr. Adam Gormley). It is a documentation/content repo, not a software project: there is no build, lint, or test tooling. The `.gitignore` is the stock Python template, anticipating future Python code.

Students build a multi-axis robotic arm (Arduino + Python, machine vision via OpenCV/Roboflow, natural-language control via an LLM API). The course is being updated for **Spring 2027** (Tuesdays, 2–5 PM); see the note in `README.md`.

## Files

- `README.md` — syllabus: course description, format, 5-phase schedule, grading breakdown.
- `Assignments.md` — weekly assignment table (week, due date, topic, resources). Due dates are from the previous offering and need to be re-dated for each new semester.
- `arduino_motor_control_handout.md` — long-form handout for the Phase 1 motors module, with embedded Arduino C++ sketches and ASCII wiring diagrams.
- `CAD/` — robotic arm part models as STEP files (belt drive arm, joints 1–2, two-stage 16:1 planetary gearbox). Earlier Fusion 360 `.f3z` versions remain in git history.

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
