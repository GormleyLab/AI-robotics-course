"""NEMA17 stepper, 48 mm body, 5 mm shaft (23.7 mm from face). Stand-in; see lib/cots.py.

The course's STEPPERONLINE 2 A, 59 N·cm motors (J1, J2, J3; I-19). J4 uses the
pancake, purchased/nema17_pancake.py (I-18).

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots

BODY_LENGTH = 48.0


@step(out="../../STEP/purchased/nema17.step")
def nema17():
    part = cots.nema17(body_length=BODY_LENGTH)
    part.label = "nema17"
    return part


if __name__ == "__main__":
    nema17()
