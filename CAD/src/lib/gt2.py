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


def centre_distance(length: float, teeth_a: int, teeth_b: int) -> float:
    """Centre distance at which an open belt of pitch ``length`` fits (inverse of belt_pitch_length)."""
    da, db = pitch_diameter(teeth_a), pitch_diameter(teeth_b)
    k = length - math.pi * (da + db) / 2
    return (k + math.sqrt(k * k - 2 * (da - db) ** 2)) / 4


def belt_teeth(length: float) -> float:
    return length / PITCH


# --- Flanged pulley (the Fusion arm pulleys: 20T and 80T sections, GT2-80 output)
FLANGE_H = 1.5        # each flange: 0.2 chamfer + 0.3 rim + 1.0 rise at 45 deg
FLANGE_RISE = 1.0
FLANGE_CHAMFER = 0.2


def flanged_pulley(teeth: int, band_width: float = 7.0) -> bd.Part:
    """Solid toothed band between two flanges (no bore), z = 0 at the lower
    flange face; the band runs from FLANGE_H to FLANGE_H + band_width.
    Each flange rises 1 mm at 45 deg from the OD to OD + 2 with 0.2 edge
    chamfers, as on the Fusion pulleys."""
    r_od = outside_diameter(teeth) / 2
    r_flange, r_core = r_od + FLANGE_RISE, r_od - 1.5
    z0, z1 = FLANGE_H, FLANGE_H + band_width
    top = z1 + FLANGE_H
    rz = [
        (0, 0), (r_flange - FLANGE_CHAMFER, 0), (r_flange, FLANGE_CHAMFER),
        (r_flange, z0 - FLANGE_RISE), (r_od, z0), (r_core, z0),
        (r_core, z1), (r_od, z1), (r_flange, z1 + FLANGE_RISE),
        (r_flange, top - FLANGE_CHAMFER), (r_flange - FLANGE_CHAMFER, top), (0, top),
    ]
    wire = bd.Wire.make_polygon([bd.Vector(r, 0, z) for r, z in rz], close=True)
    body = bd.revolve(bd.Face(wire), bd.Axis.Z)
    return body + bd.Pos(0, 0, z0) * toothed_ring(teeth, band_width)


# --- Belt path over pulleys and idlers
BELT_BACK = 0.376     # pitch line to belt back (1.38 belt - 0.75 tooth - 0.254)
BELT_LAND = PITCH_LINE_OFFSET   # pitch line to the land between belt teeth (pulley OD)


def _tangent(c1, r1, c2, r2):
    """Tangent from circle 1 to circle 2 for a CCW belt loop. A positive
    radius keeps the circle on the belt's left (wrapped CCW, inside the
    loop); a negative one on its right (an idler pressing from outside)."""
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    theta = math.atan2(dy, dx) - math.asin((r2 - r1) / math.hypot(dx, dy))
    lx, ly = -math.sin(theta), math.cos(theta)
    return (c1[0] - r1 * lx, c1[1] - r1 * ly), (c2[0] - r2 * lx, c2[1] - r2 * ly)


def belt_path(circles: list[tuple[float, float, float]]) -> tuple[bd.Wire, float]:
    """Closed belt line (wire) and its length over circles (x, y, signed r)
    listed in CCW loop order; see _tangent for the sign convention."""
    n = len(circles)
    tans = [_tangent(circles[i][:2], circles[i][2], circles[(i + 1) % n][:2], circles[(i + 1) % n][2])
            for i in range(n)]
    edges, length = [], 0.0
    for i, (x, y, r) in enumerate(circles):
        p_in, p_out = tans[i - 1][1], tans[i][0]
        a0, a1 = (math.atan2(p[1] - y, p[0] - x) for p in (p_in, p_out))
        sweep = (a1 - a0) % (2 * math.pi) if r > 0 else -((a0 - a1) % (2 * math.pi))
        mid = a0 + sweep / 2
        ar = abs(r)
        edges.append(bd.Edge.make_three_point_arc(
            bd.Vector(*p_in), bd.Vector(x + ar * math.cos(mid), y + ar * math.sin(mid)), bd.Vector(*p_out)))
        edges.append(bd.Edge.make_line(bd.Vector(*p_out), bd.Vector(*tans[i][1])))
        length += ar * abs(sweep) + math.dist(p_out, tans[i][1])
    return bd.Wire(edges), length


def belt_envelope(circles: list[tuple[float, float, float]], width: float = 6.0) -> bd.Part:
    """Belt body from z = 0 to width: the pitch line offset BELT_LAND toward
    the pulleys (the land, on the pulley OD) and BELT_BACK away from them.
    The teeth are left out: they sit in the pulley grooves. Give pulleys
    their pitch radius and back-side idlers (negative r) -(OD / 2 + BELT_BACK)."""
    loop = bd.Face(belt_path(circles)[0])
    band = bd.offset(loop, BELT_BACK) - bd.offset(loop, -BELT_LAND)
    return bd.extrude(band, width)


def idler_depth(a: tuple[float, float, float], b: tuple[float, float, float],
                idler: tuple[float, float, float]) -> float:
    """How far a back-side idler (x, y, signed r < 0) pushes into the open
    strand from circle a to b (CCW loop order); <= 0 means it misses the belt."""
    p, q = _tangent(a[:2], a[2], b[:2], b[2])
    right = ((q[1] - p[1]) * (idler[0] - p[0]) - (q[0] - p[0]) * (idler[1] - p[1])) / math.dist(p, q)
    return -idler[2] - right
