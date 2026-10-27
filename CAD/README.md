# Robotic Arm CAD

**14:125:444 Smart Prosthetics and Robotic Systems** — Dr. Adam Gormley

CAD for the course's 4‑axis robotic arm: a base with J1 (waist yaw), a 16:1
planetary gearbox on J2 (shoulder), and two identical belt-drive arm segments
on J3 (elbow) and J4 (wrist). The parts are Python models (build123d via
[cadgen](https://pypi.org/project/cadgen/)) recreated from the original Fusion
360 design. The generated STEP files are committed, so you can open or reuse
them without installing anything.

## Printing the parts

> **The committed STEP files are not print-ready.** They keep the original
> Fusion sizes, so bearing seats, pin holes and hex sockets are exactly the size
> of the parts that go in them, with no allowance. Printed as-is, most fits
> will be too tight.

To get print-ready parts:

1. **Tune the fits.** Print the fit coupon (one of each fit, including the
   threaded-insert holes) on each printer you will use, and try it with your
   bearings, pins, bushings, screws, M5 nut and inserts. Adjust the `PLA_FDM`
   or `RESIN` values in `src/lib/tolerances.py` until each one fits. The
   committed `STEP/fit_coupon.step` is nominal, so regenerate it first as in
   steps 2–3: with `DEFAULT = PLA_FDM` for the PLA coupon, and with
   `"fit_coupon": RESIN` in `PART_PROFILES` for the resin one.
2. **Choose profiles.** In `src/lib/tolerances.py`:
   - change `DEFAULT = FUSION` to `DEFAULT = PLA_FDM`;
   - list any parts going to the resin (Formlabs) printer in `PART_PROFILES`,
     by model name, for example `PART_PROFILES = {"wall": RESIN, "pin": RESIN}`.
     The names are in `PARTS` in the same file; a misspelled one is an error.

   Each part sizes only its own holes, seats and shafts, so a resin part next
   to a PLA part needs nothing else.
3. **Regenerate.** From `CAD/`, rebuild the full arm, which rebuilds every part:

   ```bash
   PYTHONPATH=src uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.26 python src/full_arm/robot_arm.py
   PYTHONPATH=src uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.26 python src/fit_coupon.py
   ```

4. **Print from the regenerated `STEP/` files**, then set `DEFAULT` back to
   `FUSION`, empty `PART_PROFILES`, and regenerate again before committing
   anything. The committed files are the nominal set; small allowances can
   still pass the Fusion comparison (`checks/compare_to_fusion.py`), so it
   won't reliably catch a profile left switched on.

**Threaded inserts in resin.** Cured resin does not melt, so heat-set inserts
don't work in it. Use the same ruthex inserts bonded with slow-cure epoxy: the
`RESIN` profile makes their holes Ø4.8 (M3) and Ø7.3 (M5), the knurl diameter
plus a glue gap. Put the epoxy on the hole wall and thread a greased screw into
the insert while it cures, so no glue gets into the threads.

Which features get which allowance (press, slip, clearance, hex socket,
inserts), and what is deliberately left alone (gear teeth), is in
[design.md §6, Fasteners and print fits](docs/design.md#6-fasteners-and-print-fits).

## Layout

| Folder | Contents |
|---|---|
| `STEP/` | Generated parts and assemblies: `joint12/` (base, J1, hinge), `gearbox/` (J2), `belt_arm/` (one arm segment), `full_arm/` (the whole arm, with joint kinematics), `purchased/` (bearings, motors, hardware) |
| `STEP/imported/` | The original Fusion 360 exports (`fusion/`) and downloaded vendor parts (`vendor/`) |
| `src/` | The Python models; catalog and run instructions in [`src/README.md`](src/README.md) |
| `checks/` | Verification scripts: the Fusion comparison, interference and joint-clearance sweeps |
| `docs/` | [`design.md`](docs/design.md) (parts, interfaces, gear and belt data, issue log) and [`migration-log.md`](docs/migration-log.md) (the Fusion → Python migration, session by session) |
