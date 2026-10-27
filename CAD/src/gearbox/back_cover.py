"""Back cover (motor end), gearbox frame z 0..14 (design.md §3).

Ø72 x 7 recess for the stage-1 carrier, Ø26 x 5 seat for the 6803
(17x26x5) input bearing, Ø24 lip, Ø18 through bore. 6 x M3 clearance to the
ring gear inserts with nut/head pockets that run out to the rim; 4 x M3
inserts for the NEMA17 mount.
"""
from cadgen import step

from gearbox.common import (BOLT_ANGLES, BOLT_R, M3_CLEAR, M3_INSERT, NUT_POCKET_DEPTH, OD,
                            disc, hole, nut_slot_pocket)

Z0, Z1 = 0.0, 14.0
MOUNT_INSERT_R = 29.125
MOUNT_INSERT_ANGLES = (55.49, 124.51, -55.49, -124.51)  # 33 x 48 rectangle
MOUNT_INSERT_DEPTH = 6.0


def back_cover_body():
    body = disc(OD, Z0, Z1)
    body -= disc(72.0, Z0, 7.0)
    body -= disc(26.0, 7.0, 12.0)
    body -= disc(24.0, 12.0, 12.6)
    body -= disc(18.0, 12.6, Z1)
    for a in BOLT_ANGLES:
        body -= hole(M3_CLEAR, BOLT_R, a, Z0, Z1)
        body -= nut_slot_pocket(BOLT_R, a, Z1 - NUT_POCKET_DEPTH, Z1)
    for a in MOUNT_INSERT_ANGLES:
        body -= hole(M3_INSERT, MOUNT_INSERT_R, a, Z1 - MOUNT_INSERT_DEPTH, Z1)
    return body


@step(out="../../STEP/gearbox/back_cover.step")
def back_cover():
    part = back_cover_body()
    part.label = "back_cover"
    return part


if __name__ == "__main__":
    back_cover()
