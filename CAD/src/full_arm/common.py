"""Robot frame, subassembly placements and joint axes for the full arm (design.md §7).

Robot frame: origin on the J1 axis at the top face of the box top, +Z up,
+X along the arm's reach at J1 = 0 (base-frame +Y), +Y toward the gearbox
(base-frame -X). J2, J3 and J4 are parallel to +Y, so a positive angle
tips the arm toward +X. Joint zero is the Fusion pose: arm vertical.

Segment 1 sits on the coupling shaft's link face (IF-8): its proximal end
face (arm x = -40) on the coupling top (base z = 100.5), arm +X up, arm +Y
along base +Y, so the arm's Base plate (z = 0) faces +X in the base frame
(the right cheek side). The mirror mounting (Base plate toward the gearbox)
puts the segment motor into the ring gear, front cover and hinge
(2150 mm³), so it is not used. Segment 2 is the same model on segment 1's
Output block distal face (arm x = 234.175), 0.2 mm up in arm z: the block's
M3 holes are at z 3.7 / 40.7, the proximal inserts at 3.5 / 40.5.

Placements are pairs (rotation in degrees for ``bd.Rot``, translation),
applied rotation first, so this module does not touch the CAD kernel.
"""
from __future__ import annotations

from belt_arm.common import J3_X, J3_Y, X_PROXIMAL
from belt_arm.output_block import X_END as OUTPUT_FACE_X, Z0 as OUTPUT_Z0
from joint12.common import J1_X, J1_Y, J2_Y, J2_Z
from joint12.coupling_shaft import X1 as COUPLING_X1, Y0 as COUPLING_Y0, Z_TOP as COUPLING_TOP
from lib import params

# base frame -> robot frame: p_robot = (y - 75, -(x - 75), z - 12)
ROBOT_FROM_BASE = ((0, 0, -90), (-J1_Y, J1_X, -params.BOX_TOP_H))
# arm frame -> base frame: p_base = (96.8 - z, 35 + y, 140.5 + x)
BASE_FROM_SEGMENT = ((0, -90, 0), (COUPLING_X1, COUPLING_Y0, COUPLING_TOP - X_PROXIMAL))
# segment 2 arm frame -> segment 1 arm frame
SEGMENT_1_FROM_SEGMENT_2 = ((0, 0, 0), (OUTPUT_FACE_X - X_PROXIMAL, 0.0, OUTPUT_Z0))


def base_to_robot(p):
    x, y, z = p
    return (y - J1_Y, J1_X - x, z - params.BOX_TOP_H)


def segment_to_base(p):
    x, y, z = p
    return (COUPLING_X1 - z, COUPLING_Y0 + y, COUPLING_TOP - X_PROXIMAL + x)


def segment_2_to_segment_1(p):
    x, y, z = p
    return (x + OUTPUT_FACE_X - X_PROXIMAL, y, z + OUTPUT_Z0)


def _r(p):
    return tuple(round(c, 6) + 0.0 for c in p)


J1_ORIGIN = (0.0, 0.0, 0.0)
J2_ORIGIN = _r(base_to_robot((J1_X, J2_Y, J2_Z)))                                       # hinge axis, z 58.5
J3_ORIGIN = _r(base_to_robot(segment_to_base((J3_X, J3_Y, 0.0))))                        # z 288.5
J4_ORIGIN = _r(base_to_robot(segment_to_base(segment_2_to_segment_1((J3_X, J3_Y, 0.0)))))  # z 562.675
END_FACE = _r(base_to_robot(segment_to_base(segment_2_to_segment_1((OUTPUT_FACE_X, J3_Y, 0.0)))))
UP = (0.0, 0.0, 1.0)
PITCH = (0.0, 1.0, 0.0)

# Joint limits (deg), from checks/joint_clearance.py (I-14, I-16; J3/J4 after the I-17 fix).
# J3/J4 negative side: the Output block meets the idler-2 jack screw head at -95 deg
# with the screw backed out to slack (-97 at a 280 mm loop), I-4; +103 is the Wall.
J1_LIMITS = (-40, 40)
J2_LIMITS = (-63, 63)
J3_LIMITS = (-94, 103)
J4_LIMITS = (-94, 103)


def placement(pair):
    """``bd.Location`` for a (rotation, translation) pair."""
    from cadgen import build123d as bd

    rot, pos = pair
    return bd.Pos(*pos) * bd.Rot(*rot)
