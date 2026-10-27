"""6801 deep-groove bearing 12x21x5. Stand-in (no step.parts match).

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/bearing_6801.step")
def bearing_6801():
    part = cots.ball_bearing(12, 21, 5)
    part.label = "bearing_6801"
    return part


if __name__ == "__main__":
    bearing_6801()
