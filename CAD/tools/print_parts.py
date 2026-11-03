"""Build a print set: the printed parts at chosen fit profiles, as meshes for the slicer.

    ~/.local/bin/cadgen +0.8.2 run tools/print_parts.py print_configs/<name>.json [--only PART ...]

The config picks the profiles (``lib/tolerances.configure``) and, optionally,
the parts. Configs validated with the fit coupon are committed in
``print_configs/`` (one per printer and material, with the coupon results in
``notes``); drafts and experiments go in ``tmp/print/``, which git ignores::

    {
      "notes": ["Form 4, Grey V5: validated 2026-11-03 ..."],  # free text, copied to the manifest
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
STL, moved so it is centred in XY on z = 0 (the slicer orients it),
``manifest.json`` with each part's resolved profile values, count per arm,
size, volume and mesh check, and ``print_list.txt``, a plain checklist of how
many of each file to print for one arm (for whoever runs the printer).

The STL is meshed at an absolute deflection with OCCT directly: build123d's
``export_stl`` and ``Mesher`` use a relative one, which leaves cracks between
faces (49 open edges on the carrier plate). Vertex copies a hair apart are
then welded to one exact position (``weld``), and each STL is checked closed
on exact positions: every edge shared by exactly two triangles.
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
# Vertex copies closer than this (mm) are one vertex. The copies seen are
# under 1e-6 apart; distinct vertices are 0.001 or more (ring gear flanks).
WELD = 1e-4


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
    weld(path)


def _triangles(path: Path) -> list[tuple]:
    data = path.read_bytes()
    n = struct.unpack_from("<I", data, 80)[0]
    return [struct.unpack_from("<9f", data, 84 + 50 * i + 12) for i in range(n)]


def weld(path: Path) -> None:
    """Rewrite a binary STL so each shared vertex has one exact position.

    OCCT writes each face's own copy of a vertex, from that face's
    parametrisation, so copies on a seam or a face boundary can differ in the
    last float bits (the Pin: 8 pairs under 1e-6 mm apart). PreForm compares
    exact positions and calls such a mesh broken. Copies within WELD of each
    other take the first one's position (and -0.0 becomes 0.0)."""
    tris = _triangles(path)
    points = sorted({v[j:j + 3] for v in tris for j in (0, 3, 6)})
    canon: dict[tuple, tuple] = {}
    for i, p in enumerate(points):
        if p in canon:
            continue
        canon[p] = tuple(x + 0.0 for x in p)
        for j in range(i + 1, len(points)):
            q = points[j]
            if q[0] - p[0] > WELD:
                break
            if q not in canon and max(abs(q[k] - p[k]) for k in range(3)) <= WELD:
                canon[q] = canon[p]
    out = bytearray(b"Binary STL from tools/print_parts.py (welded)".ljust(80, b" "))
    kept = []
    for v in tris:
        a, b, c = (canon[v[j:j + 3]] for j in (0, 3, 6))
        if a != b and b != c and c != a:
            kept.append((a, b, c))
    out += struct.pack("<I", len(kept))
    for a, b, c in kept:
        u = [b[k] - a[k] for k in range(3)]
        w = [c[k] - a[k] for k in range(3)]
        nrm = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        size = sum(x * x for x in nrm) ** 0.5 or 1.0
        out += struct.pack("<12fH", *(x / size for x in nrm), *a, *b, *c, 0)
    path.write_bytes(bytes(out))


def open_edges(path: Path) -> tuple[int, int]:
    """(triangles, edges not shared by exactly two triangles) of a binary STL,
    comparing exact vertex positions, as a slicer does."""
    tris = _triangles(path)
    edges: Counter = Counter()
    for v in tris:
        a, b, c = v[0:3], v[3:6], v[6:9]
        edges.update(frozenset(e) for e in ((a, b), (b, c), (c, a)))
    return len(tris), sum(1 for count in edges.values() if count != 2)


ASSEMBLY = {"joint12": "Base and J1", "gearbox": "J2 gearbox", "belt_arm": "Arm segments (J3, J4)"}


def _assembly(part: str) -> str:
    return ASSEMBLY.get(PRINTED[part][0].split(".")[0], "Other")


def write_print_list(out: Path, manifest: dict) -> None:
    """``print_list.txt``: how many of each file to print for one arm, grouped by assembly."""
    config = manifest["config"]
    notes = config.get("notes", [])
    notes = [notes] if isinstance(notes, str) else notes
    rows = [r for r in manifest["parts"] if r["count_per_arm"]]
    tests = [r["part"] for r in manifest["parts"] if not r["count_per_arm"]]
    lines = [f"PRINT LIST: {out.name}",
             f"Settings: {manifest['config_file']} (profile {config.get('default', 'FUSION')})",
             ""]
    if rows:
        lines += ["Print this many of each file for ONE arm (multiply for more arms).",
                  "Tick each line off as the prints come off the printer.", ""]
    width = max((len(r["part"]) for r in rows), default=6) + 4
    pieces = 0
    for group in dict.fromkeys(_assembly(r["part"]) for r in rows):
        lines.append(group)
        for r in rows:
            if _assembly(r["part"]) == group:
                size = " x ".join(f"{v:.1f}".removesuffix(".0") for v in r["size_mm"])
                lines.append(f"  [ ] {r['part'] + '.stl':<{width}} x{r['count_per_arm']:<3} {size} mm")
                pieces += r["count_per_arm"]
        lines.append("")
    if rows:
        lines.append(f"{len(rows)} files, {pieces} prints per arm, about "
                     f"{manifest['volume_per_arm_cm3']:.0f} cm3 of material per arm before supports.")
    if tests:
        lines.append(("Test pieces, not arm parts (print only if asked): " if rows else "Test pieces, print one of each: ")
                     + ", ".join(t + ".stl" for t in tests))
    lines += ["", "Use the .stl files. The .step files and manifest.json are for reference.",
              "Orientation, supports and avoiding warped flat parts: CAD/docs/claude-code-guide.md,",
              "section 3, Step 4 (Slice and print)."]
    if notes:
        lines += ["", "Notes from the print settings:"] + [f"  - {n}" for n in notes]
    (out / "print_list.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("config", type=Path)
    parser.add_argument("--only", nargs="+", metavar="PART", help="parts to build (overrides the config's)")
    parser.add_argument("--out", type=Path, help="output folder (default tmp/print/<config name>/)")
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    unknown = set(config) - {"notes", "default", "parts", "profiles", "only"}
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
    manifest = {"config": config, "config_file": str(args.config),
                "mesh_deflection": {"linear_mm": LINEAR, "angular_rad": ANGULAR},
                "parts": rows, "volume_per_arm_cm3": round(total, 1)}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    write_print_list(out, manifest)
    print(f"\n{len(rows)} parts, {total:.0f} cm3 per arm (solid, no supports) -> {out}")
    if any(r["open_edges"] for r in rows):
        sys.exit("some meshes are not closed: repair them in the slicer or report the part")


if __name__ == "__main__":
    main()
