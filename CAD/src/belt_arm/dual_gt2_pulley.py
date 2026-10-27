"""Dual GT2 pulley (Fusion "Dual GT2 pulley"), arm frame at (75, 40) (design.md §4).

One body: an 80T flanged pulley (z 10.7..20.7, band 12.2..19.2) driven by
the motor, with a 20T flanged pulley on top (z 20.7..30.7, band 22.2..29.2)
driving the GT2-80 output. Ø8 bore through for two 6x8x10 bushings on the
6 mm dowel. Groove 0 of both bands on +X, as in Fusion.
"""
from cadgen import build123d as bd
from cadgen import step

from belt_arm.common import DUAL_X, DUAL_Y, zcyl
from lib import gt2, params

Z_80T, Z_20T, Z_TOP = 10.7, 20.7, 30.7
BORE = 8.0


def dual_gt2_pulley_body():
    body = bd.Pos(DUAL_X, DUAL_Y, Z_80T) * gt2.flanged_pulley(params.GT2_TEETH_ARM_DRIVEN)
    body += bd.Pos(DUAL_X, DUAL_Y, Z_20T) * gt2.flanged_pulley(params.GT2_TEETH_MOTOR)
    return body - zcyl(BORE, DUAL_X, DUAL_Y, Z_80T, Z_TOP)


@step(out="../../STEP/belt_arm/dual_gt2_pulley.step")
def dual_gt2_pulley():
    part = dual_gt2_pulley_body()
    part.label = "dual_gt2_pulley"
    return part


if __name__ == "__main__":
    dual_gt2_pulley()
