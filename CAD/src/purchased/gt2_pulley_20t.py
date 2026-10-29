"""GT2 20T pulley, 5 mm bore, 6 mm belt.

Vendor STEP from step.parts: https://www.step.parts/parts/gt2_pulley_20t_bore5_w6
(downloaded and sha256-verified 2026-10-26). Frame: axis +Z, end face at z=0.
The vendor file bores only the toothed band (z 1..9) and leaves both 1 mm
flanges solid, so the Ø5 bore is cut through here (found in Session 4: the
J1 motor shaft ran into the flange).
"""
from pathlib import Path

import build123d as bd
from cadgen import read_step, step

BORE = 5.0
_VENDOR = Path(__file__).resolve().parents[2] / "STEP" / "imported" / "vendor"


@step(out="../../STEP/purchased/gt2_pulley_20t.step")
def gt2_pulley_20t():
    part = bd.Pos(0, 0, 5.0) * read_step(_VENDOR / "gt2_pulley_20t_bore5_w6.step")
    part -= bd.Cylinder(BORE / 2, 10.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    part.label = "gt2_pulley_20t"
    return part


if __name__ == "__main__":
    gt2_pulley_20t()
