"""Output block (Fusion "Output block"), arm frame (design.md §4).

J3 output bracket. A 20 mm distal end plate (x 214.175..234.175, the full
80 x 44 section, z 0.2..44.2) carries the 73 x 37 M3 link interface (IF-8):
Ø3.3 through with Ø6 x 3 counterbores from the inside, each run out
through the two faces of its corner (I-21). A 35 x 28 fork
(y 22.5..57.5, z 8.2..36.2) runs back to x = 144.175 and joins the plate
with R5 fillets, mitred at the corners (the Session 1 "Ø10 cross holes").
The fork is split by a 10.5 slot (z 21.7..32.2, to x = 199.175) for the
GT2-80 output. On J3, a 21.65 AF hex socket (circumradius 12.5, corners on
±Y) runs through both prongs and through two Ø28.5 x 1 bosses with R1
rounded edges that bear on the 6805 inner races (z 7.2 / 37.2). The Pin
hexes and the GT2-80 output socket line up with it (I-6 fixed; in Fusion
the Pins are 30 and 17.2 deg off).
"""
from cadgen import build123d as bd
from cadgen import step

from belt_arm.common import J3_X, J3_Y, M3_CBORE, box, xcyl
from joint12.common import corner_runout
from lib import params
from lib.tolerances import hex_socket_r, profile

FIT = profile("output_block")

X_FORK, X_SLOT_END, X_PLATE, X_END = 144.175, 199.175, 214.175, 234.175
Z0, Z1 = 0.2, 44.2
FORK_Y = (22.5, 57.5)
FORK_Z = (8.2, 36.2)
SLOT_Z = (21.7, 32.2)
FILLET_R = 5.0
BOSS_R, BOSS_H, BOSS_ROUND = 14.25, 1.0, 1.0
LINK_Y = (3.5, 76.5)
LINK_Z = (3.7, 40.7)
CBORE_DEPTH = 3.0
_CMIN = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)


def _fillet() -> bd.Part:
    """R5 fillets round the fork root, mitred at the corners: the
    intersection of the Y-side and Z-side fillet prisms."""
    xf = X_PLATE - FILLET_R
    y0, y1 = FORK_Y[0] - FILLET_R, FORK_Y[1] + FILLET_R
    z0, z1 = FORK_Z[0] - FILLET_R, FORK_Z[1] + FILLET_R
    along_z = box(xf, X_PLATE, y0, y1, z0, z1)
    along_y = box(xf, X_PLATE, y0, y1, z0, z1)
    for y in (y0, y1):
        along_z -= bd.Pos(xf, y, z0) * bd.Cylinder(FILLET_R, z1 - z0, align=_CMIN)
    for z in (z0, z1):
        along_y -= bd.Pos(xf, y0, z) * bd.Rot(-90, 0, 0) * bd.Cylinder(FILLET_R, y1 - y0, align=_CMIN)
    return along_z & along_y


def _boss(z_face: float, down: bool) -> bd.Part:
    """Ø28.5 x 1 disc on the fork face at z_face, outer edge rounded R1."""
    s = -1 if down else 1
    zr = z_face + s * BOSS_H
    r_in = BOSS_R - BOSS_ROUND
    arc_mid = (r_in + BOSS_ROUND * 0.7071067811865476, z_face + s * BOSS_ROUND * 0.7071067811865476)
    edges = [
        bd.Edge.make_line(bd.Vector(0, 0, z_face), bd.Vector(BOSS_R, 0, z_face)),
        bd.Edge.make_three_point_arc(bd.Vector(BOSS_R, 0, z_face), bd.Vector(arc_mid[0], 0, arc_mid[1]),
                                     bd.Vector(r_in, 0, zr)),
        bd.Edge.make_line(bd.Vector(r_in, 0, zr), bd.Vector(0, 0, zr)),
        bd.Edge.make_line(bd.Vector(0, 0, zr), bd.Vector(0, 0, z_face)),
    ]
    return bd.Pos(J3_X, J3_Y, 0) * bd.revolve(bd.Face(bd.Wire(edges)), bd.Axis.Z)


def output_block_body():
    body = box(X_PLATE, X_END, 0, params.ARM_WIDTH, Z0, Z1)
    body += box(X_FORK, X_PLATE, *FORK_Y, *FORK_Z)
    body += _fillet()
    body += _boss(FORK_Z[0], down=True) + _boss(FORK_Z[1], down=False)
    body -= box(X_FORK - 1, X_SLOT_END, FORK_Y[0] - 1, FORK_Y[1] + 1, *SLOT_Z)
    hex_z0, hex_z1 = FORK_Z[0] - BOSS_H, FORK_Z[1] + BOSS_H
    body -= bd.Pos(J3_X, J3_Y, hex_z0) * bd.extrude(
        bd.RegularPolygon(hex_socket_r(params.OUTPUT_HEX_SOCKET_R, FIT.hex_socket), 6, rotation=90), hex_z1 - hex_z0)
    for y in LINK_Y:
        for z in LINK_Z:
            corner = (0.0 if y < params.ARM_WIDTH / 2 else params.ARM_WIDTH, Z0 if z < (Z0 + Z1) / 2 else Z1)
            body -= bd.extrude(bd.Plane.YZ.offset(X_PLATE) * corner_runout(M3_CBORE, y, z, *corner), CBORE_DEPTH)
            body -= xcyl(FIT.m3_clear, y, z, X_PLATE + CBORE_DEPTH, X_END)
    return body


@step(out="../../STEP/belt_arm/output_block.step")
def output_block():
    part = output_block_body()
    part.label = "output_block"
    return part


if __name__ == "__main__":
    output_block()
