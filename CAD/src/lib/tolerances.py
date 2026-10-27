"""Print-process fit allowances.

The replica keeps every Fusion dimension at its nominal value (Fusion had no
allowances; issue I-11), so these presets are all zero-offset in the
``FUSION`` profile. The fix phase switches parts to ``PLA_FDM`` or ``RESIN``.

Each fit is a diametral allowance in mm, added to a nominal hole diameter
(or subtracted from a nominal shaft): ``hole_d = nominal + fit``.
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
