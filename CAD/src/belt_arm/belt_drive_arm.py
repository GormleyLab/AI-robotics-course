"""Belt drive arm segment assembly (J3 elbow), arm frame.

Printed parts are modelled in place; purchased parts use the Fusion
placements. I-5 is fixed: the idler axles are M5 x 40 button head screws
(head in the Base's Ø10 slot, seat at z 3) with an M5 nut in the Top's 8 mm
slot (z 39..43), as built; Fusion had 6 x 30 dowels in the 5 mm idler bores.
I-4 is fixed: an M3 x 35 jack screw through the y = 0 Wall rail pushes each
idler's 15 mm spacer to set belt tension, shown backed off to the slack end.
I-6 is fixed: the GT2-80 output and both Pin hexes sit on J3, in line with
the Output block socket. I-15 is fixed: every band on a belt is in line with
it (the motor 20T slides down its shaft; the dual pulley changed).

The segment's motor is the full-size NEMA17; the full arm builds segment 2
with the pancake instead, as on the built arm (I-18).

Belts are not in Fusion (I-8) and are added here as envelopes (not gated):
the GT2 pitch line over the pitch circles from lib/gt2.py, offset to the
land (pulley OD) and the belt back, teeth left out, 6 mm wide and centred on each stage's driven
80T band. An idler is wrapped (on the belt back) only if it reaches the
strand at its Fusion position, at the y = 20 slot end. Both stages are now
the same 85 mm 20T -> 80T layout, so both idlers deflect their belts 1.8 mm.
(With Fusion's off-axis output pulley, I-6, the stage-2 idler missed its belt
by 2.0 mm.)
"""
import build123d as bd
from cadgen import step

from belt_arm.base import base
from belt_arm.common import DUAL_X, DUAL_Y, IDLER_SLOT_Y, IDLER_XS, J3_X, J3_Y, JACK_SCREW_LEN, JACK_SCREW_XZ, \
    MOTOR_X, MOTOR_Y, PIN_2_PLACEMENT, SPACER_R, Z_BASE_TOP
from belt_arm.dual_gt2_pulley import dual_gt2_pulley
from belt_arm.gt2_80_output import gt2_80_output
from belt_arm.output_block import output_block
from belt_arm.pin import pin
from belt_arm.spacer_5mm import spacer_5mm
from belt_arm.spacer_15mm import spacer_15mm
from belt_arm.top import top
from belt_arm.wall import wall
from lib import gt2, params
from purchased.bearing_6805 import bearing_6805
from purchased.bushing_6x8x10 import bushing_6x8x10
from purchased.button_head_m5x40 import button_head_m5x40
from purchased.dowel_pin_6x30 import dowel_pin_6x30
from purchased.gt2_idler_20t import gt2_idler_20t
from purchased.gt2_pulley_20t import gt2_pulley_20t
from purchased.hex_nut_m5 import hex_nut_m5
from purchased.nema17 import nema17
from purchased.nema17_pancake import nema17_pancake
from purchased.socket_head_m3x35 import socket_head_m3x35

# Belt planes (I-15 fixed): stage 1 centred at z 17.0 on the idler-1 band, stage 2 at
# 26.7 on the GT2-80 output band (idler 2 is 0.3 high, inside the output's 0.5 slot play).
MOTOR_PULLEY_Z = 12.0                  # vendor 20T bottom face, band 13.5..20.5 (Fusion 13.7: band 15.2..22.2)
IDLER_Z = (12.0, 22.0)                 # idler bottom faces (bands 13.5..20.5 / 23.5..30.5)
IDLER_2_SHIFT = bd.Pos(IDLER_XS[1] - IDLER_XS[0], 0, 0)
BELT_Z = (14.0, 23.7)                  # belt bottoms: centred on the 80T bands 13.5..20.5 / 23.2..30.2
BUSHING_Z = (10.7, 21.7)               # bushing bottoms in the dual pulley bore 10.7..31.7 (Fusion 10.7, 20.7)
IDLER_SCREW_Z = 3.0                    # button head seat: top of the Base's Ø10 x 3 slot (I-5)
IDLER_NUT_Z = 39.0                     # nut seat: floor of the Top's 8 mm slot (I-5)
# Jack screws (I-4) touch the 15 mm spacers with the idlers at the slack end (y = 20):
# head seat 20 mm out from the rail. A 280 mm loop needs y ~33.8; the screw reaches y 40.
JACK_SCREW_SEAT_Y = IDLER_SLOT_Y[0] - SPACER_R - JACK_SCREW_LEN

R_PITCH_20 = gt2.pitch_diameter(params.GT2_TEETH_MOTOR) / 2
R_PITCH_80 = gt2.pitch_diameter(params.GT2_TEETH_ARM_DRIVEN) / 2
R_IDLER_BACK = -(gt2.outside_diameter(params.GT2_TEETH_MOTOR) / 2 + gt2.BELT_BACK)


def stage_circles(driver_xy, driven_xy, idler_xy):
    """Belt circles in CCW loop order: driver, idler (if it reaches the
    lower strand), driven."""
    a, b = (*driver_xy, R_PITCH_20), (*driven_xy, R_PITCH_80)
    idler = (*idler_xy, R_IDLER_BACK)
    return [a, idler, b] if gt2.idler_depth(a, b, idler) > 0 else [a, b]


STAGE_1 = stage_circles((MOTOR_X, MOTOR_Y), (DUAL_X, DUAL_Y), (IDLER_XS[0], IDLER_SLOT_Y[0]))
STAGE_2 = stage_circles((DUAL_X, DUAL_Y), (J3_X, J3_Y), (IDLER_XS[1], IDLER_SLOT_Y[0]))


def _named(shape, label):
    shape.label = label
    return shape


def segment_parts(pancake=False):
    """Labelled parts of one segment, in the arm frame (also used by the full arm).

    ``pancake`` drives the segment with the 20 mm pancake NEMA17 (segment 2, J4; I-18).
    """
    idler_1 = (IDLER_XS[0], IDLER_SLOT_Y[0])
    idler_2 = (IDLER_XS[1], IDLER_SLOT_Y[0])
    return [
        _named(base().shape, "base"),
        _named(wall().shape, "wall"),
        _named(top().shape, "top"),
        _named(dual_gt2_pulley().shape, "dual_gt2_pulley"),
        _named(gt2_80_output().shape, "gt2_80_output"),
        _named(pin().shape, "pin:base"),
        _named(PIN_2_PLACEMENT * pin().shape, "pin:top"),
        _named(output_block().shape, "output_block"),
        _named(spacer_5mm().shape, "spacer_5mm:idler_1"),
        _named(spacer_15mm().shape, "spacer_15mm:idler_1"),
        _named(IDLER_2_SHIFT * bd.Pos(0, 0, 25.0) * spacer_5mm().shape, "spacer_5mm:idler_2"),
        _named(IDLER_2_SHIFT * bd.Pos(0, 0, -15.0) * spacer_15mm().shape, "spacer_15mm:idler_2"),
        _named(bd.Pos(MOTOR_X, MOTOR_Y, 0) * (nema17_pancake().shape if pancake else nema17().shape),
               "nema17_pancake:j3" if pancake else "nema17:j3"),
        _named(bd.Pos(MOTOR_X, MOTOR_Y, MOTOR_PULLEY_Z) * gt2_pulley_20t().shape, "gt2_pulley_20t:j3"),
        _named(bd.Pos(DUAL_X, DUAL_Y, Z_BASE_TOP) * dowel_pin_6x30().shape, "dowel_pin:dual_pulley"),
        _named(bd.Pos(*idler_1, IDLER_SCREW_Z) * button_head_m5x40().shape, "button_head_m5x40:idler_1"),
        _named(bd.Pos(*idler_2, IDLER_SCREW_Z) * button_head_m5x40().shape, "button_head_m5x40:idler_2"),
        _named(bd.Pos(*idler_1, IDLER_NUT_Z) * hex_nut_m5().shape, "hex_nut_m5:idler_1"),
        _named(bd.Pos(*idler_2, IDLER_NUT_Z) * hex_nut_m5().shape, "hex_nut_m5:idler_2"),
        _named(bd.Pos(DUAL_X, DUAL_Y, BUSHING_Z[0]) * bushing_6x8x10().shape, "bushing:lower"),
        _named(bd.Pos(DUAL_X, DUAL_Y, BUSHING_Z[1]) * bushing_6x8x10().shape, "bushing:upper"),
        *(_named(bd.Pos(x, JACK_SCREW_SEAT_Y, z) * bd.Rot(-90, 0, 0) * socket_head_m3x35().shape,
                 f"socket_head_m3x35:jack_{i}") for i, (x, z) in enumerate(JACK_SCREW_XZ, 1)),
        _named(bd.Pos(*idler_1, IDLER_Z[0]) * gt2_idler_20t().shape, "gt2_idler_20t:1"),
        _named(bd.Pos(*idler_2, IDLER_Z[1]) * gt2_idler_20t().shape, "gt2_idler_20t:2"),
        _named(bd.Pos(J3_X, J3_Y, 0.2) * bearing_6805().shape, "bearing_6805:base"),
        _named(bd.Pos(J3_X, J3_Y, 37.2) * bearing_6805().shape, "bearing_6805:top"),
        _named(bd.Pos(0, 0, BELT_Z[0]) * gt2.belt_envelope(STAGE_1), "belt:stage_1"),
        _named(bd.Pos(0, 0, BELT_Z[1]) * gt2.belt_envelope(STAGE_2), "belt:stage_2"),
    ]


@step(out="../../STEP/belt_arm/belt_drive_arm.step")
def belt_drive_arm():
    return bd.Compound(children=segment_parts(), label="belt_drive_arm")


if __name__ == "__main__":
    belt_drive_arm()
