"""The arm segments chapter's steps and pictures (docs/assembly-4-arm-segments.md).

Assembly: the arm frame of belt_arm/belt_drive_arm.py. Plates in XY with the Base's underside
at z = 0 and +Z toward the Top, J3 along Z at (160, 40), the motor at (-10, 40), the dual
pulley at (75, 40). The STEP has the idlers at the slack end of their slots (y = 20) and the
jack screws backed off. It holds one segment; the arm has two.
"""
from __future__ import annotations

from assembly_steps import Guide, Hw, Label, Step, View, Vec, along_z

NAME = "segment"
ASSEMBLY = "STEP/belt_arm/belt_drive_arm.step"
COPIES = 2

COLOURS = {
    "base": "#5ba7c4",
    "wall": "#62b39a",
    "top": "#7fb0a0",
    "dual_gt2_pulley": "#93bb63",
    "gt2_80_output": "#6fb35a",
    "pin": "#c77db0",
    "output_block": "#d0a044",
    "spacer": "#e0774a",
    "nema17": "#9d86c9",
    "gt2_pulley_20t": "#4f9a43",
    "dowel_pin": "#8a949e",
    "button_head": "#2e3540",
    "hex_nut": "#5c6670",
    "bushing": "#e3bd45",
    "socket_head": "#39424e",
    "gt2_idler": "#6f8fc9",
    "bearing_6805": "#98a3ad",
    "belt": "#3b3f46",
}


def colour_of(label: str) -> str:
    return next(colour for key, colour in COLOURS.items() if label.startswith(key))


J3 = (160.0, 40.0)
MOTOR_XY, DUAL_XY = (-10.0, 40.0), (75.0, 40.0)
IDLER_XS, IDLER_Y = (27.65, 112.65), 20.0
WALL_SCREWS = ((75.0, 76.5), (0.0, 3.5), (75.0, 3.5), (130.0, 76.5), (-36.5, 40.0), (0.0, 76.5), (130.0, 3.5))
JACK_XZ = ((27.65, 29.5), (112.65, 14.5))
END_INSERT_Y = (3.5, 76.5)
MOTOR_SCREWS = tuple((-10.0 + dx, 40.0 + dy) for dx in (-15.5, 15.5) for dy in (-15.5, 15.5))

BEARINGS = ("bearing_6805:base", "bearing_6805:top")
BUSHINGS = ("bushing:lower", "bushing:upper")
MOTOR_SET = ("nema17:j3", "gt2_pulley_20t:j3")
OUTPUT_SET = ("output_block", "gt2_80_output")
BELT_1, BELT_2 = "belt:stage_1", "belt:stage_2"
IDLER_1 = ("button_head_m5x40:idler_1", "spacer_5mm:idler_1", "gt2_idler_20t:1", "spacer_15mm:idler_1")
IDLER_2 = ("button_head_m5x40:idler_2", "spacer_15mm:idler_2", "gt2_idler_20t:2", "spacer_5mm:idler_2")
NUTS = ("hex_nut_m5:idler_1", "hex_nut_m5:idler_2")
JACKS = ("socket_head_m3x35:jack_1", "socket_head_m3x35:jack_2")
DUAL_SET = ("dowel_pin:dual_pulley", "dual_gt2_pulley", *BUSHINGS)
PARTS = ("base", "wall", "top", *BEARINGS, *MOTOR_SET, *OUTPUT_SET, "pin:base", "pin:top", *DUAL_SET,
         BELT_1, BELT_2, *IDLER_1, *IDLER_2, *NUTS, *JACKS)

COVERAGE = PARTS

FRAME = ("base", "wall", "bearing_6805:base", *MOTOR_SET)
PIN_1_SET = (*OUTPUT_SET, "pin:base", BELT_2)
BELOW_TOP = (*FRAME, *PIN_1_SET, *DUAL_SET, BELT_1, *IDLER_1, *IDLER_2)
CLOSED = (*BELOW_TOP, "top", "bearing_6805:top", *NUTS)

overview = Step(
    "overview", "One segment",
    views=(
        View("overview_inside",
             added=along_z(tuple(p for p in PARTS if p not in ("top", "bearing_6805:top", "pin:top", *NUTS)), 0.0),
             azimuth=-72.0, elevation=48.0,
             labels=(Label("Motor, under the base plate", at=(-10, 18.9, -24), side="left"),
                     Label("Wall", at=(-36, 3, 37), side="left"),
                     Label("Belt 1", at=(30, 55.4, 20), side="left"),
                     Label("Dual pulley", at=(75, 62, 22), side="right"),
                     Label("Belt 2", at=(120, 56.6, 29.7), side="right"),
                     Label("Idler and jack screw", at=(27.65, -22, 29.5), side="left"),
                     Label("Output pulley in the block's slot", at=(160, 15, 31), side="right"),
                     Label("Output block", at=(225, 75, 44), side="right"))),
        View("overview_section",
             added=along_z(("base", "wall", "top", *BEARINGS, *MOTOR_SET, *OUTPUT_SET, "pin:base", "pin:top",
                            *DUAL_SET, BELT_1, BELT_2), 0.0),
             clip_y=40.0, elevation=0.0,
             labels=(Label("Top plate", at=(40, 40, 40), side="right"),
                     Label("Base plate", at=(40, 40, 3), side="right"),
                     Label("Motor pulley", at=(-15, 40, 17), side="right"),
                     Label("Dual pulley on its dowel", at=(60, 40, 17), side="right"),
                     Label("Pin, from each side", at=(160, 40, -4), side="left"),
                     Label("6805 in each plate", at=(176, 40, 40), side="left"),
                     Label("Output pulley", at=(180, 40, 27), side="left"))),
    ),
)

parts_sheets = Step(
    "parts", "Parts",
    views=(
        View("parts_printed", azimuth=-80.0, elevation=48.0,
             layout={"base": (-20, 190), "top": (-20, 90), "wall": (-20, -10), "output_block": (175, -135),
                     "dual_gt2_pulley": (-140, -130), "gt2_80_output": (-70, -130), "pin:base": (0, -130),
                     "spacer_5mm:idler_1": (55, -115), "spacer_15mm:idler_1": (55, -150)},
             labels=(Label("Base", "base", side="left"), Label("Top", "top", side="left"),
                     Label("Wall", "wall", side="left"), Label("Output block", "output_block", side="right"),
                     Label("Dual pulley", "dual_gt2_pulley", side="left"),
                     Label("Output pulley", "gt2_80_output", side="left"),
                     Label("Pin × 2", "pin:base", side="right"),
                     Label("5 mm spacer × 2", "spacer_5mm:idler_1", side="right"),
                     Label("15 mm spacer × 2", "spacer_15mm:idler_1", side="right"))),
        View("parts_bought", azimuth=-70.0, elevation=40.0,
             layout={"nema17:j3": (-120, 70), "gt2_pulley_20t:j3": (-55, 70), "gt2_idler_20t:1": (-20, 70),
                     "bearing_6805:base": (35, 70), BELT_1: (130, 70), "bushing:lower": (-60, -10),
                     "dowel_pin:dual_pulley": (-30, -10), "button_head_m5x40:idler_1": (0, -10),
                     "hex_nut_m5:idler_1": (30, -10), "socket_head_m3x35:jack_1": (60, -10)},
             hardware=(Hw.at("m3x8", 95, -10, 2), Hw.at("m3x10", 125, -10, 2), Hw.at("insert_m3", 155, -10)),
             labels=(Label("Motor", "nema17:j3", side="left"), Label("20T pulley", "gt2_pulley_20t:j3", side="left"),
                     Label("20T idler × 2", "gt2_idler_20t:1", side="left"),
                     Label("6805 bearing × 2", "bearing_6805:base", side="right"),
                     Label("280 mm belt × 2", BELT_1, side="right"),
                     Label("Bushing × 2", "bushing:lower", side="left"),
                     Label("6 × 30 dowel", "dowel_pin:dual_pulley", side="left"),
                     Label("M5 × 40 × 2", "button_head_m5x40:idler_1", side="left"),
                     Label("M5 nut × 2", "hex_nut_m5:idler_1", side="left"),
                     Label("M3 × 35 socket head × 2", "socket_head_m3x35:jack_1", side="right"),
                     Label("M3 × 8 × 4", "hw:0", side="right"), Label("M3 × 10 × 14", "hw:1", side="right"),
                     Label("M3 × 5.7 insert × 20", "hw:2", side="right"))),
    ),
)

step34 = Step("34", "Check the parts and the fits")

_WALL_INSERTS = (*(Hw.line("insert_m3", (x, y, 37.0), (0, 0, -1), offset=(0, 0, 28)) for x, y in WALL_SCREWS),
                 *(Hw.line("insert_m3", (x, y, 7.0), (0, 0, 1), offset=(0, 0, -28)) for x, y in WALL_SCREWS),
                 *(Hw.line("insert_m3", (x, 0.0, z), (0, 1, 0), offset=(0, -28, 0)) for x, z in JACK_XZ))
_PLATE_GAP = 110.0
step35 = Step(
    "35", "Install the threaded inserts",
    views=(
        View("step35a_wall",
             added={"wall": (0, 0, 0)},
             hardware=_WALL_INSERTS,
             guides=(*(Guide.between((x, y, 37), (x, y, 63)) for x, y in WALL_SCREWS),
                     *(Guide.between((x, -24, z), (x, 0, z)) for x, z in JACK_XZ)),
             azimuth=-70.0, elevation=30.0,
             labels=(Label("Insert in the top of each of the 7 holes", "hw:1", side="right"),
                     Label("And in the bottom of each", "hw:8", side="right"),
                     Label("2 in the outside of this rail", "hw:14", side="left"))),
        View("step35b_ends",
             added={"base": (0, _PLATE_GAP, 0), "top": (0, 0, -37)},
             hardware=(*(Hw.line("insert_m3", (-40.0, y + _PLATE_GAP, 3.5), (1, 0, 0), offset=(-26, 0, 0)) for y in END_INSERT_Y),
                       *(Hw.line("insert_m3", (-40.0, y, 3.5), (1, 0, 0), offset=(-26, 0, 0)) for y in END_INSERT_Y)),
             guides=(*(Guide.between((-62, y + _PLATE_GAP, 3.5), (-40, y + _PLATE_GAP, 3.5)) for y in END_INSERT_Y),
                     *(Guide.between((-62, y, 3.5), (-40, y, 3.5)) for y in END_INSERT_Y)),
             azimuth=-125.0, elevation=30.0,
             labels=(Label("Base: 2 inserts in the end face", "hw:0", side="left"),
                     Label("Top: 2 inserts, the same", "hw:2", side="left"))),
    ),
)

step36 = Step(
    "36", "Press the bushings into the dual pulley",
    adds=BUSHINGS,
    views=(
        View("step36_bushings",
             added={"dual_gt2_pulley": (0, 0, 0), "bushing:lower": (0, 0, -28), "bushing:upper": (0, 0, 28)},
             guides=(Guide.between((75, 40, -17.3), (75, 40, 60)),), clip_y=40.0, elevation=0.0, frame=1.1,
             labels=(Label("Bushing, from this end", "bushing:upper", side="right"),
                     Label("Bushing, from this end", "bushing:lower", side="right"),
                     Label("Dual pulley: 21 mm bore, 1 mm gap in the middle", at=(55, 40, 21), side="left"))),
    ),
)

step37 = Step(
    "37", "Press the 6805 bearings into the plates",
    adds=BEARINGS,
    views=(
        View("step37_bearings",
             added={"base": (0, 110, 0), "bearing_6805:base": (0, 110, 40), "top": (0, 0, -37),
                    "bearing_6805:top": (0, 0, 3)},
             hardware=(Hw.line("plate", (160.0, 150.0, 0.0), (0, 0, -1)), Hw.line("plate", (160.0, 40.0, 0.0), (0, 0, -1))),
             guides=(Guide.between((160, 150, 7), (160, 150, 40)), Guide.between((160, 40, 7), (160, 40, 40))),
             azimuth=-40.0, elevation=30.0,
             labels=(Label("6805, into the base plate", "bearing_6805:base", side="right"),
                     Label("6805, into the top plate", "bearing_6805:top", side="right"),
                     Label("Flat plate below: stops it flush", "hw:1", side="right"))),
    ),
)

_WALL_M3 = tuple(Hw.line("m3x10", (x, y, 3.0), (0, 0, 1), offset=(0, 0, -30)) for x, y in WALL_SCREWS)
step38 = Step(
    "38", "Bolt the wall to the base",
    adds=("base", "wall"),
    views=(
        View("step38_wall",
             added={"base": (0, 0, 0), "bearing_6805:base": (0, 0, 0), "wall": (0, 0, 45)},
             hardware=_WALL_M3,
             guides=(*(Guide.between((x, y, -22), (x, y, 3)) for x, y in WALL_SCREWS),
                     *(Guide.between((x, y, 8), (x, y, 50)) for x, y in WALL_SCREWS[:4])),
             azimuth=-70.0, elevation=-24.0,
             labels=(Label("Wall", "wall", side="left"), Label("Base", at=(120, 0, 3), side="right"),
                     Label("M3 × 10 × 7, from below", "hw:3", side="right"))),
    ),
)

_MOTOR_M3 = tuple(Hw.line("m3x8", (x, y, 4.0), (0, 0, -1), offset=(0, 0, 30)) for x, y in MOTOR_SCREWS)
step39 = Step(
    "39", "Fit the motor and its pulley",
    adds=MOTOR_SET,
    views=(
        View("step39a_pulley",
             added={"nema17:j3": (0, 0, 0), "gt2_pulley_20t:j3": (0, 0, 30)},
             guides=(Guide.between((-10, 40, 24), (-10, 40, 42)),), azimuth=-40.0, elevation=16.0, frame=1.1,
             labels=(Label("20T pulley: 12 mm from the motor's face", "gt2_pulley_20t:j3", side="right"),
                     Label("Motor, shaft up", at=(-31, 19, -24), side="left"))),
        View("step39b_motor",
             built=("base", "wall", "bearing_6805:base"),
             added={"nema17:j3": (0, 0, -60), "gt2_pulley_20t:j3": (0, 0, -60)},
             hardware=_MOTOR_M3,
             guides=(*(Guide.between((x, y, 8), (x, y, 28)) for x, y in MOTOR_SCREWS),
                     *(Guide.between((x, y, -60), (x, y, 0)) for x, y in MOTOR_SCREWS)),
             azimuth=-105.0, elevation=24.0,
             labels=(Label("Motor, up from below", "nema17:j3", side="right"),
                     Label("M3 × 8 × 4, from inside", "hw:0", side="left"))),
    ),
)

_OUT = (-45.0, 0.0, 0.0)
_DROP = (0.0, 0.0, 50.0)
step40 = Step(
    "40", "Fit the output pulley, the block and the first pin",
    adds=(*OUTPUT_SET, "pin:base", BELT_2),
    views=(
        View("step40a_slot",
             added={"output_block": (0, 0, 0), "gt2_80_output": _OUT, BELT_2: _OUT},
             guides=(Guide.between((186, 40, 26.7), (205, 40, 26.7)),), azimuth=-55.0, elevation=32.0,
             labels=(Label("Belt 2, looped on the pulley", at=(23.5, 40, 26.7), side="left"),
                     Label("Output pulley", "gt2_80_output", side="right"),
                     Label("Slot in the block's fork", at=(172, 22.5, 27), side="right"))),
        View("step40b_pin",
             built=FRAME,
             added={"output_block": _DROP, "gt2_80_output": _DROP, BELT_2: _DROP, "pin:base": (0, 0, -32)},
             guides=(Guide.between((160, 40, -20), (160, 40, 60)),), azimuth=-55.0, elevation=24.0,
             labels=(Label("Block, pulley and belt together", at=(225, 75, 94), side="right"),
                     Label("Pin, up from below, through the 6805", "pin:base", side="right"))),
        View("step40c_section",
             added=along_z(("base", "bearing_6805:base", *OUTPUT_SET, "pin:base"), 0.0),
             trim_x_from={"base": 120.0},
             clip_y=40.0, elevation=0.0, frame=1.05,
             labels=(Label("Pin stops against the block's boss", at=(148, 40, 7.2), side="right"),
                     Label("About 3 mm under the flange", at=(150, 40, -1.5), side="right"),
                     Label("Pin's tip just enters the pulley", at=(160, 40, 22), side="right"),
                     Label("Thick prong toward the base", at=(205, 40, 15), side="left"))),
    ),
)

_UP = (0.0, 0.0, 45.0)
step41 = Step(
    "41", "Fit the dual pulley and the belts",
    adds=("dowel_pin:dual_pulley", "dual_gt2_pulley", BELT_1),
    views=(
        View("step41a_dual",
             built=(*FRAME, *OUTPUT_SET, "pin:base", BELT_2),
             added={"dowel_pin:dual_pulley": (0, 0, 40), "dual_gt2_pulley": (0, 0, 75), "bushing:lower": (0, 0, 75),
                    "bushing:upper": (0, 0, 75)},
             guides=(Guide.between((75, 40, 10), (75, 40, 86)),), azimuth=-70.0, elevation=34.0,
             labels=(Label("Dual pulley: larger pulley down", "dual_gt2_pulley", side="left"),
                     Label("6 × 30 dowel, in the base's boss", "dowel_pin:dual_pulley", side="right"))),
        View("step41b_belts",
             built=(*FRAME, *OUTPUT_SET, "pin:base", *DUAL_SET),
             added={BELT_1: (0, 0, 0), BELT_2: (0, 0, 0)},
             azimuth=-80.0, elevation=58.0,
             labels=(Label("Belt 1: motor pulley to large dual pulley", at=(30, 55.4, 20), side="left"),
                     Label("Belt 2: small dual pulley to output pulley", at=(120, 56.6, 29.7), side="right"))),
    ),
)

step42 = Step(
    "42", "Fit the idlers and check the ratio",
    adds=(*IDLER_1, *IDLER_2),
    views=(
        View("step42a_stacks",
             built=(*FRAME, *PIN_1_SET, *DUAL_SET, BELT_1),
             added={"button_head_m5x40:idler_1": (0, 0, -40), "spacer_5mm:idler_1": (0, 0, 35),
                    "gt2_idler_20t:1": (0, 0, 50), "spacer_15mm:idler_1": (0, 0, 65),
                    "button_head_m5x40:idler_2": (0, 0, -40), "spacer_15mm:idler_2": (0, 0, 35),
                    "gt2_idler_20t:2": (0, 0, 50), "spacer_5mm:idler_2": (0, 0, 65)},
             guides=tuple(Guide.between((x, IDLER_Y, 4), (x, IDLER_Y, 45)) for x in IDLER_XS),
             azimuth=-75.0, elevation=20.0,
             labels=(Label("M5 × 40, up through the slot", "button_head_m5x40:idler_1", side="left"),
                     Label("15 mm spacer", "spacer_15mm:idler_1", side="left"),
                     Label("Idler", "gt2_idler_20t:1", side="left"),
                     Label("5 mm spacer", "spacer_5mm:idler_1", side="left"),
                     Label("5 mm spacer", "spacer_5mm:idler_2", side="right"),
                     Label("Idler", "gt2_idler_20t:2", side="right"),
                     Label("15 mm spacer", "spacer_15mm:idler_2", side="right"))),
        View("step42b_section",
             added=along_z(("base", "wall", "top", *IDLER_1, *IDLER_2, *NUTS), 0.0),
             trim_x={p: 130.0 for p in ("base", "wall", "top")},
             trim_x_from={p: 8.0 for p in ("base", "wall", "top")},
             clip_y=IDLER_Y, elevation=0.0, frame=1.3,
             labels=(Label("Motor end: 5 mm, idler, 15 mm", at=(32, 20, 17), side="right"),
                     Label("Joint end: 15 mm, idler, 5 mm", at=(117, 20, 27), side="left"),
                     Label("Head in the base's recess", at=(27.65, 20, 1.5), side="right"),
                     Label("Nut in the top's slot", at=(112.65, 20, 41), side="left"))),
    ),
)

_TOP_M3 = tuple(Hw.line("m3x10", (x, y, 41.0), (0, 0, -1), offset=(0, 0, 80)) for x, y in WALL_SCREWS)
step43 = Step(
    "43", "Close the segment with the top plate",
    adds=("top", *NUTS),
    views=(
        View("step43_top",
             built=BELOW_TOP,
             added={"top": (0, 0, 42), "bearing_6805:top": (0, 0, 42), NUTS[0]: (0, 0, 62), NUTS[1]: (0, 0, 62)},
             hardware=_TOP_M3,
             guides=(*(Guide.between((x, y, 37), (x, y, 110)) for x, y in WALL_SCREWS),
                     *(Guide.between((x, IDLER_Y, 44), (x, IDLER_Y, 100)) for x in IDLER_XS)),
             azimuth=-70.0, elevation=30.0,
             labels=(Label("Top", at=(190, 40, 86), side="right"),
                     Label("M5 nut × 2, in the slots", NUTS[0], side="left"),
                     Label("M3 × 10 × 7", "hw:5", side="right"))),
    ),
)

step44 = Step(
    "44", "Fit the second pin",
    adds=("pin:top",),
    views=(
        View("step44_pin",
             added={**along_z(("base", "top", *BEARINGS, *OUTPUT_SET, "pin:base"), 0.0), "pin:top": (0, 0, 35)},
             trim_x_from={"base": 120.0, "top": 120.0},
             guides=(Guide.between((160, 40, 52), (160, 40, 70)),), clip_y=40.0, elevation=0.0, frame=1.05,
             labels=(Label("Second pin, down from above", "pin:top", side="right"),
                     Label("Hex through the fork and the pulley", at=(170, 40, 27), side="left"),
                     Label("Clamp between the two flanges", at=(150, 40, -4.8), side="right"))),
    ),
)

step45 = Step(
    "45", "Fit the jack screws",
    adds=JACKS,
    views=(
        View("step45_jacks",
             built=(*CLOSED, "pin:top"),
             added={JACKS[0]: (0, -30, 0), JACKS[1]: (0, -30, 0)},
             guides=tuple(Guide.between((x, -55, z), (x, 0, z)) for x, z in JACK_XZ),
             azimuth=-75.0, elevation=16.0,
             labels=(Label("M3 × 35 × 2, in the rail's inserts", JACKS[1], side="right"),)),
    ),
)

_J3_SET = (*OUTPUT_SET, "pin:base", "pin:top")
step46 = Step(
    "46", "Tension the belts",
    views=(
        View("step46a_inside",
             built=(*FRAME, *PIN_1_SET, *DUAL_SET, *IDLER_1, *IDLER_2),
             added={BELT_1: (0, 0, 0), BELT_2: (0, 0, 0), JACKS[0]: (0, 0, 0), JACKS[1]: (0, 0, 0)},
             azimuth=-78.0, elevation=52.0,
             labels=(Label("Jack screw pushes the idler into the belt", JACKS[0], side="left"),
                     Label("Second jack screw, the same", JACKS[1], side="right"),
                     Label("Top left off in this picture", at=(200, 70, 30), side="right"))),
        View("step46b_below",
             added=along_z(("base", "wall", "bearing_6805:base", *MOTOR_SET, "pin:base", "output_block",
                            *JACKS, IDLER_1[0], IDLER_2[0]), 0.0),
             azimuth=-70.0, elevation=-40.0,
             labels=(Label("Tighten each M5 from below", at=(112.65, 20, 0.3), side="right"),
                     Label("Motor-end M5", at=(27.65, 20, 0.3), side="left"),
                     Label("Motor", "nema17:j3", side="left"))),
    ),
)

_J3_AXIS = ((*J3, 0.0), (0.0, 0.0, 1.0))
step47 = Step(
    "47", "Check the segment",
    views=(
        View("step47_turned",
             built=tuple(p for p in PARTS if p not in _J3_SET),
             added=along_z(_J3_SET, 0.0),
             turned={p: (*_J3_AXIS, 90.0) for p in _J3_SET},
             azimuth=-60.0, elevation=32.0,
             labels=(Label("Block: −94° to +103° from straight", "output_block", side="right"),)),
    ),
)

step48 = Step("48", "Build the second segment")

STEPS = [overview, parts_sheets, step34, step35, step36, step37, step38, step39, step40, step41, step42,
         step43, step44, step45, step46, step47, step48]
