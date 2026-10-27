"""Stage-2 carrier output half = gearbox output shaft (Fusion "Carrier p2 - stage 2 - Output v5").

Gearbox frame z -83.8..-36. Plate z -41..-36; Ø29 shoulder, Ø25 x 24.3 shaft
through the front-cover and hinge 6805 bearings, and a 21.48 AF x 14.5 hex
(IF-7) that drives the coupling shaft.

I-2 fix (Fusion: z -90..-36, Ø25 x 30 shaft, 21.65 AF x 15 hex at a -16.54 deg
flat normal). In the assembly the Fusion shaft ran 5.2 mm into the coupling
face and the hex 5.2 mm past the socket floor, line-to-line and 43.5 deg off
the socket. Now the shaft stops 0.5 mm short of the coupling face, the hex
stops 1 mm short of the socket floor (14 mm engaged), it is the Pin size
(0.17 under the socket) and its corners are on gearbox +-Y, which is base
+-Z, as in the coupling socket.
"""
from cadgen import build123d as bd
from cadgen import step

from gearbox.carrier import carrier_output_plate
from gearbox.common import disc
from lib import params

Z_TOP, PIN_ANGLE = -36.0, 43.46
HEX_AF = params.OUTPUT_HEX_AF      # 21.48 (I-2 fixed: Fusion 21.65)
HEX_FLAT_ANGLE = 0.0               # normal of one hex flat (I-2 fixed: Fusion -16.54)
SHAFT_END_Z = -69.3                # 0.5 short of the coupling face (I-2 fixed: Fusion -75)
HEX_LEN = 14.5                     # 1.0 short of the socket floor (I-2 fixed: Fusion 15)


def carrier_stage2_output_body():
    body = carrier_output_plate(Z_TOP, PIN_ANGLE)
    body += disc(29.0, -45.0, -43.0)
    body += disc(params.OUTPUT_SHAFT_D, SHAFT_END_Z, -45.0)
    hex_prism = bd.extrude(bd.RegularPolygon(HEX_AF / 2, 6, major_radius=False, rotation=HEX_FLAT_ANGLE + 30.0), HEX_LEN)
    body += bd.Pos(0, 0, SHAFT_END_Z - HEX_LEN) * hex_prism
    return body


@step(out="../../STEP/gearbox/carrier_stage2_output.step")
def carrier_stage2_output():
    part = carrier_stage2_output_body()
    part.label = "carrier_stage2_output"
    return part


if __name__ == "__main__":
    carrier_stage2_output()
