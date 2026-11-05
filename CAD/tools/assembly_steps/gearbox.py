"""The gearbox chapter's steps and pictures (docs/assembly-guide.md).

Gearbox frame: +Z toward the motor, so a picture stands on the output with the
motor end up. Positions are from gearbox/planetary_gearbox.py (STAGES),
gearbox/carrier.py and the part modules. The build order follows the design's
source article (see the guide), checked against this model's geometry.
"""
from __future__ import annotations

import math

from assembly_steps import Guide, Hw, Label, Step, View, Vec, along_z

NAME = "gearbox"
ASSEMBLY = "STEP/gearbox/planetary_gearbox.step"

COLOURS = {
    "ring_gear": "#c77db0",
    "back_cover": "#62b39a",
    "front_cover": "#93bb63",
    "nema17_mount": "#d0a044",
    "nema17": "#9d86c9",
    "input_shaft": "#5ba7c4",
    "carrier_stage1_output": "#6f8fc9",
    "carrier_stage2_output": "#6f8fc9",
    "carrier_plate": "#b98ae0",
    "planet_gear": "#6fb35a",
    "planet_pin": "#e0774a",
    "bushing": "#e3bd45",
    "washer": "#3f9c9c",
    "bearing": "#98a3ad",
}


def colour_of(label: str) -> str:
    return next(colour for key, colour in COLOURS.items() if label.startswith(key))


PIN_R, SCREW_R, BOLT_R = 22.5, 22.0, 39.25
BOLT_ANGLES = tuple(30.0 + 60.0 * k for k in range(6))
STAGE1_TURN, INPUT_TURN = 6.2947, 9.1834
SET_SCREW_Z = 16.8
SET_SCREW_ANGLE = 180.0 + INPUT_TURN
MOTOR_SCREW_R, MOTOR_SCREW_ANGLES = 21.92, (45.0, 135.0, -45.0, -135.0)
MOUNT_SCREW_R, MOUNT_SCREW_ANGLES = 29.125, (55.49, 124.51, -55.49, -124.51)
LIFT_PIN, LIFT_BEARING = 34.0, 62.0


class Stage:
    """One stage's labels and positions."""

    def __init__(self, n: int, angles: tuple[float, ...], plate_bottom: float, output: str):
        self.n, self.angles, self.z = n, angles, plate_bottom
        self.output, self.bearing, self.plate = output, f"bearing_6801:stage{n}", f"carrier_plate:stage{n}"
        tags = tuple(f"s{n}p{i}" for i in (1, 2, 3))
        self.pins = tuple(f"planet_pin:{t}" for t in tags)
        self.bushings = tuple(f"bushing:{t}" for t in tags)
        self.planets = tuple(f"planet_gear:{t}" for t in tags)
        self.low_washers = tuple(f"washer:{t}w1" for t in tags)
        self.high_washers = tuple(f"washer:{t}w2" for t in tags)
        self.screw_angles = tuple(a - 60.0 for a in angles)
        self.washers = self.low_washers + self.high_washers
        self.carrier = (output, self.bearing, self.plate, *self.pins, *self.bushings, *self.planets, *self.washers)
        self.face = angles[2]    # azimuth with one planet in front, the others either side


S1 = Stage(1, tuple(a + STAGE1_TURN for a in (26.41, 146.41, -93.59)), -12.0, "carrier_stage1_output")
S2 = Stage(2, (43.46, 163.46, -76.54), -36.0, "carrier_stage2_output")


def carrier_views(step: str, s: Stage, carrier_name: str) -> tuple[View, ...]:
    """Bearing and pins, then the planet stacks, the plate and the screws."""
    z = s.z
    # Screw head seat: its Ø5.7 head meets the output half's Ø7.5 -> Ø2.8 cone 0.9 mm in.
    seat = z - 4.1
    closed = (s.output, s.bearing, *s.pins, *s.washers, *s.planets, *s.bushings)
    return (
        View(f"{step}a_pins_bearing",
             added={s.output: (0, 0, 0), s.bearing: (0, 0, LIFT_BEARING), **along_z(s.pins, LIFT_PIN)},
             guides=(Guide(0, 0, z, z + 57), *(Guide(PIN_R, a, z, z + 29) for a in s.angles)),
             azimuth=s.face, elevation=30.0,
             labels=(Label("6801 bearing", s.bearing), Label("Pin 6 × 22 × 3", s.pins[0]),
                     Label(carrier_name, s.output, at=(0, 0, z - 5)))),
        View(f"{step}b_planets",
             built=(s.output, s.bearing, *s.pins),
             added={**along_z(s.low_washers, 30), **along_z(s.planets, 42), **along_z(s.bushings, 42),
                    **along_z(s.high_washers, 54)},
             guides=tuple(Guide(PIN_R, a, z + 17, z + 70) for a in s.angles),
             azimuth=s.face, elevation=30.0,
             labels=(Label("Washer", s.high_washers[0]), Label("Planet with bushing × 3", s.planets[1]),
                     Label("Washer", s.low_washers[2]))),
        View(f"{step}c_plate",
             built=closed,
             added={s.plate: (0, 0, 32)},
             guides=tuple(Guide(PIN_R, a, z + 17, z + 49) for a in s.angles),
             azimuth=s.face, elevation=30.0,
             labels=(Label("Carrier plate (inserts face down)", s.plate),)),
        View(f"{step}d_screws",
             built=(*closed, s.plate),
             hardware=tuple(Hw("m3x10", SCREW_R, a, seat, offset=(0, 0, -14)) for a in s.screw_angles),
             guides=tuple(Guide(SCREW_R, a, z - 8, z) for a in s.screw_angles),
             azimuth=s.screw_angles[0], elevation=-48.0,
             labels=(Label("M3 screw × 3", "hw:0"),)),
    )


INNER = (*S2.carrier, *S1.carrier, "input_shaft", "ring_gear")
COVERED = (*INNER, "bearing_6805:output", "front_cover", "bearing_6803:input", "back_cover")
WHOLE = (*COVERED, "nema17_mount", "nema17")


def _radial(angle: float, r: float, dz: float) -> Vec:
    a = math.radians(angle)
    return (r * math.cos(a), r * math.sin(a), dz)


def _exploded_stack(s: Stage, r: float, base: float) -> dict[str, Vec]:
    parts: dict[str, Vec] = {}
    for i, a in enumerate(s.angles):
        parts[s.low_washers[i]] = _radial(a, r, base - 20)
        parts[s.planets[i]] = _radial(a, r, base)
        parts[s.bushings[i]] = _radial(a, r, base)
        parts[s.high_washers[i]] = _radial(a, r, base + 20)
        parts[s.pins[i]] = _radial(a, r, base + 55)
    return parts


# Offsets of the full exploded view: every part clear of its neighbours along the axis,
# the planet stacks out to the sides.
EXPLODED: dict[str, Vec] = {
    "nema17": (0, 0, 310), "nema17_mount": (0, 0, 260), "back_cover": (0, 0, 215),
    "bearing_6803:input": (0, 0, 190), "input_shaft": (0, 0, 165),
    S1.plate: (0, 0, 115), S1.bearing: (0, 0, 70), S1.output: (0, 0, 60), "ring_gear": (0, 0, 0),
    S2.plate: (0, 0, -50), S2.bearing: (0, 0, -85), S2.output: (0, 0, -110),
    "bearing_6805:output": (0, 0, -160), "front_cover": (0, 0, -175),
    **_exploded_stack(S1, 58.0, 80.0), **_exploded_stack(S2, 58.0, -65.0),
}

overview = Step(
    "overview", "The whole gearbox",
    views=(
        View("overview_exploded", added=EXPLODED, azimuth=-60.0, elevation=18.0, roll=52.0,
             path="gearbox_exploded.png"),
        # Turned so that a stage-2 pin lies on the cut; the stage-1 pin is then 4.2 mm off, so
        # y = 2.1 cuts through both. Looking along -y, +x is on the left of the picture.
        View("overview_section", added=along_z(WHOLE, 0.0), turn=16.54, clip_y=2.1, elevation=0.0,
             labels=(Label("Motor", "nema17", side="right"),
                     Label("Motor mount", at=(-20, 2.1, 23), side="right"),
                     Label("Input shaft (stage-1 sun)", at=(-7, 2.1, 17), side="right"),
                     Label("6803 bearing", at=(-11, 2.1, 9.5), side="right"),
                     Label("Pin", at=(-22.5, 2.1, 3), side="right"),
                     Label("Stage-1 planet", at=(-30, 2.1, -5.7), side="right"),
                     Label("Bushing", at=(-18.5, 2.1, -30), side="right"),
                     Label("Stage-2 planet", at=(-30, 2.1, -29.7), side="right"),
                     Label("6805 bearing", at=(-15.5, 2.1, -48.5), side="right"),
                     Label("Output hex", at=(0, 2.1, -78), side="right"),
                     Label("Back cover", at=(36, 2.1, 10), side="left"),
                     Label("Stage-1 carrier", at=(25, 2.1, -3), side="left"),
                     Label("Ring gear", at=(38, 2.1, -24), side="left"),
                     Label("Stage-2 carrier", at=(25, 2.1, -38.5), side="left"),
                     Label("Front cover", at=(36, 2.1, -52), side="left"))),
    ),
)

_SHEET = 95.0
parts_sheets = Step(
    "parts", "Parts",
    views=(
        View("parts_printed", azimuth=-65.0, elevation=38.0, frame=0.82,
             layout={"ring_gear": (-_SHEET, _SHEET), "back_cover": (0, _SHEET), "front_cover": (_SHEET, _SHEET),
                     "nema17_mount": (-_SHEET, 0), "input_shaft": (0, 0), "planet_gear:s1p1": (_SHEET, 0),
                     "carrier_plate:stage1": (-_SHEET, -_SHEET), "carrier_stage1_output": (0, -_SHEET),
                     "carrier_stage2_output": (_SHEET, -_SHEET)},
             labels=(Label("Ring gear", "ring_gear", side="left"), Label("Back cover", "back_cover", side="right"),
                     Label("Front cover", "front_cover", side="right"), Label("Motor mount", "nema17_mount", side="left"),
                     Label("Input shaft", "input_shaft", side="left"), Label("Planet gear × 6", "planet_gear:s1p1", side="right"),
                     Label("Carrier plate × 2", "carrier_plate:stage1", side="left"),
                     Label("Stage-1 output carrier", "carrier_stage1_output", side="left"),
                     Label("Stage-2 output carrier", "carrier_stage2_output", side="right"))),
        View("parts_bought", azimuth=-65.0, elevation=38.0, frame=0.9,
             layout={"nema17": (-115, 80), "bearing_6805:output": (-15, 75), "bearing_6803:input": (35, 75),
                     "bearing_6801:stage1": (80, 75), "planet_pin:s1p1": (-15, 25), "bushing:s1p1": (20, 25),
                     "washer:s1p1w1": (55, 25)},
             hardware=(Hw.at("m3x10", 95, 30, 2), Hw.at("m3x12", 70, -25, 2), Hw.at("m3x16", 45, -25, 2),
                       Hw.at("m3x18", 20, -25, 2), Hw.at("m3x22", -5, -25, 2), Hw.at("insert_m3", -35, -25),
                       Hw.at("insert_m3s", -60, -25), Hw.at("set_screw", -85, -25)),
             labels=(Label("NEMA17 motor", "nema17", side="left"), Label("6805 bearing × 1", "bearing_6805:output", side="left"),
                     Label("6803 bearing × 1", "bearing_6803:input", side="right"),
                     Label("6801 bearing × 2", "bearing_6801:stage1", side="right"),
                     Label("Pin 6 × 22 × 6", "planet_pin:s1p1", side="left"), Label("Bushing × 6", "bushing:s1p1", side="left"),
                     Label("M6 washer × 12", "washer:s1p1w1", side="right"), Label("M3 × 10 × 6", "hw:0", side="right"),
                     Label("M3 × 12 × 6", "hw:1", side="right"), Label("M3 × 16 × 6", "hw:2", side="right"),
                     Label("M3 × 18 × 4", "hw:3", side="right"), Label("M3 × 22 × 4", "hw:4", side="left"),
                     Label("M3 × 5.7 insert × 18", "hw:5", side="left"), Label("M3S × 4 insert × 4", "hw:6", side="left"),
                     Label("Set screw × 1", "hw:7", side="left"))),
    ),
)

step00 = Step("0", "Check the parts")

step01 = Step(
    "1", "Install the threaded inserts",
    views=(
        View("step01a_ring",
             added={"ring_gear": (0, 0, 0)},
             hardware=tuple(Hw("insert_m3", BOLT_R, a, 0.0, down=True, offset=(0, 0, 22)) for a in BOLT_ANGLES),
             guides=tuple(Guide(BOLT_R, a, 0, 16) for a in BOLT_ANGLES), elevation=32.0,
             labels=(Label("M3 × 5.7 insert × 6 (each end)", "hw:5"), Label("Ring gear", at=(42, 0, -24)))),
        View("step01b_back_cover",
             added={"back_cover": (0, 0, 0)},
             hardware=tuple(Hw("insert_m3s", MOUNT_SCREW_R, a, 14.0, down=True, offset=(0, 0, 16)) for a in MOUNT_SCREW_ANGLES),
             guides=tuple(Guide(MOUNT_SCREW_R, a, 14, 26) for a in MOUNT_SCREW_ANGLES), elevation=38.0, azimuth=-30.0,
             labels=(Label("Short M3S × 4 insert × 4", "hw:0"), Label("Back cover, motor side up", at=(35, -20, 7)))),
        View("step01c_plate",
             added={S2.plate: (0, 0, 0)},
             hardware=tuple(Hw("insert_m3", SCREW_R, a, S2.z, offset=(0, 0, -16)) for a in S2.screw_angles),
             guides=tuple(Guide(SCREW_R, a, S2.z - 10, S2.z) for a in S2.screw_angles),
             azimuth=S2.screw_angles[0], elevation=-38.0,
             labels=(Label("M3 × 5.7 insert × 3", "hw:0"), Label("Carrier plate × 2", at=(28, 0, -27)))),
    ),
)

_P, _B = "planet_gear:s2p1", "bushing:s2p1"
step02 = Step(
    "2", "Press the bushings into the planets",
    adds=(*S1.planets, *S2.planets, *S1.bushings, *S2.bushings),
    views=(
        View("step02a_bushing",
             added={_P: (0, 0, 0), _B: (0, 0, 24)},
             guides=(Guide(PIN_R, S2.angles[0], -25, -10),), elevation=32.0,
             labels=(Label("Bushing 6 × 8 × 10", _B, side="right"), Label("Planet gear", _P, side="left"))),
        # Turned so that this planet is on the cut, which shows the bushing proud of both faces.
        View("step02b_section",
             added={_P: (0, 0, 0), _B: (0, 0, 0)}, turn=-S2.angles[0], clip_y=0.0, elevation=0.0, frame=1.25,
             labels=(Label("Bushing: 0.5 mm proud at each face", at=(19.2, 0, -24.9), side="right"),
                     Label("Planet gear (9 mm)", at=(30, 0, -30), side="left"))),
    ),
)

step03 = Step("3", "Build the stage-2 carrier",
              adds=tuple(p for p in S2.carrier if p not in step02.adds),
              views=carrier_views("step03", S2, "Stage-2 output carrier"))

step04 = Step("4", "Build the stage-1 carrier",
              adds=tuple(p for p in S1.carrier if p not in step02.adds),
              views=carrier_views("step04", S1, "Stage-1 output carrier"))

step05 = Step(
    "5", "Fit the input shaft into the stage-1 carrier",
    adds=("input_shaft",),
    views=(
        View("step05a_input_shaft",
             built=S1.carrier, added={"input_shaft": (0, 0, 62)},
             guides=(Guide(0, 0, 5, 45),), azimuth=S1.face, elevation=30.0,
             labels=(Label("Input shaft", "input_shaft"),)),
        View("step05b_section",
             added=along_z((*S1.carrier, "input_shaft"), 0.0), turn=180.0 - S1.angles[1], clip_y=0.0, elevation=0.0,
             labels=(Label("Sun meshes with the planets", at=(-11, 0, -6), side="right"),
                     Label("Journal in the 6801", at=(-5, 0, -14.5), side="right"),
                     Label("Stage-2 sun (on the stem)", at=(10, 0, -28), side="left"))),
    ),
)

_S1_SET = (*S1.carrier, "input_shaft")
step06 = Step(
    "6", "Twist stage 1 into the ring gear",
    adds=("ring_gear",),
    views=(
        View("step06_stage1_in_ring",
             added={"ring_gear": (0, 0, 0), **along_z(_S1_SET, 70)},
             guides=(Guide(0, 0, 0, 30),), azimuth=S1.face, elevation=26.0,
             labels=(Label("Stage 1 with input shaft", S1.plate), Label("Ring gear: motor end up", at=(42, 0, -24)))),
    ),
)

step07 = Step(
    "7", "Twist stage 2 in from the other end",
    views=(
        View("step07a_stage2_in_ring",
             built=(*_S1_SET, "ring_gear"), added=along_z(S2.carrier, -75),
             guides=(Guide(0, 0, -94, -47),), azimuth=S2.face, elevation=-24.0,
             labels=(Label("Stage 2", S2.plate), Label("Ring gear, stage 1 inside", at=(42, 0, -24)))),
        View("step07b_section",
             added=along_z(INNER, 0.0), turn=16.54, clip_y=2.1, elevation=0.0,
             labels=(Label("Stage-1 journal in the stage-2 6801", at=(0, 2.1, -38.5), side="right"),
                     Label("Stage-2 sun in the stage-2 planets", at=(-11, 2.1, -30), side="right"),
                     Label("Input journal in the stage-1 6801", at=(0, 2.1, -14.5), side="left"))),
    ),
)

step08 = Step("8", "Grease the gears and check the mesh")

_BOLTS_FRONT = tuple(Hw("m3x12", BOLT_R, a, -52.8, offset=(0, 0, -95)) for a in BOLT_ANGLES)
step09 = Step(
    "9", "Fit the output bearing and front cover",
    adds=("bearing_6805:output", "front_cover"),
    views=(
        View("step09_front_cover",
             built=INNER, added={"bearing_6805:output": (0, 0, -50), "front_cover": (0, 0, -75)},
             hardware=_BOLTS_FRONT,
             guides=(Guide(0, 0, -95, -84), *(Guide(BOLT_R, a, -136, -47) for a in BOLT_ANGLES)),
             elevation=-26.0,
             labels=(Label("6805 bearing", "bearing_6805:output", side="right"),
                     Label("Front cover", at=(42, 0, -125), side="left"),
                     Label("M3 × 12 screw × 6", "hw:0"))),
    ),
)

_BOLTS_BACK = tuple(Hw("m3x16", BOLT_R, a, 10.8, down=True, offset=(0, 0, 110)) for a in BOLT_ANGLES)
step10 = Step(
    "10", "Fit the input bearing and back cover",
    adds=("bearing_6803:input", "back_cover"),
    views=(
        View("step10_back_cover",
             built=(*INNER, "bearing_6805:output", "front_cover"),
             added={"bearing_6803:input": (0, 0, 28), "back_cover": (0, 0, 85)},
             hardware=_BOLTS_BACK,
             guides=(Guide(0, 0, 19.6, 35), *(Guide(BOLT_R, a, 0, 104) for a in BOLT_ANGLES)),
             elevation=30.0,
             labels=(Label("6803 bearing (press into the cover first)", "bearing_6803:input", side="right"),
                     Label("Back cover", at=(42, 0, 92), side="left"),
                     Label("M3 × 16 screw × 6", "hw:0"))),
    ),
)

step11 = Step(
    "11", "Check the ratio",
    views=(
        View("step11_closed",
             added=along_z(COVERED, 0.0), elevation=24.0,
             labels=(Label("Input: 16 turns", at=(0, 0, 19.6), side="right"),
                     Label("Output: 1 turn", at=(5.3, -9.2, -76), side="left"))),
    ),
)

step12 = Step(
    "12", "Start the set screw",
    views=(
        View("step12_set_screw",
             built=("back_cover",), added={"input_shaft": (0, 0, 0)},
             hardware=(Hw("set_screw", 26.0, SET_SCREW_ANGLE, SET_SCREW_Z, radial=True),),
             azimuth=SET_SCREW_ANGLE + 35.0, elevation=24.0, frame=0.8,
             labels=(Label("Set screw", "hw:0", side="right"),
                     Label("Hole over the flat side of the bore", at=(-8.3, -1.3, SET_SCREW_Z), side="left"))),
    ),
)

_MOTOR_SCREWS = tuple(Hw("m3x18", MOTOR_SCREW_R, a, 17.0, offset=(0, 0, -68)) for a in MOTOR_SCREW_ANGLES)
step13 = Step(
    "13", "Fix the mount to the motor",
    adds=("nema17_mount", "nema17"),
    views=(
        View("step13_motor_mount",
             added={"nema17": (0, 0, 0), "nema17_mount": (0, 0, -32)},
             hardware=_MOTOR_SCREWS,
             guides=tuple(Guide(MOTOR_SCREW_R, a, -34, 32) for a in MOTOR_SCREW_ANGLES),
             azimuth=-25.0, elevation=-24.0,
             labels=(Label("NEMA17 motor", "nema17", side="right"),
                     Label("Motor mount, counterbores down", "nema17_mount", side="left"),
                     Label("M3 × 18 screw × 4", "hw:0"))),
    ),
)

_MOUNT_SCREWS = tuple(Hw("m3x22", MOUNT_SCREW_R, a, 32.0, down=True, offset=(0, 0, 105)) for a in MOUNT_SCREW_ANGLES)
step14 = Step(
    "14", "Slide the motor shaft in and bolt the mount down",
    views=(
        View("step14_motor_on",
             built=COVERED, added=along_z(("nema17", "nema17_mount"), 70),
             hardware=(*_MOUNT_SCREWS, Hw("set_screw", 11.0, SET_SCREW_ANGLE, SET_SCREW_Z, radial=True, built=True)),
             guides=tuple(Guide(MOUNT_SCREW_R, a, 14, 115) for a in MOUNT_SCREW_ANGLES),
             azimuth=-120.0, elevation=24.0,
             labels=(Label("Motor and mount", "nema17_mount"),
                     Label("Access slot faces the set screw", at=(-20.5, 0, 87), side="left"),
                     Label("M3 × 22 screw × 4", "hw:2", side="right"))),
    ),
)

step15 = Step(
    "15", "Tighten the set screw",
    views=(
        View("step15_section",
             added=along_z(("input_shaft", "back_cover", "nema17_mount", "nema17"), 0.0),
             hardware=(Hw("set_screw", 7.2, SET_SCREW_ANGLE, SET_SCREW_Z, radial=True),),
             clip_y=0.0, elevation=0.0,
             labels=(Label("Set screw, on the motor shaft's flat", "hw:0", side="right"),
                     Label("Key enters through the mount's slot", at=(-15, 0, 16.8), side="right"))),
    ),
)

STEPS = [overview, parts_sheets, step00, step01, step02, step03, step04, step05, step06, step07,
         step08, step09, step10, step11, step12, step13, step14, step15]
