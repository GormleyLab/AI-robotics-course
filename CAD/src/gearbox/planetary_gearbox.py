"""Two-stage 16:1 planetary gearbox assembly (joint 2), gearbox frame.

Placements reproduce the Fusion gearbox, including the planets' tooth
phases, so the Fusion meshing overlaps (issue I-7) are reproduced too.
``gearbox.common.TO_FUSION`` maps this frame onto the Fusion gearbox frame.
"""
from cadgen import build123d as bd
from cadgen import step

from gearbox.back_cover import back_cover
from gearbox.carrier_plate import STAGE2_PLACEMENT, carrier_plate
from gearbox.carrier_stage1_output import carrier_stage1_output
from gearbox.carrier_stage2_output import carrier_stage2_output
from gearbox.common import polar
from gearbox.front_cover import front_cover
from gearbox.input_shaft import input_shaft
from gearbox.nema17_mount import nema17_mount
from gearbox.planet_gear import planet_gear
from gearbox.ring_gear import ring_gear
from lib import params
from purchased.bearing_6801 import bearing_6801
from purchased.bearing_6803 import bearing_6803
from purchased.bearing_6805 import bearing_6805
from purchased.bushing_6x8x10 import bushing_6x8x10
from purchased.nema17 import nema17
from purchased.planet_pin_6x22 import planet_pin_6x22
from purchased.washer_6 import washer_6

R = params.PLANET_CENTRE_R
# Per stage: planet angles about the axis, planet z range bottom, tooth phase
# at the planet's bottom face (absolute, measured from Fusion), pin bottom,
# bushing bottom and the two washer bottoms.
STAGES = {
    1: dict(angles=(26.41, 146.41, -93.59), planet_z=-10.2, phase=4.830,
            pin_z=-17.0, bushing_z=-10.7, washer_z=(-12.0, -0.3)),
    2: dict(angles=(43.46, 163.46, -76.54), planet_z=-34.2, phase=3.530,
            pin_z=-41.0, bushing_z=-34.7, washer_z=(-36.0, -24.3)),
}
MOTOR_FACE_Z = 24.0


def _named(shape, label):
    shape.label = label
    return shape


@step(out="../../STEP/gearbox/planetary_gearbox.step")
def planetary_gearbox():
    parts = [
        _named(ring_gear(), "ring_gear"),
        _named(back_cover(), "back_cover"),
        _named(front_cover(), "front_cover"),
        _named(nema17_mount(), "nema17_mount"),
        _named(input_shaft(), "input_shaft"),
        _named(carrier_plate(), "carrier_plate:stage1"),
        _named(carrier_stage1_output(), "carrier_stage1_output"),
        _named(STAGE2_PLACEMENT * carrier_plate(), "carrier_plate:stage2"),
        _named(carrier_stage2_output(), "carrier_stage2_output"),
        _named(bd.Pos(0, 0, 7.0) * bearing_6803(), "bearing_6803:input"),
        _named(bd.Pos(0, 0, -17.0) * bearing_6801(), "bearing_6801:stage1"),
        _named(bd.Pos(0, 0, -41.0) * bearing_6801(), "bearing_6801:stage2"),
        _named(bd.Pos(0, 0, -52.0) * bearing_6805(), "bearing_6805:output"),
        _named(bd.Pos(0, 0, MOTOR_FACE_Z) * bd.Rot(180, 0, 0) * nema17(), "nema17"),
    ]
    for stage, cfg in STAGES.items():
        for i, a in enumerate(cfg["angles"], start=1):
            centre = polar(R, a).position
            tag = f"s{stage}p{i}"
            parts.append(_named(bd.Pos(centre.X, centre.Y, cfg["planet_z"]) * bd.Rot(0, 0, cfg["phase"]) * planet_gear(),
                                f"planet_gear:{tag}"))
            parts.append(_named(polar(R, a, cfg["pin_z"]) * planet_pin_6x22(), f"planet_pin:{tag}"))
            parts.append(_named(polar(R, a, cfg["bushing_z"]) * bushing_6x8x10(), f"bushing:{tag}"))
            for j, wz in enumerate(cfg["washer_z"], start=1):
                parts.append(_named(polar(R, a, wz) * washer_6(), f"washer:{tag}w{j}"))
    return bd.Compound(children=parts, label="planetary_gearbox")


if __name__ == "__main__":
    planetary_gearbox()
