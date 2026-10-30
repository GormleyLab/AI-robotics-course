"""NEMA17 mount plate, gearbox frame z 14..32 (design.md §3, I-25).

Fusion "NEMA17 thicker mount" (STEP/imported/fusion/NEMA17_thicker_mount.step):
41 x 56 x 18 plate with R5 corners, Ø24 bore for the motor boss. It is 18
thick (was 10) so the motor face sits at z = 32 and the set screw in the
input shaft (z = 16.8) lands on the shaft's flat, not its round first ~10 mm.
The motor screws (31 mm pattern) go in from the back-cover side (z = 14)
through Ø7 x 3 counterbores; 4 x M3 clearance holes on a 33 x 48 rectangle
take screws into the back-cover inserts. A Ø7 radial hole from the -X side
reaches the bore at z = 19.5.
"""
import build123d as bd
from cadgen import step

from gearbox.common import disc, hole
from lib import params
from lib.tolerances import profile

FIT = profile("nema17_mount")

Z0, Z1 = 14.0, 32.0
PLATE_X, PLATE_Y, CORNER_R = 41.0, 56.0, 5.0
MOTOR_SCREW_R = params.NEMA17_BOLT_SPACING / 2 * 2**0.5   # 21.92
CBORE_D, CBORE_DEPTH = 7.0, 3.0
COVER_SCREW_R, COVER_SCREW_ANGLES = 29.125, (55.49, 124.51, -55.49, -124.51)
ACCESS_D, ACCESS_Z = 7.0, 19.5


def nema17_mount_body():
    plate = bd.Pos(0, 0, Z0) * bd.extrude(bd.RectangleRounded(PLATE_X, PLATE_Y, CORNER_R), Z1 - Z0)
    plate -= disc(params.NEMA17_PILOT_D + 2.0, Z0, Z1)  # Ø24 boss bore
    for a in (45.0, 135.0, -45.0, -135.0):
        plate -= hole(FIT.m3_clear, MOTOR_SCREW_R, a, Z0, Z1)
        plate -= hole(CBORE_D, MOTOR_SCREW_R, a, Z0, Z0 + CBORE_DEPTH)
    for a in COVER_SCREW_ANGLES:
        plate -= hole(FIT.m3_clear, COVER_SCREW_R, a, Z0, Z1)
    access_len = PLATE_X / 2 - 11.0  # from the -X edge into the Ø24 bore
    access = bd.Pos(-(PLATE_X / 2 - access_len / 2), 0, ACCESS_Z) * bd.Rot(0, 90, 0) * bd.Cylinder(
        ACCESS_D / 2, access_len)
    return plate - access


@step(out="../../STEP/gearbox/nema17_mount.step")
def nema17_mount():
    part = nema17_mount_body()
    part.label = "nema17_mount"
    return part


if __name__ == "__main__":
    nema17_mount()
