"""J3 Pin (Fusion "Pin", x2), arm frame as Pin:1 (design.md §4).

Ø30 x 2 flange (z -4.8..-2.8, under the Base), Ø25 x 10 journal in the
Base 6805 (z -2.8..7.2) and a 21.48 AF x 15 hex (circumradius 12.4, corners
on ±Y like the Output block socket, z 7.2..22.2) into the Output block and
the GT2-80 output. Fusion has the hex corners on ±X, 30 deg off the socket
(I-6, fixed). Pin:2 is the same part at common.PIN_2_PLACEMENT.
"""
from cadgen import build123d as bd
from cadgen import step

from belt_arm.common import J3_X, J3_Y, zcyl
from lib import params
from lib.tolerances import ACTIVE as FIT, shaft

Z_FLANGE, Z_JOURNAL, Z_HEX, Z_END = -4.8, -2.8, 7.2, 22.2
FLANGE_D = 30.0


def pin_body():
    body = zcyl(FLANGE_D, J3_X, J3_Y, Z_FLANGE, Z_JOURNAL)
    body += zcyl(shaft(params.OUTPUT_SHAFT_D, FIT.press), J3_X, J3_Y, Z_JOURNAL, Z_HEX)
    body += bd.Pos(J3_X, J3_Y, Z_HEX) * bd.extrude(bd.RegularPolygon(params.PIN_HEX_R, 6, rotation=90), Z_END - Z_HEX)
    return body


@step(out="../../STEP/belt_arm/pin.step")
def pin():
    part = pin_body()
    part.label = "pin"
    return part


if __name__ == "__main__":
    pin()
