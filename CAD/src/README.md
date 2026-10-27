# Models

Run from `CAD/` with cadgen's pinned Python:

```bash
PY="uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.26 python"
PYTHONPATH=src $PY src/purchased/nema17.py
```

Unchanged models report `current`. Assemblies (Sessions 3–6) build their children.

## Shared library (`lib/`, not entrypoints)

| Module | Purpose |
| --- | --- |
| `params.py` | Locked interface dimensions (design.md §5) |
| `tolerances.py` | Fit profiles: `FUSION` (nominal, replica phase), `PLA_FDM`, `RESIN` |
| `gears.py` | Involute spur gear and internal ring-gear cutter (validated: 15T m1.5 planet within 0.09 % of Fusion volume) |
| `gt2.py` | GT2 pulley profile, flanged pulley, pitch/outside diameter, belt length; belt path, idler engagement and belt envelope over pulleys and idlers (validated: 20T/80T sections within 0.1 % of Fusion) |
| `cots.py` | Parametric stand-ins for purchased parts with no usable step.parts model |

## Purchased parts (`purchased/` → `STEP/purchased/`)

Frame: axis +Z, end face (motor: mounting face) at z = 0.

| Script | Source | Used in |
| --- | --- | --- |
| `nema17.py` | Stand-in, 42.3 frame, 40 body, Ø5 × 23.7 shaft | J1, J2, J3, J4 |
| `bearing_608.py` | step.parts `bearing_608_2rs_sealed_simple` | J1 pulley hub |
| `bearing_6801.py` | Stand-in 12×21×5 | Gearbox (×2) |
| `bearing_6803.py` | step.parts `bearing_6803_2rs` | Gearbox back cover |
| `bearing_6805.py` | Stand-in 25×37×7 | Hinge (×2), gearbox front cover, arm J3 (×2 per segment) |
| `bearing_6807.py` | Stand-in 35×47×7 | Box top (J1) |
| `thrust_bearing_51108.py` | Stand-in 40×60×13 | J1 (×2) |
| `gt2_pulley_20t.py` | step.parts `gt2_pulley_20t_bore5_w6`, bore cut through both flanges (the vendor file leaves them solid) | Motor pulleys |
| `gt2_idler_20t.py` | step.parts `gt2_toothed_idler_bore5_w6`, bore cut through both flanges (Fusion bore; see I-5) | Arm idlers (×2 per segment) |
| `dowel_pin_6x30.py` | Stand-in | Arm axles (×3 per segment) |
| `planet_pin_6x22.py` | Stand-in (Fusion "Pin 6x11mm") | Planets (×6) |
| `bushing_6x8x10.py` | Stand-in | Planets (×6), dual pulley (×2 per segment) |
| `washer_6.py` | Stand-in 6.2×11.8×1.3 | Planets (×12) |

Imported sources: `STEP/imported/fusion/` (the three Fusion exports, the replica reference) and `STEP/imported/vendor/` (step.parts downloads, sha256-verified).

## Planetary gearbox (`gearbox/` → `STEP/gearbox/`), Session 3

Gearbox frame: axis +Z, z = 0 at the ring / back-cover joint, motor at +Z
(`gearbox/common.py`; `TO_FUSION = Rot(-90, 0, 0)` maps onto the Fusion gearbox).

| Script | Fusion part | Notes |
| --- | --- | --- |
| `ring_gear.py` | Ring gear | 45T helical internal, two bands with separate cutters |
| `back_cover.py`, `front_cover.py` | Back / Front cover | Slot-pocket helper in `common.py` |
| `nema17_mount.py` | NEMA17 mount | |
| `input_shaft.py` | Input shaft v5 | Stage-1 sun (left-hand) |
| `carrier_plate.py` | Carrier p1 - stage 1 / stage 2 | One model, two placements |
| `carrier_stage1_output.py` | Carrier p1 - stage 1 - Output | Stage-2 sun |
| `carrier_stage2_output.py` | Carrier p2 - stage 2 - Output v5 | Output shaft + hex |
| `planet_gear.py` | Planet gear (×6) | Right-hand helix |
| `planetary_gearbox.py` | Assembly | Not named `gearbox.py`: running it would shadow the package |

Helpers (not entrypoints): `common.py`, `carrier.py`.

## Joint 1 and 2 base (`joint12/` → `STEP/joint12/`), Session 4

Base frame: the Fusion "Joint 1 and 2" frame as-is (box corner origin, top of
the box bottom at z = 0, J1 at (75, 75), J2 ‖ X at z = 70.5). Parts are
modelled in place; `common.py` holds `GEARBOX_PLACEMENT` (gearbox frame →
base frame) and shared helpers.

| Script | Fusion part | Notes |
| --- | --- | --- |
| `box_bottom.py` | Box bottom v5 | |
| `box_top.py` | Box top v6 | J1 motor slot and M3 slots |
| `hinge.py` | Hinge v8 | Cheeks rounded at z 70.5 / 62.5 (I-13); 5 of 6 cover holes (I-10) |
| `coupling_shaft.py` | Coupling shaft v1 | 21.65 AF socket, line-to-line with the gearbox hex (I-2) |
| `gt2_pulley_160t.py` | GT2-120 v4 (160T, I-9) | `lib/gt2.py` profile |
| `joint_1_and_2.py` | Assembly | Adds the J1 NEMA17 and 20T pulley at mid-slot (not in Fusion, not gated) |

Helper (not an entrypoint): `common.py`. Check: `checks/j1_yaw_clearance.py` (I-14).

Both vendor 20T files are plain Ø15.23 bands, not toothed (a GT2 20T has OD 12.22); belt envelopes use the `lib/gt2.py` diameters.

## Belt drive arm segment (`belt_arm/` → `STEP/belt_arm/`), Session 5

Arm frame: the Fusion "Belt Drive Arm" frame as-is (plates in XY, Base
underside at z = 0, proximal end at x = -40, J3 ‖ Z through (160, 40)).
Parts are modelled in place; `common.py` holds the shared positions,
`OUTPUT_PULLEY_XY` (9.08 mm off J3, I-6) and `PIN_2_PLACEMENT`.

| Script | Fusion part | Notes |
| --- | --- | --- |
| `base.py` | Base | Motor pilot, J3 6805 seat, dowel boss, idler slots |
| `wall.py` | Wall | U-frame, 7 insert holes |
| `top.py` | Top | |
| `dual_gt2_pulley.py` | Dual GT2 pulley | 80T + 20T flanged, `lib/gt2.flanged_pulley` |
| `gt2_80_output.py` | GT2-80 output | 21.65 AF socket; gated with `"method": "sliced"` (the 3D boolean returns a wrong result) |
| `pin.py` | Pin (×2) | Modelled as Pin:1; Pin:2 at `PIN_2_PLACEMENT` |
| `output_block.py` | Output block | Fork, mitred R5 root fillets, hex socket, link interface |
| `spacer_5mm.py`, `spacer_15mm.py` | Spacer 5mm / 15mm (×2 each) | Modelled at idler 1 |
| `belt_drive_arm.py` | Assembly | Adds the two belt envelopes (not in Fusion, not gated). Not named `belt_arm.py`: that would shadow the package |

Helper (not an entrypoint): `common.py`.

## Full arm (`full_arm/` → `STEP/full_arm/`), Session 6

Robot frame: origin on J1 at the top of the box top, +Z up, +X = base-frame
+Y, J2–J4 along +Y (design.md §7). `common.py` holds the placements
(base → robot, segment → base, segment 2 → segment 1), joint axes and limits.

| Script | Contents | Notes |
| --- | --- | --- |
| `robot_arm.py` | Base + segment 1 + segment 2 | Five links (base, waist, upper arm, forearm, wrist) with `revolute` mates J1–J4 and poses `zero`, `reach`, `pick`, `folded`. Built from `joint12_parts()` and `segment_parts()`. Not gated |

Helper (not an entrypoint): `common.py`. Check: `checks/joint_clearance.py --joint <name> --angles ...` (I-14, I-16, I-17).

## Printed parts still to come

None for the replica. Every printed part needs an entry in `checks/fusion_map.json`, and must pass `python checks/compare_to_fusion.py --map checks/fusion_map.json`.
