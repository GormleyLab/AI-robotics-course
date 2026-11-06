"""The hinge and joint 2 chapter's steps and pictures (docs/assembly-3-hinge-joint2.md).

Assembly: as joint1.py, J1 at (0, 0). J2 runs along X at y = 0, z = 70.5, and the gearbox
is on the -X side. Cheek x: left -36..-29, right 27..34. The gearbox comes from Chapter 1
and is shown as one colour.
"""
from __future__ import annotations

import math

from assembly_steps import Guide, Hw, Label, Step, View, Vec, along_z
from assembly_steps.gearbox import WHOLE as GEARBOX
from assembly_steps.joint1 import COVERAGE, LEFT_6805, MOTOR_SET, PARTS as CHAPTER_2, STACK

NAME = "joint2"
ASSEMBLY = "STEP/joint12/joint_1_and_2.step"
ORIGIN: Vec = (75.0, 75.0, 0.0)

RIGHT_6805, COUPLING = "bearing_6805:right_cheek", "coupling_shaft"
PARTS = (COUPLING, RIGHT_6805)
PREBUILT = (*CHAPTER_2, *GEARBOX)
ALSO_COUNTED = (LEFT_6805,)
COVERAGE = COVERAGE
BASE = CHAPTER_2

# Parts with identical geometry render in one colour, whatever the scene says. So the gearbox's
# motor and 6805 can't be gearbox blue without turning the J1 motor and the cheek bearings blue too.
SHARED_GREY = "#b4bbc3"
COLOURS = {COUPLING: "#d0a044", RIGHT_6805: SHARED_GREY, LEFT_6805: SHARED_GREY, "bearing_6805:output": SHARED_GREY,
           "nema17": SHARED_GREY, "hinge": "#c77db0"}
GEARBOX_COLOUR = "#6f8fc9"


def colour_of(label: str) -> str:
    return COLOURS.get(label, GEARBOX_COLOUR)


J2_Z, BOLT_R = 70.5, 39.25
ALIGN_LEFT = -6.8                      # the coupling against the left cheek, stub out of the right seat
SEAT_X, COVER_POCKET_X = -31.0, -39.2  # hinge screw head seat; the M3 x 12 head seats in the cover
TURNED = 40.0                          # J2 angle that clears the 30 and 150 degree screw lines


def _on_circle(angle: float, x: float) -> Vec:
    a = math.radians(angle)
    return (x, BOLT_R * math.cos(a), J2_Z + BOLT_R * math.sin(a))


FIRST, SECOND = (-30.0, 90.0, 210.0), (30.0, 150.0)
ALL_HOLES = (*FIRST, *SECOND)
J2_AXIS = ((0.0, 0.0, J2_Z), (1.0, 0.0, 0.0))
_INTO_RING: Vec = (-1.0, 0.0, 0.0)

overview = Step(
    "overview", "Joint 2",
    views=(
        View("overview_section",
             added=along_z(("hinge", LEFT_6805, RIGHT_6805, COUPLING, *GEARBOX), 0.0),
             clip_y=0.0, elevation=0.0,
             labels=(Label("Coupling shaft", at=(5, 0, 90), side="left"),
                     Label("Right-cheek 6805", at=(30.5, 0, 56), side="left"),
                     Label("Hinge", at=(30.5, 0, 25), side="left"),
                     Label("Gearbox output hex in the socket", at=(-15, 0, 70.5), side="right"),
                     Label("Left-cheek 6805", at=(-32.5, 0, 56), side="right"),
                     Label("Front cover", at=(-41, 0, 30), side="right"))),
    ),
)

parts_sheets = Step(
    "parts", "Parts",
    views=(
        View("parts_sheet", azimuth=-65.0, elevation=38.0, frame=1.0,
             layout={COUPLING: (-45, 0), RIGHT_6805: (55, 25)},
             hardware=(Hw.at("m3x20", 55, -30, 2),),
             labels=(Label("Coupling shaft (printed)", COUPLING, side="left"),
                     Label("6805 bearing", RIGHT_6805, side="right"),
                     Label("M3 × 20 × 5", "hw:0", side="right"))),
    ),
)

step27 = Step("27", "Check the fits")

_HINGE = ("hinge", LEFT_6805, "box_top")
step28 = Step(
    "28", "Put the coupling between the cheeks",
    adds=(COUPLING, RIGHT_6805),
    views=(
        View("step28a_drop",
             built=_HINGE, added={COUPLING: (ALIGN_LEFT, 0, 65)},
             guides=(Guide.between((0, 0, 100), (0, 0, 135)),), azimuth=-30.0, elevation=24.0,
             labels=(Label("Stub: toward the shorter cheek", at=(ALIGN_LEFT + 30, 0, J2_Z + 65), side="right"),
                     Label("Gearbox cheek", at=(-32, -30, 90), side="left"),
                     Label("Right seat still empty", at=(30.5, -20, 62), side="right"))),
        View("step28b_right_6805",
             built=_HINGE, added={COUPLING: (ALIGN_LEFT, 0, 0), RIGHT_6805: (45, 0, 0)},
             guides=(Guide.between((34, 0, J2_Z), (72, 0, J2_Z)),), clip_y=0.0, elevation=0.0, frame=1.05,
             labels=(Label("6805, pressed in from outside", RIGHT_6805, side="left"),
                     Label("Coupling held against the left cheek", at=(0, 0, 90), side="right"))),
    ),
)

step29 = Step(
    "29", "Press the stub into the right bearing",
    views=(
        View("step29_stub",
             built=_HINGE, added={COUPLING: (0, 0, 0), RIGHT_6805: (0, 0, 0)},
             hardware=(Hw.line("plate", (34.0, 0, J2_Z), (1, 0, 0)),
                       Hw.line("spacer", (-22.2, 0, J2_Z), _INTO_RING)),
             clip_y=0.0, elevation=0.0, frame=1.05,
             labels=(Label("Plate over the cheek and the bearing", "hw:0", side="left"),
                     Label("Ø24 spacer through the left bearing", "hw:1", side="right"),
                     Label("Stub stops at the plate", at=(33.5, 0, J2_Z + 10), side="left"))),
    ),
)

_OUT: Vec = (45.0, 0.0, 0.0)
step30 = Step(
    "30", "Take out five front cover screws",
    views=(
        View("step30_screws",
             added=along_z(GEARBOX, 0.0),
             hardware=(*(Hw.line("m3x12", _on_circle(a, COVER_POCKET_X), _INTO_RING, offset=_OUT) for a in ALL_HOLES),
                       Hw.line("m3x12", _on_circle(270.0, COVER_POCKET_X), _INTO_RING, built=True)),
             guides=tuple(Guide.between(_on_circle(a, -36.0), _on_circle(a, -3.0)) for a in ALL_HOLES),
             azimuth=25.0, elevation=16.0,
             labels=(Label("M3 × 12 out × 5", "hw:2", side="right"),
                     Label("This one stays, at the bottom", at=(-36, 0, 31.25), side="right"))),
    ),
)

_BUILT = (*_HINGE, COUPLING, RIGHT_6805)
_INSIDE = {"built": ("hinge", LEFT_6805, "box_top", COUPLING, *GEARBOX), "trim_x": {"hinge": 20.0},
           "azimuth": 12.0, "elevation": 14.0}
_SECTION = ("hinge", LEFT_6805, RIGHT_6805, COUPLING, "front_cover", "ring_gear", "bearing_6805:output",
            "carrier_stage2_output")
_FIRST_SCREWS = tuple(Hw.line("m3x20", _on_circle(a, SEAT_X), _INTO_RING, offset=(30, 0, 0)) for a in FIRST)
step31 = Step(
    "31", "Slide the gearbox in and start three screws",
    views=(
        View("step31a_gearbox",
             built=_BUILT, added=along_z(GEARBOX, 0.0) | {g: (-60.0, 0.0, 0.0) for g in GEARBOX},
             guides=(Guide.between((-82, 0, J2_Z), (-36, 0, J2_Z)),), azimuth=-140.0, elevation=20.0,
             labels=(Label("Gearbox, hex first", "front_cover", side="left"),
                     Label("Coupling socket, lined up with the hex", at=(-22, 0, 70.5), side="right"),
                     Label("Access slot faces this way", at=(-175, -20.5, 70.5), side="left"))),
        View("step31b_screws",
             **_INSIDE,
             hardware=_FIRST_SCREWS,
             guides=tuple(Guide.between(_on_circle(a, SEAT_X), _on_circle(a, SEAT_X + 12)) for a in FIRST),
             labels=(Label("M3 × 20 × 3, with the coupling square", "hw:1", side="right"),
                     Label("Right cheek cut away in this picture", at=(20, -35, 28), side="right"))),
        View("step31c_section",
             added=along_z(_SECTION, 0.0),
             hardware=(Hw.line("m3x20", _on_circle(90.0, SEAT_X), _INTO_RING),),
             clip_y=0.0, elevation=0.0,
             labels=(Label("Screw: through cheek and cover into the insert", at=(-41, 0, 109.75), side="right"),
                     Label("Hex in the socket", at=(-15, 0, J2_Z), side="left"),
                     Label("Cover flat on the cheek", at=(-36, 0, 40), side="right"))),
    ),
)

_SECOND_SCREWS = tuple(Hw.line("m3x20", _on_circle(a, SEAT_X), _INTO_RING, offset=(30, 0, 0)) for a in SECOND)
step32 = Step(
    "32", "Turn joint 2 and fit the last two screws",
    views=(
        View("step32_screws",
             **_INSIDE, turned={COUPLING: (*J2_AXIS, TURNED)},
             hardware=(*_SECOND_SCREWS, *(Hw.line("m3x20", _on_circle(a, SEAT_X), _INTO_RING, built=True) for a in FIRST)),
             guides=tuple(Guide.between(_on_circle(a, SEAT_X), _on_circle(a, SEAT_X + 12)) for a in SECOND),
             labels=(Label("M3 × 20 × 2, with the coupling turned about 40°", "hw:0", side="right"),)),
    ),
)

step33 = Step(
    "33", "Check joint 2",
    views=(
        View("step33_closed",
             built=BASE, added=along_z((COUPLING, RIGHT_6805, *GEARBOX), 0.0), azimuth=-50.0, elevation=24.0,
             labels=(Label("Gearbox on the left cheek", "ring_gear", side="left"),
                     Label("Coupling: turn gently by hand", COUPLING, side="right"),
                     Label("Top face: arm segment 1 bolts here", at=(0, 20, 100.5), side="right"))),
    ),
)

STEPS = [overview, parts_sheets, step27, step28, step29, step30, step31, step32, step33]
