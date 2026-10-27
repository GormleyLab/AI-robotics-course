"""51108 thrust ball bearing 40x60x13. Stand-in (no step.parts match).

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/thrust_bearing_51108.step")
def thrust_bearing_51108():
    part = cots.thrust_bearing(40, 60, 13)
    part.label = "thrust_bearing_51108"
    return part


if __name__ == "__main__":
    thrust_bearing_51108()
