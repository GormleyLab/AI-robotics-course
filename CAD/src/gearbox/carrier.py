"""Planet-carrier factories (helpers, not entrypoints); design.md §3.

Each stage's carrier is two printed halves clamped by 3 x M3 around the
planet pins:

- carrier plate (Fusion "Carrier p1 - stage 1/2"): Ø56 plate with three Ø29.5
  planet pockets, blind Ø6 pin holes, M3 heat-set inserts and three tapered
  locating pegs;
- output half: Ø56 plate with a Ø21 bearing recess, through pin holes,
  countersunk M3 holes and peg sockets, on a stem carrying the next stage's
  sun gear (stage 1) or the output shaft and hex (stage 2).

Angles are relative to ``pin_angle`` (the first planet pin). Gearbox frame.
"""
from __future__ import annotations

from cadgen import build123d as bd

from gearbox.common import disc, hole, polar, revolve_rz
from lib import gears, params
from lib.tolerances import FitProfile, hole as fit_hole

PLATE_D = 56.0
PIN_R = params.PLANET_CENTRE_R          # 22.5
PIN_D = 6.0                             # planet pins (+ fit.press)
POCKET_D = 29.5
BORE_D = 32.5
POCKET_FILLET = 1.0
SCREW_R, SCREW_OFFSET = 22.0, -60.0     # M3 insert / screw, relative to pin_angle
PEG_R, PEG_OFFSET = 25.0, 165.0         # locating peg / socket, relative to pin_angle
PEG_BASE_R, PEG_TIP_R, PEG_H = 1.0, 0.464, 2.0
SOCKET_TIP_R, SOCKET_DEPTH = 0.532, 2.2
INSERT_DEPTH = 8.0
PILOT_D, PILOT_DEPTH = 2.8, 2.65
CSK_D = 7.5

SUN_TEETH = params.SUN_TEETH
MODULE = params.GEAR_MODULE
HELIX = params.GEAR_HELIX_ANGLE
BACKLASH = 0.053                        # 11.728 deg tooth width at the pitch circle
TIP_CHAMFER = 0.4
ROOT_FILLET = 0.635                      # fitted to the Fusion section area (0.42 m)


def _three(angle0: float) -> list[float]:
    return [angle0 + 120.0 * k for k in range(3)]


def carrier_plate(z_bottom: float, pin_angle: float, fit: FitProfile) -> bd.Part:
    """Carrier plate from z_bottom to z_bottom + 17, pegs below z_bottom."""
    z_top = z_bottom + 17.0
    z_pocket_top = z_bottom + 13.0
    body = disc(PLATE_D, z_bottom, z_top) - disc(BORE_D, z_bottom, z_top)
    for a in _three(pin_angle):
        body -= hole(POCKET_D, PIN_R, a, z_bottom, z_pocket_top)
        body -= hole(fit_hole(PIN_D, fit.press), PIN_R, a, z_pocket_top, z_top)
    # R1 rounds on the vertical edges where the pockets break into the bore and the OD
    edges = [
        e for e in body.edges()
        if e.geom_type.name == "LINE"
        and abs(e.tangent_at(0).Z) > 0.999
        and z_bottom - 1e-6 <= min(e.start_point().Z, e.end_point().Z)
        and max(e.start_point().Z, e.end_point().Z) <= z_pocket_top + 1e-6
    ]
    body = body.fillet(POCKET_FILLET, edges)
    for a in _three(pin_angle + SCREW_OFFSET):
        body -= hole(fit.insert_m3, SCREW_R, a, z_bottom, z_bottom + INSERT_DEPTH)
    for a in _three(pin_angle + PEG_OFFSET):
        peg = bd.Cone(PEG_BASE_R, PEG_TIP_R, PEG_H, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        body += polar(PEG_R, a, z_bottom) * bd.Rot(180, 0, 0) * peg
    return body


def carrier_output_plate(z_top: float, pin_angle: float, fit: FitProfile) -> bd.Part:
    """Output-half plate from z_top - 5 to z_top, with the stem cone below it."""
    z_bottom = z_top - 5.0
    body = disc(PLATE_D, z_bottom, z_top)
    body += revolve_rz([(0, z_bottom - 2.0), (14.5, z_bottom - 2.0), (16.5, z_bottom), (0, z_bottom)])
    body -= disc(fit_hole(21.0, fit.press), z_bottom, z_top)            # 6801 bearing recess
    body -= disc(18.0, z_bottom - 0.4, z_bottom)
    for a in _three(pin_angle):
        body -= hole(fit_hole(PIN_D, fit.press), PIN_R, a, z_bottom, z_top)
    for a in _three(pin_angle + SCREW_OFFSET):
        body -= hole(PILOT_D, SCREW_R, a, z_top - PILOT_DEPTH, z_top)
        csk = bd.Cone(CSK_D / 2, PILOT_D / 2, z_top - PILOT_DEPTH - z_bottom,
                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        body -= polar(SCREW_R, a, z_bottom) * csk
    for a in _three(pin_angle + PEG_OFFSET):
        socket = bd.Cone(PEG_BASE_R, SOCKET_TIP_R, SOCKET_DEPTH,
                         align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        body -= polar(PEG_R, a, z_top) * bd.Rot(180, 0, 0) * socket
    return body


def sun_gear(z_bottom: float, width: float, tooth_centre_at_bottom: float,
             top_chamfer: bool = True) -> bd.Part:
    """15T sun, left-hand 15 deg helix, tip chamfered at the bottom (and top)."""
    gear = gears.spur_gear(SUN_TEETH, MODULE, width, backlash=BACKLASH, root_fillet=ROOT_FILLET,
                           helix_angle=-HELIX, tip_chamfer=TIP_CHAMFER if top_chamfer else 0.0)
    if not top_chamfer:
        r_tip = MODULE * SUN_TEETH / 2 + MODULE
        gear &= revolve_rz([(0, 0), (r_tip - TIP_CHAMFER, 0), (r_tip, TIP_CHAMFER),
                            (r_tip, width + 1), (0, width + 1)])
    return bd.Pos(0, 0, z_bottom) * bd.Rot(0, 0, tooth_centre_at_bottom) * gear
