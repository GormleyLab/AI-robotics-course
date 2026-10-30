"""Build a print set: the printed parts at chosen fit profiles, as meshes for the slicer.

    ~/.local/bin/cadgen +0.8.2 run tools/print_parts.py tmp/print/<name>.json [--only PART ...]

The config (keep it in ``tmp/print/``, which git ignores) picks the profiles
(``lib/tolerances.configure``) and, optionally, the parts::

    {
      "default": "RESIN",                          # FUSION, PLA_FDM, RESIN or one defined below
      "parts": {"box_bottom": "PLA_FDM"},          # per-part profile
      "profiles": {"RESIN": {"press": 0.07},       # adjust a preset ...
                   "TOUGH": {"base": "RESIN", "insert_m3": 4.9}},  # ... or add one
      "only": ["ring_gear", "planet_gear"]         # default: every arm part (not the coupon)
    }

Everything runs in this process: the profiles are set before any part module
is imported, and each part is its model's undecorated function, so no
``@step`` output is written and the committed STEPs are untouched. Output
goes to ``tmp/print/<config name>/`` (or ``--out``): per part a STEP and an
STL, moved so it is centred in XY on z = 0 (the slicer orients it), and
``manifest.json`` with each part's resolved profile values, count per arm,
size, volume and mesh check.

The STL is meshed at an absolute deflection with OCCT directly: build123d's
``export_stl`` and ``Mesher`` use a relative one, which leaves cracks between
faces (49 open edges on the carrier plate). Each STL is checked closed: every
edge shared by exactly two triangles.
"""
from __future__ import annotations

import argparse
import importlib
import json
import struct
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

CAD = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CAD / "src"))

# Printed parts: name -> (module, count per arm). The two arm segments print the same parts.
PRINTED = {
    "box_bottom": ("joint12.box_bottom", 1),
    "box_top": ("joint12.box_top", 1),
    "hinge": ("joint12.hinge", 1),
    "coupling_shaft": ("joint12.coupling_shaft", 1),
    "gt2_pulley_160t": ("joint12.gt2_pulley_160t", 1),
    "ring_gear": ("gearbox.ring_gear", 1),
    "back_cover": ("gearbox.back_cover", 1),
    "front_cover": ("gearbox.front_cover", 1),
    "nema17_mount": ("gearbox.nema17_mount", 1),
    "input_shaft": ("gearbox.input_shaft", 1),
    "planet_gear": ("gearbox.planet_gear", 6),
    "carrier_plate": ("gearbox.carrier_plate", 2),
    "carrier_stage1_output": ("gearbox.carrier_stage1_output", 1),
    "carrier_stage2_output": ("gearbox.carrier_stage2_output", 1),
    "base": ("belt_arm.base", 2),
    "top": ("belt_arm.top", 2),
    "wall": ("belt_arm.wall", 2),
    "dual_gt2_pulley": ("belt_arm.dual_gt2_pulley", 2),
    "gt2_80_output": ("belt_arm.gt2_80_output", 2),
    "output_block": ("belt_arm.output_block", 2),
    "pin": ("belt_arm.pin", 4),
    "spacer_5mm": ("belt_arm.spacer_5mm", 4),
    "spacer_15mm": ("belt_arm.spacer_15mm", 4),
    "fit_coupon": ("fit_coupon", 0),
}

# Mesh deflection, mm and rad: fine enough for bearing seats and gear flanks.
LINEAR, ANGULAR = 0.01, 0.1


def write_stl(part, path: Path) -> None:
    """Binary STL of ``part`` at the absolute LINEAR / ANGULAR deflection."""
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.BRepTools import BRepTools
    from OCP.IMeshTools import IMeshTools_Parameters
    from OCP.StlAPI import StlAPI_Writer

    BRepTools.Clean_s(part.wrapped)
    parameters = IMeshTools_Parameters()
    parameters.Deflection, parameters.Angle, parameters.Relative, parameters.InParallel = LINEAR, ANGULAR, False, True
    BRepMesh_IncrementalMesh(part.wrapped, parameters)
    writer = StlAPI_Writer()
    writer.ASCIIMode = False
    if not writer.Write(part.wrapped, str(path)):
        raise RuntimeError(f"could not write {path}")


def open_edges(path: Path) -> tuple[int, int]:
    """(triangles, edges not shared by exactly two triangles) of a binary STL."""
    data = path.read_bytes()
    n = struct.unpack_from("<I", data, 80)[0]
    ids: dict[tuple, int] = {}
    edges: Counter = Counter()
    for i in range(n):
        v = struct.unpack_from("<9f", data, 84 + 50 * i + 12)
        a, b, c = (ids.setdefault(tuple(round(x, 5) for x in v[j:j + 3]), len(ids)) for j in (0, 3, 6))
        edges.update((min(p, q), max(p, q)) for p, q in ((a, b), (b, c), (c, a)))
    return n, sum(1 for count in edges.values() if count != 2)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("config", type=Path)
    parser.add_argument("--only", nargs="+", metavar="PART", help="parts to build (overrides the config's)")
    parser.add_argument("--out", type=Path, help="output folder (default tmp/print/<config name>/)")
    args = parser.parse_args()

    config = json.loads(args.config.read_text())
    unknown = set(config) - {"default", "parts", "profiles", "only"}
    if unknown:
        sys.exit(f"{args.config}: unknown keys {sorted(unknown)}")
    only = args.only or config.get("only") or [p for p, (_, n) in PRINTED.items() if n]
    unknown = set(only) - set(PRINTED)
    if unknown:
        sys.exit(f"unknown parts {sorted(unknown)}; known: {list(PRINTED)}")
    out = (args.out or CAD / "tmp" / "print" / args.config.stem).resolve()
    if out.is_relative_to(CAD / "STEP") or out.is_relative_to(CAD / "src"):
        sys.exit(f"{out}: print sets go outside STEP/ and src/ (default tmp/print/)")

    from lib import tolerances

    tolerances.configure(config.get("default", "FUSION"), config.get("parts"), config.get("profiles"))

    import build123d as bd

    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in only:
        module, count = PRINTED[name]
        model = getattr(importlib.import_module(module), name)
        part = model.function()  # the body, without the build that writes the model's STEP
        box = part.bounding_box()
        part = bd.Pos(-box.center().X, -box.center().Y, -box.min.Z) * part
        part.label = name
        bd.export_step(part, out / f"{name}.step")
        write_stl(part, out / f"{name}.stl")
        triangles, bad = open_edges(out / f"{name}.stl")
        fit = tolerances.profile(name) if name in tolerances.PARTS else None
        rows.append({"part": name, "count_per_arm": count, "profile": asdict(fit) if fit else None,
                     "size_mm": [round(v, 2) for v in (box.size.X, box.size.Y, box.size.Z)],
                     "volume_cm3": round(part.volume / 1000, 2), "triangles": triangles, "open_edges": bad})
        print(f"{name:<24} x{count}  {fit.name if fit else '(no fits)':<14} "
              f"{box.size.X:6.1f} x {box.size.Y:6.1f} x {box.size.Z:6.1f} mm  {part.volume / 1000:7.1f} cm3"
              + (f"  MESH NOT CLOSED: {bad} open edges" if bad else ""))

    total = sum(r["volume_cm3"] * r["count_per_arm"] for r in rows)
    (out / "manifest.json").write_text(json.dumps(
        {"config": config, "config_file": str(args.config),
         "mesh_deflection": {"linear_mm": LINEAR, "angular_rad": ANGULAR},
         "parts": rows, "volume_per_arm_cm3": round(total, 1)}, indent=2) + "\n")
    print(f"\n{len(rows)} parts, {total:.0f} cm3 per arm (solid, no supports) -> {out}")
    if any(r["open_edges"] for r in rows):
        sys.exit("some meshes are not closed: repair them in the slicer or report the part")


if __name__ == "__main__":
    main()
