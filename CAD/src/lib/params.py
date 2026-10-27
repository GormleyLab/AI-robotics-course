"""Locked interface dimensions (CAD/docs/design.md §5).

Values are the Fusion baseline, measured from the STEP exports. Changing any
of these is a breaking interface change: update design.md §5 in the same
commit and call it out.
"""

# --- IF-1: J1 axis (Joint 1 and 2 frame: box corner origin, top of Box bottom at z=0)
J1_AXIS_XY = (75.0, 75.0)
J1_SHAFT_D = 35.0                 # Hinge vertical shaft (6807 bore)
BEARING_6807_SEAT_D = 47.0
THRUST_RECESS_BOX_D = 60.0        # Box top underside recess (lower thrust bearing)
THRUST_RECESS_HINGE_D = 61.0      # Hinge underside pocket (upper thrust bearing)
BEARING_608_SEAT_D = 22.0

# --- IF-2: base box
BOX_X, BOX_Y = 180.0, 150.0
BOX_BOTTOM_H, BOX_TOP_H = 30.0, 12.0
BOX_M5_XY = (
    (7.5, 7.5), (90.0, 7.5), (172.5, 7.5),
    (7.5, 142.5), (90.0, 142.5), (172.5, 142.5),
    (7.5, 75.0),
)

# --- IF-3: J1 motor slot in Box top
J1_MOTOR_SLOT_W = 25.0
J1_MOTOR_SLOT_X = (140.0, 160.0)  # motor-centre travel
J1_MOTOR_SLOT_Y = 75.0
J1_MOTOR_SCREW_SLOT_Y = (59.5, 90.5)

# --- IF-4/5: J2 axis and gearbox-to-hinge bolt circle
J2_AXIS_YZ_HINGE = (75.0, 70.5)    # hinge 6805 seats and coupling shaft
J2_AXIS_YZ_GEARBOX = (75.0, 70.0)  # gearbox (0.5 mm low: issue I-1, reproduced)
BEARING_6805_SEAT_D = 37.0
GEARBOX_BOLT_CIRCLE_R = 39.25
GEARBOX_BOLT_COUNT = 6

# --- IF-6: gearbox internals
GEAR_MODULE = 1.5
GEAR_PRESSURE_ANGLE = 20.0
GEAR_HELIX_ANGLE = 15.0           # transverse module 1.5; measured Session 3
SUN_TEETH = 15
PLANET_TEETH = 15
RING_TEETH = 45
PLANETS_PER_STAGE = 3
PLANET_CENTRE_R = GEAR_MODULE * (SUN_TEETH + PLANET_TEETH) / 2  # 22.5
GEAR_FACE_WIDTH = 9.0
GEARBOX_OD = 85.0

# --- IF-7: gearbox output hex
OUTPUT_HEX_AF = 21.48              # male hex on Carrier p2 output and arm Pins
OUTPUT_HEX_SOCKET_AF = 21.66       # female hex in Coupling shaft and GT2-80 output
OUTPUT_SHAFT_D = 25.0

# --- IF-8: universal link interface (4 x M3)
LINK_BOLT_SPACING = (73.0, 37.0)   # across arm width x across arm thickness
ARM_WIDTH = 80.0
ARM_THICKNESS = 44.0

# --- IF-9: NEMA17
NEMA17_BOLT_SPACING = 31.0
NEMA17_PILOT_D = 22.0
NEMA17_SHAFT_D = 5.0

# --- IF-10: J3 output (Belt Drive Arm frame: plates in XY, Base underside z=0)
J3_AXIS_XY = (160.0, 40.0)
ARM_MOTOR_XY = (-10.0, 40.0)
ARM_DUAL_PULLEY_XY = (75.0, 40.0)
ARM_IDLER_XY = ((27.65, 20.0), (112.65, 20.0))

# --- IF-11: GT2 belt drive
GT2_PITCH = 2.0
GT2_BELT_WIDTH = 6.0
GT2_TEETH_MOTOR = 20
GT2_TEETH_ARM_DRIVEN = 80
GT2_TEETH_J1 = 160
