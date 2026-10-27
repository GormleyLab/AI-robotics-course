"""Washer 6.2x11.8x1.3 (Fusion 'Washer 6mm'). Stand-in, Fusion size.

Frame: axis +Z, end face (motor: mounting face) at z=0.
"""
from cadgen import step

from lib import cots


@step(out="../../STEP/purchased/washer_6.step")
def washer_6():
    part = cots.annulus(6.2, 11.8, 1.3)
    part.label = "washer_6"
    return part


if __name__ == "__main__":
    washer_6()
