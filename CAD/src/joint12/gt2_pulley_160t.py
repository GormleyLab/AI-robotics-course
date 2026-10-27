"""GT2 160T J1 pulley (Fusion "GT2-120 v4", I-9), base frame on J1 (design.md §2).

7 mm toothed band (z -11.5..-4.5, OD 101.35, groove 0 on +X as in Fusion)
between two flanges that rise 1 mm at 45 deg to Ø103.35 with 0.2 mm edge
chamfers. Disc z -13..-3 with a Ø60 x 5 lower-thrust pocket on top and
4 x Ø5.3 at r = 10 (M5 to the hinge); solid Ø8 x 12 hub down into the 608.
"""
from cadgen import build123d as bd
from cadgen import step

from joint12.common import J1_X, J1_Y, M5_CLEAR, zcyl
from lib import gt2, params
from lib.tolerances import ACTIVE as FIT, hole

TEETH = params.GT2_TEETH_J1
R_OD = gt2.outside_diameter(TEETH) / 2      # 50.676
R_FLANGE = R_OD + 1.0
CHAMFER = 0.2
Z_HUB, Z_BOTTOM, Z_BAND0, Z_BAND1, Z_TOP = -25.0, -13.0, -11.5, -4.5, -3.0
HUB_R = 4.0
POCKET_R, POCKET_DEPTH = hole(params.THRUST_RECESS_BOX_D, FIT.slip) / 2, 5.0
BOLT_R = 10.0
R_CORE = R_OD - 1.5                          # inside the groove bottoms


def _body_rz() -> list[tuple[float, float]]:
    return [
        (0, Z_HUB), (HUB_R, Z_HUB), (HUB_R, Z_BOTTOM),
        (R_FLANGE - CHAMFER, Z_BOTTOM), (R_FLANGE, Z_BOTTOM + CHAMFER),
        (R_FLANGE, Z_BAND0 - 1.0), (R_OD, Z_BAND0), (R_CORE, Z_BAND0),
        (R_CORE, Z_BAND1), (R_OD, Z_BAND1), (R_FLANGE, Z_BAND1 + 1.0),
        (R_FLANGE, Z_TOP - CHAMFER), (R_FLANGE - CHAMFER, Z_TOP),
        (0, Z_TOP),
    ]


def gt2_pulley_160t_body():
    wire = bd.Wire.make_polygon([bd.Vector(r, 0, z) for r, z in _body_rz()], close=True)
    body = bd.revolve(bd.Face(wire), bd.Axis.Z)
    body += bd.Pos(0, 0, Z_BAND0) * gt2.toothed_ring(TEETH, Z_BAND1 - Z_BAND0)
    body -= zcyl(2 * POCKET_R, 0, 0, Z_TOP - POCKET_DEPTH, Z_TOP)
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        body -= zcyl(M5_CLEAR, dx * BOLT_R, dy * BOLT_R, Z_BOTTOM, Z_TOP - POCKET_DEPTH)
    return bd.Pos(J1_X, J1_Y, 0) * body


@step(out="../../STEP/joint12/gt2_pulley_160t.step")
def gt2_pulley_160t():
    part = gt2_pulley_160t_body()
    part.label = "gt2_pulley_160t"
    return part


if __name__ == "__main__":
    gt2_pulley_160t()
