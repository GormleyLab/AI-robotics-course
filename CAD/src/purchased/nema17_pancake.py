"""NEMA17 pancake stepper, 20 mm body, 5 mm shaft (23.7 mm from face). Stand-in; see lib/cots.py.

The course's STEPPERONLINE 1 A, 16 N·cm motor (Amazon B091YDBK1S), used for J4
on segment 2: it is lighter and J4 needs less torque (I-18). Same face, pilot
and 31 mm screw pattern as nema17.py (IF-9). The shaft length is not on the
listing; it is taken equal to the full-size motor's.

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots

BODY_LENGTH = 20.0


@step(out="../../STEP/purchased/nema17_pancake.step")
def nema17_pancake():
    part = cots.nema17(body_length=BODY_LENGTH)
    part.label = "nema17_pancake"
    return part


if __name__ == "__main__":
    nema17_pancake()
