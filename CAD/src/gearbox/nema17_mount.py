"""NEMA17 mount plate, gearbox frame z 14..24 (design.md §3).

41 x 56 x 10 plate with R5 corners, Ø24 bore for the motor boss. The motor
screws (31 mm pattern) are countersunk from the back-cover side (z = 14); 4 x
Ø3 holes on a 33 x 48 rectangle take screws into the back-cover inserts. A
Ø3.5 radial hole from the -X side reaches the bore.
"""
from cadgen import build123d as bd
from cadgen import step

from gearbox.common import disc, hole, polar
from lib import params

Z0, Z1 = 14.0, 24.0
PLATE_X, PLATE_Y, CORNER_R = 41.0, 56.0, 5.0
MOTOR_SCREW_R = params.NEMA17_BOLT_SPACING / 2 * 2**0.5   # 21.92
MOTOR_SCREW_D = 3.0
CSK_D, CSK_DEPTH = 7.0, 2.0
COVER_SCREW_R, COVER_SCREW_ANGLES = 29.125, (55.49, 124.51, -55.49, -124.51)
ACCESS_D, ACCESS_Z = 3.5, 19.5


def nema17_mount_body():
    plate = bd.Pos(0, 0, Z0) * bd.extrude(bd.RectangleRounded(PLATE_X, PLATE_Y, CORNER_R), Z1 - Z0)
    plate -= disc(params.NEMA17_PILOT_D + 2.0, Z0, Z1)  # Ø24 boss bore
    for a in (45.0, 135.0, -45.0, -135.0):
        plate -= hole(MOTOR_SCREW_D, MOTOR_SCREW_R, a, Z0, Z1)
        csk = bd.Cone(CSK_D / 2, MOTOR_SCREW_D / 2, CSK_DEPTH, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        plate -= polar(MOTOR_SCREW_R, a, Z0) * csk
    for a in COVER_SCREW_ANGLES:
        plate -= hole(MOTOR_SCREW_D, COVER_SCREW_R, a, Z0, Z1)
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
