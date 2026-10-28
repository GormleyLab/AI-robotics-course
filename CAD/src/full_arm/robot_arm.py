"""Full arm: base, segment 1 and segment 2 in the robot frame, with J1-J4 kinematics.

The parts are the Session 4/5 subassemblies (joint12_parts, segment_parts),
regrouped by the joint that carries them; placements are in full_arm/common.py.
Zero is the Fusion pose (arm vertical). Links:

- base_link: box, J1 bearings, J1 motor and 20T pulley;
- waist_link (J1): hinge, 160T pulley, cheek 6805s, the whole gearbox;
- upper_arm_link (J2): coupling shaft, segment 1 except its J3 output;
- forearm_link (J3): segment 1's Output block, GT2-80 output and Pins,
  and segment 2 except its J4 output;
- wrist_link (J4): segment 2's J4 output (end effector mount, IF-8).

Segment 2 is driven by the pancake NEMA17 (I-18); segment 1 by the full-size one.

Simplifications: the gearbox rides the waist rigidly (its output carrier
does not turn with J2), and no pulley or idler spins with its joint. The
replica's open issues (design.md §8) come along with the parts.
"""
import cadgen
from cadgen import step

from full_arm.common import (BASE_FROM_SEGMENT, J1_LIMITS, J1_ORIGIN, J2_LIMITS, J2_ORIGIN, J3_LIMITS,
                             J3_ORIGIN, J4_LIMITS, J4_ORIGIN, PITCH, ROBOT_FROM_BASE, SEGMENT_1_FROM_SEGMENT_2,
                             UP, placement)

BASE_LINK = {"box_bottom", "box_top", "thrust_bearing:upper", "thrust_bearing:lower", "bearing_6807",
             "bearing_608", "nema17:j1", "gt2_pulley_20t:j1"}
UPPER_ARM = {"coupling_shaft"}
SEGMENT_OUTPUT = {"output_block", "gt2_80_output", "pin:base", "pin:top"}

KINEMATICS = {
    "mates": [
        cadgen.revolute("j1_waist", parent="#base_link", child="#waist_link",
                        origin=J1_ORIGIN, direction=UP, limits=J1_LIMITS),
        cadgen.revolute("j2_shoulder", parent="#waist_link", child="#upper_arm_link",
                        origin=J2_ORIGIN, direction=PITCH, limits=J2_LIMITS),
        cadgen.revolute("j3_elbow", parent="#upper_arm_link", child="#forearm_link",
                        origin=J3_ORIGIN, direction=PITCH, limits=J3_LIMITS),
        cadgen.revolute("j4_wrist", parent="#forearm_link", child="#wrist_link",
                        origin=J4_ORIGIN, direction=PITCH, limits=J4_LIMITS),
    ],
    "poses": {
        "zero": {"j1_waist": 0, "j2_shoulder": 0, "j3_elbow": 0, "j4_wrist": 0},
        "reach": {"j2_shoulder": 45, "j3_elbow": 45, "j4_wrist": 0},
        "pick": {"j1_waist": 30, "j2_shoulder": 50, "j3_elbow": 54, "j4_wrist": 54},
        "folded": {"j2_shoulder": -40, "j3_elbow": 54, "j4_wrist": 54},
    },
}


def _group(label, parts, loc):
    from cadgen import build123d as bd

    group = loc * bd.Compound(children=parts, label=label)
    group.label = label
    return group


@step(out="../../STEP/full_arm/robot_arm.step", kinematics=KINEMATICS)
def robot_arm():
    from cadgen import build123d as bd

    from belt_arm.belt_drive_arm import segment_parts
    from joint12.joint_1_and_2 import joint12_parts

    base = joint12_parts()
    seg_1, seg_2 = segment_parts(), segment_parts(pancake=True)
    on_base = placement(ROBOT_FROM_BASE)
    on_seg_1 = on_base * placement(BASE_FROM_SEGMENT)
    on_seg_2 = on_seg_1 * placement(SEGMENT_1_FROM_SEGMENT_2)

    def frame(parts):
        return [p for p in parts if p.label not in SEGMENT_OUTPUT]

    def output(parts):
        return [p for p in parts if p.label in SEGMENT_OUTPUT]

    links = [
        _group("base_link", [p for p in base if p.label in BASE_LINK], on_base),
        _group("waist_link", [p for p in base if p.label not in BASE_LINK | UPPER_ARM], on_base),
        _group("upper_arm_link", [
            _group("coupling", [p for p in base if p.label in UPPER_ARM], on_base),
            _group("segment_1", frame(seg_1), on_seg_1),
        ], bd.Location()),
        _group("forearm_link", [
            _group("segment_1_output", output(seg_1), on_seg_1),
            _group("segment_2", frame(seg_2), on_seg_2),
        ], bd.Location()),
        _group("wrist_link", [_group("segment_2_output", output(seg_2), on_seg_2)], bd.Location()),
    ]
    return bd.Compound(children=links, label="robot_arm")


if __name__ == "__main__":
    robot_arm()
