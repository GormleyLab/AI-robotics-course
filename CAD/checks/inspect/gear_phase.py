"""Find the tooth phase and tip/root radii of a toothed Fusion part.

Usage (from CAD/):
    python checks/inspect/gear_phase.py FUSION.step REF --z Z --r R --teeth N
        [--to-part rx,ry,rz] [--axis-xy X,Y]

The Fusion part is taken as placed in its assembly and rotated by
``--to-part`` (degrees; default 90,0,0 = Fusion gearbox frame -> gearbox
part frame). Points on the circle of radius R at height Z about the axis
through (X, Y) are tested for material; the centre angle of each material
arc is reported, folded into one pitch, and the radial extent of material
along the first tooth centre gives tip and root radii (searched within
+/-8 mm of R).
"""
from __future__ import annotations

import argparse
import math

from cadgen import build123d as bd
from cadgen import read_scene


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step")
    ap.add_argument("ref")
    ap.add_argument("--z", type=float, required=True)
    ap.add_argument("--r", type=float, required=True)
    ap.add_argument("--teeth", type=int, required=True)
    ap.add_argument("--to-part", default="90,0,0")
    ap.add_argument("--axis-xy", default="0,0")
    ap.add_argument("--step-deg", type=float, default=0.05)
    a = ap.parse_args()

    (sel,) = read_scene(a.step).resolve(a.ref)
    rx, ry, rz = (float(v) for v in a.to_part.split(","))
    part = bd.Rot(rx, ry, rz) * sel.shape()
    cx, cy = (float(v) for v in a.axis_xy.split(","))

    def inside(r, deg):
        t = math.radians(deg)
        return part.is_inside(bd.Vector(cx + r * math.cos(t), cy + r * math.sin(t), a.z))

    pitch = 360.0 / a.teeth
    n = int(round(2 * pitch / a.step_deg))
    states = [inside(a.r, i * a.step_deg) for i in range(n)]
    # first material arc fully inside the two-pitch window
    start = next(i for i in range(1, n) if states[i] and not states[i - 1])
    end = next(i for i in range(start, n) if not states[i])
    centre = (start + end - 1) / 2 * a.step_deg
    width = (end - start) * a.step_deg
    print(f"material arc at r={a.r}: centre {centre:.3f} deg (mod pitch {centre % pitch:.3f}), "
          f"angular width {width:.3f} deg, pitch {pitch:.3f} deg")

    # radial extent of material along the arc centre and along the gap centre
    for label, ang in (("tooth centre", centre), ("gap centre", centre + pitch / 2)):
        rs = [max(0.0, a.r - 8.0) + i * 0.05 for i in range(int(16.0 / 0.05))]
        hits = [r for r in rs if inside(r, ang)]
        if hits:
            print(f"  {label} {ang:.3f} deg: material r from {min(hits):.2f} to {max(hits):.2f} (0.05 mm steps)")


if __name__ == "__main__":
    main()
