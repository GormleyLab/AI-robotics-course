"""Print-process fit allowances.

Every fit feature of the printed parts (I-11 fixed) is its Fusion value
plus (hole) or minus (shaft) the allowance for its class in ``ACTIVE``. The
committed STEPs use ``FUSION`` (all zero), so they stay the Fusion replica
and pass the gate. To print, set ``ACTIVE = PLA_FDM`` (or ``RESIN``) and
rerun the models; tune the profile first with ``src/fit_coupon.py``.

Each fit is a diametral allowance in mm. Classes (design.md §6, Print fits):
``press`` bearing ODs in printed seats, printed shafts in bearing bores,
bushings and planet pins in printed holes; ``slip`` parts that slide in or
along by hand (dowel, M5 nut slot, thrust washer recess, motor shaft bore);
``running`` is unused (nothing turns in a printed bore); ``clearance`` screw
holes and slots; ``hex_socket`` female hexes, across flats. Heat-set insert
holes follow the insert maker's size and are not adjusted.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FitProfile:
    name: str
    press: float      # bearing OD into printed seat
    slip: float       # dowel / pin that must slide in by hand
    running: float    # shaft turning in a printed bore
    clearance: float  # screw clearance on top of the nominal clearance hole
    hex_socket: float # male hex into female hex (across flats)


FUSION = FitProfile("fusion-nominal", 0.0, 0.0, 0.0, 0.0, 0.0)

# Starting points for PLA on a 0.4 mm nozzle; tune with test coupons.
PLA_FDM = FitProfile("pla-fdm", press=0.10, slip=0.20, running=0.35, clearance=0.2, hex_socket=0.25)

# Starting points for standard resin (SLA/MSLA).
RESIN = FitProfile("resin-sla", press=0.05, slip=0.10, running=0.20, clearance=0.1, hex_socket=0.15)

ACTIVE = FUSION


def hole(nominal: float, fit: float) -> float:
    """Diameter to model for a hole that must accept ``nominal`` with ``fit``."""
    return nominal + fit


def shaft(nominal: float, fit: float) -> float:
    """Diameter to model for a printed shaft that must enter a ``nominal`` bore with ``fit``."""
    return nominal - fit


def hex_socket_r(circumradius: float, fit: float) -> float:
    """Circumradius of a female hex opened by ``fit`` across flats."""
    return circumradius + fit / 3 ** 0.5
