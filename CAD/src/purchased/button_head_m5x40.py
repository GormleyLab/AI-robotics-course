"""ISO 7380 button head socket screw M5 x 40: the arm idler axle (I-5).

Vendor STEP from step.parts: https://www.step.parts/parts/button_head_screw_m5_l0040_simple
(downloaded and sha256-verified 2026-10-27). The vendor frame has the head
seat at z=0 and the shank along -Z; it is flipped here so the shank runs
along +Z from the seat at z=0 and the head (Ø9.5 x 2.75) sits below.
"""
from pathlib import Path

import build123d as bd
from cadgen import read_step, step

_VENDOR = Path(__file__).resolve().parents[2] / "STEP" / "imported" / "vendor"


@step(out="../../STEP/purchased/button_head_m5x40.step")
def button_head_m5x40():
    part = bd.Rot(180, 0, 0) * read_step(_VENDOR / "button_head_screw_m5_l0040_simple.step")
    part.label = "button_head_m5x40"
    return part


if __name__ == "__main__":
    button_head_m5x40()
