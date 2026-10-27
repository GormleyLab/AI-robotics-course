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
| 5 | Belt drive arm segment parts + assembly (belt envelopes) | Done |
| 6 | Full arm (two segments), kinematics, optional URDF | Done (URDF deferred) |
| 7+ | Design review and fixes (I‑1 first), DfAM/DFM checks; optional URDF | Next |

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

## Session 5 — 2026-10-27
- The "Belt Drive Arm" frame is clean: every occurrence is at identity rotation except Pin:2 and the Output block (the block is a single placement, so it is modelled in world coordinates).
- Recreated the 9 printed arm models in `src/belt_arm/`, modelled in place (`belt_arm/common.py`), plus the `belt_drive_arm.py` assembly. The name `belt_arm.py` would shadow the package, as with the gearbox.
- Gate: 12 new entries (Pin, Spacer 5mm and Spacer 15mm have two each; the second copies use transforms). All 32 map entries pass.
  - Base, Wall, Pin ×2 and the spacers: 0.000 %. Top: 0.001 % symmetric difference. Output block: 0.088 %.
  - Dual pulley and GT2-80 output: 0.042 %, from the omitted groove blend arcs (as on the 160T).
  - The GT2-80 output needs `"method": "sliced"`: the 3D boolean drops the whole Fusion solid and reports 7.2 %.
- Exact re-measurements (`world_faces.py`):
  - GT2-80 output socket: 21.65 AF (circumradius 12.5), the same as the coupling. `params.OUTPUT_HEX_SOCKET_AF = 21.66` is retired; `params` now has `OUTPUT_HEX_SOCKET_R = 12.5` and `PIN_HEX_R = 12.4`. IF‑10 updated.
  - Pin hex: 21.48 AF (circumradius 12.4), corners on ±X.
  - Output block socket: 21.65 AF, corners on ±Y. It runs through both prongs and the two Ø28.5 × 1 R1-rounded bosses on the 6805 inner races, so the pocket depths are fine.
  - Tooth phase: groove 0 on +X on all three 80T/20T bands, so no rotation is needed.
- **Finding: the GT2-80 output is centred at (165.5935, 47.1522), 9.08 mm off J3.** This explains the Pin overlaps of 98 / 1812 mm³. I‑6 is rewritten and raised to Medium. The Pin hexes are 30° (Pin 1) and 17.2° (Pin 2) off the block socket, which explains 374 / 83 mm³. Stage 2 runs at a 90.87 center distance.
- Interference matches Fusion pair for pair: I‑5 86.4 ×2; I‑6 98.0, 1812.0, 373.7 and 83.0.
- Vendor idler fix: the step.parts idler leaves its flanges solid, as the 20T pulley does. `purchased/gt2_idler_20t.py` now cuts the Ø5 bore through. Both vendor parts are plain Ø15.23 bands, not toothed.
- Belts (not gated):
  - `lib/gt2.py` gained `flanged_pulley`, `belt_path` (exact tangent/arc pitch line and length, signed radii for back-side idlers), `idler_depth` and `belt_envelope` (pitch line −0.254 / +0.376, teeth left out).
  - Stage 1: the idler at the y = 20 slot end deflects the belt 1.8 mm; 274.39 mm loop (277.65 at y = 30).
  - Stage 2: the idler misses its belt by 2.0 mm (I‑6); 285.78 mm open loop.
  - Each belt is centred on its 80T band.
  - Remaining belt overlaps are vendor geometry: the motor 20T (84 mm³) and idler 1 (34 mm³). The exception is dual × belt 2 (2.5 mm³), which is I‑15.
- **New issue I‑15: the arm pulley bands are out of line axially.** The motor 20T band is 3 mm above the dual 80T band; the dual 20T band is 1 mm below the output 80T band.
- Corrections to `design.md` §4:
  - the Base idler holes are slots as in the Top;
  - the idler dowels are only clamped between the plates (I‑4);
  - the Output block "Ø10 cross holes" are mitred R5 root fillets;
  - the fork has a slot, a hex socket and bosses;
  - the Top has no motor holes.

## Session 6 — 2026-10-27
- Robot frame fixed (design.md §7): origin on J1 at the top of `Box top`, +Z up, +X = base-frame +Y (the base has no front, so this is a convention), +Y toward the gearbox. J2–J4 point along +Y; positive angles tip the arm toward +X.
- IF‑8 mounting: the hole pattern is symmetric, so there are two ways to mount the arm. With the Base plate toward the gearbox, the segment motor hits the ring gear, front cover and hinge (2150 mm³). With the Base plate toward the right cheek, it is clear. The second is used: segment 1 → base is `p = (96.8 − z, 35 + y, 140.5 + x)`. Segment 2 sits on the Output block face, at +274.175 in x and +0.2 in z.
- `src/full_arm/`:
  - `common.py`: the placements as plain (rotation, translation) pairs, plus the joint axes and limits. The module touches no kernel objects.
  - `robot_arm.py`: the assembly, regrouped into five links (base, waist, upper arm, forearm, wrist), with `revolute` mates J1–J4 and poses zero / reach / pick / folded.
  - `joint_1_and_2.py` and `belt_drive_arm.py` now expose `joint12_parts()` and `segment_parts()`; their STEP bytes are unchanged.
- Verified in the saved STEP: the bearing centres sit on the declared axes. J2 is at z 58.5, J3 at 288.5, J4 at 562.675; the end-effector face is at 636.85. Link lengths and the joint table are in design.md §1.
- New check `checks/joint_clearance.py`: turns one joint (reading the mates from the sidecar) and reports overlap growth over the zero pose. Clear travel:
  - J1 ±40° (I‑14 unchanged with the arm on).
  - J2 ±63°: the segment‑1 motor hits the right hinge cheek. **New I‑16.**
  - J3/J4 ±54°: the Output block fork hits the Wall's distal rail ends. **New I‑17.**
  - The off-axis GT2‑80 output (I‑6) orbits and rubs the Wall from +5°. Noted under I‑6.
  - Instructor: the built arm used standard 40 mm NEMA17s, so the stand-in is right. J2 at ±63° is acceptable and not a priority (I‑16 Low, accepted). J3/J4 must reach at least ±90° (I‑17 High 🔧).
- Known artefacts in the check (not issues):
  - `gt2_80_output × belt:stage_2`: the belt is static while its pulley orbits.
  - `coupling_shaft × carrier_stage2_output` grows by about 20 mm³ at +63°, because the gearbox rides the waist rigidly.
- Simplifications: no pulley, idler or gearbox output spins with its joint. `STEP/full_arm/robot_arm.step` is 34 MB.
- Pre-existing build hint, not fixed: `gearbox/common.py` (`TO_FUSION`) and the other `common.py` modules build kernel objects at import, so every rerun pays the kernel import.
- Snapshots: `docs/img/robot_arm_zero.png` and `robot_arm_pick.png`.
- URDF deferred: it needs a mesh per link in link frames, and nothing downstream uses it yet.

### Next session (7): design review, I‑1 first
1. Fix order: I‑1 (J2 axis 0.5 mm offset, three bearings) first. Then I‑6 (J3 output on axis; this also removes the pulley's rub on the Wall), then I‑17 (J3/J4 travel ≥ ±90°: clear the Wall's distal end against the Output block fork. Travel is currently ±54°, and the Wall is the only obstacle out to about ±100°). I‑2 comes after these. I‑16 (J2 ±63°) is accepted, so leave it. Confirm I‑17 with `checks/joint_clearance.py --joint j3_elbow --angles 90,-90,95,-95` (and `j4_wrist`).
2. One issue per commit: change the model, rerun the gate (expect the fixed part to leave the Fusion replica; record it as an intentional departure in `checks/fusion_map.json` or retire its entry), update design.md (part rows, §5, §8 with the commit).
3. Re-run `checks/joint_clearance.py` after any change near a joint; I‑16 and I‑17 decide the usable workspace.
4. DfAM/DFM checks on the printed parts (`$dfam-check`), with the `PLA_FDM` tolerance profile.
5. Optional URDF (`$urdf`) from `full_arm/common.py`: one STL per link, in the link's joint frame.
