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
| 4 | Joint 1/2 base parts + assembly (add the J1 motor and 20T pulley) | Done |
| 5 | Belt drive arm segment parts + assembly (belt envelopes) | Next |
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

## Session 4 — 2026-10-27
- Recreated the 5 printed joint 1/2 parts in `src/joint12/` plus the `joint_1_and_2.py` assembly. They are modelled in place in the Fusion "Joint 1 and 2" frame (`joint12/common.py`).
- Gate (`frame: world`, no transform): box bottom, box top and hinge at 0.000 %; coupling shaft 0.001 % volume; 160T pulley 0.020 % symmetric difference.
- 160T groove check: the r 49.5–51 tooth-band section is 0.69 % heavier than Fusion (`lib/gt2.py` omits the blend arcs). That is about 0.011 mm² per groove. The tooth phase matches Fusion: groove 0 on +X.
- The gearbox goes in rigidly: `GEARBOX_PLACEMENT = Pos(-17, 75, 70) * Rot(0, 0, 90) * TO_FUSION`. Ring, back cover, output carrier and planet give the same transform.
- Interference matches Fusion pair for pair:
  - I‑2: coupling × output carrier 2802.6 mm³ (Fusion 2802.8).
  - I‑1: left 6805 × output carrier 87.5 mm³ (Fusion 86.1; the gap is the 6805 stand-in's internals).
  - The gearbox pairs are as in Session 3.
  - Not reproduced: the gearbox NEMA17 mount × motor pair (8.7 mm³ in Fusion), because the motor is a stand-in.
- I‑10 (5 of 6 cheek holes), I‑12 and I‑13 are reproduced in the geometry.
- J1 NEMA17 and 20T pulley added (not gated). Assumptions:
  - mounting face on the box top (z = 12), shaft down, at mid-slot (x = 150);
  - motor square to the box, so the screws sit in the M3 slots;
  - the 20T band (z 1–9 of the vendor part) centred on the 160T band (z −12…−4);
  - the shaft reaches z −11.7, so it engages 8.7 of the 10 mm bore;
  - belt pitch length at mid-slot: 356.5 (`lib/gt2.belt_pitch_length`).
- Vendor 20T pulley (`step.parts gt2_pulley_20t_bore5_w6`):
  - its bore runs only through the band; both flanges are solid. `purchased/gt2_pulley_20t.py` now cuts the Ø5 bore through.
  - it is also not toothed: a plain Ø15.23 band, where a real GT2 20T has OD 12.22. For belt envelopes, use the `lib/gt2.py` pitch diameters, not the vendor geometry.
- **New issue I‑14: J1 yaw is limited by the J1 motor.**
  - The hinge corners (r 55.7) hit the motor at ±30° at x = 140 and at ±50° at mid-slot.
  - The gearbox hits it beyond ±120° at every slot position.
  - New check: `checks/j1_yaw_clearance.py`.
- Corrections to `design.md`:
  - the hinge "Ø10 cross holes" are R5 floor-to-cheek fillets;
  - the cheek bolt circle is r = 39.25;
  - the coupling hex socket is 21.65 AF (circumradius 12.5) and 15 deep, not 21.66 / 29. The fit is line-to-line (I‑2, IF‑7);
  - the coupling has a curved Ø33 → Ø29 transition;
  - the 160T flange shape.
  - `params.OUTPUT_HEX_SOCKET_AF` (21.66) is kept only for the GT2‑80 output until Session 5 re-measures it.
- New inspection tool: `checks/inspect/world_faces.py` (every face in world frame; `--min-area` hides teeth).

### Next session (5): belt drive arm segment
1. Check that the "Belt Drive Arm" frame is clean. Use the placements in `tmp/inspect/Belt Drive Arm.txt` (regenerate with `dump_features.py`). If it is, model in place as in `joint12/`; otherwise pick one clean frame and a single transform.
2. Recreate in `src/belt_arm/`: `base.py`, `wall.py`, `top.py`, `dual_gt2_pulley.py` (80T + 20T), `gt2_80_output.py`, `pin.py`, `output_block.py`, `spacer_5mm.py`, `spacer_15mm.py`. Get features with `checks/inspect/world_faces.py` and tooth phases with `tooth_phase.py` (`--to-part 0,0,0 --centre X,Y`).
3. Re-measure exactly (not from the 2-decimal dumps):
   - the GT2‑80 output hex socket. If it is 21.65, retire `params.OUTPUT_HEX_SOCKET_AF = 21.66` and update IF‑7/IF‑10;
   - the Pin hex (21.48);
   - check the Output block hex pockets (I‑6).
4. Assembly `belt_arm.py`:
   - purchased parts: NEMA17 under the Base, 20T, idlers, dowels, bushings, 6805s;
   - two belt envelopes from `lib/gt2.py` pitch circles (centre distance 85, idler positions from IF‑10).
5. Gate every printed part (`frame: world`); run the interference check; reproduce I‑4, I‑5 and I‑6.
