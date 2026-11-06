"""Step lists for the assembly guide (docs/assembly-*.md), rendered by tools/render_assembly.py.

One module per chapter. A chapter names its assembly STEP, its image folder and a
list of ``Step``. Each step says which assembly parts it adds (``adds``, checked
by checks/assembly_steps.py: every part exactly once) and which pictures show it.
A picture (``View``) places parts of three kinds:

- ``added``: drawn in colour, each moved by its offset along its insertion path;
- ``built``: already in place, drawn pale;
- ``hardware``: screws, inserts and the set screw, which the CAD assemblies do not
  model. They exist only in these pictures.

Everything is in the assembly's own frame. For the gearbox: axis +Z, toward the motor.
A chapter can set ``ORIGIN`` (a point in the assembly's frame) to work with that point
at the origin, as the joint chapters do with J1.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

Vec = tuple[float, float, float]


@dataclass(frozen=True)
class Hw:
    """One piece of hardware: ``kind`` (see render_assembly.HARDWARE) at cylindrical
    (r, angle, z). Its seat is at z and its body runs toward +z, or -z if ``down``."""
    kind: str
    r: float
    angle: float
    z: float
    down: bool = False
    built: bool = False            # drawn pale, like ``built``
    offset: Vec = (0.0, 0.0, 0.0)
    radial: bool = False           # body points in toward the axis, seat at r, instead of along z
    seat: Vec | None = None        # with ``direction``: a seat and body direction, in place of r, angle, z
    direction: Vec | None = None

    @classmethod
    def at(cls, kind: str, x: float, y: float, z: float = 0.0) -> "Hw":
        """Hardware laid out at (x, y), for the parts sheets."""
        return cls(kind, math.hypot(x, y), math.degrees(math.atan2(y, x)), z)

    @classmethod
    def line(cls, kind: str, seat: Vec, direction: Vec, offset: Vec = (0.0, 0.0, 0.0), built: bool = False) -> "Hw":
        """Hardware along any direction, for screws that don't run along the chapter's axis."""
        return cls(kind, 0.0, 0.0, 0.0, built=built, offset=offset, seat=seat, direction=direction)


@dataclass(frozen=True)
class Guide:
    """A dashed line, from the part to where it goes, at cylindrical (r, angle)."""
    r: float
    angle: float
    z0: float
    z1: float
    p0: Vec | None = None          # with ``p1``: a line between two points, in place of the above
    p1: Vec | None = None

    @classmethod
    def between(cls, p0: Vec, p1: Vec) -> "Guide":
        return cls(0.0, 0.0, 0.0, 0.0, p0=p0, p1=p1)


@dataclass(frozen=True)
class Label:
    """A callout: ``text`` with a leader to ``part`` (an assembly label or a hardware
    index "hw:N"), or to the point ``at`` if given. ``side`` picks the margin."""
    text: str
    part: str = ""
    at: Vec | None = None
    nudge: Vec = (0.0, 0.0, 0.0)
    side: str = "auto"


@dataclass
class View:
    name: str
    added: dict[str, Vec] = field(default_factory=dict)
    # label -> (point on the axis, axis direction, degrees), applied before any offset:
    # a part shown turned on its joint.
    turned: dict[str, tuple[Vec, Vec, float]] = field(default_factory=dict)
    trim_x: dict[str, float] = field(default_factory=dict)  # label -> keep only x below this: a cut-away part
    trim_x_from: dict[str, float] = field(default_factory=dict)  # label -> keep only x above this
    built: tuple[str, ...] = ()
    hardware: tuple[Hw, ...] = ()
    guides: tuple[Guide, ...] = ()
    labels: tuple[Label, ...] = ()
    azimuth: float = -60.0
    elevation: float = 22.0
    turn: float = 0.0              # the whole scene about +Z, degrees
    clip_y: float | None = None    # keep y below this plane; look from +y
    ghost: bool = False            # ``built`` parts see-through instead of pale
    frame: float = 1.0             # >1 leaves more room around the model
    roll: float = 0.0              # turns the picture, degrees: a long axis can lie on the diagonal
    layout: dict[str, tuple[float, float]] = field(default_factory=dict)  # part -> (x, y), standing on z = 0
    path: str = ""                 # picture, relative to docs/img, in place of the chapter's folder
    size: tuple[int, int] = (1600, 1200)


@dataclass
class Step:
    number: str
    title: str
    adds: tuple[str, ...] = ()
    views: tuple[View, ...] = ()


def along_z(labels, dz: float) -> dict[str, Vec]:
    """Offsets moving each of ``labels`` by dz along the axis."""
    return {label: (0.0, 0.0, dz) for label in labels}
