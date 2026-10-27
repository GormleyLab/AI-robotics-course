"""Input shaft = stage-1 sun (Fusion "Input shaft v5"), gearbox frame z -16.8..19.6.

Ø11.94 journal (stage-1 6801) and Ø15 shoulder below the 15T left-hand
helical sun (z -10.8..~0.9, tooth centre 11.998 deg at z = -10.8, tips
chamfered, conical top); Ø16.94 neck with a Ø19.94 collar, then the Ø16.94
journal through the 6803 in the back cover. Ø5.3 motor bore with a D-flat
(x >= -2.138) and a Ø4 set-screw hole from -X at z = 16.8.
"""
from cadgen import build123d as bd
from cadgen import step

from gearbox.carrier import sun_gear
from gearbox.common import revolve_rz
from lib.tolerances import ACTIVE as FIT, hole as fit_hole

# Outer envelope (r, z): journal, shoulder, gear tips with 0.4 chamfers,
# conical gear top, neck, collar with 45 deg chamfer, upper journal.
R12 = 5.97 - FIT.press / 2              # Ø11.94 journal in the 6801 (Fusion: 0.06 under the bore)
R17 = 8.47 - FIT.press / 2              # Ø16.94 neck and journal in the 6803
ENVELOPE = [
    (0, -16.8), (R12, -16.8), (R12, -11.8), (7.5, -11.8), (7.5, -10.8),
    (12.35, -10.8), (12.75, -10.4), (12.75, -0.8), (12.35, -0.4), (9.162, 0.908),
    (R17, 1.6), (R17, 3.4), (9.97, 3.4), (9.97, 4.486), (R17, 5.986 + FIT.press / 2), (R17, 19.6), (0, 19.6),
]
# Solid core: the same profile with the gear zone at the root radius.
CORE = ENVELOPE[:5] + [(9.375, -10.8), (9.375, 0.695)] + ENVELOPE[9:]
SUN_Z, SUN_PHASE = -10.8, 11.998
BORE_D, BORE_Z0, FLAT_X = fit_hole(5.3, FIT.slip), -5.4, -2.138 - FIT.slip / 2
SET_SCREW_D, SET_SCREW_Z = 4.0, 16.8


def input_shaft_body():
    envelope = revolve_rz(ENVELOPE)
    body = revolve_rz(CORE)
    body += sun_gear(SUN_Z, 0.908 - SUN_Z + 0.5, SUN_PHASE, top_chamfer=False)
    body &= envelope
    bore = bd.Pos(0, 0, BORE_Z0) * bd.extrude(
        bd.Circle(BORE_D / 2) - bd.Pos(FLAT_X - 5.0, 0) * bd.Rectangle(10.0, 10.0), 19.6 - BORE_Z0)
    body -= bore
    body -= bd.Pos(-6.0, 0, SET_SCREW_Z) * bd.Rot(0, 90, 0) * bd.Cylinder(SET_SCREW_D / 2, 12.0)
    return body


@step(out="../../STEP/gearbox/input_shaft.step")
def input_shaft():
    part = input_shaft_body()
    part.label = "input_shaft"
    return part


if __name__ == "__main__":
    input_shaft()
