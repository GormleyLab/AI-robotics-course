"""Shared frame, dimensions and helpers for the planetary gearbox parts.

Gearbox frame (every gearbox part is modelled in it): the gearbox axis is +Z
through the origin, z = 0 is the ring gear / back cover joint, +Z points to
the motor, -Z to the output. It is the Fusion gearbox frame rotated so
that part +Z = Fusion +Y; ``TO_FUSION`` maps a part into the Fusion gearbox
assembly. Feature angles are measured about +Z from +X in this frame.
"""
from __future__ import annotations

import math

from cadgen import build123d as bd

from lib import params

TO_FUSION = bd.Rot(-90, 0, 0)

OD = params.GEARBOX_OD                      # 85
BOLT_R = params.GEARBOX_BOLT_CIRCLE_R       # 39.25
BOLT_ANGLES = tuple(30.0 + 60.0 * k for k in range(params.GEARBOX_BOLT_COUNT))

M3_CLEAR = 3.3
M3_INSERT = 4.2
NUT_POCKET_D = 7.5     # cover pockets: counterbore + open radial slot to the rim
NUT_POCKET_DEPTH = 3.2

_MIN = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)


def polar(r: float, angle_deg: float, z: float = 0.0) -> bd.Location:
    a = math.radians(angle_deg)
    return bd.Location((r * math.cos(a), r * math.sin(a), z))


def disc(d: float, z0: float, z1: float) -> bd.Part:
    """Cylinder of diameter d on the axis from z0 to z1."""
    return bd.Pos(0, 0, min(z0, z1)) * bd.Cylinder(d / 2, abs(z1 - z0), align=_MIN)


def hole(d: float, r: float, angle_deg: float, z0: float, z1: float) -> bd.Part:
    """Axial hole of diameter d at polar (r, angle) from z0 to z1."""
    return polar(r, angle_deg, min(z0, z1)) * bd.Cylinder(d / 2, abs(z1 - z0), align=_MIN)


def revolve_rz(points: list[tuple[float, float]]) -> bd.Part:
    """Revolve a closed (r, z) polygon about the axis."""
    wire = bd.Wire.make_polygon([bd.Vector(r, 0, z) for r, z in points], close=True)
    return bd.revolve(bd.Face(wire), bd.Axis.Z)


def nut_slot_pocket(r: float, angle_deg: float, z0: float, z1: float,
                    width: float = NUT_POCKET_D, to_r: float = OD) -> bd.Part:
    """Counterbore of diameter ``width`` at (r, angle) that runs out radially to ``to_r``."""
    h = abs(z1 - z0)
    length = to_r - r + 1.0
    slot = bd.Pos(length / 2, 0, 0) * bd.Box(length, width, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    pocket = bd.Cylinder(width / 2, h, align=_MIN) + slot
    return bd.Rot(0, 0, angle_deg) * bd.Pos(r, 0, min(z0, z1)) * pocket
