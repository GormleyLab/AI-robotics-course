"""Joint 1 and 2 assembly: base, J1 waist, hinge, J2 gearbox and coupling, base frame.

Printed parts are modelled in place; purchased parts and the gearbox use the
Fusion placements, so I-1 (gearbox 0.5 mm below the hinge J2 axis), I-2
(output hex rotated 43.5 deg in its socket) and I-12 (thrust bearings on the
Ø35 shaft) are reproduced.

The J1 motor and its 20T pulley are not in Fusion (I-8) and are added here
(not gated). Assumed placement: NEMA17 mounting face on the box top (z = 12),
shaft down, at mid-slot (x = 150, y = 75; 75 mm centre distance), square to
the box so its screws sit in the M3 slots; the 20T pulley's toothed band
(z 1..9 of the vendor part) centred on the 160T band (z = -8).
"""
from cadgen import build123d as bd
from cadgen import step

from gearbox.planetary_gearbox import planetary_gearbox
from joint12.box_bottom import box_bottom
from joint12.box_top import box_top
from joint12.common import GEARBOX_PLACEMENT, J1_X, J1_Y, J2_Y, J2_Z, Z_TO_X
from joint12.coupling_shaft import coupling_shaft
from joint12.gt2_pulley_160t import gt2_pulley_160t
from joint12.hinge import hinge
from lib import params
from purchased.bearing_608 import bearing_608
from purchased.bearing_6805 import bearing_6805
from purchased.bearing_6807 import bearing_6807
from purchased.gt2_pulley_20t import gt2_pulley_20t
from purchased.nema17 import nema17
from purchased.thrust_bearing_51108 import thrust_bearing_51108

J1_MOTOR_X = sum(params.J1_MOTOR_SLOT_X) / 2   # 150, mid-slot
J1_MOTOR_FACE_Z = params.BOX_TOP_H             # 12
J1_PULLEY_Z = -13.0                            # 20T band z -12..-4, centred on the 160T band


def _named(shape, label):
    shape.label = label
    return shape


def joint12_parts():
    """Labelled parts of the base, in the base frame (also used by the full arm)."""
    return [
        _named(box_bottom(), "box_bottom"),
        _named(box_top(), "box_top"),
        _named(hinge(), "hinge"),
        _named(gt2_pulley_160t(), "gt2_pulley_160t"),
        _named(coupling_shaft(), "coupling_shaft"),
        _named(bd.Pos(J1_X, J1_Y, 12.0) * thrust_bearing_51108(), "thrust_bearing:upper"),
        _named(bd.Pos(J1_X, J1_Y, -8.0) * thrust_bearing_51108(), "thrust_bearing:lower"),
        _named(bd.Pos(J1_X, J1_Y, 5.0) * bearing_6807(), "bearing_6807"),
        _named(bd.Pos(J1_X, J1_Y, -25.0) * bearing_608(), "bearing_608"),
        _named(bd.Pos(39.0, J2_Y, J2_Z) * Z_TO_X * bearing_6805(), "bearing_6805:left_cheek"),
        _named(bd.Pos(102.0, J2_Y, J2_Z) * Z_TO_X * bearing_6805(), "bearing_6805:right_cheek"),
        _named(GEARBOX_PLACEMENT * planetary_gearbox(), "planetary_gearbox"),
        _named(bd.Pos(J1_MOTOR_X, params.J1_MOTOR_SLOT_Y, J1_MOTOR_FACE_Z) * bd.Rot(180, 0, 0) * nema17(),
               "nema17:j1"),
        _named(bd.Pos(J1_MOTOR_X, params.J1_MOTOR_SLOT_Y, J1_PULLEY_Z) * gt2_pulley_20t(), "gt2_pulley_20t:j1"),
    ]


@step(out="../../STEP/joint12/joint_1_and_2.step")
def joint_1_and_2():
    return bd.Compound(children=joint12_parts(), label="joint_1_and_2")


if __name__ == "__main__":
    joint_1_and_2()
