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
| 2 | Project scaffold (`src/`, `STEP/`, `lib/`), tolerance and gear/GT2 helpers, COTS via step.parts, `checks/compare_to_fusion.py` | Done |
| 3 | Planetary gearbox parts + assembly | Next |
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

## Session 2 — 2026-10-26
- Moved the Fusion exports to `STEP/imported/fusion/` (upstream filenames kept).
- `src/lib/`:
  - `params.py`: interface constants from design.md §5.
  - `tolerances.py`: `FUSION` nominal profile for the replica; `PLA_FDM` and `RESIN` presets for the fix phase.
  - `gears.py`: involute spur gear and ring cutter. A 15T m1.5 planet built with it is 2999.4 mm³ vs Fusion 2996.7 (0.09 %).
  - `gt2.py`: groove matched to the Fusion arc construction. 20T and 80T sections are within 0.1 % of Fusion.
  - `cots.py`: stand-ins for purchased parts.
- `src/purchased/`: 13 models. Four wrap step.parts files (608, 6803, GT2 20T pulley, GT2 20T idler with 5 mm bore). Nine are stand-ins:
  - no catalog match: 6801, 6805, 6807, 51108 thrust, 6×8×10 bushing;
  - bad catalog geometry: the D6×30 dowel file is 60 mm long; the NEMA17 L40 shaft is about 13 mm (needs ~23.7);
  - non-standard Fusion sizes: the 6×22 pin and the 6.2×11.8×1.3 washer.
- `checks/compare_to_fusion.py` and `checks/fusion_map.json`:
  - The exact-size stand-ins pass with 0 % error.
  - The 6805 stand-in correctly fails (internals differ; 1.4 % symmetric difference). Bearings are COTS, so they are not gated.
  - OCCT booleans return empty results for exactly coincident cylinders, so the check also evaluates the overlap with a 1e-4 mm nudge and keeps the larger value.
- Generated STEP files are committed, so students can use them without cadgen.

### Next session (3): planetary gearbox
1. Build in this order:
   1. `src/gearbox/ring_gear.py`
   2. `back_cover.py`, `front_cover.py`, `nema17_mount.py`
   3. `carrier_stage1.py` and `carrier_stage2.py` (identical geometry; one factory)
   4. `carrier_stage1_output.py` (stage-2 sun)
   5. `carrier_stage2_output.py` (output shaft + hex)
   6. `input_shaft.py`, `planet_gear.py`
   7. the `gearbox.py` assembly
2. Model each part in its Fusion local frame. Get the frame and features from
   `tmp/inspect/Planetary Gearbox - Two-stage 16to1 ratio.txt`; regenerate it
   with `checks/inspect/dump_features.py` (design.md §9).
3. Gear phase: before each `compare_to_fusion` run, find each gear's tooth
   rotation from the Fusion part, e.g. the angle of a tip-land face centre.
4. Ring gear: Fusion root Ø70.9 implies a dedendum of about 1.133 m. Fit
   addendum and dedendum to the Fusion faces before gating.
5. Add every part to `checks/fusion_map.json`, then run the gate, snapshot
   review, and `checks/inspect/interference.py` on the assembly. Reproduce
   I-1/I-2/I-7; don't fix them.
