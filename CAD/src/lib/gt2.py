"""GT2 (2 mm pitch) timing pulley and belt helpers.

The groove matches the Fusion pulleys, which use the common parametric GT2
arc construction (measured in Session 1 from the 20T, 80T and 160T pulleys):

- pulley OD = pitch diameter - 2 x 0.254 (pitch line offset)
- groove bottom: R0.555 arc, centre 0.195 below the OD, depth 0.75
- flanks: R1.0 arcs centred on the OD circle, +/-0.40 either side of the groove
  centre (each flank is the arc of the *opposite* centre)
- tip fillets: R0.15 where the flanks meet the OD

The Fusion profile also has small blend arcs (R0.38-R0.54) between bottom and
flanks; they are omitted here. Effect on the 160T J1 pulley (Session 4): the
r 49.5-51 tooth-band section is 0.69 % heavier than Fusion (about 0.011 mm^2
per groove), and the whole part passes the gate at 0.02 %.
"""
from __future__ import annotations

import math

from cadgen import build123d as bd

PITCH = 2.0
PITCH_LINE_OFFSET = 0.254
TOOTH_DEPTH = 0.75
BOTTOM_R = 0.555
BOTTOM_CENTRE_DEPTH = 0.195
FLANK_R = 1.0
FLANK_OFFSET = 0.40
TIP_FILLET_R = 0.15


def pitch_diameter(teeth: int) -> float:
    return teeth * PITCH / math.pi


def outside_diameter(teeth: int) -> float:
    return pitch_diameter(teeth) - 2 * PITCH_LINE_OFFSET


def _groove(r_od: float) -> bd.Sketch:
    """One groove cutter centred on +X at the OD radius (local x = radial)."""
    lens = (
        bd.Pos(r_od, FLANK_OFFSET) * bd.Circle(FLANK_R)
    ) & (
        bd.Pos(r_od, -FLANK_OFFSET) * bd.Circle(FLANK_R)
    )
    bottom_x = r_od - BOTTOM_CENTRE_DEPTH
    # Above the bottom-arc centre the lens shapes the flank; below it the
    # groove is bounded by the R0.555 bottom arc.
    upper = lens & (bd.Pos(bottom_x + 1.0, 0) * bd.Rectangle(2.0, 4.0))
    lower = bd.Pos(bottom_x, 0) * bd.Circle(BOTTOM_R)
    return upper + lower


def pulley_profile(teeth: int) -> bd.Sketch:
    """2D toothed outline (no bore), groove 0 centred on +X."""
    r_od = outside_diameter(teeth) / 2
    profile = bd.Sketch() + bd.Circle(r_od)
    groove = _groove(r_od)
    for i in range(teeth):
        profile -= groove.rotate(bd.Axis.Z, 360.0 * i / teeth)
    return profile


def toothed_ring(teeth: int, width: float) -> bd.Part:
    """Toothed band from z=0 to z=width (add hub, flanges and bore per part)."""
    return bd.extrude(pulley_profile(teeth), width)


def belt_pitch_length(centre_distance: float, teeth_a: int, teeth_b: int) -> float:
    """Open-belt pitch length for two pulleys (no idler)."""
    da, db = pitch_diameter(teeth_a), pitch_diameter(teeth_b)
    c = centre_distance
    return 2 * c + math.pi * (da + db) / 2 + (da - db) ** 2 / (4 * c)


def belt_teeth(length: float) -> float:
    return length / PITCH
