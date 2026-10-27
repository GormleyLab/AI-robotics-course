"""Hinge (Fusion "Hinge v8"), base frame (design.md §2).

U-bracket that turns on J1 and carries J2. A 20 mm floor (z 15..35) with
R5 inner fillets joins two 7 mm cheeks, each a rectangle with an R42.5
rounded top: the left (gearbox) cheek is rounded about z = 70.5, the right
about z = 62.5 (I-13). Both cheeks have Ø37 6805 seats on J2 at z = 70.5
(IF-4; the gearbox sits at 70.0, I-1). Underneath: a Ø35 J1 shaft down to
z = -8 and a Ø61 x 10 upper-thrust pocket (IF-1). 4 x M5 Ø5.3 at r = 10
with Ø12 counterbores from the floor take the bolts into the 160T pulley.
The left cheek has 5 of the 6 front-cover M3 holes, the bottom one is
missing (I-10).
"""
from cadgen import build123d as bd
from cadgen import step

from joint12.common import (J1_X, J1_Y, J2_Y, J2_Z, M3_CBORE, M3_CLEAR, M5_CLEAR, box, on_j2_circle,
                            xcyl, zcyl)
from lib import params

X0, X1 = 39.0, 109.0
Y0, Y1 = J2_Y - 42.5, J2_Y + 42.5
CHEEK = 7.0
Z_FLOOR_BOTTOM, Z_FLOOR_TOP = 15.0, 35.0
CHEEK_TOP_R = 42.5
LEFT_ROUND_Z, RIGHT_ROUND_Z = J2_Z, 62.5
FILLET_R = 5.0
SHAFT_Z0 = -8.0
POCKET_DEPTH = 10.0
PULLEY_BOLT_R = 10.0
CBORE_D, CBORE_Z0 = 12.0, 23.0
COVER_BOLT_ANGLES = (-30.0, 30.0, 90.0, 150.0, 210.0)   # 270 missing (I-10)
COVER_CBORE_DEPTH = 2.0


def _cheek(x0: float, x1: float, round_z: float) -> bd.Part:
    return box(x0, x1, Y0, Y1, Z_FLOOR_BOTTOM, round_z) + xcyl(2 * CHEEK_TOP_R, J2_Y, round_z, x0, x1)


def _inner_fillet(x_wall: float, toward: float) -> bd.Part:
    """R5 fillet along Y between the floor top and a cheek's inner face."""
    xa, xb = sorted((x_wall, x_wall + toward * FILLET_R))
    block = box(xa, xb, Y0, Y1, Z_FLOOR_TOP, Z_FLOOR_TOP + FILLET_R)
    centre_x = x_wall + toward * FILLET_R
    cut = bd.Pos(centre_x, Y0, Z_FLOOR_TOP + FILLET_R) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        FILLET_R, Y1 - Y0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return block - cut


def hinge_body():
    body = box(X0, X1, Y0, Y1, Z_FLOOR_BOTTOM, Z_FLOOR_TOP)
    body += _cheek(X0, X0 + CHEEK, LEFT_ROUND_Z) + _cheek(X1 - CHEEK, X1, RIGHT_ROUND_Z)
    body += _inner_fillet(X0 + CHEEK, +1) + _inner_fillet(X1 - CHEEK, -1)

    body -= zcyl(params.THRUST_RECESS_HINGE_D, J1_X, J1_Y, Z_FLOOR_BOTTOM, Z_FLOOR_BOTTOM + POCKET_DEPTH)
    body += zcyl(params.J1_SHAFT_D, J1_X, J1_Y, SHAFT_Z0, Z_FLOOR_BOTTOM + POCKET_DEPTH)
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        x, y = J1_X + dx * PULLEY_BOLT_R, J1_Y + dy * PULLEY_BOLT_R
        body -= zcyl(M5_CLEAR, x, y, SHAFT_Z0, CBORE_Z0)
        body -= zcyl(CBORE_D, x, y, CBORE_Z0, Z_FLOOR_TOP)

    body -= xcyl(params.BEARING_6805_SEAT_D, J2_Y, J2_Z, X0, X0 + CHEEK)
    body -= xcyl(params.BEARING_6805_SEAT_D, J2_Y, J2_Z, X1 - CHEEK, X1)
    for a in COVER_BOLT_ANGLES:
        y, z = on_j2_circle(params.GEARBOX_BOLT_CIRCLE_R, a)
        body -= xcyl(M3_CLEAR, y, z, X0, X0 + CHEEK - COVER_CBORE_DEPTH)
        body -= xcyl(M3_CBORE, y, z, X0 + CHEEK - COVER_CBORE_DEPTH, X0 + CHEEK)
    return body


@step(out="../../STEP/joint12/hinge.step")
def hinge():
    part = hinge_body()
    part.label = "hinge"
    return part


if __name__ == "__main__":
    hinge()
