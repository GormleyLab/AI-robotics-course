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
| 3 | Planetary gearbox parts + assembly | Done |
| 4 | Joint 1/2 base parts + assembly (add the J1 motor and 20T pulley) | Next |
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

## Session 3 — 2026-10-26
- Recreated all 9 printed gearbox models plus the `planetary_gearbox.py` assembly in one gearbox frame (`gearbox/common.py`). All 10 map entries pass the gate (worst: ring gear at 0.364 % symmetric difference).
- **Finding: the gears are 15° helical, not spur.** Measurements:
  - transverse m1.5; ring and planets right-hand, suns left-hand;
  - 0.053 mm backlash;
  - root fillets 0.635 mm; ring tips rounded 0.385 mm;
  - ring tip Ø64.0 / root Ø70.9;
  - each ring band is a separate cutter; tooth centre at 0° at each band's lower end.
  - `design.md` §3 and IF‑6 are corrected.
- Other corrections in `design.md`:
  - the bolt circle is r = 39.25;
  - the output hex is 21.65 AF;
  - the cover pockets are open radial U-slots (Q4 partly resolved).
- `lib/gears.py` gained `helix_angle` (uniformly twisted extrusion), `root_fillet` and `tip_round`.
- Tools in `checks/inspect/`:
  - `part_features.py`: polar feature dump of Fusion parts in a subassembly frame (`--to-part`);
  - `tooth_phase.py`: fast tooth phase and width versus height (helix), for gears and pulleys;
  - `gear_phase.py`: tip/root radii by point sampling (slow).
- Gate (`compare_to_fusion.py`) now has:
  - `frame: world`, step-list transforms, `--only`, `--explain` and per-entry timing;
  - nudged retries for coincident faces;
  - a sliced method (planar sections, polygonised when the exact 2D boolean fails), calibrated against the 6805 stand-in. Helical gears skip the 3D boolean (`"method": "sliced"`) and take 20–90 s each.
- The assembly interference matches Fusion except ring × planet (54/52 vs 36/26 mm³; I‑7 updated).
- Stage-1 and stage-2 planets in Fusion each share one absolute tooth phase (4.830° / 3.530° at their bottom faces); `planetary_gearbox.py` uses them.

### Next session (4): joint 1/2 base
1. Recreate in `src/joint12/`: `box_bottom.py`, `box_top.py`, `hinge.py`, `coupling_shaft.py`, `gt2_pulley_160t.py` (the Fusion "GT2-120"; use `lib/gt2.py`, and check its groove against Fusion with a section like the gear checks).
2. Get features with `checks/inspect/part_features.py "STEP/imported/fusion/Joint 1 and 2.step" REF --to-part 0,0,0`, and tooth phases with `tooth_phase.py`.
3. Pick one clean frame for the base, e.g. the Fusion "Joint 1 and 2" frame as-is (axes already clean: J1 at (75, 75), J2 ‖ X). Place the gearbox with `TO_FUSION` composed with the gearbox's placement in that file. The gearbox axis is at z = 70.0 and the hinge at 70.5 (I‑1): reproduce it.
4. Add the J1 NEMA17 on top of the box top, shaft down through the slot at mid-travel (x = 150, y = 75), with the 20T pulley on the shaft level with the 160T teeth (z ≈ −11.5…−4.5) (design.md §2). They aren't in Fusion, so they're not gated; record the placement assumption.
5. Assembly `src/joint12/joint_1_and_2.py`; gate all parts with `frame: world` against `Joint 1 and 2.step`; run the interference check; reproduce I‑1/I‑2/I‑10/I‑12.
