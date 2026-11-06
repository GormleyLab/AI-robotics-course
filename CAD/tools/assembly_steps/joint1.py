"""The base and joint 1 chapter's steps and pictures (docs/assembly-guide.md).

Assembly: the base frame of joint12/joint_1_and_2.py, with ORIGIN putting J1 at (0, 0).
+Z up, and the J1 motor toward +X. z = 0 is the top of the box bottom. Positions are
from the joint12 part modules. The stack goes together from the pulley up, so nothing
has to be flipped; the pictures keep +Z up throughout.
"""
from __future__ import annotations

import math

from assembly_steps import Guide, Hw, Label, Step, View, Vec, along_z
from assembly_steps.gearbox import WHOLE as GEARBOX

NAME = "joint1"
ASSEMBLY = "STEP/joint12/joint_1_and_2.step"
ORIGIN: Vec = (75.0, 75.0, 0.0)

COLOURS = {
    "box_bottom": "#62b39a",
    "box_top": "#5ba7c4",
    "hinge": "#c77db0",
    "coupling_shaft": "#d0a044",
    "gt2_pulley_160t": "#93bb63",
    "gt2_pulley_20t": "#6fb35a",
    "nema17": "#9d86c9",
    "thrust_bearing": "#e0774a",
    "bearing_6807": "#6f8fc9",
    "bearing_608": "#e3bd45",
    "bearing_6805": "#98a3ad",
}


def colour_of(label: str) -> str:
    return next(colour for key, colour in COLOURS.items() if label.startswith(key))


UPPER, LOWER = "thrust_bearing:upper", "thrust_bearing:lower"
LEFT_6805, MOTOR, PULLEY_20T = "bearing_6805:left_cheek", "nema17:j1", "gt2_pulley_20t:j1"
HINGE_SET = ("hinge", LEFT_6805)
STACK = ("gt2_pulley_160t", LOWER, "box_top", "bearing_6807", UPPER, *HINGE_SET)
MOTOR_SET = (MOTOR, PULLEY_20T)
PARTS = (*STACK, *MOTOR_SET, "box_bottom", "bearing_608")
COVERAGE = (*PARTS, *GEARBOX, "coupling_shaft", "bearing_6805:right_cheek")

CENTRES = 83.043                                   # J1 to motor, 370 mm belt
SLACK = 18.0                                       # the motor at the slot's hinge end (x = 140)
BELT_Z = -11.0                                     # the 6 mm belt, centred on the 160T band
BOX_M5 = ((7.5, 7.5), (90.0, 7.5), (172.5, 7.5), (7.5, 142.5), (90.0, 142.5), (172.5, 142.5), (7.5, 75.0))
BOX_XY = tuple((x - ORIGIN[0], y - ORIGIN[1]) for x, y in BOX_M5)
CLAMP_R, CLAMP_ANGLES = 10.0, (0.0, 90.0, 180.0, 270.0)
MOTOR_XY = tuple((CENTRES + dx, dy) for dx in (-15.5, 15.5) for dy in (-15.5, 15.5))


def _polar(x: float, y: float) -> tuple[float, float]:
    return math.hypot(x, y), math.degrees(math.atan2(y, x))


def _box_screws(kind: str, z: float, lift: float) -> tuple[Hw, ...]:
    return tuple(Hw(kind, *_polar(x, y), z, down=True, offset=(0, 0, lift)) for x, y in BOX_XY)


def _box_guides(z0: float, z1: float) -> tuple[Guide, ...]:
    return tuple(Guide(*_polar(x, y), z0, z1) for x, y in BOX_XY)


overview = Step(
    "overview", "The whole base",
    views=(
        View("overview_section", added=along_z(PARTS, 0.0), clip_y=0.0, elevation=0.0,
             hardware=(Hw.at("belt_j1", 0, 0, BELT_Z),),
             labels=(Label("Motor", MOTOR, at=(CENTRES, 0, 40), side="left"),
                     Label("20T pulley", at=(CENTRES, 0, -8), side="left"),
                     Label("Box top", at=(50, 0, 6), side="left"),
                     Label("160T pulley", at=(35, 0, -8), side="left"),
                     Label("Box bottom", at=(70, 0, -27), side="left"),
                     Label("Hinge", at=(-30, 0, 60), side="right"),
                     Label("Upper thrust bearing", at=(-25, 0, 18), side="right"),
                     Label("6807 bearing", at=(-20.5, 0, 8.5), side="right"),
                     Label("Lower thrust bearing", at=(-25, 0, -1), side="right"),
                     Label("608 bearing", at=(-7.5, 0, -21.5), side="right"))),
    ),
)

_SHEET = 130.0
parts_sheets = Step(
    "parts", "Parts",
    views=(
        View("parts_printed", azimuth=-65.0, elevation=38.0, frame=0.9,
             layout={"box_bottom": (-_SHEET, _SHEET), "box_top": (_SHEET, _SHEET),
                     "hinge": (-_SHEET, -_SHEET), "gt2_pulley_160t": (_SHEET, -_SHEET)},
             labels=(Label("Box bottom", "box_bottom", side="left"), Label("Box top", "box_top", side="right"),
                     Label("Hinge", "hinge", side="left"), Label("160T pulley", "gt2_pulley_160t", side="right"))),
        View("parts_bought", azimuth=-65.0, elevation=38.0, frame=0.9,
             layout={MOTOR: (-105, 70), UPPER: (-25, 70), "bearing_6807": (40, 70), LEFT_6805: (95, 70),
                     "bearing_608": (-60, 5), PULLEY_20T: (-25, 5)},
             hardware=(Hw.at("m5x40", 25, 0, 3), Hw.at("m5x20", 50, 0, 3), Hw.at("nut_m5", 75, 0),
                       Hw.at("insert_m5", 100, 0), Hw.at("m3x16", 125, 0, 2)),
             labels=(Label("NEMA17 motor", MOTOR, side="left"), Label("Thrust bearing × 2", UPPER, side="left"),
                     Label("6807 bearing", "bearing_6807", side="right"),
                     Label("6805 bearing", LEFT_6805, side="right"),
                     Label("608 bearing", "bearing_608", side="left"), Label("20T pulley", PULLEY_20T, side="left"),
                     Label("M5 × 40 × 4", "hw:0", side="left"), Label("M5 × 20 × 7", "hw:1", side="right"),
                     Label("M5 nut × 4", "hw:2", side="right"), Label("M5 × 9.5 insert × 7", "hw:3", side="right"),
                     Label("M3 × 16 × 4", "hw:4", side="right"))),
    ),
)

step16 = Step("16", "Check the parts")

step17 = Step(
    "17", "Install the threaded inserts in the box bottom",
    views=(
        View("step17_inserts",
             added={"box_bottom": (0, 0, 0)},
             hardware=_box_screws("insert_m5", 0.0, 30.0),
             guides=_box_guides(0.0, 22.0), elevation=38.0,
             labels=(Label("M5 × 9.5 insert × 7", "hw:1"), Label("Box bottom", at=(-82, 0, -15), side="left"))),
    ),
)

step18 = Step(
    "18", "Press the 608 and 6807 bearings",
    adds=("bearing_608", "bearing_6807"),
    views=(
        View("step18a_608",
             added={"box_bottom": (0, 0, 0), "bearing_608": (0, 0, 35)},
             guides=(Guide(0, 0, -18, 8),), elevation=38.0,
             labels=(Label("608 bearing", "bearing_608"), Label("Box bottom", at=(-82, 0, -15), side="left"))),
        View("step18b_6807",
             added={"box_top": (0, 0, 0), "bearing_6807": (0, 0, -40)},
             hardware=(Hw.line("plate", (0, 0, 12.0), (0, 0, 1), offset=(0, 0, 12)),),
             guides=(Guide(0, 0, -33, 5),), clip_y=0.0, elevation=0.0, roll=180.0, frame=1.05,
             labels=(Label("6807: in from the recess side", "bearing_6807", side="right"),
                     Label("Flat surface: the bearing stops flush", "hw:0", side="right"),
                     Label("Box top, top face down", at=(-60, 0, 6), side="left"))),
    ),
)

step19 = Step(
    "19", "Press a 6805 bearing into the hinge's gearbox cheek",
    adds=(LEFT_6805,),
    views=(
        View("step19_left_6805",
             added={"hinge": (0, 0, 0), LEFT_6805: (-45, 0, 0)},
             guides=(Guide.between((-81, 0, 70.5), (-36, 0, 70.5)),), azimuth=-140.0, elevation=20.0,
             labels=(Label("6805 bearing", LEFT_6805, side="left"),
                     Label("Hinge: the taller cheek takes the gearbox", at=(-36, -30, 90), side="right"))),
    ),
)

step20 = Step(
    "20", "Stack the joint 1 parts",
    adds=("gt2_pulley_160t", LOWER, "box_top", UPPER, "hinge"),
    views=(
        View("step20a_stack",
             added={"gt2_pulley_160t": (0, 0, -105), LOWER: (0, 0, -60), "box_top": (0, 0, 0),
                    "bearing_6807": (0, 0, 0), UPPER: (0, 0, 40), "hinge": (0, 0, 85), LEFT_6805: (0, 0, 85)},
             guides=(Guide(0, 0, -110, -68), Guide(0, 0, -55, 5), Guide(0, 0, 14, 40), Guide(0, 0, 66, 77)),
             azimuth=-50.0, elevation=18.0,
             labels=(Label("Hinge", at=(-20, -42, 150), side="left"), Label("Upper thrust bearing", UPPER, side="left"),
                     Label("Box top with 6807", at=(90, -75, 6), side="right"),
                     Label("Lower thrust bearing", LOWER, side="left"),
                     Label("160T pulley, hub down", "gt2_pulley_160t", side="right"))),
        View("step20b_section",
             added=along_z(STACK, 0.0), clip_y=0.0, elevation=0.0, frame=1.05,
             labels=(Label("Upper thrust, in the hinge's pocket", at=(-25, 0, 18), side="right"),
                     Label("6807: hinge shaft pressed through", at=(-20.5, 0, 8.5), side="right"),
                     Label("Lower thrust: 5 mm in each part", at=(-25, 0, -1), side="right"),
                     Label("Shaft end on the pocket floor", at=(10, 0, -8), side="left"),
                     Label("Hub goes down into the 608 later", at=(4, 0, -20), side="left"))),
    ),
)

_CLAMP = tuple(Hw("m5x40", CLAMP_R, a, 23.0, down=True, offset=(0, 0, 90)) for a in CLAMP_ANGLES)
_NUTS = tuple(Hw("nut_m5", CLAMP_R, a, -13.0, down=True, offset=(0, 0, -35)) for a in CLAMP_ANGLES)
step21 = Step(
    "21", "Clamp the stack with the M5 screws",
    views=(
        View("step21a_clamp",
             built=STACK, hardware=(*_CLAMP, *_NUTS),
             guides=tuple(Guide(CLAMP_R, a, -48, -17) for a in CLAMP_ANGLES)
             + tuple(Guide(CLAMP_R, a, 35, 73) for a in CLAMP_ANGLES),
             azimuth=-60.0, elevation=10.0,
             labels=(Label("M5 × 40 screw × 4", "hw:1", side="left"), Label("M5 nut × 4", "hw:5", side="right"))),
        View("step21b_section",
             added=along_z(STACK, 0.0), turn=0.0, clip_y=0.0, elevation=0.0, frame=1.05,
             hardware=tuple(Hw("m5x40", CLAMP_R, a, 23.0, down=True) for a in (0.0, 180.0))
             + tuple(Hw("nut_m5", CLAMP_R, a, -13.0, down=True) for a in (0.0, 180.0)),
             labels=(Label("M5 × 40: head in the floor's counterbore", at=(-10, 0, 24.4), side="right"),
                     Label("Nut under the pulley", at=(10, 0, -15.4), side="left"))),
    ),
)

step22 = Step(
    "22", "Fit the 20T pulley to the J1 motor",
    adds=MOTOR_SET,
    views=(
        View("step22_pulley",
             added={MOTOR: (0, 0, 0), PULLEY_20T: (0, 0, -30)},
             guides=(Guide.between((CENTRES, 0, -13), (CENTRES, 0, -33)),), azimuth=-40.0, elevation=-22.0, frame=1.1,
             labels=(Label("20T pulley", PULLEY_20T, side="right"), Label("J1 motor, shaft down", MOTOR, side="left"))),
    ),
)

_MOTOR_SCREWS = tuple(Hw.line("m3x16", (x - SLACK, y, 0.0), (0, 0, 1), offset=(0, 0, -30)) for x, y in MOTOR_XY)
step23 = Step(
    "23", "Fit the motor to the box top",
    views=(
        View("step23_motor",
             built=STACK,
             added={MOTOR: (-SLACK, 0, 70), PULLEY_20T: (-SLACK, 0, 70)},
             hardware=_MOTOR_SCREWS,
             guides=tuple(Guide.between((x - SLACK, y, -30), (x - SLACK, y, 80)) for x, y in MOTOR_XY),
             azimuth=-35.0, elevation=16.0,
             labels=(Label("Motor, at the hinge end of the slot", MOTOR, side="right"),
                     Label("M3 × 16 screw × 4, from below", "hw:0", side="right"))),
    ),
)

step24 = Step(
    "24", "Fit the belt",
    views=(
        View("step24_belt",
             built=(*STACK, *MOTOR_SET),
             hardware=(Hw.at("belt_j1", 0, 0, BELT_Z - 45),),
             guides=(Guide.between((-50.9, 0, BELT_Z - 39), (-50.9, 0, BELT_Z)),
                     Guide.between((CENTRES, 6.4, BELT_Z - 39), (CENTRES, 6.4, BELT_Z))),
             azimuth=-60.0, elevation=-26.0,
             labels=(Label("370 mm belt", at=(30, -38, BELT_Z - 42), side="right"),)),
    ),
)

_COVER_SCREWS = _box_screws("m5x20", 12.0, 55.0)
step25 = Step(
    "25", "Close the box",
    adds=("box_bottom",),
    views=(
        View("step25_close",
             built=(*STACK, *MOTOR_SET),
             added={"box_bottom": (0, 0, -60)},
             hardware=(*_COVER_SCREWS, Hw.at("belt_j1", 0, 0, BELT_Z)),
             guides=(*_box_guides(12.0, 47.0), *(Guide(*_polar(x, y), -60, 0) for x, y in BOX_XY[:3])),
             azimuth=-55.0, elevation=20.0,
             labels=(Label("Box bottom: the hub enters the 608", "box_bottom", side="right"),
                     Label("M5 × 20 screw × 7", "hw:1", side="left"))),
    ),
)

step26 = Step(
    "26", "Tension the belt and check joint 1",
    views=(
        View("step26a_window",
             added=along_z(PARTS, 0.0),
             hardware=(*(Hw.line("m3x16", (x, y, 0.0), (0, 0, 1)) for x, y in MOTOR_XY),
                       Hw.at("belt_j1", 0, 0, BELT_Z)),
             clip_y=-15.0, elevation=0.0,
             labels=(Label("First: this screw, above the window", at=(CENTRES + 15.5, -15.5, -1), side="left"),
                     Label("Then this one: long ball-end key", at=(CENTRES - 15.5, -15.5, -1), side="right"),
                     Label("Pull the motor this way, away from the hinge", at=(CENTRES + 21, -15, 40), side="left"))),
        View("step26b_closed",
             added=along_z(PARTS, 0.0), azimuth=-45.0, elevation=24.0,
             labels=(Label("Motor pulley: 8 turns", at=(CENTRES, 0, -3), side="right"),
                     Label("Hinge: 1 turn", "hinge", side="left"))),
    ),
)

STEPS = [overview, parts_sheets, step16, step17, step18, step19, step20, step21, step22, step23,
         step24, step25, step26]
