"""Shared frame, placements and helpers for the joint 1/2 base parts.

Base frame (every joint12 part is modelled in it): the Fusion "Joint 1 and 2"
frame as-is. Origin at the box corner, top of the box bottom at z = 0,
+Z up; J1 is vertical through (75, 75); J2 is parallel to X at y = 75,
z = 70.5 (hinge, coupling shaft and gearbox). Fusion had the gearbox 0.5 mm
lower, at 70.0 (issue I-1, fixed).
"""
from __future__ import annotations

import math

from cadgen import build123d as bd

from gearbox.common import TO_FUSION
from lib import params

J1_X, J1_Y = params.J1_AXIS_XY                 # (75, 75)
J2_Y, J2_Z = params.J2_AXIS_YZ                 # (75, 70.5)

# Gearbox frame -> base frame: the gearbox is placed rigidly on J2 with its
# ring / back-cover joint at x = -17, motor toward -X (Fusion: z = 70.0, I-1).
GEARBOX_PLACEMENT = bd.Pos(-17.0, J2_Y, J2_Z) * bd.Rot(0, 0, 90) * TO_FUSION

# Along-X parts (axis on J2) are modelled about +Z, then turned onto +X.
Z_TO_X = bd.Rot(0, 90, 0)

M3_CLEAR = 3.3
M3_CBORE = 6.0
M5_CLEAR = 5.3
M5_INSERT = 6.4

_MIN = (bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)
_CMIN = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)


def box(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> bd.Part:
    """Axis-aligned box between the given coordinates."""
    return bd.Pos(x0, y0, z0) * bd.Box(x1 - x0, y1 - y0, z1 - z0, align=_MIN)


def zcyl(d: float, x: float, y: float, z0: float, z1: float) -> bd.Part:
    """Vertical cylinder of diameter d at (x, y) from z0 to z1."""
    return bd.Pos(x, y, z0) * bd.Cylinder(d / 2, z1 - z0, align=_CMIN)


def xcyl(d: float, y: float, z: float, x0: float, x1: float) -> bd.Part:
    """Cylinder of diameter d along X through (y, z) from x0 to x1."""
    return bd.Pos(x0, y, z) * Z_TO_X * bd.Cylinder(d / 2, x1 - x0, align=_CMIN)


def zslot(x0: float, x1: float, y: float, width: float, z0: float, z1: float) -> bd.Part:
    """Vertical stadium slot along X: end-circle centres x0..x1 at y."""
    return box(x0, x1, y - width / 2, y + width / 2, z0, z1) + zcyl(width, x0, y, z0, z1) + zcyl(width, x1, y, z0, z1)


def on_j2_circle(r: float, angle_deg: float) -> tuple[float, float]:
    """(y, z) at radius r about the hinge J2 axis; angle from +Y toward +Z."""
    a = math.radians(angle_deg)
    return J2_Y + r * math.cos(a), J2_Z + r * math.sin(a)
