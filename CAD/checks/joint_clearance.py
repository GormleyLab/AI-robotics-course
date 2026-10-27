"""Joint clearance: turn one joint of the full arm and test the links it carries against the rest.

Usage (from CAD/):
    python checks/joint_clearance.py --joint j3_elbow --angles 30,60,90,-30,-60,-90
        [--step STEP/full_arm/robot_arm.step] [--min 0.5]

Reads the mates from the STEP's sidecar (``<name>.step.json``). The links
downstream of the joint's child (following the mate chain) are rotated about
the joint axis, every other joint held at zero, and tested part against part
(bounding-box prefilter, then the boolean common) against the upstream links.
Contacts already present at zero (gear meshes, bearings on journals, ...) are the
baseline: only pairs whose overlap grows by more than ``--min`` mm³ over it
are reported. Run the angles of a slow joint as parallel processes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cadgen import build123d as bd
from cadgen import read_scene


def _leaves(occ, link):
    if not occ.children:
        yield link, occ.label or "", occ.shape()
    for c in occ.children:
        yield from _leaves(c, link)


def _overlap(a, b):
    ba, bb = a.bounding_box(), b.bounding_box()
    if (ba.min.X > bb.max.X or ba.max.X < bb.min.X or ba.min.Y > bb.max.Y or ba.max.Y < bb.min.Y
            or ba.min.Z > bb.max.Z or ba.max.Z < bb.min.Z):
        return 0.0
    r = a & b
    return r.volume if r is not None else 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step", default="STEP/full_arm/robot_arm.step")
    ap.add_argument("--joint", required=True)
    ap.add_argument("--angles", required=True, help="comma-separated degrees")
    ap.add_argument("--min", type=float, default=0.5, help="mm³ growth over the zero pose to report")
    a = ap.parse_args()

    mates = json.loads(Path(a.step + ".json").read_text())["kinematics"]["mates"]
    mate = next((m for m in mates if m["name"] == a.joint), None)
    if mate is None:
        raise SystemExit(f"no joint {a.joint!r}; have {[m['name'] for m in mates]}")
    children = {m["parent"]: m["child"] for m in mates}
    moving, link = set(), mate["child"]
    while link:
        moving.add(link.lstrip("#"))
        link = children.get(link)

    scene = read_scene(a.step)
    parts = [p for root in scene.roots for occ in root.children for p in _leaves(occ, occ.label)]
    mov = [(f"{l}/{n}", s) for l, n, s in parts if l in moving]
    fix = [(f"{l}/{n}", s) for l, n, s in parts if l not in moving]
    axis = bd.Axis(tuple(mate["axis"]["origin"]), tuple(mate["axis"]["dir"]))

    def hits(angle):
        out = {}
        for mn, m in mov:
            mr = m.rotate(axis, angle) if angle else m
            for fn, f in fix:
                v = _overlap(mr, f)
                if v > 0:
                    out[(mn, fn)] = v
        return out

    base = hits(0.0)
    lo, hi = mate["limits"]["value"]
    print(f"{a.joint}: {len(mov)} moving x {len(fix)} fixed parts, declared limits {lo:g}..{hi:g} deg", flush=True)
    for ang in (float(v) for v in a.angles.split(",")):
        h = hits(ang)
        grown = {k: v - base.get(k, 0.0) for k, v in h.items() if v - base.get(k, 0.0) > a.min}
        rows = ", ".join(f"{mn} x {fn} {v:.0f}" for (mn, fn), v in sorted(grown.items(), key=lambda kv: -kv[1]))
        print(f"{ang:7.1f}  {'CLEAR' if not grown else 'HIT  ' + rows}", flush=True)


if __name__ == "__main__":
    main()
