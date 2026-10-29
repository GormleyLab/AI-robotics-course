"""List every face of Fusion parts as placed in their assembly (world frame).

Usage (from CAD/):
    python checks/inspect/world_faces.py FUSION.step REF [REF ...] [--min-area A]

For subassemblies whose Fusion frame is already clean (Joint 1 and 2), the
world frame is the modelling frame, so each line reads directly as a
feature: planes with their normal and extent, cylinders and cones with
radius, axis point and direction. Faces smaller than ``--min-area`` mm^2
(default 0) are skipped, which hides pulley and gear teeth.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # checks/: scene.py
from scene import read_scene  # noqa: E402


def _v(p) -> str:
    return f"({p.X:.3f}, {p.Y:.3f}, {p.Z:.3f})"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step")
    ap.add_argument("refs", nargs="+")
    ap.add_argument("--min-area", type=float, default=0.0)
    a = ap.parse_args()
    scene = read_scene(a.step)
    for ref in a.refs:
        (sel,) = scene.resolve(ref)
        shape = sel.shape()
        bb = shape.bounding_box()
        print(f"\n### {ref} vol={shape.volume:.2f} bbox {_v(bb.min)}..{_v(bb.max)} faces={len(shape.faces())}")
        for i, f in enumerate(shape.faces()):
            if f.area < a.min_area:
                continue
            kind, fb = f.geom_type.name, f.bounding_box()
            extent = f"bb {_v(fb.min)}..{_v(fb.max)} A={f.area:.2f}"
            if kind == "PLANE":
                print(f" f{i} PLANE n={_v(f.normal_at())} {extent}")
            elif kind in ("CYLINDER", "CONE"):
                ax = f.axis_of_rotation
                r = f"r={f.radius:.4f} " if f.radius is not None else ""
                print(f" f{i} {kind} {r}ax={_v(ax.position)} d={_v(ax.direction)} {extent}")
            else:
                print(f" f{i} {kind} {extent}")


if __name__ == "__main__":
    main()
