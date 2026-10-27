"""6805 deep-groove bearing 25x37x7. Stand-in (no step.parts match).

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/bearing_6805.step")
def bearing_6805():
    part = cots.ball_bearing(25, 37, 7)
    part.label = "bearing_6805"
    return part


if __name__ == "__main__":
    bearing_6805()
