"""GT2 20T toothed idler, 5 mm bore, 6 mm belt (Fusion bore; issue I-5).

Vendor STEP from step.parts: https://www.step.parts/parts/gt2_toothed_idler_bore5_w6
(downloaded and sha256-verified 2026-10-26). Frame: axis +Z, end face at z=0.
Like the vendor 20T pulley, the file bores only the toothed band and leaves
both 1 mm flanges solid, so the Ø5 bore is cut through here (Session 5).
"""
from pathlib import Path

import build123d as bd
from cadgen import read_step, step

BORE = 5.0
_VENDOR = Path(__file__).resolve().parents[2] / "STEP" / "imported" / "vendor"


@step(out="../../STEP/purchased/gt2_idler_20t.step")
def gt2_idler_20t():
    part = bd.Pos(0, 0, 5.0) * read_step(_VENDOR / "gt2_toothed_idler_bore5_w6.step")
    part -= bd.Cylinder(BORE / 2, 10.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    part.label = "gt2_idler_20t"
    return part


if __name__ == "__main__":
    gt2_idler_20t()
