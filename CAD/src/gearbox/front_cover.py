"""Front cover (output end), gearbox frame z -56..-45 (design.md §3).

9 mm flange with a Ø41 x 2 pilot boss into the ring gear, Ø37 x 7 seat for
the output 6805 bearing, Ø34 lip and Ø26 through bore. 6 x M3 clearance with
nut pockets that run out to the rim; bolts to the ring gear and the hinge.
"""
from cadgen import step

from gearbox.common import BOLT_ANGLES, BOLT_R, M3_CLEAR, NUT_POCKET_DEPTH, OD, disc, hole, nut_slot_pocket

Z_OUT, Z_FLANGE, Z_IN = -56.0, -47.0, -45.0


def front_cover_body():
    body = disc(OD, Z_OUT, Z_FLANGE) + disc(41.0, Z_FLANGE, Z_IN)
    body -= disc(37.0, -52.0, Z_IN)
    body -= disc(34.0, -52.5, -52.0)
    body -= disc(26.0, Z_OUT, -52.5)
    for a in BOLT_ANGLES:
        body -= hole(M3_CLEAR, BOLT_R, a, Z_OUT, Z_FLANGE)
        body -= nut_slot_pocket(BOLT_R, a, Z_OUT, Z_OUT + NUT_POCKET_DEPTH)
    return body


@step(out="../../STEP/gearbox/front_cover.step")
def front_cover():
    part = front_cover_body()
    part.label = "front_cover"
    return part


if __name__ == "__main__":
    front_cover()
