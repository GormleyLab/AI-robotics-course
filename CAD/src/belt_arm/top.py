"""Top plate (Fusion "Top"), arm frame (design.md §4).

7 mm plate z 37..44 with the R40 distal end. Ø37 6805 seat through at
J3. Ø10 x 1.7 boss underneath at the dual pulley with a Ø6.1 dowel socket
(floor at the plate underside). Idler slots y 20..65 at both idler x:
Ø5.3 x 2 from below, then an 8 mm nut slot (end centres y 19..66) above:
the M5 nut (8 AF) slides in it flats-first. The nut slot runs 1 mm past the
Ø5.3 slot at each end, so the nut's corners (4.62 from its centre) clear the
R4 ends with the screw at either end (I-4 fix; Fusion: y 20..65, nut
0.62 mm short). 7 x M3 to the Wall (Ø3.3, Ø6 x 3
counterbore from the top, run out through the nearest edge as an open
U-slot, I-21) and two Ø4.2 x 10 proximal inserts at z = 40.5.
No motor holes.
"""
from cadgen import step

from belt_arm.common import (DOWEL_BOSS_D, DOWEL_HOLE_D, DUAL_X, DUAL_Y, IDLER_SLOT_Y, IDLER_XS, J3_X, J3_Y,
                             PROXIMAL_INSERT_DEPTH, PROXIMAL_INSERT_Y,
                             WALL_SCREW_XY, X_PROXIMAL, Z_TOP_TOP, Z_WALL_TOP, edge_runout, plate, xcyl, yslot,
                             zcyl)
from lib import params
from lib.tolerances import hole, profile

FIT = profile("top")

BOSS_BOTTOM = 35.3
IDLER_SLOT_W, IDLER_SLOT_Z = hole(5.3, FIT.clearance), 39.0
IDLER_CBORE_W = hole(8.0, FIT.slip)   # M5 nut 8 AF: line-to-line in Fusion, FIT.slip lets it slide (I-11)
IDLER_NUT_SLOT_Y = (IDLER_SLOT_Y[0] - 1.0, IDLER_SLOT_Y[1] + 1.0)   # I-4 fixed: Fusion = IDLER_SLOT_Y
WALL_CBORE_Z = 41.0
INSERT_Z = 40.5


def top_body():
    body = plate(Z_WALL_TOP, Z_TOP_TOP)
    body += zcyl(DOWEL_BOSS_D, DUAL_X, DUAL_Y, BOSS_BOTTOM, Z_WALL_TOP)
    body -= zcyl(hole(DOWEL_HOLE_D, FIT.slip), DUAL_X, DUAL_Y, BOSS_BOTTOM, Z_WALL_TOP)
    body -= zcyl(hole(params.BEARING_6805_SEAT_D, FIT.press), J3_X, J3_Y, Z_WALL_TOP, Z_TOP_TOP)
    for x in IDLER_XS:
        body -= yslot(x, *IDLER_SLOT_Y, IDLER_SLOT_W, Z_WALL_TOP, IDLER_SLOT_Z)
        body -= yslot(x, *IDLER_NUT_SLOT_Y, IDLER_CBORE_W, IDLER_SLOT_Z, Z_TOP_TOP)
    for x, y in WALL_SCREW_XY:
        body -= zcyl(FIT.m3_clear, x, y, Z_WALL_TOP, WALL_CBORE_Z)
        body -= edge_runout(x, y, WALL_CBORE_Z, Z_TOP_TOP)
    for y in PROXIMAL_INSERT_Y:
        body -= xcyl(FIT.insert_m3, y, INSERT_Z, X_PROXIMAL, X_PROXIMAL + PROXIMAL_INSERT_DEPTH)
    return body


@step(out="../../STEP/belt_arm/top.step")
def top():
    part = top_body()
    part.label = "top"
    return part


if __name__ == "__main__":
    top()
