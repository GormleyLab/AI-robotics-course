"""Shared frame, placements and helpers for the belt drive arm segment.

Arm frame (every belt_arm part is modelled in it): the Fusion "Belt Drive
Arm" frame as-is. Plates in XY with the Base underside at z = 0 and +Z
toward the Top; the proximal end face at x = -40; J3 parallel to Z through
(160, 40). The motor is at (-10, 40), the dual pulley at (75, 40).
"""
from __future__ import annotations

from cadgen import build123d as bd

from joint12.common import box, xcyl, zcyl  # noqa: F401  (re-exported for the arm parts)
from lib import params

J3_X, J3_Y = params.J3_AXIS_XY                 # (160, 40)
MOTOR_X, MOTOR_Y = params.ARM_MOTOR_XY         # (-10, 40)
DUAL_X, DUAL_Y = params.ARM_DUAL_PULLEY_XY     # (75, 40)
IDLER_XS = tuple(x for x, _ in params.ARM_IDLER_XY)   # 27.65, 112.65
IDLER_SLOT_Y = (20.0, 65.0)                    # slot end-circle centres

X_PROXIMAL = -40.0
END_R = params.ARM_WIDTH / 2                   # R40 distal end about J3
Z_BASE_TOP = 7.0
Z_WALL_TOP = 37.0
Z_TOP_TOP = 44.0

# Pin:2 is the Pin:1 model flipped onto the Top. The flip keeps the hex
# corners on ±Y, in line with the Output block socket. Fusion also turned it
# 137.23 deg and put the GT2-80 output 9.08 mm off J3 (I-6, fixed).
PIN_2_PLACEMENT = bd.Pos(J3_X, J3_Y, 47.4) * bd.Rot(-180, 0, 0) * bd.Pos(-J3_X, -J3_Y, 2.8)

# Wall side rails end in half-rounds centred at x = RAIL_END_X. Fusion runs
# them to J3 (x = 160), where the Output block fork hits them at +-55 deg
# (I-17). Ending them at 130 clears the fork to about +-100 deg (9 mm at 90).
RAIL_END_X = 130.0

# M3 screws from the Base / Top into Ø4.2 inserts through the Wall. The two
# distal ones sit at the rail ends (Fusion: x = 160, I-17).
WALL_SCREW_XY = ((75.0, 76.5), (0.0, 3.5), (75.0, 3.5), (RAIL_END_X, 76.5), (-36.5, 40.0), (0.0, 76.5),
                 (RAIL_END_X, 3.5))
# Idler jack screws (I-4): an M3 x 35 in a Ø4.2 heat-set insert through the y = 0
# Wall rail at each idler, pushing the idler's 15 mm spacer (R5) toward +y. The
# belt pushes the idler back toward -y, so the screw works in compression only.
# (x, z) per idler: mid-height of its 15 mm spacer (z 22..37 / 7..22).
JACK_SCREW_XZ = ((IDLER_XS[0], 29.5), (IDLER_XS[1], 14.5))
JACK_SCREW_LEN = 35.0
SPACER_R = 5.0

# Ø4.2 insert holes in the proximal end faces of Base and Top (IF-8).
PROXIMAL_INSERT_Y = (3.5, 76.5)
PROXIMAL_INSERT_DEPTH = 10.0

M3_CBORE = 6.0      # M3 button head (ISO 7380, Ø5.7)
DOWEL_HOLE_D = 6.1                  # Fusion: 0.1 over the 6 mm dowel; + FIT.slip in each plate
DOWEL_BOSS_D = 10.0


def plate(z0: float, z1: float) -> bd.Part:
    """Arm outline (x -40..160 with the R40 end about J3), z0..z1."""
    return box(X_PROXIMAL, J3_X, 0, params.ARM_WIDTH, z0, z1) + zcyl(2 * END_R, J3_X, J3_Y, z0, z1)


def edge_runout(x: float, y: float, z0: float, z1: float) -> bd.Part:
    """Ø6 counterbore at (x, y) run out through the nearest plate edge as an
    open U-slot (I-21). The Wall screws sit 3.5 from an edge, which left a
    0.5 mm skin outside a Ø6 counterbore."""
    w = M3_CBORE
    to_y0, to_y1, to_x0 = y, params.ARM_WIDTH - y, x - X_PROXIMAL
    if to_x0 < min(to_y0, to_y1):
        return zcyl(w, x, y, z0, z1) + box(X_PROXIMAL - 1, x, y - w / 2, y + w / 2, z0, z1)
    if to_y0 < to_y1:
        return zcyl(w, x, y, z0, z1) + box(x - w / 2, x + w / 2, -1, y, z0, z1)
    return zcyl(w, x, y, z0, z1) + box(x - w / 2, x + w / 2, y, params.ARM_WIDTH + 1, z0, z1)


def ycyl(d: float, x: float, z: float, y0: float, y1: float) -> bd.Part:
    """Cylinder of diameter d along Y through (x, z) from y0 to y1."""
    return bd.Pos(x, y0, z) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        d / 2, y1 - y0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def yslot(x: float, y0: float, y1: float, width: float, z0: float, z1: float) -> bd.Part:
    """Vertical stadium slot along Y: end-circle centres y0..y1 at x."""
    return box(x - width / 2, x + width / 2, y0, y1, z0, z1) + zcyl(width, x, y0, z0, z1) + zcyl(width, x, y1, z0, z1)
