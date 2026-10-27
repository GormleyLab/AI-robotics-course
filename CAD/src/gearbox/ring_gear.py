"""Ring gear: 45T internal m1.5, shared by both stages (design.md §3).

Gearbox frame (gearbox/common.py), z from -47 (front cover) to 0 (back cover).
Two 12-wide toothed bands (stage 1 at z -12..0, stage 2 at -35.5..-23.5),
a Ø72 relief groove between them and a Ø72 counterbore at the front, each
ending in a 45 deg chamfer onto the tooth tips. 6 x M3 heat-set inserts at
each end.
"""
from cadgen import build123d as bd
from cadgen import step

from gearbox.common import BOLT_ANGLES, BOLT_R, OD, disc, hole, revolve_rz
from lib import gears, params
from lib.tolerances import profile

FIT = profile("ring_gear")

Z_FRONT, Z_BACK = -47.0, 0.0
RING_ADDENDUM = 1.1667         # ring tooth height inside the pitch circle (x m): tip Ø64.0
RING_DEDENDUM = 1.1333         # space depth outside it: root Ø70.9
RING_BACKLASH = 0.053          # ring teeth 3.91 deg thick at the pitch circle (nominal 4.0)
RING_TIP_ROUND = 0.385         # tooth-tip corner radius, fitted to the Fusion section area
RELIEF_D = 72.0
INSERT_DEPTH = 10.0
# (relief start z, chamfer start z): relief is Ø72 from start to chamfer start
RELIEFS = ((-47.0, -39.3), (-23.5, -15.8))
HELIX_ANGLE = params.GEAR_HELIX_ANGLE  # 15 deg; teeth turn CCW as z increases
# Both bands are the same helix shifted axially: measured (tmp slices at the
# pitch circle) tooth centre 0.0 deg at each band's lower end, +5.458 deg at
# its upper end. The cutter's tooth 0 (a ring tooth *space*) is on +X, so it
# is rotated by -half a pitch at the band's lower end.
BANDS = (  # (band lower z, band upper z); cutters span the relief/chamfer below
    (-12.0, 0.0),
    (-35.5, -23.5),
)
CUTTER_EXTRA_BELOW = 11.5     # cutter starts at the relief groove (z -23.5 / -47)


def ring_gear_body():
    m, z = params.GEAR_MODULE, params.RING_TEETH
    r_tip = m * z / 2 - RING_ADDENDUM * m
    body = disc(OD, Z_FRONT, Z_BACK)
    half_pitch = 180.0 / z
    for z_low, z_high in BANDS:
        z0 = z_low - CUTTER_EXTRA_BELOW
        width = z_high - z0
        # phase at z0 so that the tooth centre is at 0 deg at z_low
        start = -gears.twist_deg(HELIX_ANGLE, m * z / 2, CUTTER_EXTRA_BELOW) - half_pitch
        cutter = gears.ring_gear_cutter(z, m, width, addendum=RING_ADDENDUM, dedendum=RING_DEDENDUM,
                                        backlash=RING_BACKLASH, helix_angle=HELIX_ANGLE,
                                        tip_round=RING_TIP_ROUND)
        body -= bd.Pos(0, 0, z0) * bd.Rot(0, 0, start) * cutter
    for z0, z_chamfer in RELIEFS:
        r = RELIEF_D / 2
        body -= revolve_rz([(0, z0), (r, z0), (r, z_chamfer), (r_tip, z_chamfer + (r - r_tip)), (0, z_chamfer + (r - r_tip))])
    for a in BOLT_ANGLES:
        body -= hole(FIT.insert_m3, BOLT_R, a, Z_BACK - INSERT_DEPTH, Z_BACK)
        body -= hole(FIT.insert_m3, BOLT_R, a, Z_FRONT, Z_FRONT + INSERT_DEPTH)
    return body


@step(out="../../STEP/gearbox/ring_gear.step")
def ring_gear():
    part = ring_gear_body()
    part.label = "ring_gear"
    return part


if __name__ == "__main__":
    ring_gear()
