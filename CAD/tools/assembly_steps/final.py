"""The final assembly chapter's steps and pictures (docs/assembly-5-final.md).

Assembly: the robot frame of full_arm/robot_arm.py. Origin on J1 at the top of the box top,
+Z up, +Y toward the gearbox, +X along the arm's reach. The arm stands straight up at zero.

Both segments use the same labels, so parts are named "<group>/<label>", as in
"segment_2/base". This chapter adds no CAD parts, only the link screws.

Parts with identical geometry render in one colour, whatever the scene says, and the arm has
several of the motor, the 6805 and the 20T pulley. So those always go in ``added``, in one
colour each, and never in ``built``: otherwise a pale copy could turn a coloured one pale.
"""
from __future__ import annotations

from assembly_steps import Guide, Hw, Label, Step, View, along_z
from assembly_steps import joint1, joint2, segment
from assembly_steps.gearbox import WHOLE as GEARBOX

NAME = "final"
ASSEMBLY = "STEP/full_arm/robot_arm.step"


def leaf_key(leaf) -> str:
    return "/".join(leaf.path[-2:])


BASE_LINK = {"box_bottom", "box_top", "thrust_bearing:upper", "thrust_bearing:lower", "bearing_6807",
             "bearing_608", "nema17:j1", "gt2_pulley_20t:j1"}
OUTPUT = {"output_block", "gt2_80_output", "pin:base", "pin:top"}


def _base_key(label: str) -> str:
    if label == "coupling_shaft":
        return "coupling/coupling_shaft"
    if label in GEARBOX:
        return f"planetary_gearbox/{label}"
    return f"{'base_link' if label in BASE_LINK else 'waist_link'}/{label}"


def _segment(number: int, parts=segment.PARTS) -> tuple[str, ...]:
    group = f"segment_{number}"
    names = []
    for label in parts:
        if number == 2 and label.startswith("nema17"):
            label = "nema17_pancake:j3"
        names.append(f"{group}_output/{label}" if label in OUTPUT else f"{group}/{label}")
    return tuple(names)


BASE = tuple(_base_key(p) for p in (*joint1.PARTS, *joint2.PARTS, *GEARBOX))
SEGMENT_1, SEGMENT_2 = _segment(1), _segment(2)
COVERAGE = (*BASE, *SEGMENT_1, *SEGMENT_2)
PARTS: tuple[str, ...] = ()
PREBUILT = COVERAGE

# Parts the base and the segments share. Everything else on the base stays pale.
SHARED = {"nema17": "#9d86c9", "gt2_pulley_20t": "#93a0ac", "bearing_6805": "#98a3ad"}
BASE_COLOURS = {"hinge": "#c9ced6", "coupling_shaft": "#d0a044"}


def _shared_colour(key: str) -> str | None:
    return SHARED.get(key.split("/")[-1].split(":")[0])


def colour_of(key: str) -> str:
    label = key.split("/")[-1]
    if label.startswith("nema17_pancake"):
        return "#b08fd8"
    return _shared_colour(key) or BASE_COLOURS.get(label) or segment.colour_of(label)


def _pale(labels):
    """(built, added): every part pale, except the shared ones, which can only be coloured."""
    return (tuple(p for p in labels if not _shared_colour(p)),
            {p: (0.0, 0.0, 0.0) for p in labels if _shared_colour(p)})


# Robot-frame positions: see design.md §7.
COUPLING_SEAT_Z, BLOCK_SEAT_Z = 68.5, 345.675
LINK_X = (-36.5, 36.5)
COUPLING_Y, BLOCK_Y = (-18.3, 18.7), (-18.1, 18.9)
J2_Z, J3_Z, J4_Z, END_Z = 58.5, 288.5, 562.675, 636.85

_BASE_BUILT, _BASE_SHARED = _pale(BASE)

overview = Step(
    "overview", "The whole arm",
    views=(
        View("overview_arm",
             built=_BASE_BUILT, added={**_BASE_SHARED, **along_z((*SEGMENT_1, *SEGMENT_2), 0.0)},
             azimuth=-35.0, elevation=12.0,
             labels=(Label("Base and shoulder (Chapters 1 to 3)", at=(-40, 40, 40), side="left"),
                     Label("Segment 1", at=(40, -20, 190), side="right"),
                     Label("Segment 2", at=(40, -20, 460), side="right"),
                     Label("Pancake motor on segment 2", at=(0, -40, 390), side="left"),
                     Label("Full-size motor on segment 1", at=(0, -50, 120), side="left"),
                     Label("Output blocks: joints 3 and 4", at=(40, 0, 340), side="right"))),
    ),
)

step49 = Step("49", "Get ready")

_S1_DROP = 70.0
_COUPLING_SCREWS = tuple(Hw.line("m3x25", (x, y, COUPLING_SEAT_Z), (0, 0, 1)) for x in LINK_X for y in COUPLING_Y)
step50 = Step(
    "50", "Bolt segment 1 to the coupling",
    views=(
        View("step50a_lower",
             built=_BASE_BUILT, added={**_BASE_SHARED, **along_z(SEGMENT_1, _S1_DROP)},
             guides=(Guide.between((36.5, -18.3, 88.5), (36.5, -18.3, 158.5)),
                     Guide.between((-36.5, -18.3, 88.5), (-36.5, -18.3, 158.5))),
             azimuth=-35.0, elevation=14.0,
             labels=(Label("Motor toward the shorter cheek", at=(0, -50, 190), side="left"),
                     Label("Gearbox: not on this side", at=(0, 70, 101), side="right"),
                     Label("Segment 1, straight down", at=(40, -20, 280), side="right"),
                     Label("Coupling's top face", at=(30, 0, 88.5), side="right"))),
        View("step50b_section",
             added=along_z(("coupling/coupling_shaft", "waist_link/hinge", "segment_1/base", "segment_1/wall",
                            "segment_1/nema17:j3"), 0.0),
             hardware=_COUPLING_SCREWS[:1] + _COUPLING_SCREWS[2:3],
             clip_y=COUPLING_Y[0], elevation=0.0, frame=1.0,
             labels=(Label("M3 × 25, into the insert in the base plate", at=(36.5, -18.3, 90), side="right"),
                     Label("Head up inside the coupling's corner", at=(-36.5, -18.3, 68), side="left"),
                     Label("Hinge's shorter cheek", at=(-20, -18.3, 40), side="left"))),
    ),
)

_BLOCK_SCREWS = tuple(Hw.line("m3x25", (x, y, BLOCK_SEAT_Z), (0, 0, 1)) for x in LINK_X for y in BLOCK_Y)
_S2_DROP = 70.0
_SEG1_ADDED = along_z(SEGMENT_1, 0.0)
step51 = Step(
    "51", "Bolt segment 2 to the output block",
    views=(
        View("step51a_lower",
             built=_BASE_BUILT, added={**_BASE_SHARED, **_SEG1_ADDED, **along_z(SEGMENT_2, _S2_DROP)},
             guides=(Guide.between((36.5, -18.1, 362.7), (36.5, -18.1, 432.7)),
                     Guide.between((-36.5, -18.1, 362.7), (-36.5, -18.1, 432.7))),
             azimuth=-35.0, elevation=12.0,
             labels=(Label("Segment 2: motor on the same side", at=(0, -30, 460), side="left"),
                     Label("Segment 1's output block", at=(40, 0, 345), side="right"))),
        View("step51b_section",
             added=along_z(("segment_1_output/output_block", "segment_2/base", "segment_2/wall",
                            "segment_2/nema17_pancake:j3"), 0.0),
             hardware=_BLOCK_SCREWS[:1] + _BLOCK_SCREWS[2:3],
             clip_y=BLOCK_Y[0], elevation=0.0, frame=1.0,
             labels=(Label("M3 × 25, into the insert in segment 2", at=(36.5, -18.1, 364), side="right"),
                     Label("Head inside the block's end plate", at=(-36.5, -18.1, 345), side="left"))),
    ),
)

step52 = Step(
    "52", "Check the whole arm",
    views=(
        View("step52_joints",
             built=_BASE_BUILT, added={**_BASE_SHARED, **along_z((*SEGMENT_1, *SEGMENT_2), 0.0)},
             azimuth=-35.0, elevation=12.0,
             labels=(Label("End-effector face", at=(0, 0, END_Z), side="right"),
                     Label("Joint 4: −94° to +103°", at=(0, -22, J4_Z), side="right"),
                     Label("Joint 3: −94° to +103°", at=(0, -22, J3_Z), side="right"),
                     Label("Joint 2: ±63°", at=(0, 0, J2_Z), side="right"),
                     Label("Joint 1: ±124°", at=(0, 40, 6), side="left"))),
    ),
)

STEPS = [overview, step49, step50, step51, step52]
