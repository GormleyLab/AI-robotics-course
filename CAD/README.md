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

Print-ready parts come from `tools/print_parts.py`, which builds a print set
at the fit profiles you choose and writes it to `tmp/print/` (git-ignored). It
never edits `src/lib/tolerances.py` or writes to `STEP/`, so the committed
files stay the nominal set.

1. **Write a print config** in `tmp/print/`, for example `tmp/print/resin.json`:

   ```json
   {
     "default": "RESIN",
     "parts": {"box_bottom": "PLA_FDM"},
     "profiles": {"RESIN": {"press": 0.07},
                  "TOUGH": {"base": "RESIN", "insert_m3": 4.9}},
     "only": ["ring_gear", "planet_gear"]
   }
   ```

   - `default`: the profile for every part not listed in `parts`: `FUSION`,
     `PLA_FDM`, `RESIN` (Formlabs), or one defined in `profiles`.
   - `parts`: a profile per part, by model name (the names in `PARTS` in
     `src/lib/tolerances.py`). Each part sizes only its own holes, seats and
     shafts, so a resin part next to a PLA part needs nothing else.
   - `profiles`: changes to a preset's values (`press`, `slip`, `clearance`,
     `hex_socket`, `insert_m3`, `insert_m5`, ...), or a new profile from a
     `base`. The committed presets are unchanged.
   - `only`: the parts to build. Without it, every arm part is built (not the
     fit coupon).

   A misspelled part, profile or value is an error.
2. **Tune the fits first.** Build `fit_coupon` (one of each fit, including the
   threaded-insert holes) at the profile of each printer you will use. Try it
   with your bearings, pins, bushings, screws, M5 nut and inserts, and adjust
   the profile's values in the config until each one fits.
3. **Build.** From `CAD/`:

   ```bash
   ~/.local/bin/cadgen +0.8.2 run tools/print_parts.py tmp/print/resin.json
   ```

   `--only PART ...` overrides the config's list, and `--out DIR` the output
   folder (default `tmp/print/<config name>/`). The first time, install
   cadgen 0.8.2 and its `cadgen` launcher with

   ```bash
   uvx --no-config --managed-python --python 3.13 --from cadgen==0.8.2 cadgen doctor
   ```

4. **Print from the output folder.** Each part has an STL (meshed to
   0.01 mm and checked closed) and a STEP, centred on the origin with its
   base at z = 0 in the model's orientation; orient it in the slicer.
   `manifest.json` records each part's profile values, count per arm, size
   and volume, so a print can be traced to the settings that made it.

The script sets the profiles in its own process before it imports any part,
and builds each part from its model's undecorated function. A normal model
run never sees the config. Don't edit `DEFAULT` or `PART_PROFILES` to print:
a regenerated `STEP/` set with a profile left switched can still pass the
Fusion comparison (`checks/compare_to_fusion.py`).

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
| `tools/` | `print_parts.py`: builds print sets at chosen fit profiles into `tmp/print/` ([Printing the parts](#printing-the-parts)) |
| `docs/` | [`design.md`](docs/design.md) (parts, interfaces, gear and belt data, issue log) and [`migration-log.md`](docs/migration-log.md) (the Fusion → Python migration, session by session) |
