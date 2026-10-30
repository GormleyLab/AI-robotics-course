"""Print-process fit allowances, chosen per part.

Every fit feature of the printed parts (I-11 fixed) is its Fusion value
plus (hole) or minus (shaft) the allowance for its class in the part's
profile: ``profile("<part>")`` returns ``PART_PROFILES[part]`` if listed,
else ``DEFAULT``. The committed values are ``DEFAULT = FUSION`` and no
overrides, so the models and their STEPs stay the Fusion replica and pass
the gate; never commit them changed. Print sets are built by
``tools/print_parts.py``, which calls ``configure()`` with a git-ignored
config in its own process before importing any part, and writes to
``tmp/print/``, never ``STEP/``. Each part sizes only the features it
contains, so a resin part next to a PLA part needs nothing else.

Each fit is a diametral allowance in mm. Classes (design.md §6, Print fits):
``press`` bearing ODs in printed seats, printed shafts in bearing bores,
bushings and planet pins in printed holes; ``slip`` parts that slide in or
along by hand (dowel, M5 nut slot, thrust washer recess, motor shaft bore);
``running`` is unused (nothing turns in a printed bore); ``clearance`` screw
holes and slots; ``hex_socket`` female hexes, across flats.

Threaded-insert holes are absolute diameters per profile, not allowances,
because the method differs: heat-set inserts melt into a hole smaller than
their knurls (FDM), and cured resin does not melt, so resin parts take the
same inserts bonded with epoxy in a hole over the knurls. Inserts: ruthex
M3 x 5.7 (knurl Ø4.6, heat-set hole Ø4.0) and M5 x 9.5 (knurl Ø7.1, hole
Ø6.4).
"""
from __future__ import annotations

from dataclasses import dataclass, fields, replace


@dataclass(frozen=True)
class FitProfile:
    name: str
    press: float      # bearing OD into printed seat
    slip: float       # dowel / pin that must slide in by hand
    running: float    # shaft turning in a printed bore
    clearance: float  # screw clearance on top of the nominal clearance hole
    hex_socket: float # male hex into female hex (across flats)
    insert_m3: float  # M3 threaded-insert hole diameter
    insert_m5: float  # M5 threaded-insert hole diameter

    @property
    def m3_clear(self) -> float:
        return hole(3.3, self.clearance)

    @property
    def m5_clear(self) -> float:
        return hole(5.3, self.clearance)


# Fusion's sizes; its insert holes are heat-set holes (M3 0.2 over the ruthex 4.0).
FUSION = FitProfile("fusion-nominal", 0.0, 0.0, 0.0, 0.0, 0.0, insert_m3=4.2, insert_m5=6.4)

# Starting points for PLA on a 0.4 mm nozzle; tune with the fit coupon.
# Heat-set insert holes as on the built arm.
PLA_FDM = FitProfile("pla-fdm", press=0.10, slip=0.20, running=0.35, clearance=0.2, hex_socket=0.25,
                     insert_m3=4.2, insert_m5=6.4)

# Starting points for Formlabs / standard resin (SLA/MSLA). Inserts are bonded
# with epoxy, not heat-set: knurl OD + 0.2 glue gap.
RESIN = FitProfile("resin-sla", press=0.05, slip=0.10, running=0.20, clearance=0.1, hex_socket=0.15,
                   insert_m3=4.8, insert_m5=7.3)

DEFAULT = FUSION

# Per-part overrides: part name (its model / STEP name) -> profile.
PART_PROFILES: dict[str, FitProfile] = {}

# Printed parts that call profile(); PART_PROFILES keys must be among them.
PARTS = (
    "box_bottom", "box_top", "hinge", "coupling_shaft", "gt2_pulley_160t",
    "ring_gear", "back_cover", "front_cover", "nema17_mount", "input_shaft", "planet_gear",
    "carrier_plate", "carrier_stage1_output", "carrier_stage2_output",
    "base", "wall", "top", "dual_gt2_pulley", "gt2_80_output", "pin", "output_block",
    "fit_coupon",
)
_unknown = set(PART_PROFILES) - set(PARTS)
if _unknown:
    raise ValueError(f"PART_PROFILES names unknown parts {sorted(_unknown)}; known: {PARTS}")


# The presets by name, as a print config names them.
PROFILES = {"FUSION": FUSION, "PLA_FDM": PLA_FDM, "RESIN": RESIN}

_resolved = False  # set by the first profile() call; configure() must come before it


def profile(part: str) -> FitProfile:
    """Fit profile for the printed part ``part`` (its model name)."""
    global _resolved
    if part not in PARTS:
        raise ValueError(f"{part!r} is not in tolerances.PARTS")
    _resolved = True
    return PART_PROFILES.get(part, DEFAULT)


def configure(default: str = "FUSION", parts: dict[str, str] | None = None,
              profiles: dict[str, dict] | None = None) -> None:
    """Choose this process's profiles from a print config (``tools/print_parts.py``).

    ``profiles`` adjusts a preset (``{"RESIN": {"press": 0.07}}``) or adds one
    from a ``base`` (``{"TOUGH": {"base": "RESIN", "press": 0.08}}``);
    ``default`` and ``parts`` (part name -> profile name) pick from them. Each
    part module reads its profile once, at import, so this must run before any
    part is imported; it raises if a profile was already handed out. It changes
    only this process: the models and committed STEPs keep ``FUSION``."""
    global DEFAULT, PART_PROFILES
    if _resolved:
        raise RuntimeError("configure() after profile(): a part module was imported first")
    named = dict(PROFILES)
    for name, values in (profiles or {}).items():
        values = dict(values)
        base = values.pop("base", name)
        if base not in named:
            raise ValueError(f"profile {name!r}: unknown base {base!r}; known: {sorted(named)}")
        unknown = set(values) - {f.name for f in fields(FitProfile)} - {"name"}
        if unknown:
            raise ValueError(f"profile {name!r}: unknown fields {sorted(unknown)}")
        values.setdefault("name", name.lower().replace("_", "-"))
        named[name] = replace(named[base], **values)
    for name in [default, *(parts or {}).values()]:
        if name not in named:
            raise ValueError(f"unknown profile {name!r}; known: {sorted(named)}")
    unknown = set(parts or {}) - set(PARTS)
    if unknown:
        raise ValueError(f"parts names unknown parts {sorted(unknown)}; known: {PARTS}")
    DEFAULT = named[default]
    PART_PROFILES = {part: named[name] for part, name in (parts or {}).items()}


def hole(nominal: float, fit: float) -> float:
    """Diameter to model for a hole that must accept ``nominal`` with ``fit``."""
    return nominal + fit


def shaft(nominal: float, fit: float) -> float:
    """Diameter to model for a printed shaft that must enter a ``nominal`` bore with ``fit``."""
    return nominal - fit


def hex_socket_r(circumradius: float, fit: float) -> float:
    """Circumradius of a female hex opened by ``fit`` across flats."""
    return circumradius + fit / 3 ** 0.5
