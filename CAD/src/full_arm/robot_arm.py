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
import build123d as bd
from cadgen import step
from cadgen.ap242 import mechanism_state

from full_arm.common import (BASE_FROM_SEGMENT, JOINTS, POSES, ROBOT_FROM_BASE, SEGMENT_1_FROM_SEGMENT_2,
                             placement)

BASE_LINK = {"box_bottom", "box_top", "thrust_bearing:upper", "thrust_bearing:lower", "bearing_6807",
             "bearing_608", "nema17:j1", "gt2_pulley_20t:j1"}
UPPER_ARM = {"coupling_shaft"}
SEGMENT_OUTPUT = {"output_block", "gt2_80_output", "pin:base", "pin:top"}


def _group(label, parts, loc):
    group = loc * bd.Compound(children=parts, label=label)
    group.label = label
    return group


def _add_joints(links):
    """J1-J4 from full_arm/common.JOINTS. The links are siblings in the robot
    frame, so each joint is given in world coordinates and paired by label:
    a revolute joint on the parent link, a rigid joint at the same frame on
    the child. Every joint reads 0 as built (the Fusion pose)."""
    by_label = {link.label: link for link in links}
    for j in JOINTS:
        parent, child = by_label[j.parent], by_label[j.child]
        joint = bd.RevoluteJoint(j.name, parent, axis=bd.Axis(j.origin, j.direction), angular_range=j.limits)
        bd.RigidJoint(j.name, child, joint.location)


@step(out="../../STEP/full_arm/robot_arm.step")
def robot_arm():
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
    _add_joints(links)
    arm = bd.Compound(children=links, label="robot_arm")
    for name, values in POSES.items():
        mechanism_state(arm, name, **values)
    return arm


if __name__ == "__main__":
    robot_arm()
