# Fusion → text-to-cad migration log

Plan: replica first (match the Fusion STEP files), then fix the logged issues in
[design.md §8](design.md#8-observed-issues-and-open-questions). Purchased parts
come from step.parts vendor STEP files, with parametric placeholders as a
fallback. Prints are FDM PLA, with resin as an option. Interfaces stay locked
during recreation.

| Session | Scope | Status |
|---|---|---|
| 0 | Install the text-to-cad plugin | Done |
| 1 | Measure the Fusion STEP files; write `docs/design.md` | Done |
| 2 | Project scaffold (`src/`, `STEP/`, `lib/`), tolerance and gear/GT2 helpers, COTS via step.parts, `checks/compare_to_fusion.py` | Next |
| 3 | Planetary gearbox parts + assembly | |
| 4 | Joint 1/2 base parts + assembly (add the J1 motor and 20T pulley) | |
| 5 | Belt drive arm segment parts + assembly (belt envelopes) | |
| 6 | Full arm (two segments), kinematics, optional URDF | |
| 7+ | Design review and fixes (I‑1 first), DfAM/DFM checks | |

## Session 1 — 2026-10-26
- Added `checks/inspect/dump_features.py` (tree, placements, per-part
  cylinders/planes/gear heuristics → `tmp/inspect/*.txt`) and
  `checks/inspect/interference.py` (pairwise solid overlaps).
- Wrote `docs/design.md` with snapshots in `docs/img/`.
- Answers from the instructor:
  - J1 is 160T / 8:1, as modeled.
  - Field problems: J2 binding, belt slip/tensioning, gear wear/backlash.
  - Segment 2 is an identical copy.
  - All parts PLA.
  - 20T pulleys bought, the rest printed.
  - The idler actually used is not remembered.
- Telemetry turned off (`cadgen telemetry off`).

### Next session (2)
1. Create `CAD/src/{lib,purchased,gearbox,joint12,belt_arm}` and
   `CAD/STEP/imported/fusion/`, and `git mv` the three Fusion STEP files there.
   Update the paths in `CLAUDE.md`, `README.md` and `design.md`.
2. Write `lib/params.py` from design.md §5 (the interface table).
3. Write `lib/tolerances.py` (PLA FDM fit presets).
4. Write `lib/gears.py` (involute m1.5 spur and internal). First check
   whether `bd_warehouse` is in the cadgen environment.
5. Write `lib/gt2.py` (pulley profile and belt length).
6. Use `step-parts` to find the NEMA17, bearings 6805/6807/608/6801/6803, the
   40×60×13 thrust bearing, the GT2 20T pulley and the 6 mm dowel pins.
7. Write `checks/compare_to_fusion.py` (bbox ±0.1, volume ±0.5 %,
   symmetric-difference volume).
