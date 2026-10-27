"""Tooth phase and width of a toothed part (gear or pulley) versus height.

Usage (from CAD/):
    python checks/inspect/tooth_phase.py SOURCE --r R --pitch DEG --z Z1,Z2,... \
        [--ref REF] [--to-part rx,ry,rz] [--centre X,Y]

SOURCE is a Fusion STEP with ``--ref`` (the part as placed in its assembly,
rotated by ``--to-part``, default 90,0,0 = gearbox frame), or a generated
single-part STEP without ``--ref`` (used as-is). At each height Z the part
is intersected with a thin annulus of radius R about the axis through
``--centre``; the pieces are the teeth (or ring-gear teeth), and their mean
angle modulo the pitch is the tooth phase. The phase change with Z gives
the helix: tan(beta) = R * dphase/dz (radians). Much faster than
gear_phase.py's point sampling.
"""
from __future__ import annotations

import argparse
import math

from cadgen import build123d as bd
from cadgen import read_scene, read_step

_MIN = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("--ref")
    ap.add_argument("--r", type=float, required=True, help="sampling radius, usually the pitch radius")
    ap.add_argument("--pitch", type=float, required=True, help="angular pitch in degrees (360 / teeth)")
    ap.add_argument("--z", required=True, help="comma-separated heights")
    ap.add_argument("--to-part", default="90,0,0")
    ap.add_argument("--centre", default="0,0")
    a = ap.parse_args()

    if a.ref:
        (sel,) = read_scene(a.source).resolve(a.ref)
        part = bd.Rot(*(float(v) for v in a.to_part.split(","))) * sel.shape()
    else:
        part = read_step(a.source)
    cx, cy = (float(v) for v in a.centre.split(","))
    r, pitch = a.r, a.pitch

    for z in (float(v) for v in a.z.split(",")):
        annulus = bd.Pos(cx, cy, z - 0.01) * (bd.Cylinder(r + 0.05, 0.02, align=_MIN)
                                              - bd.Cylinder(r - 0.05, 0.02, align=_MIN))
        pieces = [p for p in (part & annulus).solids()
                  if math.hypot(p.center().X - cx, p.center().Y - cy) < r + 1]
        if not pieces:
            print(f"z={z:7.2f}: no material at r={r}")
            continue
        angs = [math.degrees(math.atan2(p.center().Y - cy, p.center().X - cx)) % pitch for p in pieces]
        s = sum(math.sin(2 * math.pi * x / pitch) for x in angs)
        c = sum(math.cos(2 * math.pi * x / pitch) for x in angs)
        mean = (math.atan2(s, c) * pitch / (2 * math.pi)) % pitch
        width = sum(math.degrees(p.volume / (0.1 * 0.02 * r)) for p in pieces) / len(pieces)
        print(f"z={z:7.2f}: n={len(pieces):3d} tooth centre {mean:7.3f} deg "
              f"(spread {max(angs) - min(angs):.3f}) width {width:.3f} deg")


if __name__ == "__main__":
    main()
