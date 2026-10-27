"""Carrier plate (Fusion "Carrier p1 - stage 1" and "- stage 2"): one model, two placements.

Modelled in its stage-1 placement (gearbox frame z -14..5, first pin at
26.41 deg). Stage 2 uses ``STAGE2_PLACEMENT``.
"""
from cadgen import build123d as bd
from cadgen import step

from gearbox.carrier import carrier_plate as plate_factory
from lib.tolerances import profile

FIT = profile("carrier_plate")

Z_BOTTOM, PIN_ANGLE = -12.0, 26.41
STAGE2_PLACEMENT = bd.Pos(0, 0, -24.0) * bd.Rot(0, 0, 43.46 - PIN_ANGLE)


@step(out="../../STEP/gearbox/carrier_plate.step")
def carrier_plate():
    part = plate_factory(Z_BOTTOM, PIN_ANGLE, FIT)
    part.label = "carrier_plate"
    return part


if __name__ == "__main__":
    carrier_plate()
