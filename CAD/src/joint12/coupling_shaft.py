"""Coupling shaft (Fusion "Coupling shaft v1"), base frame (design.md §2).

J2 output and segment-1 mount, on the hinge J2 axis (y = 75, z = 70.5).
A 44 mm block (x 52.8..96.8, 80 wide) with an R40 rounded bottom and a flat
top at z = 100.5 carrying the 73 x 37 M3 link interface (IF-8): Ø6 access
bores up to z = 80.5 from below, each run out through the two faces of its
corner (I-21). A hex
socket 21.65 AF x 15 deep (circumradius 12.5, corners at +-Z) takes the
gearbox output hex from the -X face (IF-7). The +X face carries a curved
transition (Ø33 -> Ø29 over 3 mm, three-point arc through the Fusion
B-spline), a Ø29 x 2 shoulder and a Ø25 x 7 stub that runs in the right
cheek 6805.
"""
from cadgen import build123d as bd
from cadgen import step

from joint12.common import J2_Y, J2_Z, M3_CBORE, Z_TO_X, box, corner_runout, xcyl, zcyl
from lib import params
from lib.tolerances import hex_socket_r, profile, shaft

FIT = profile("coupling_shaft")

X0, X1 = 52.8, 96.8
Y0, Y1 = J2_Y - params.ARM_WIDTH / 2, J2_Y + params.ARM_WIDTH / 2
END_R = 40.0
ROUND_Z = 90.5
Z_TOP = 100.5
HEX_CIRCUMR = hex_socket_r(12.5, FIT.hex_socket)
HEX_DEPTH = 15.0
# Stub profile along +X: (x, r) from the block face.
TRANSITION = ((96.8, 16.5), (98.365, 15.597), (99.8, 14.5))
SHOULDER_X1 = 101.8
STUB_X1 = 108.8
STUB_R = shaft(params.OUTPUT_SHAFT_D, FIT.press) / 2
LINK_X = (56.3, 93.3)
LINK_Y = (38.5, 111.5)
LINK_CBORE_Z1 = 80.5


def _stub() -> bd.Part:
    """Revolved stub, sketched in (x, r) on the XZ plane about the J2 axis."""
    (xa, ra), (xm, rm), (xb, rb) = TRANSITION
    with bd.BuildSketch(bd.Plane.XZ) as sk:
        with bd.BuildLine():
            bd.Polyline((xa, 0), (xa, ra))
            bd.ThreePointArc((xa, ra), (xm, rm), (xb, rb))
            bd.Polyline((xb, rb), (SHOULDER_X1, rb), (SHOULDER_X1, STUB_R), (STUB_X1, STUB_R), (STUB_X1, 0), (xa, 0))
        bd.make_face()
    stub = bd.revolve(sk.sketch, bd.Axis.X)
    return bd.Pos(0, J2_Y, J2_Z) * stub


def coupling_shaft_body():
    rounded = xcyl(2 * END_R, J2_Y, ROUND_Z, X0, X1) & box(X0, X1, Y0, Y1, ROUND_Z - END_R, ROUND_Z)
    body = rounded + box(X0, X1, Y0, Y1, ROUND_Z, Z_TOP)
    hexagon = bd.extrude(bd.RegularPolygon(HEX_CIRCUMR, 6), HEX_DEPTH)
    body -= bd.Pos(X0, J2_Y, J2_Z) * Z_TO_X * hexagon
    body += _stub()
    for x in LINK_X:
        for y in LINK_Y:
            body -= zcyl(FIT.m3_clear, x, y, LINK_CBORE_Z1, Z_TOP)
            corner = (X0 if x < (X0 + X1) / 2 else X1, Y0 if y < J2_Y else Y1)
            z0 = ROUND_Z - END_R
            body -= bd.Pos(0, 0, z0) * bd.extrude(corner_runout(M3_CBORE, x, y, *corner), LINK_CBORE_Z1 - z0)
    return body


@step(out="../../STEP/joint12/coupling_shaft.step")
def coupling_shaft():
    part = coupling_shaft_body()
    part.label = "coupling_shaft"
    return part


if __name__ == "__main__":
    coupling_shaft()
