"""Parametric stand-ins for purchased parts that step.parts does not carry.

Frame convention for every purchased part: axis along +Z, one end face (or
the motor mounting face) at z=0. Searches run in Session 2 (2026-10-26):

- 6801/6805/6807 thin-section bearings, 51108 thrust bearing, 6x8x10
  bushings: no catalog match.
- ISO 2338 D6x30 dowel: catalog file is 60 mm long (bad geometry), rejected.
- NEMA17 L40: catalog shaft ~13 mm; the arm needs the Fusion 20 mm-class
  shaft, rejected.
- Fusion "Pin 6x11mm" (6 x 22) and "Washer 6mm" (6.2 x 11.8 x 1.3) are
  non-standard sizes; modelled to the Fusion dimensions.
"""
from __future__ import annotations

import build123d as bd

_MIN = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)


def annulus(inner_d: float, outer_d: float, height: float) -> bd.Part:
    return bd.Cylinder(outer_d / 2, height, align=_MIN) - bd.Cylinder(inner_d / 2, height, align=_MIN)


def ball_bearing(bore: float, od: float, width: float) -> bd.Part:
    """Deep-groove bearing envelope: inner and outer rings with a shield recess."""
    ring_wall = (od - bore) / 2
    recess = min(0.2, width * 0.05)
    shield_in, shield_out = bore + 0.3 * ring_wall, od - 0.3 * ring_wall
    body = annulus(bore, od, width)
    for z in (0.0, width - recess):
        body -= bd.Pos(0, 0, z) * annulus(shield_in, shield_out, recess)
    return body


def thrust_bearing(bore: float, od: float, height: float) -> bd.Part:
    return annulus(bore, od, height)


def pin(diameter: float, length: float) -> bd.Part:
    return bd.Cylinder(diameter / 2, length, align=_MIN)


def nema17(body_length: float = 40.0, shaft_length: float = 23.7) -> bd.Part:
    """NEMA17 stepper, mounting face at z=0, shaft along +Z, body below.

    Shaft length is measured from the mounting face, matching the Fusion
    motor (boss 2 mm, shaft tip 23.7 mm above the face).
    """
    frame, chamfer = 42.3, 4.0
    outline = bd.Sketch() + bd.Rectangle(frame, frame)
    for sx in (-1, 1):
        for sy in (-1, 1):
            # 45 deg corner chamfers, `chamfer` along each edge
            outline -= bd.Pos(sx * frame / 2, sy * frame / 2) * bd.Rectangle(
                chamfer * 2**0.5, chamfer * 2**0.5, rotation=45
            )
    body = bd.extrude(outline, -body_length)
    for sx in (-1, 1):
        for sy in (-1, 1):
            body -= bd.Pos(sx * 15.5, sy * 15.5, -4.5) * bd.Cylinder(1.5, 4.5, align=_MIN)
    boss = bd.Cylinder(11.0, 2.0, align=_MIN)
    shaft = bd.Cylinder(2.5, shaft_length, align=_MIN)
    flat = bd.Pos(0, 2.0 + 2.5, shaft_length - 15 + 7.5) * bd.Box(10, 5, 15)  # 0.5 mm D-flat, 15 long
    return body + boss + (shaft - flat)
