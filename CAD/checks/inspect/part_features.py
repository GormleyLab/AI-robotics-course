"""Polar feature dump of Fusion parts in a chosen subassembly frame.

Usage (from CAD/):
    python checks/inspect/part_features.py FUSION.step REF [REF ...] [--to-part rx,ry,rz]

Each part is taken as placed in its assembly and rotated by ``--to-part``
(degrees; default 90,0,0 maps the Fusion gearbox frame onto the gearbox part
frame of src/gearbox/common.py). Features are then reported about the +Z
axis through the origin: coaxial and off-axis cylinders/cones as (r, angle,
z-span), z-levels of planar faces, and side planes as (normal angle, offset,
z-span). Pick ``--to-part`` so the subassembly's main axis becomes +Z.
"""
from __future__ import annotations

import argparse
import collections
import math
import sys
from pathlib import Path

import build123d as bd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # checks/: scene.py
from scene import read_scene  # noqa: E402


def describe(ref: str, s: bd.Shape) -> None:
    bb = s.bounding_box()
    print(f"\n### {ref}  vol={s.volume:.1f}  z=[{bb.min.Z:.3f},{bb.max.Z:.3f}]")
    rows = collections.defaultdict(list)
    for f in s.faces():
        t = f.geom_type.name
        if t not in ("CYLINDER", "CONE"):
            continue
        a = f.axis_of_rotation
        p = a.position
        dia = round(f.radius * 2, 3) if t == "CYLINDER" else 0.0
        if abs(abs(a.direction.Z) - 1) > 1e-3:
            rows[(t, "off-axis", dia)].append(
                (round(p.X, 3), round(p.Y, 3), round(p.Z, 3), tuple(round(v, 3) for v in a.direction)))
            continue
        r = math.hypot(p.X, p.Y)
        ang = math.degrees(math.atan2(p.Y, p.X)) if r > 1e-3 else 0.0
        fb = f.bounding_box()
        rows[(t, dia)].append((round(r, 3), round(ang, 2), round(fb.min.Z, 3), round(fb.max.Z, 3)))
    for k in sorted(rows, key=lambda k: (k[0], -k[-1])):
        uniq = sorted(set(rows[k]), key=lambda e: (e[0], e[1]))
        txt = "; ".join(str(e) for e in uniq[:8])
        print(f"  {k}: n={len(rows[k])} {txt}{' ...' if len(uniq) > 8 else ''}")

    z_levels, sides = set(), set()
    for f in s.faces():
        if f.geom_type.name != "PLANE":
            continue
        n, c = f.normal_at(), f.center()
        if abs(n.Z) > 0.999:
            z_levels.add(round(c.Z, 3))
        else:
            fb = f.bounding_box()
            sides.add((round(math.degrees(math.atan2(n.Y, n.X)), 2), round(c.X * n.X + c.Y * n.Y, 3),
                       round(fb.min.Z, 2), round(fb.max.Z, 2)))
    print("  z planes:", sorted(z_levels))
    if sides:
        print("  side planes (normal angle, offset from axis, z-span):", sorted(sides)[:16])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step")
    ap.add_argument("refs", nargs="+")
    ap.add_argument("--to-part", default="90,0,0")
    a = ap.parse_args()
    rot = bd.Rot(*(float(v) for v in a.to_part.split(",")))
    scene = read_scene(a.step)
    for ref in a.refs:
        (sel,) = scene.resolve(ref)
        describe(ref, rot * sel.shape())


if __name__ == "__main__":
    main()
