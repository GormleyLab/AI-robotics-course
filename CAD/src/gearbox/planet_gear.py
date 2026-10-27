"""Planet gear: 15T, transverse m1.5, right-hand 15 deg helix, 9 wide, Ø8 bore.

Own frame: axis +Z, z 0..9, tooth 0 centred on +X at z = 0. Placements (6,
see gearbox.py) put it at r = 22.5 with the measured Fusion tooth phases.
"""
from cadgen import step

from gearbox.carrier import BACKLASH, HELIX, MODULE, ROOT_FILLET, TIP_CHAMFER
from lib import gears, params
from lib.tolerances import ACTIVE as FIT, hole as fit_hole

WIDTH = params.GEAR_FACE_WIDTH
BORE = fit_hole(8.0, FIT.press)        # 6 x 8 x 10 bushing OD


@step(out="../../STEP/gearbox/planet_gear.step")
def planet_gear():
    part = gears.spur_gear(params.PLANET_TEETH, MODULE, WIDTH, backlash=BACKLASH, bore=BORE,
                           tip_chamfer=TIP_CHAMFER, helix_angle=HELIX, root_fillet=ROOT_FILLET)
    part.label = "planet_gear"
    return part


if __name__ == "__main__":
    planet_gear()
