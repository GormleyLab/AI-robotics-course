"""Box top (Fusion "Box top v6"), base frame z 0..12 (design.md §2).

180 x 150 x 12 plate. On J1: Ø60 x 5 recess underneath (lower thrust
bearing) stepping to a Ø47 x 7 seat on top (6807), IF-1. J1 motor slot 25
wide with centres x 140..160, and two 3.3 wide M3 slots for the NEMA17's
31 mm pattern, IF-3. 7 x M5 clearance holes over the box-bottom inserts.
"""
from cadgen import step

from joint12.common import J1_X, J1_Y, M3_CLEAR, M5_CLEAR, box, zcyl, zslot
from lib import params

Z_BOTTOM, Z_TOP = 0.0, 12.0
RECESS_DEPTH = 5.0
SCREW_SLOT_X = (124.5, 175.5)


def box_top_body():
    body = box(0, params.BOX_X, 0, params.BOX_Y, Z_BOTTOM, Z_TOP)
    body -= zcyl(params.THRUST_RECESS_BOX_D, J1_X, J1_Y, Z_BOTTOM, Z_BOTTOM + RECESS_DEPTH)
    body -= zcyl(params.BEARING_6807_SEAT_D, J1_X, J1_Y, Z_BOTTOM + RECESS_DEPTH, Z_TOP)
    body -= zslot(*params.J1_MOTOR_SLOT_X, params.J1_MOTOR_SLOT_Y, params.J1_MOTOR_SLOT_W, Z_BOTTOM, Z_TOP)
    for y in params.J1_MOTOR_SCREW_SLOT_Y:
        body -= zslot(*SCREW_SLOT_X, y, M3_CLEAR, Z_BOTTOM, Z_TOP)
    for x, y in params.BOX_M5_XY:
        body -= zcyl(M5_CLEAR, x, y, Z_BOTTOM, Z_TOP)
    return body


@step(out="../../STEP/joint12/box_top.step")
def box_top():
    part = box_top_body()
    part.label = "box_top"
    return part


if __name__ == "__main__":
    box_top()
