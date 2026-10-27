"""Wall (Fusion "Wall"), arm frame (design.md §4).

30 mm U-frame between the plates (z 7..37): a 7 mm proximal end wall
(x -40..-33) and two 7 mm side rails to x = 160 with half-round R3.5 ends,
open at the distal end for the Output block. 7 x Ø4.2 M3 insert holes
through the full height, used from both faces.
"""
from cadgen import step

from belt_arm.common import M3_INSERT, WALL_SCREW_XY, X_PROXIMAL, Z_BASE_TOP, Z_WALL_TOP, J3_X, box, zcyl
from lib import params

T = 7.0


def wall_body():
    w = params.ARM_WIDTH
    body = box(X_PROXIMAL, X_PROXIMAL + T, 0, w, Z_BASE_TOP, Z_WALL_TOP)
    for y0 in (0.0, w - T):
        body += box(X_PROXIMAL, J3_X, y0, y0 + T, Z_BASE_TOP, Z_WALL_TOP)
        body += zcyl(T, J3_X, y0 + T / 2, Z_BASE_TOP, Z_WALL_TOP)
    for x, y in WALL_SCREW_XY:
        body -= zcyl(M3_INSERT, x, y, Z_BASE_TOP, Z_WALL_TOP)
    return body


@step(out="../../STEP/belt_arm/wall.step")
def wall():
    part = wall_body()
    part.label = "wall"
    return part


if __name__ == "__main__":
    wall()
