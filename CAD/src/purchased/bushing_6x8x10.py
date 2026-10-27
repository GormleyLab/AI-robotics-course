"""Plain bushing 6x8x10 (planets, dual pulley). Stand-in.

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/bushing_6x8x10.step")
def bushing_6x8x10():
    part = cots.annulus(6, 8, 10)
    part.label = "bushing_6x8x10"
    return part


if __name__ == "__main__":
    bushing_6x8x10()
