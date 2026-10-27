"""Report solid-solid overlaps between occurrences of a STEP assembly.

Usage (from CAD/):
    python checks/inspect/interference.py "STEP/imported/fusion/Joint 1 and 2.step" [--min 1.0]

Lists every pair of leaf occurrences whose common volume exceeds --min mm^3
(default 1.0). Expected overlaps (press fits, gear meshes at an unlucky
phase, bolts in holes) still appear; judge each one.
"""
from __future__ import annotations

import argparse
import itertools

from cadgen import read_scene


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", nargs="+")
    ap.add_argument("--min", type=float, default=1.0)
    args = ap.parse_args()
    for path in args.step:
        scene = read_scene(path)
        leaves = []
        for leaf in scene.leaves():
            sh = leaf.shape()
            if sh.volume <= 0:
                continue
            leaves.append((leaf.ref, leaf.label, sh, sh.bounding_box(optimal=False)))
        print(f"# {path}: {len(leaves)} solids")
        hits = 0
        for (ra, la, a, ba), (rb, lb, b, bb) in itertools.combinations(leaves, 2):
            if not ba.overlaps(bb):
                continue
            try:
                common = a & b
                v = common.volume if common is not None else 0.0
            except Exception as e:
                print(f"  ERR {ra} {la} x {rb} {lb}: {e!r}")
                continue
            if v > args.min:
                hits += 1
                print(f"  {v:10.1f} mm^3  {ra} {la}  x  {rb} {lb}")
        print(f"  -> {hits} overlapping pairs above {args.min} mm^3\n")


if __name__ == "__main__":
    main()
