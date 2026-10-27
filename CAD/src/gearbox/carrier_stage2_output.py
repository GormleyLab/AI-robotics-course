"""Stage-2 carrier output half = gearbox output shaft (Fusion "Carrier p2 - stage 2 - Output v5").

Gearbox frame z -90..-36. Plate z -41..-36; Ø29 shoulder, Ø25 x 30 shaft
through the front-cover and hinge 6805 bearings, and a 21.65 AF x 15 hex
(IF-7) that drives the coupling shaft.
"""
from cadgen import build123d as bd
from cadgen import step

from gearbox.carrier import carrier_output_plate
from gearbox.common import disc
from lib import params

Z_TOP, PIN_ANGLE = -36.0, 43.46
HEX_AF = 21.65                     # measured; design.md lists 21.48 for the arm Pins
HEX_FLAT_ANGLE = -16.54            # normal of one hex flat


def carrier_stage2_output_body():
    body = carrier_output_plate(Z_TOP, PIN_ANGLE)
    body += disc(29.0, -45.0, -43.0)
    body += disc(params.OUTPUT_SHAFT_D, -75.0, -45.0)
    hex_prism = bd.extrude(bd.RegularPolygon(HEX_AF / 2, 6, major_radius=False, rotation=HEX_FLAT_ANGLE + 30.0), 15.0)
    body += bd.Pos(0, 0, -90.0) * hex_prism
    return body


@step(out="../../STEP/gearbox/carrier_stage2_output.step")
def carrier_stage2_output():
    part = carrier_stage2_output_body()
    part.label = "carrier_stage2_output"
    return part


if __name__ == "__main__":
    carrier_stage2_output()
