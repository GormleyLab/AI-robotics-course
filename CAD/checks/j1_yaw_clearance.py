"""J1 yaw clearance: rotate the J1 stack about the J1 axis and test it against the J1 motor.

Usage (from CAD/):
    python checks/j1_yaw_clearance.py [STEP/joint12/joint_1_and_2.step] [--slot-x 140,150,160] [--step 10]

The rotating stack is the hinge, the coupling shaft, the hinge 6805s and the
whole gearbox. The motor (``nema17:j1``) is moved along the slot from its
modelled position (read from its bounding box) to each ``--slot-x``. Prints one row per slot
position, one character per yaw angle from -180 deg (``.`` clear, ``X``
contact), then the clear range around 0 deg and the parts that hit first.
"""
from __future__ import annotations

import argparse

from cadgen import build123d as bd
from cadgen import read_scene

J1 = (75.0, 75.0)
ROTATING = ("hinge", "coupling_shaft", "bearing_6805:left_cheek", "bearing_6805:right_cheek")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", nargs="?", default="STEP/joint12/joint_1_and_2.step")
    ap.add_argument("--slot-x", default="140,150,160")
    ap.add_argument("--step", type=float, default=10.0, dest="step_deg")
    a = ap.parse_args()

    scene = read_scene(a.step)
    motor, stack = None, []
    for leaf in scene.leaves():
        label = leaf.label or ""
        parent = leaf.ref.rsplit(".", 1)[0]
        if label == "nema17:j1":
            motor = leaf.shape()
        elif label in ROTATING or (scene.resolve(f"{a.step}{parent}")[0].label == "planetary_gearbox"):
            stack.append((label, leaf.shape()))
    if motor is None:
        raise SystemExit("no nema17:j1 occurrence")

    mb0 = motor.bounding_box()
    modelled_x = (mb0.min.X + mb0.max.X) / 2
    angles = [-180.0 + i * a.step_deg for i in range(int(round(360 / a.step_deg)))]
    pivot = bd.Pos(J1[0], J1[1], 0)
    for x in (float(v) for v in a.slot_x.split(",")):
        m = bd.Pos(x - modelled_x, 0, 0) * motor
        mb = m.bounding_box()
        row, hits = [], {}
        for ang in angles:
            who = []
            for label, s in stack:
                r = pivot * bd.Rot(0, 0, ang) * pivot.inverse() * s
                if not r.bounding_box().overlaps(mb):
                    continue
                c = r & m
                if c is not None and c.volume > 0.01:
                    who.append(label)
            row.append("X" if who else ".")
            hits[ang] = who
        i0 = angles.index(0.0)
        lo = hi = i0
        while lo > 0 and row[lo - 1] == ".":
            lo -= 1
        while hi < len(row) - 1 and row[hi + 1] == ".":
            hi += 1
        print(f"slot x={x:g}: {''.join(row)}")
        print(f"  clear around 0: {angles[lo]:g} .. {angles[hi]:g} deg")
        for edge in (lo - 1, hi + 1):
            if 0 <= edge < len(angles):
                print(f"  at {angles[edge]:g} deg: {', '.join(sorted(set(hits[angles[edge]])))}")


if __name__ == "__main__":
    main()
