"""Base plate (Fusion "Base"), arm frame (design.md §4).

7 mm plate z 0..7 with the R40 distal end. NEMA17 underneath at (-10, 40):
Ø30 pilot hole and 4 x M3 on the 31 mm square (Ø3.3, Ø6 x 3 counterbore
from the top). Ø37 6805 seat through at J3. Ø10 x 3.7 boss on top at the
dual pulley with a Ø6.1 dowel socket (floor at the plate top). Idler slots
y 20..65 at both idler x: Ø10 x 3 from below, Ø5.3 above. 7 x M3 to the
Wall (Ø6 x 3 counterbore from below, Ø3.3) and two Ø4.2 x 10 proximal
inserts at z = 3.5.
"""
from cadgen import build123d as bd
from cadgen import step

from belt_arm.common import (DOWEL_BOSS_D, DOWEL_HOLE, DUAL_X, DUAL_Y, IDLER_SLOT_Y, IDLER_XS, J3_X, J3_Y,
                             M3_CBORE, M3_CLEAR, M3_INSERT, MOTOR_X, MOTOR_Y, PROXIMAL_INSERT_DEPTH,
                             PROXIMAL_INSERT_Y, WALL_SCREW_XY, X_PROXIMAL, Z_BASE_TOP, plate, xcyl, yslot, zcyl)
from lib import params

BOSS_TOP = 10.7
MOTOR_PILOT_D = 30.0
MOTOR_SCREW_CBORE_Z = 4.0
IDLER_CBORE_D, IDLER_CBORE_Z = 10.0, 3.0
IDLER_SLOT_W = 5.3
WALL_CBORE_Z = 3.0
INSERT_Z = 3.5


def base_body():
    body = plate(0, Z_BASE_TOP)
    body += zcyl(DOWEL_BOSS_D, DUAL_X, DUAL_Y, Z_BASE_TOP, BOSS_TOP)
    body -= zcyl(DOWEL_HOLE, DUAL_X, DUAL_Y, Z_BASE_TOP, BOSS_TOP)
    body -= zcyl(params.BEARING_6805_SEAT_D, J3_X, J3_Y, 0, Z_BASE_TOP)

    body -= zcyl(MOTOR_PILOT_D, MOTOR_X, MOTOR_Y, 0, Z_BASE_TOP)
    half = params.NEMA17_BOLT_SPACING / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = MOTOR_X + sx * half, MOTOR_Y + sy * half
            body -= zcyl(M3_CLEAR, x, y, 0, MOTOR_SCREW_CBORE_Z)
            body -= zcyl(M3_CBORE, x, y, MOTOR_SCREW_CBORE_Z, Z_BASE_TOP)

    for x in IDLER_XS:
        body -= yslot(x, *IDLER_SLOT_Y, IDLER_CBORE_D, 0, IDLER_CBORE_Z)
        body -= yslot(x, *IDLER_SLOT_Y, IDLER_SLOT_W, IDLER_CBORE_Z, Z_BASE_TOP)

    for x, y in WALL_SCREW_XY:
        body -= zcyl(M3_CBORE, x, y, 0, WALL_CBORE_Z)
        body -= zcyl(M3_CLEAR, x, y, WALL_CBORE_Z, Z_BASE_TOP)
    for y in PROXIMAL_INSERT_Y:
        body -= xcyl(M3_INSERT, y, INSERT_Z, X_PROXIMAL, X_PROXIMAL + PROXIMAL_INSERT_DEPTH)
    return body


@step(out="../../STEP/belt_arm/base.step")
def base():
    part = base_body()
    part.label = "base"
    return part


if __name__ == "__main__":
    base()
