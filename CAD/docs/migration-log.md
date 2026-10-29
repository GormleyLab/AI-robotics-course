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
| 7+ | Design review and fixes (I‑1 first), DfAM/DFM checks; optional URDF | In progress (I‑1, I‑2, I‑4 arm, I‑5, I‑6, I‑7, I‑9, I‑11, I‑14, I‑15, I‑17, I‑18, I‑19 done; I‑3, I‑4 J1, I‑10, I‑12, I‑16 accepted; I‑13 intentional; I‑20 fixed; I‑8, I‑21–I‑23 open) |

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

## Session 7 — 2026-10-27
- **I‑1 fixed** (commit "Fix I-1"). The hinge seats, the coupling and the hinge's front-cover bolt circle all sit at z = 70.5, so the gearbox moved up 0.5 mm. The hinge did not move down. `params.J2_AXIS_YZ` replaces the separate `_HINGE` / `_GEARBOX` constants, and `GEARBOX_PLACEMENT` uses it.
- No part STEP changed. Only `joint12/joint_1_and_2.step` and `full_arm/robot_arm.step` were rebuilt, and the joint12 gate still passes. No fusion_map entry changed: the gearbox parts are gated in the gearbox frame, not the base frame.
- Checks: the carrier output × left 6805 overlap went from 87.5 to 0 mm³. The coupling × output hex overlap went from 2803 to 2783 mm³; what remains is I‑2. J1 is still ±40° and J2 still ±63°.

- **I‑6 fixed** (commit "Fix I-6"). The GT2‑80 output is centred on J3. The Pin hex and the pulley socket are turned 90° (corners on ±Y) to match the Output block socket, which keeps its orientation for the wall thickness. Pin 2 is now a plain flip (`Rot(-180, 0, 0)`). `OUTPUT_PULLEY_XY` is gone.
- Gate: there was no departure mechanism, and none was needed. The two changed parts are rigid motions of their Fusion originals (a 90° turn maps the 80T teeth onto themselves), so their `fusion_map.json` entries gained a transform back and a `note` key (the gate ignores it). Pin ×2 and gt2_80_output still pass at 0 / 0.04 %.
- Checks: all four J3-output overlaps in `belt_drive_arm.step` are gone (98 / 1812 / 374 / 83 mm³). The stage‑2 idler now wraps its belt (1.83 mm, 274.4 mm loop, the same as stage 1). J3/J4 are clear at +5° and ±54°, and the Wall is the only contact out to ±95°.
- Re-rendered `docs/img/belt_arm_internals.png` (top hidden, `--display parts`) and `belt_arm_iso.png` (`--display parts`). The robot_arm images were left as they are: the pulley is hidden inside the fork at that scale.

- **I‑17 fixed** (commit "Fix I-17"), option 1 of three put to the instructor: the Wall rails are trimmed and the two distal screws moved inboard. The other options were dropping those two screws, or a spacer post. `belt_arm/common.py` gains `RAIL_END_X = 130`, and `WALL_SCREW_XY` uses it, so Base and Top follow. The end was chosen with a 2D sweep of the fork outline (`tmp/i17_sweep.py`, not kept): x = 130 leaves 9 mm at 90° and 2.2 mm at 100°.
- J3/J4 clear to ±103° (first contact Output block × Wall at ±104°, 59 mm³), and `J3_LIMITS` / `J4_LIMITS` are now ±103°. The `pick` and `folded` poses still use 54°; they were not changed.
- The gate gained intentional departures: a map entry with `departure: {issue, why, bbox, vol_pct, symdiff_pct}` reports DEPART and passes only while the measured deviation stays within 0.05 of the recorded one. Wall (30 mm bbox, 13.1 %), Base (0.43 % symdiff) and Top (0.41 %) use it; Base and Top would still pass the plain tolerance, but they are recorded as departures so later drift is caught.
- Re-rendered `belt_arm_internals.png`, `belt_arm_iso.png`, `robot_arm_zero.png` and `robot_arm_pick.png` (`--kinematics zero|pick --camera iso` reproduces the Session 6 framing).

- **I‑2 fixed** (commit "Fix I-2"), a change to the carrier only.
  - Most of the 2783 mm³ was axial, not rotational. The gearbox output was 5.2 mm too long: the Ø25 shaft ran 5.2 mm into the coupling face (6 × 74 mm³) and the hex 5.2 mm past the socket floor (2077 mm³). The 43.5° turn was only about 260 mm³. Neither part can slide: the gearbox is bolted to the left cheek, and the coupling's stub shoulder is 0.2 mm from the right-cheek 6805.
  - Fusion aligned the hex to the carrier pins (flat normal −16.54° = PIN_ANGLE − 60°), not to the socket.
  - Fix: the shaft ends 0.5 mm short of the coupling face (`SHAFT_END_Z = -69.3`). The hex is 14.5 long, leaving 1 mm at the floor. It is the Pin size (`params.OUTPUT_HEX_AF = PIN_HEX_AF`, 21.48 AF), with its flat normal at 0° (corners on gearbox ±Y = base ±Z). The coupling and the socket constant are unchanged. IF‑7 is changed (breaking).
  - The other option, a deeper socket plus a Ø25 counterbore in the coupling, was rejected because it changes a second part.
- Gate: `carrier_stage2_output` is a departure (bbox 6.2, 9.242 % vol, 10.304 % symdiff).
- Checks:
  - Coupling × carrier output went from 2783 to 0 mm³, and the joint12 assembly has no new pair.
  - `joint_clearance.py --joint j2_shoulder`: J2 is still ±63°, with the first real contact segment‑1 motor × hinge at ±64° (5 mm³, I‑16). Coupling × carrier output now reports 361 mm³ at ±30° and 41 at ±63°. That is the Session 6 artefact (the carrier rides the waist instead of turning with J2), now visible because the zero-pose baseline is 0. It follows the hex's 60° period, so it is not a contact.
- Build hygiene: changing `params.py` rebuilds every model that imports it, and the rebuilt STEPs differ only in float noise (`2.2e-16` → `0`). Those files were restored with `git checkout`, so the commit carries only the carrier, gearbox, joint12 and full-arm STEPs.
- Not re-rendered: `docs/img/gearbox_exploded.png` still shows the Fusion carrier, 6 mm longer at the output. It was an exploded view made in the viewer GUI, and the CLI `exploded` setting only spreads the parts along the axis, which hides the shaft. Re-capture it from the viewer if the difference matters.

- **I‑15 fixed** (commit "Fix I-15"). Idler 1 was also out of line: its band (13.5–20.5) was 1.3 mm above the dual 80T, and belt 1 rode its lower flange. That was the Session 5 "vendor" 34 mm³.
  - The design intent is the spacers: 5 + 15 and 15 + 5 put the idler bands 10 apart, at z 17.0 and 27.0.
  - Belts aligned to the parts that can't move: idler 1 (z 17.0) and the output 80T in its fork slot (z 26.7, with 0.5 mm play).
  - Dual pulley: the 80T is up 1.3 on a new Ø12 × 1.3 hub (it still sits on the Base boss), and the 20T is up 1.0. Its lower flange merges 0.3 mm into the 80T's top flange.
  - Assembly: the motor 20T slides 1.7 mm down its shaft (`MOTOR_PULLEY_Z = 12.0`), belt 1 moves to z 14.0, and the upper bushing to 21.7 (`BUSHING_Z`).
- Gate: the dual pulley is a departure (bbox 1.0, 0.28 % vol, 29.06 % symdiff; the symdiff is the Ø52 flanges swept 1.3 mm).
- Checks (`interference.py` on `belt_drive_arm.step`):
  - dual × belt 2 went from 2.5 mm³ to 0;
  - every belt now lies inside the band of each pulley and idler it runs on;
  - the radial vendor-band overlaps remain: motor 20T × belt 1 is 97 mm³ (was 84, since the whole belt height is now on the band), and each idler × its belt is 33 mm³.
- Snapshots not re-rendered: the 1–1.7 mm axial shifts don't show at the scale of the `belt_arm_*` images.

- **I‑10 accepted** (commit "Close I-10"), with no model change. The missing hole is the bottom one (270°, z 31.25). It lies inside the 20 mm hinge floor: its counterbore is all hinge, and the screw path from the inner face is 58 % hinge. Adding it would mean a pocket about 24 mm long into the floor top, leaving about 3 mm over the thrust pocket and breaking into an M5 counterbore. Five M3 carry about 31 N each at the most the ring sees (about 6 Nm). Options put to the instructor: accept, add a pocket, or skip. The instructor chose accept.

- **I‑5 fixed** (commit "Fix I-5"). The instructor confirmed the idler axles are M5 bolts, clamped by the head and a nut (this also answers Q3). The plates show which way round: the Base slot is Ø10 × 3, which fits an ISO 7380 button head (Ø9.5 × 2.75), and the Top slot is 8 wide, which fits an M5 nut (8 AF) flats-first so it cannot turn. step.parts supplied `button_head_screw_m5_l0040_simple` and `iso4032_hex_nut_m5` (sha256-verified, in `STEP/imported/vendor/`), wrapped as `purchased/button_head_m5x40.py` (flipped: shank +Z from the seat) and `purchased/hex_nut_m5.py`. Head seat z 3, nut z 39–43, tip z 43. No printed part changes, so the gate is unaffected.
- Checks: idler × axle went from 86.4 mm³ to 0 on both idlers. New: nut × Top 9.8 mm³ on both, because the Top slot's R4 end stops the nut 0.62 mm short of the y = 20 end (corners at 4.62), and the slot is line-to-line with the nut's flats. Both are logged under I‑4, whose jack-screw rework touches these slots.
- I‑4 plan agreed with the instructor: an M3 jack screw in a heat-set insert in the y = 0 Wall rail at each idler, pushing toward +y (compression only, turned from outside), then tighten the M5. J1 motor next, in its own commit.

- **I‑4 (arm) fixed** (commit "Fix I-4 (arm)"). An M3 × 35 ISO 4762 jack screw (step.parts `iso4762_socket_head_cap_screw_m3x35`, `purchased/socket_head_m3x35.py`) sits in a Ø4.2 insert through the y = 0 Wall rail at each idler. It pushes the 15 mm spacer at mid-height (idler 1 at z 29.5, idler 2 at z 14.5). Constants are in `belt_arm/common.py` (`JACK_SCREW_XZ`, `ycyl`).
  - Loop length against idler y: 274.4 at 20, 277.7 at 30, 280.3 at 34, 285.6 at 40. A 280 loop is at about y 33.8; the stroke reaches y 40.
  - The model shows the screws backed off to slack (seat y −20).
  - The Top nut slots run 1 mm further at each end (y 19 ↔ 66), so nut × Top went from 9.8 mm³ to 0. The slot width stays 8 (line-to-line, I‑11).
- Gate: the Wall and Top departures drifted (13.111 → 13.312 %, 0.412 → 0.550 %), and the gate caught it. Both are re-recorded as `"I-17, I-4"`. All belt_arm entries pass or depart as recorded.
- Checks:
  - jack strokes y 0 → 35 are clear;
  - J2 is unchanged;
  - **J3/J4 negative travel is now −94°**: the idler‑2 screw head meets the Output block end plate at −95° at slack (−97° at a 280 loop, −105° at y 40). +103° is unchanged. `J3_LIMITS` / `J4_LIMITS` are (−94, 103), verified clear at −94° and hit at −95°. This is still past the ±90° target. A pull screw from y = 80 would move the conflict to +103°, and the head cannot be recessed with a 20 mm stroke in a 7 mm rail.
- Re-rendered `docs/img/belt_arm_iso.png` (`--display parts --camera iso`). `belt_arm_internals.png` was not re-rendered: its top-hidden view was made in the viewer, and the screws are outside the plates it shows.
- Still open under I‑4: a jack screw for the J1 motor slot in Box top.
- **I‑4 (J1) accepted** (commit "Close I-4 (J1)"; instructor's choice, docs only). A push screw must sit between the motor and J1, which the hinge floor sweeps (r 55.7, underside z 15, 3 mm above Box top). A pull screw needs a new printed sled (breaking IF‑3, travel x 140–152). An idler on the slack strand takes up only about 2 mm of loop over 8 mm of travel (`tmp/i4_j1_belt.py`). The tensioning procedure is in design.md §2 Load path item 2.
- Finding: `checks/j1_yaw_clearance.py --slot-x 155,158,159,160` clears ±120° at every one of them. So a 366–372 mm J1 belt (motor at x ≈ 155.7–159.2) gives ±120° instead of the mid-slot ±40°. Recorded in §1, §2, the belt row and I‑14 (still open). `J1_LIMITS` stays (−40, 40) because the model's motor is at mid-slot.
- **I‑7 fixed** (commit "Fix I-7"; assembly only, no printed part or gate change). Done before I‑3 so that backlash can be checked from a meshing pose. Mesh condition (15/15/45, phases at one z): planet 3·ring − 2a − 12, sun 4a − 3·ring + 204 (mod 24°), checked on 2D sections (`tmp/i7_phase.py`). The output hex fixes stage 2's carrier (60° steps are 0 mod 24°), so the stage‑1 carrier turns +6.2947° and the input shaft +9.1834°; planet phases are 21.0469° / 22.8541°. Interference: the 12 gear pairs (3.4–65.0 mm³) went to none above 0.001 mm³; input shaft × stand-in NEMA17 9.8 mm³ is unchanged. Rebuilt planetary_gearbox, joint_1_and_2 and robot_arm; the part STEPs' float-noise rewrites were restored. No snapshot shows the planet phases (`gearbox_exploded.png` is a viewer view), so none was re-rendered.
- **I‑3 accepted** (commit "Close I-3"; instructor's choice, docs only). Measured: 0.106 mm circular backlash per mesh (each gear thinned 0.053); tip clearance 0.375 sun–planet, 0.125 ring tip → planet root, 0.20 planet tip → ring root. Offered 0.30 or 0.20 mm backlash with a Ø64.5 ring tip, or the ring tip alone; the built gears run acceptably. design.md I‑3 names the first change if a reprint binds.
- **I‑14 fixed** (commit "Fix I-14"; no printed part changes). The instructor has a stock of GT2 6 mm loops in several lengths, so the J1 belt is chosen to put the motor far out. The model uses 370 mm (`J1_BELT_LOOP` in `joint12/joint_1_and_2.py`; motor x = 158.04 from the new `gt2.centre_distance`). `checks/j1_yaw_clearance.py` (2° steps; now reads the motor's x from the STEP): clear to ±124° at 366 mm, ±128° at 370 and 372 mm; the ring gear hits next. Full arm, `--joint j1_waist`: clear at ±40…±80 (10° steps), ±90…±110, ±116…±128; ring gear × J1 motor 18 mm³ at ±130°. `J1_LIMITS` is now ±124°, which holds for any 366–372 mm belt. Q1 is resolved for J1. Re-rendered `joint12_iso.png`, `robot_arm_zero.png` and `robot_arm_pick.png`.
- **I‑11 fixed** (commit "Fix I-11"; instructor's choice: switchable, nominal default). Every fit feature in 21 part sources now takes its allowance from `lib/tolerances.py` `ACTIVE` by class (new `shaft` and `hex_socket_r` helpers; in the gearbox the tolerances `hole` is imported as `fit_hole`, because `gearbox.common.hole` is the axial-hole factory). `ACTIVE = FUSION` keeps every STEP: after a full rebuild all rewritten STEPs matched HEAD (volume within 5e‑10, same bbox and face count) and were restored. With `PLA_FDM`, all 19 fitted bodies build as valid single solids, 11–559 mm³ lighter (`tmp/i11_pla.py`, in memory: the decorated models return the stored STEP, so the check calls the `*_body` functions). New `src/fit_coupon.py` (172 × 64 × 6, one of each fit) is not gated: it has no Fusion counterpart. The class table is in design.md §6. Also: an edit script wrote `§` and `Ø` in the Windows default encoding; `tolerances.py` and `input_shaft.py` were repaired to UTF‑8 before the build.
- **Print fits per part** (commit "Make print fits per part, with bonded inserts for resin"). Parts go to whichever printer is free (PLA FDM, or a Formlabs SLA), so `lib/tolerances.py` now has `DEFAULT` plus a `PART_PROFILES` override by model name (checked against `PARTS`; a typo is an error), and each part reads `FIT = profile("<part>")`. The profile-derived constants left the three `common.py` files (`M3_CLEAR`, `M5_CLEAR`, `M3_INSERT`, `M5_INSERT`, `DOWEL_HOLE`) for `FitProfile` properties; the carrier factories take the profile. Threaded-insert holes are now per profile: heat-set Ø4.2 / Ø6.4 (`FUSION`, `PLA_FDM`) and bonded Ø4.8 / Ø7.3 (`RESIN`: ruthex knurl Ø4.6 / Ø7.1 + 0.2 for epoxy), because cured resin doesn't melt. Also sized: the `nema17_mount` M3 holes (Ø3.0, missed in I‑11). The coupon gained M3/M5 insert holes. Checks: with the defaults every rebuilt STEP matched HEAD (coupon aside); with `{"wall": RESIN}` the Wall's insert holes became Ø4.8 and the Base's stayed Ø4.2 (`tmp/perpart_test.py`).
- **I‑9 fixed by the recreation** (commit "Close I-9"; docs only). No product in the four assembly STEPs is named `Component*`, `test`, `GT2-120` or `6x11`. The parts are `gt2_pulley_160t` and `planet_pin_6x22`. The Fusion names stay in design.md's part tables, which describe the reference.
- **I‑12 accepted** (commit "Close I-12"; instructor's choice, docs only). Both thrust bearings are held by their OD. The lower one sits 5 mm in each Ø60 recess. The upper one sits 10 of 13 mm in the hinge's Ø61 pocket, and its bottom washer, which doesn't turn, is centred only by the balls. Options offered: accept, a Ø40 land on the hinge shaft, or a Ø60 lip on `Box top`.
- **I‑13 intentional** (commit "Close I-13"; docs only). The right cheek is rounded about z 62.5 instead of 70.5 to clear the segment‑1 motor. A right cheek rounded about 70.5 overlaps the motor by 592 mm³ at every J2 angle, 0° included. The cheek as built is clear to ±63° and touches at ±64° (5 mm³, I‑16) (`tmp/i13_cheek.py`). Gotcha: segments 1 and 2 both label their motor `nema17:j3`, so key leaves by link plus label; the first version of the script keyed by label alone, lost segment 1's motor and reported clear.

## Session 8 — 2026-10-27

- Purchased-parts inventory (`inventory.md`, repo root) from the Amazon orders; it linked the parts to the CAD and turned up two motor mismatches, logged as I‑18 and I‑19.
- **I‑19 fixed** (commit "Fix I-19"; no printed part or gate change). The instructor confirmed that the course motors have a 48 mm body, so `purchased/nema17.py` now has `body_length=48.0` (J1, J2, J3). Checks: J1 ±124° now needs a 370–372 mm belt (366 / 368 mm: ±122° / ±123°; `checks/j1_yaw_clearance.py` at 1° steps, which takes over an hour for four slot positions, so it was narrowed to 122°–126° in `tmp/`). J2 is unchanged at ±63° (motor × hinge at ±64°). J3 and J4 are clear at their limits. design.md §1, §2, I‑14 and I‑16 were updated, `docs/img/joint12_iso.png` was re-rendered (`--display parts --camera iso`), and the `inventory.md` J1 belt note now says 370–372 mm.
- **I‑18 fixed** (commit "Fix I-18"; no printed part or gate change). New `purchased/nema17_pancake.py` (20 mm body). `segment_parts(pancake=True)` swaps the segment motor; the full arm builds segment 2 that way, while `belt_drive_arm.step` keeps the full-size motor. J3 and J4 limits are unchanged (first contacts at +104° / −95°, as before). `docs/img/robot_arm_zero.png` and `robot_arm_pick.png` were re-rendered (`--kinematics zero|pick --camera iso`); they also show the 48 mm motors of I‑19.
- STEP rewrites of unchanged parts (1e‑16 float noise in a few printed parts and vendor fasteners) were reverted before committing.
- **DfAM pass** (commit "Log I-20 to I-23 from the DfAM pass"; docs only). The project was copied to `tmp/dfam/` with `DEFAULT = PLA_FDM`, the 23 printed parts were rebuilt there and exported to STL, and each was run through `$dfam-check` (`dfam_tool.py measure --samples 5000` and `orientations`, FDM limits: wall ≥ 1.2 mm supported, 45°). The committed STEPs and `tolerances.py` were not touched. Findings, logged in design.md §8:
  - I‑20: the three GT2 pulley STLs are not watertight (T-junctions at the tooth band / flange seam; the B-rep is valid).
  - I‑21: Ø6 M3 counterbores 3.5 mm from an edge leave 0.25–0.5 mm skins (Base, Top, Output block, Coupling shaft, Hinge left cheek).
  - I‑22: Back cover, 1.0 mm floor between the NEMA17-mount inserts and the carrier recess.
  - I‑23: Ring gear, insert holes 1.15 mm from the OD.
  - Below the limit but intrinsic, not logged: gear tooth tips (0.18–0.34 mm) and GT2 teeth (0.7–0.87 mm).
  - Print orientation (support area at 45°): flip Top, Back cover, Box top, Carrier plate, both carrier outputs, Coupling shaft and Input shaft; Output block on its side (rot 90° about Y, 15.5 → 1.1 %); Hinge on its side (rot 90° about X, 11.4 → 6.9 %, still supported); pulleys axis vertical; the rest as modelled.
  - Not measured by the tool: minimum hole diameter, minimum feature, bridges (the Hinge's Ø61 pocket roof is the obvious one).
- **I‑20 fixed** (commit "Fix I-20"; `lib/gt2.py` only). Cause: a 0.0258 mm radial step on each side of every groove, where the clipped R1 flank met the R0.555 bottom arc (320 short edges on the 80T), which the mesher could not weld. `_groove` is now one explicit outline with a 0.17 mm line tangent to the bottom arc, the convex hull of the old groove: 0.00285 mm² more per groove, toward Fusion's blend arcs. An explicit groove-cut construction with the old outline (identical solid) did not help, and neither did `clean()` or `ShapeFix`.
  - Meshes at default tolerance: `gt2_80_output` and `gt2_pulley_160t` watertight. `dual_gt2_pulley` has one degenerate triangle on one 80T tooth tip (3 open edges); the B-rep there is clean, and 1e‑3 / 2e‑3 / 1e‑4 exports are watertight. Logged as a residual in I‑20.
  - Gate: 160T PASS (0.014 % vol), 80T output PASS (0.025 %), dual DEPART (I‑15) at 0.270 % vol / 29.057 % symdiff against the recorded 0.28 / 29.061; the map was not changed.
  - Rebuilt the three pulleys, `belt_drive_arm`, `joint_1_and_2` and `robot_arm`. The float-noise rewrites (Top, Wall, carrier stage‑2 output, M5 nut, M3 × 35: same volume, faces and bbox to 5e‑16) were restored. No snapshot was re-rendered: 0.003 mm² per groove does not show.

### Next steps (continue Session 8)
1. Every issue except I‑8 is closed: I‑1, I‑2, I‑5, I‑6, I‑7, I‑9, I‑11, I‑14, I‑15 and I‑17 are fixed, I‑4 is fixed for the arm (J1 accepted), I‑3, I‑10, I‑12 and I‑16 are accepted, and I‑13 is intentional. I‑8 (the J1 belt, fasteners and end effector are not modelled) is still open, I‑18 (J4 pancake motor) and I‑19 (48 mm motor body) are fixed. The DfAM pass (step 4) logged I‑20 to I‑23; I‑20 is fixed. Next: I‑21 to I‑23, each waiting on the instructor's choice among the options in design.md §8.
2. One issue per commit: change the model, rerun the gate (expect the fixed part to leave the Fusion replica; record it with a `departure` object in `checks/fusion_map.json`, or, if the part is a rigid motion of the original, a transform back, as for I‑6), update design.md (part rows, §5, §8 with the commit).
3. Re-run `checks/joint_clearance.py` after any change near a joint; I‑16 and I‑17 decide the usable workspace.
4. DfAM checks: done (PLA_FDM, Session 8). Rerun after I‑20 to I‑23 are fixed. DFM (`$dfm`) does not apply: every part is printed.
5. Optional URDF (`$urdf`) from `full_arm/common.py`: one STL per link, in the link's joint frame.
6. **cadgen 0.8 migration: deferred** (instructor, Session 8). The project stays pinned to cadgen 0.7.26. 0.8 can't run a 0.7 project: every `@step` model, the `full_arm` kinematics, the `.step.json` sidecar and the `read_scene` checks (including the Fusion gate) must be ported, and the Open CASCADE 8 kernel can shift assembled parts. Do it as its own planned session, following the 0.7 → 0.8 guide in the text-to-cad repo (`docs/migrations/migrating-0.7-to-0.8.md`), and compare every export against the committed 0.7 STEP files.
