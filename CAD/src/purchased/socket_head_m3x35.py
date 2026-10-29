"""ISO 4762 socket head cap screw M3 x 35: the arm idler jack screw (I-4).

Vendor STEP from step.parts: https://www.step.parts/parts/iso4762_socket_head_cap_screw_m3x35
(downloaded and sha256-verified 2026-10-27). The vendor frame has the head
seat at z=0 and the shank along -Z; it is flipped here so the shank runs
along +Z from the seat at z=0 and the head (Ø5.5 x 3) sits below.
"""
from pathlib import Path

import build123d as bd
from cadgen import read_step, step

_VENDOR = Path(__file__).resolve().parents[2] / "STEP" / "imported" / "vendor"


@step(out="../../STEP/purchased/socket_head_m3x35.step")
def socket_head_m3x35():
    part = bd.Rot(180, 0, 0) * read_step(_VENDOR / "iso4762_socket_head_cap_screw_m3x35.step")
    part.label = "socket_head_m3x35"
    return part


if __name__ == "__main__":
    socket_head_m3x35()
