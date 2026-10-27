"""Dual GT2 pulley (Fusion "Dual GT2 pulley"), arm frame at (75, 40) (design.md §4).

One body: a Ø12 hub (z 10.7..12, on the Base dowel boss), an 80T flanged
pulley (z 12..22, band 13.5..20.5) driven by the motor, and a 20T flanged
pulley on top (z 21.7..31.7, band 23.2..30.2; its lower flange merges 0.3 into
the 80T's upper flange) driving the GT2-80 output. Ø8 bore through for two
6x8x10 bushings on the 6 mm dowel. Groove 0 of both bands on +X, as in Fusion.

I-15 fix (Fusion: no hub, 80T band 12.2..19.2, 20T band 22.2..29.2). The 80T
band now lines up with the stage-1 idler and the 20T band with the GT2-80
output band.
"""
from cadgen import build123d as bd
from cadgen import step

from belt_arm.common import DUAL_X, DUAL_Y, zcyl
from lib import gt2, params
from lib.tolerances import hole, profile

FIT = profile("dual_gt2_pulley")

Z_BOTTOM = 10.7                    # Base dowel boss top
Z_80T, Z_20T, Z_TOP = 12.0, 21.7, 31.7   # I-15 fixed: Fusion 10.7, 20.7, 30.7
HUB_D = 12.0
BORE = hole(8.0, FIT.press)            # two 6 x 8 x 10 bushings


def dual_gt2_pulley_body():
    body = zcyl(HUB_D, DUAL_X, DUAL_Y, Z_BOTTOM, Z_80T)
    body += bd.Pos(DUAL_X, DUAL_Y, Z_80T) * gt2.flanged_pulley(params.GT2_TEETH_ARM_DRIVEN)
    body += bd.Pos(DUAL_X, DUAL_Y, Z_20T) * gt2.flanged_pulley(params.GT2_TEETH_MOTOR)
    return body - zcyl(BORE, DUAL_X, DUAL_Y, Z_BOTTOM, Z_TOP)


@step(out="../../STEP/belt_arm/dual_gt2_pulley.step")
def dual_gt2_pulley():
    part = dual_gt2_pulley_body()
    part.label = "dual_gt2_pulley"
    return part


if __name__ == "__main__":
    dual_gt2_pulley()
