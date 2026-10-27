"""GT2 80T J3 output pulley (Fusion "GT2-80 output"), arm frame (design.md §4).

80T flanged pulley, z 21.7..31.7 (band 23.2..30.2), with a 21.65 AF hex
socket through (circumradius 12.5, corners on ±X), the same socket as the
coupling shaft. Centred on J3 with the hex corners on ±Y, in line with the
Pins and the Output block socket; groove 0 on +Y. Fusion has the same
pulley turned 90 deg (corners on ±X) and centred 9.08 mm off J3 at
(165.59, 47.15) (I-6, fixed).
"""
from cadgen import build123d as bd
from cadgen import step

from belt_arm.common import J3_X, J3_Y
from lib import gt2, params

Z0 = 21.7
H = 2 * gt2.FLANGE_H + 7.0


def gt2_80_output_body():
    body = gt2.flanged_pulley(params.GT2_TEETH_ARM_DRIVEN)
    body -= bd.extrude(bd.RegularPolygon(params.OUTPUT_HEX_SOCKET_R, 6), H)
    return bd.Pos(J3_X, J3_Y, Z0) * bd.Rot(0, 0, 90) * body


@step(out="../../STEP/belt_arm/gt2_80_output.step")
def gt2_80_output():
    part = gt2_80_output_body()
    part.label = "gt2_80_output"
    return part


if __name__ == "__main__":
    gt2_80_output()
