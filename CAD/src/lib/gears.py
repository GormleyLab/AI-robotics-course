"""Involute spur/helical and internal (ring) gear factories.

No gear library ships in the cadgen environment, so the profile is built here.
Profile (transverse plane): standard involute, ``addendum``/``dedendum`` in
multiples of the module, straight radial flank below the base circle, no root
fillet. Tooth thickness at the pitch circle is ``pi*m/2 - backlash``.

Helical gears are the transverse profile extruded with a uniform twist (the
way Fusion's gear add-in builds them), so ``module`` is the *transverse*
module. ``helix_angle`` is at the pitch circle; positive = the tooth pattern
turns counter-clockwise (about +Z) as z increases.

The planetary gearbox (design.md §3) uses transverse m1.5, 20 deg, 15 deg
helix: sun and planets 15T, ring 45T.
"""
from __future__ import annotations

import math

from cadgen import build123d as bd


def _inv(a: float) -> float:
    return math.tan(a) - a


def _flank_angle(r: float, rb: float, rp: float, half_thickness_angle: float) -> float:
    """Angular half-width of the tooth at radius ``r`` (radians)."""
    r = max(r, rb)
    alpha_p = math.acos(rb / rp)
    alpha_r = math.acos(rb / r)
    return half_thickness_angle + _inv(alpha_p) - _inv(alpha_r)


def _tooth_face(r_root: float, r_tip: float, rb: float, rp: float, psi: float, n: int) -> bd.Face:
    """One tooth (centred on +X) from the root circle to the tip circle."""
    r0 = max(rb, r_root)
    radii = [r0 + (r_tip - r0) * (i / (n - 1)) for i in range(n)]
    upper = [bd.Vector(r * math.cos(t), r * math.sin(t))
             for r in radii for t in [_flank_angle(r, rb, rp, psi)]]
    lower = [bd.Vector(v.X, -v.Y) for v in upper]

    # Sink the tooth slightly below the root circle so it fuses with the disc.
    sink = r_root - 0.02 * (r_tip - r_root)
    t_base = _flank_angle(r0, rb, rp, psi)
    base_up = bd.Vector(sink * math.cos(t_base), sink * math.sin(t_base))
    base_lo = bd.Vector(base_up.X, -base_up.Y)

    tip_mid = bd.Vector(r_tip, 0)
    edges = [
        bd.Edge.make_line(base_lo, lower[0]),
        bd.Edge.make_spline(lower),
        bd.Edge.make_three_point_arc(lower[-1], tip_mid, upper[-1]),
        bd.Edge.make_spline(list(reversed(upper))),
        bd.Edge.make_line(upper[0], base_up),
        bd.Edge.make_line(base_up, base_lo),
    ]
    return bd.Face(bd.Wire(edges))


def spur_profile(
    teeth: int,
    module: float,
    pressure_angle: float = 20.0,
    addendum: float = 1.0,
    dedendum: float = 1.25,
    backlash: float = 0.0,
    samples: int = 12,
    root_fillet: float = 0.0,
) -> bd.Sketch:
    """2D external gear outline centred on the origin, tooth 0 on +X.

    ``root_fillet`` rounds the concave corners where the flanks meet the
    root circle (Fusion's gears have them)."""
    rp = module * teeth / 2
    rb = rp * math.cos(math.radians(pressure_angle))
    r_tip = rp + addendum * module
    r_root = rp - dedendum * module
    psi = (math.pi * module / 2 - backlash) / (2 * rp)

    tooth = _tooth_face(r_root, r_tip, rb, rp, psi, samples)
    profile = bd.Sketch() + bd.Circle(r_root)
    for i in range(teeth):
        profile += tooth.rotate(bd.Axis.Z, 360.0 * i / teeth)
    if root_fillet > 0:
        corners = [v for v in profile.vertices()
                   if abs(bd.Vector(v.X, v.Y).length - r_root) < 1e-3]
        profile = bd.Sketch() + bd.fillet(corners, root_fillet)
    return profile


def spur_gear(
    teeth: int,
    module: float,
    width: float,
    pressure_angle: float = 20.0,
    addendum: float = 1.0,
    dedendum: float = 1.25,
    backlash: float = 0.0,
    bore: float = 0.0,
    tip_chamfer: float = 0.0,
    helix_angle: float = 0.0,
    root_fillet: float = 0.0,
) -> bd.Part:
    """External spur/helical gear, axis +Z, from z=0 to z=width, tooth 0 on +X at z=0."""
    profile = spur_profile(teeth, module, pressure_angle, addendum, dedendum, backlash,
                           root_fillet=root_fillet)
    gear = _extrude(profile, width, twist_deg(helix_angle, module * teeth / 2, width))
    if tip_chamfer > 0:
        r_tip = module * teeth / 2 + addendum * module
        # Cones trimming the tooth tips at both faces (as the Fusion gears do).
        gear = gear & _tip_chamfer_envelope(r_tip, width, tip_chamfer)
    if bore > 0:
        gear = gear - bd.Cylinder(bore / 2, width, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return gear


def ring_gear_cutter(
    teeth: int,
    module: float,
    width: float,
    pressure_angle: float = 20.0,
    addendum: float = 1.0,
    dedendum: float = 1.25,
    backlash: float = 0.0,
    helix_angle: float = 0.0,
    tip_round: float = 0.0,
) -> bd.Part:
    """Solid to subtract from a body to cut an internal gear.

    ``tip_round`` rounds the ring's tooth-tip corners (it is the cutter's
    root fillet).

    ``addendum`` is the ring tooth height inside the pitch circle (ring tip
    radius = rp - addendum*m); ``dedendum`` is the space depth outside it
    (ring root radius = rp + dedendum*m). The ring's tooth spaces are the
    teeth of an external gear with swapped addendum/dedendum.
    """
    profile = spur_profile(
        teeth, module, pressure_angle,
        addendum=dedendum, dedendum=addendum,
        backlash=-backlash,  # wider spaces = thinner ring teeth
        root_fillet=tip_round,
    )
    return _extrude(profile, width, twist_deg(helix_angle, module * teeth / 2, width))


def twist_deg(helix_angle: float, pitch_radius: float, width: float) -> float:
    """Rotation of the tooth pattern over ``width`` for a helix at the pitch circle."""
    return math.degrees(width * math.tan(math.radians(helix_angle)) / pitch_radius)


def _extrude(profile: bd.Sketch, width: float, twist: float) -> bd.Part:
    if abs(twist) < 1e-9:
        return bd.extrude(profile, width)
    (face,) = profile.faces()
    return bd.Solid.extrude_linear_with_rotation(
        face, bd.Vector(0, 0, 0), bd.Vector(0, 0, width), twist)


def _tip_chamfer_envelope(r_tip: float, width: float, c: float) -> bd.Part:
    """Revolved envelope that removes a 45 deg chamfer of size ``c`` at the tip."""
    pts = [(0, 0), (r_tip - c, 0), (r_tip, c), (r_tip, width - c), (r_tip - c, width), (0, width)]
    section = bd.Face(bd.Wire.make_polygon([bd.Vector(x, 0, z) for x, z in pts], close=True))
    return bd.revolve(section, bd.Axis.Z)
