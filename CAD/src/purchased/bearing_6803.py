"""6803-2RS bearing 17x26x5.

Vendor STEP from step.parts: https://www.step.parts/parts/bearing_6803_2rs
(downloaded and sha256-verified 2026-10-26). Frame: axis +Z, end face at z=0.
"""
from pathlib import Path

import build123d as bd
from cadgen import read_step, step

_VENDOR = Path(__file__).resolve().parents[2] / "STEP" / "imported" / "vendor"


@step(out="../../STEP/purchased/bearing_6803.step")
def bearing_6803():
    part = bd.Pos(0, 0, 2.5) * read_step(_VENDOR / "bearing_6803_2rs.step")
    part.label = "bearing_6803"
    return part


if __name__ == "__main__":
    bearing_6803()
