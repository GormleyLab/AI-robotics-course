"""Dowel pin 6x30. Stand-in (step.parts ISO 2338 D6x30 file is 60 mm long).

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/dowel_pin_6x30.step")
def dowel_pin_6x30():
    part = cots.pin(6, 30)
    part.label = "dowel_pin_6x30"
    return part


if __name__ == "__main__":
    dowel_pin_6x30()
