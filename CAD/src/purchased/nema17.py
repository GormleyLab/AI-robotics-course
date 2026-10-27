"""NEMA17 stepper, 40 mm body, 5 mm shaft (23.7 mm from face). Stand-in; see lib/cots.py.

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/nema17.step")
def nema17():
    part = cots.nema17()
    part.label = "nema17"
    return part


if __name__ == "__main__":
    nema17()
