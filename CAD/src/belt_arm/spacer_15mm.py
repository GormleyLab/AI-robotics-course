"""Idler spacer 15 mm (Fusion "Spacer 15mm", x2), arm frame (design.md §4).

Ø10 / Ø6.3 x 15 on the idler dowel, modelled as Spacer 15mm:1 at idler 1
(27.65, 20), z 22..37; the second copy is the same part at idler 2.
"""
from cadgen import step

from belt_arm.common import IDLER_SLOT_Y, IDLER_XS, zcyl

OD, ID, H = 10.0, 6.3, 15.0
Z0 = 22.0


def spacer_15mm_body():
    x, y = IDLER_XS[0], IDLER_SLOT_Y[0]
    return zcyl(OD, x, y, Z0, Z0 + H) - zcyl(ID, x, y, Z0, Z0 + H)


@step(out="../../STEP/belt_arm/spacer_15mm.step")
def spacer_15mm():
    part = spacer_15mm_body()
    part.label = "spacer_15mm"
    return part


if __name__ == "__main__":
    spacer_15mm()
