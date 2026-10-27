"""608-2RS bearing 8x22x7.

Vendor STEP from step.parts: https://www.step.parts/parts/bearing_608_2rs_sealed_simple
(downloaded and sha256-verified 2026-10-26). Frame: axis +Z, end face at z=0.
"""
from pathlib import Path

from cadgen import read_step, step

_VENDOR = Path(__file__).resolve().parents[2] / "STEP" / "imported" / "vendor"


@step(out="../../STEP/purchased/bearing_608.step")
def bearing_608():
    part = read_step(_VENDOR / "bearing_608_2rs_sealed_simple.step")
    part.label = "bearing_608"
    return part


if __name__ == "__main__":
    bearing_608()
