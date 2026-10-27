"""Stage-1 carrier output half with the stage-2 sun (Fusion "Carrier p1 - stage 1 - Output").

Gearbox frame z -41..-12. Plate z -17..-12; stem: Ø29 collar, Ø24.7 neck,
15T sun (z -34.8..-24.4, left-hand helix, tooth centre 10.590 deg at the
bottom), Ø15 shoulder and Ø12 journal in the stage-2 6801 bearing.
"""
from cadgen import step

from gearbox.carrier import carrier_output_plate, sun_gear
from gearbox.common import disc
from lib.tolerances import ACTIVE as FIT, shaft

Z_TOP, PIN_ANGLE = -12.0, 26.41
SUN_Z, SUN_W, SUN_PHASE = -34.8, 10.4, 10.590


def carrier_stage1_output_body():
    body = carrier_output_plate(Z_TOP, PIN_ANGLE)
    body += disc(29.0, -21.0, -19.0)
    body += disc(24.7, -24.4, -21.0)
    body += sun_gear(SUN_Z, SUN_W, SUN_PHASE)
    body += disc(15.0, -36.0, SUN_Z)
    body += disc(shaft(12.0, FIT.press), -41.0, -36.0)    # journal in the stage-2 6801
    return body


@step(out="../../STEP/gearbox/carrier_stage1_output.step")
def carrier_stage1_output():
    part = carrier_stage1_output_body()
    part.label = "carrier_stage1_output"
    return part


if __name__ == "__main__":
    carrier_stage1_output()
