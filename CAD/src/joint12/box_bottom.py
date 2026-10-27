"""Box bottom (Fusion "Box bottom v5"), base frame z -30..0 (design.md §2).

180 x 150 x 30 tray: 15 mm walls, 5 mm floor, open 150 x 120 pocket and a
50 mm window through the +X wall (J1 belt / motor pulley at the far end of
the slot). Ø22 x 7 seat for the 608 on a Ø27 ring on the floor. 7 x M5
heat-set insert holes Ø6.4 x 10.5 in the top face (IF-2).
"""
from cadgen import step

from joint12.common import J1_X, J1_Y, box, zcyl
from lib import params
from lib.tolerances import hole, profile

FIT = profile("box_bottom")

Z_BOTTOM, Z_FLOOR, Z_TOP = -30.0, -25.0, 0.0
WALL = 15.0
WINDOW_Y = (50.0, 100.0)
SEAT_Z1 = -18.0
INSERT_DEPTH = 10.5


def box_bottom_body():
    body = box(0, params.BOX_X, 0, params.BOX_Y, Z_BOTTOM, Z_TOP)
    body -= box(WALL, params.BOX_X - WALL, WALL, params.BOX_Y - WALL, Z_FLOOR, Z_TOP)
    body -= box(params.BOX_X - WALL, params.BOX_X, *WINDOW_Y, Z_FLOOR, Z_TOP)
    body += zcyl(27.0, J1_X, J1_Y, Z_FLOOR, SEAT_Z1) - zcyl(hole(params.BEARING_608_SEAT_D, FIT.press), J1_X, J1_Y, Z_FLOOR, SEAT_Z1)
    for x, y in params.BOX_M5_XY:
        body -= zcyl(FIT.insert_m5, x, y, Z_TOP - INSERT_DEPTH, Z_TOP)
    return body


@step(out="../../STEP/joint12/box_bottom.step")
def box_bottom():
    part = box_bottom_body()
    part.label = "box_bottom"
    return part


if __name__ == "__main__":
    box_bottom()
