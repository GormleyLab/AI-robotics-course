"""ISO 4032 hex nut M5 (8 AF x 4): the arm idler axle nut (I-5).

Vendor STEP from step.parts: https://www.step.parts/parts/iso4032_hex_nut_m5
(downloaded and sha256-verified 2026-10-27). Frame: axis +Z, faces at z=0
and 4, flats on +-X, so it fits the Top's 8 mm idler slot (along Y)
flats-first and cannot turn in it.
"""
from pathlib import Path

from cadgen import read_step, step

_VENDOR = Path(__file__).resolve().parents[2] / "STEP" / "imported" / "vendor"


@step(out="../../STEP/purchased/hex_nut_m5.step")
def hex_nut_m5():
    part = read_step(_VENDOR / "iso4032_hex_nut_m5.step")
    part.label = "hex_nut_m5"
    return part


if __name__ == "__main__":
    hex_nut_m5()
