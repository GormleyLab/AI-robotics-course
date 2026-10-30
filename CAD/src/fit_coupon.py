"""Print-fit test coupon (I-11): one of each fit, at its profile (``profile("fit_coupon")``).

Not an arm part and not in Fusion, so it is not gated. Build it at the
profile you mean to use with ``tools/print_parts.py`` (``--only fit_coupon``),
try each feature with its hardware, and adjust the profile in the print
config before building the arm parts.

172 x 64 x 6 plate, z 0..6. Back row (y = 42), left to right: 6805 seat
Ø37 (press), output hex socket 21.65 AF (hex_socket, try the printed Pin or
the stage-2 output hex), 608 seat Ø22 (press), 6801 seat Ø21 (press), and a
Ø25 x 7 peg for the 6805 bore (printed shaft, press). Front row (y = 11):
planet pin Ø6 (press), bushing Ø8 (press), dowel Ø6.1 (slip), M3 Ø3.3 and
M5 Ø5.3 (clearance), the 8 mm M5 nut slot (slip), M3 and M5 threaded-insert
holes (heat-set in FDM, bonded in resin; the M5 insert stands 3.5 proud of
the 6 mm plate), and a Ø12 x 5 peg for the 6801 bore (printed shaft, press).
"""
import build123d as bd
from cadgen import step

from lib import params
from lib.tolerances import hex_socket_r, hole, profile, shaft

FIT = profile("fit_coupon")

L, W, T = 172.0, 64.0, 6.0
BACK_Y, FRONT_Y = 42.0, 11.0
_CMIN = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)


def _cyl(d, x, y, z0, z1):
    return bd.Pos(x, y, z0) * bd.Cylinder(d / 2, z1 - z0, align=_CMIN)


def fit_coupon_body():
    body = bd.Box(L, W, T, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN))
    for d, x in ((hole(params.BEARING_6805_SEAT_D, FIT.press), 22.0),
                 (hole(params.BEARING_608_SEAT_D, FIT.press), 94.0),
                 (hole(21.0, FIT.press), 123.0)):
        body -= _cyl(d, x, BACK_Y, 0, T)
    hex_r = hex_socket_r(params.OUTPUT_HEX_SOCKET_R, FIT.hex_socket)
    body -= bd.Pos(60.0, BACK_Y, 0) * bd.extrude(bd.RegularPolygon(hex_r, 6), T)
    body += _cyl(shaft(params.OUTPUT_SHAFT_D, FIT.press), 155.0, BACK_Y, T, T + 7.0)
    for d, x in ((hole(6.0, FIT.press), 10.0), (hole(8.0, FIT.press), 24.0), (hole(6.1, FIT.slip), 38.0),
                 (FIT.m3_clear, 52.0), (FIT.m5_clear, 66.0), (FIT.insert_m3, 106.0), (FIT.insert_m5, 122.0)):
        body -= _cyl(d, x, FRONT_Y, 0, T)
    nut_w = hole(8.0, FIT.slip)
    body -= bd.Pos(85.0, FRONT_Y, 0) * bd.extrude(bd.SlotCenterToCenter(10.0, nut_w), T)
    body += _cyl(shaft(12.0, FIT.press), 155.0, FRONT_Y, T, T + 5.0)
    return body


@step(out="../STEP/fit_coupon.step")
def fit_coupon():
    part = fit_coupon_body()
    part.label = "fit_coupon"
    return part


if __name__ == "__main__":
    fit_coupon()
