"""GT2 20T pulley, 5 mm bore, 6 mm belt.

Vendor STEP from step.parts: https://www.step.parts/parts/gt2_pulley_20t_bore5_w6
(downloaded and sha256-verified 2026-10-26). Frame: axis +Z, end face at z=0.
"""
from pathlib import Path

from cadgen import build123d as bd
from cadgen import read_step, step

_VENDOR = Path(__file__).resolve().parents[2] / "STEP" / "imported" / "vendor"


@step(out="../../STEP/purchased/gt2_pulley_20t.step")
def gt2_pulley_20t():
    part = bd.Pos(0, 0, 5.0) * read_step(_VENDOR / "gt2_pulley_20t_bore5_w6.step")
    part.label = "gt2_pulley_20t"
    return part


if __name__ == "__main__":
    gt2_pulley_20t()
