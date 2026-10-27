"""6807 deep-groove bearing 35x47x7. Stand-in (no step.parts match).

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/bearing_6807.step")
def bearing_6807():
    part = cots.ball_bearing(35, 47, 7)
    part.label = "bearing_6807"
    return part


if __name__ == "__main__":
    bearing_6807()
