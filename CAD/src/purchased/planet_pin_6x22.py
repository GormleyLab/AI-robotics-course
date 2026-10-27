"""Planet pin 6x22 (Fusion 'Pin 6x11mm'). Stand-in, Fusion size.

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/planet_pin_6x22.step")
def planet_pin_6x22():
    part = cots.pin(6, 22)
    part.label = "planet_pin_6x22"
    return part


if __name__ == "__main__":
    planet_pin_6x22()
