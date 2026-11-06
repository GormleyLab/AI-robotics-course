"""Render the assembly guide's pictures from a chapter's step list.

    cd CAD
    PYTHONPATH=src ~/.local/bin/cadgen +0.8.2 run tools/render_assembly.py gearbox
    PYTHONPATH=src ~/.local/bin/cadgen +0.8.2 run tools/render_assembly.py gearbox --only step03

Parts come from the chapter's committed assembly STEP, read and not rebuilt, so
this never writes to STEP/. Each picture's scene is written to tmp/assembly/ and
drawn by cadgen from an exact camera, which lets the callouts be placed over it
with Pillow. Pictures go to docs/img/assembly/<chapter>/.
"""
from __future__ import annotations

import argparse
import importlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for extra in (ROOT, ROOT / "tools", ROOT / "src"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))

import build123d as bd
import cadgen
from PIL import Image, ImageDraw, ImageFont

from assembly_steps import Guide, Hw, Label, View
from checks.scene import read_scene
from lib import gt2, params

PALE = "#d5d9df"
GHOST_ALPHA = 0.28
GUIDE_COLOR = "#39424e"
TAG_INK = "#1f2933"
SUPERSAMPLE = 3
TMP = ROOT / "tmp" / "assembly"


# --- hardware stand-ins, for pictures only -------------------------------------------------


def _button_head(length: float, thread: float = 3.0, head_d: float = 5.7, head_h: float = 1.65,
                 socket_d: float = 2.3) -> bd.Part:
    """ISO 7380 button head, seat at z 0, shank toward +z (M3 unless told otherwise)."""
    head = bd.Pos(0, 0, -head_h) * bd.Cylinder(head_d / 2, head_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    shank = bd.Cylinder(thread / 2, length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    socket = bd.Pos(0, 0, -head_h) * bd.Cylinder(socket_d / 2, 1.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return head + shank - socket


def _m5(length: float) -> bd.Part:
    return _button_head(length, thread=5.0, head_d=9.5, head_h=2.75, socket_d=3.4)


def _nut_m5() -> bd.Part:
    """ISO 4032 M5 nut, 8 AF x 4.7, from z 0 toward +z."""
    return (bd.extrude(bd.RegularPolygon(4.62, 6), 4.7)
            - bd.Cylinder(2.5, 4.7, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))


def _j1_belt() -> bd.Part:
    """The J1 belt, in the assembly CAD only as this stand-in (I-8): J1 at the origin, 6 mm wide from z 0."""
    centres = gt2.centre_distance(370.0, params.GT2_TEETH_J1, params.GT2_TEETH_MOTOR)
    return gt2.belt_envelope([(0.0, 0.0, gt2.pitch_diameter(params.GT2_TEETH_J1) / 2),
                              (centres, 0.0, gt2.pitch_diameter(params.GT2_TEETH_MOTOR) / 2)])


def _spacer() -> bd.Part:
    """A round press spacer, Ø24 x 40, from z 0 toward +z."""
    return bd.Cylinder(12.0, 40.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _plate() -> bd.Part:
    """A flat press plate, 60 x 60 x 4, from z 0 toward +z."""
    return bd.Box(60.0, 60.0, 4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _insert(length: float, knurl_d: float = 4.6, bore_d: float = 3.0) -> bd.Part:
    """Threaded insert, body from z 0 to +z."""
    return (bd.Cylinder(knurl_d / 2, length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            - bd.Cylinder(bore_d / 2, length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))


def _set_screw() -> bd.Part:
    """M4 x 5 set screw with a 2 mm hex socket at z 0, body toward +z."""
    return (bd.Cylinder(2.0, 5.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            - bd.extrude(bd.RegularPolygon(1.15, 6), 2.0))


HARDWARE = {
    "m3x10": (lambda: _button_head(10.0), "#2e3540"),
    "m3x12": (lambda: _button_head(12.0), "#2e3540"),
    "m3x16": (lambda: _button_head(16.0), "#2e3540"),
    "m3x18": (lambda: _button_head(18.0), "#2e3540"),
    "m3x20": (lambda: _button_head(20.0), "#2e3540"),
    "m3x22": (lambda: _button_head(22.0), "#2e3540"),
    "m5x20": (lambda: _m5(20.0), "#2e3540"),
    "m5x40": (lambda: _m5(40.0), "#2e3540"),
    "nut_m5": (_nut_m5, "#5c6670"),
    "insert_m3": (lambda: _insert(5.7), "#c9a227"),
    "insert_m3s": (lambda: _insert(4.0), "#c9a227"),
    "insert_m5": (lambda: _insert(9.5, knurl_d=7.1, bore_d=5.0), "#c9a227"),
    "belt_j1": (_j1_belt, "#3b3f46"),
    "spacer": (_spacer, "#c4b59a"),
    "plate": (_plate, "#c4b59a"),
    "set_screw": (_set_screw, "#2e3540"),
}


def _colour(text: str, alpha: float = 1.0) -> bd.Color:
    if alpha == 1.0:
        return bd.Color(text)
    r, g, b = (int(text[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return bd.Color(r, g, b, alpha)


def _polar(r: float, angle: float) -> tuple[float, float]:
    return r * math.cos(math.radians(angle)), r * math.sin(math.radians(angle))


def _hardware(hw: Hw) -> bd.Shape:
    x, y = _polar(hw.r, hw.angle)
    made, _ = HARDWARE[hw.kind]
    dx, dy, dz = hw.offset
    if hw.seat is not None:
        origin = bd.Vector(*hw.seat) + bd.Vector(*hw.offset)
        return bd.Location(bd.Plane(origin=origin, z_dir=bd.Vector(*hw.direction))) * made()
    if hw.radial:
        turn = bd.Rot(0, 0, hw.angle) * bd.Rot(0, -90, 0)
    else:
        turn = bd.Rot(180, 0, 0) if hw.down else bd.Rot(0, 0, 0)
    return bd.Pos(x + dx, y + dy, hw.z + dz) * turn * made()


def _guide(guide: Guide, dash: float = 3.5, gap: float = 2.5, radius: float = 0.28) -> list[bd.Shape]:
    if guide.p0 is not None:
        start = bd.Vector(*guide.p0)
        along = bd.Vector(*guide.p1) - start
        pieces, d = [], 0.0
        while d < along.length:
            plane = bd.Plane(origin=start + along.normalized() * d, z_dir=along.normalized())
            pieces.append(bd.Location(plane) * bd.Cylinder(radius, min(dash, along.length - d),
                                                           align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
            d += dash + gap
        return pieces
    x, y = _polar(guide.r, guide.angle)
    low, high = sorted((guide.z0, guide.z1))
    pieces, z = [], low
    while z < high:
        length = min(dash, high - z)
        pieces.append(bd.Pos(x, y, z) * bd.Cylinder(radius, length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
        z += dash + gap
    return pieces


# --- the scene ------------------------------------------------------------------------------


def compose(view: View, leaves: dict, colour_of, origin=(0.0, 0.0, 0.0)) -> tuple[bd.Compound, dict[str, bd.Shape]]:
    """The view's parts, in their colours and offsets. Also returns each by name, for callouts."""
    spin = bd.Rot(0, 0, view.turn)
    to_origin = bd.Pos(-origin[0], -origin[1], -origin[2])

    def placed(label: str) -> bd.Shape:
        shape = to_origin * leaves[label].shape()
        if label in view.turned:
            point, axis, degrees = view.turned[label]
            shape = shape.rotate(bd.Axis(point, axis), degrees)
        if label in view.trim_x:
            shape = shape & bd.Pos(view.trim_x[label] - 1000.0, 0, 0) * bd.Box(2000, 2000, 2000)
        return shape
    parts: list[bd.Shape] = []
    named: dict[str, bd.Shape] = {}

    def add(shape: bd.Shape, label: str, colour: bd.Color) -> None:
        shape = spin * shape
        shape.label = label
        shape.color = colour
        parts.append(shape)
        named[label] = shape

    for label in view.built:
        add(placed(label), label,
            _colour(colour_of(label), GHOST_ALPHA) if view.ghost else _colour(PALE))
    for label, offset in view.added.items():
        add(bd.Pos(*offset) * placed(label), label, _colour(colour_of(label)))
    for label, (x, y) in view.layout.items():
        shape = placed(label)
        box = shape.bounding_box()
        centre = box.center()
        add(bd.Pos(x - centre.X, y - centre.Y, -box.min.Z) * shape, label, _colour(colour_of(label)))
    for index, hw in enumerate(view.hardware):
        add(_hardware(hw), f"hw:{index}", _colour(PALE if hw.built else HARDWARE[hw.kind][1]))
    pieces = 0
    for guide in view.guides:
        for piece in _guide(guide):
            pieces += 1
            add(piece, f"guide:{pieces}", _colour(GUIDE_COLOR))
    return bd.Compound(children=parts, label=view.name), named


class Camera:
    """An exact orthographic camera; ``pixel`` projects a model point into the picture."""

    def __init__(self, shape: bd.Shape, view: View, margin_x: float, margin_y: float):
        az, el = math.radians(view.azimuth), math.radians(view.elevation)
        if view.clip_y is not None:   # square on to the cut
            az, el = math.radians(90.0), math.radians(view.elevation)
        self.size = view.size
        self.toward_eye = bd.Vector(math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))
        self.right = bd.Vector(0, 0, 1).cross(self.toward_eye).normalized()
        self.up = self.toward_eye.cross(self.right).normalized()
        if view.roll:
            cos, sin = math.cos(math.radians(view.roll)), math.sin(math.radians(view.roll))
            self.right, self.up = self.right * cos + self.up * sin, self.up * cos - self.right * sin
        points = [bd.Vector(*v) for child in shape.children for v in child.tessellate(0.5)[0]]
        xs = [p.dot(self.right) for p in points]
        ys = [p.dot(self.up) for p in points]
        depth = [p.dot(self.toward_eye) for p in points]
        self.target = (self.right * ((min(xs) + max(xs)) / 2) + self.up * ((min(ys) + max(ys)) / 2)
                       + self.toward_eye * ((min(depth) + max(depth)) / 2))
        width, height = view.size
        half_h = (max(ys) - min(ys)) / 2 / (1 - 2 * margin_y)
        half_w = (max(xs) - min(xs)) / 2 / (1 - 2 * margin_x)
        self.half_height = max(half_h, half_w * height / width) * view.frame
        self.position = self.target + self.toward_eye * ((max(depth) - min(depth)) * 3 + 100)
        # The model's left and right edges in the picture, for placing callouts near it.
        scale = height / (2 * self.half_height)
        self.left_px = width / 2 - (max(xs) - min(xs)) / 2 * scale
        self.right_px = width / 2 + (max(xs) - min(xs)) / 2 * scale

    def request(self) -> dict:
        def xyz(v: bd.Vector) -> list[float]:
            return [v.X, v.Y, v.Z]
        return {"position": xyz(self.position), "target": xyz(self.target), "up": xyz(self.up),
                "orthographicHalfHeight": self.half_height}

    def pixel(self, point: bd.Vector) -> tuple[float, float]:
        width, height = self.size
        scale = height / (2 * self.half_height)
        rel = point - self.target
        return width / 2 + rel.dot(self.right) * scale, height / 2 - rel.dot(self.up) * scale


# --- callouts -------------------------------------------------------------------------------


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype("arialbd.ttf", size)


def draw_labels(path: Path, view: View, camera: Camera, named: dict[str, bd.Shape]) -> None:
    if not view.labels:
        return
    image = Image.open(path).convert("RGBA")
    width, height = image.size
    k = SUPERSAMPLE
    overlay = Image.new("RGBA", (width * k, height * k), (0, 0, 0, 0))
    pen = ImageDraw.Draw(overlay)
    font = _font(24 * k)

    def anchor(label: Label) -> tuple[float, float]:
        point = (bd.Vector(*label.at) if label.at is not None
                 else named[label.part].bounding_box().center() + bd.Vector(*label.nudge))
        return camera.pixel(point)

    rows = [(label, *anchor(label)) for label in view.labels]
    columns: dict[str, list] = {"left": [], "right": []}
    for row in rows:
        side = row[0].side if row[0].side != "auto" else ("left" if row[1] < width / 2 else "right")
        columns[side].append(row)
    pad_x, pad_y, edge, gap = 14 * k, 8 * k, 24, 70
    tag_h = font.size + 2 * pad_y
    spacing = tag_h / k + 18
    for side, column in columns.items():
        column.sort(key=lambda row: row[2])
        ys = [row[2] for row in column]
        for _ in range(50):      # push overlapping tags apart, keeping them near their anchors
            moved = False
            for a in range(len(ys) - 1):
                overlap = spacing - (ys[a + 1] - ys[a])
                if overlap > 0.5:
                    ys[a] -= overlap / 2
                    ys[a + 1] += overlap / 2
                    moved = True
            if not moved:
                break
        shift = max(0.0, spacing / 2 + 10 - min(ys, default=0)) - max(0.0, max(ys, default=0) - height + spacing / 2 + 10)
        for (label, ax, ay), y in zip(column, (y + shift for y in ys)):
            box_w = pen.textlength(label.text, font=font) + 2 * pad_x
            if side == "left":
                x0 = max(edge * k, (camera.left_px - gap) * k - box_w)
            else:
                x0 = min(width * k - edge * k - box_w, (camera.right_px + gap) * k)
            top = y * k - tag_h / 2
            near = x0 + box_w if side == "left" else x0
            pen.line([(near, y * k), (ax * k, ay * k)], fill=TAG_INK, width=2 * k)
            dot = 5 * k
            pen.ellipse([ax * k - dot, ay * k - dot, ax * k + dot, ay * k + dot], fill=TAG_INK)
            pen.rounded_rectangle([x0, top, x0 + box_w, top + tag_h], radius=8 * k,
                                  fill=(255, 255, 255, 255), outline=TAG_INK, width=2 * k)
            pen.text((x0 + pad_x, top + pad_y - 2 * k), label.text, font=font, fill=TAG_INK)
    overlay = overlay.resize((width, height), Image.LANCZOS)
    Image.alpha_composite(image, overlay).convert("RGB").save(path, optimize=True)


# --- drawing --------------------------------------------------------------------------------


def render(view: View, chapter, leaves: dict, out_dir: Path) -> Path:
    shape, named = compose(view, leaves, chapter.colour_of, getattr(chapter, "ORIGIN", (0.0, 0.0, 0.0)))
    scene_file = TMP / chapter.NAME / f"{view.name}.step"
    scene_file.parent.mkdir(parents=True, exist_ok=True)
    bd.export_step(shape, str(scene_file))

    margin_x = 0.27 if view.labels else 0.05
    camera = Camera(shape, view, margin_x, 0.05)
    display: dict = {"mode": "solid"}
    if view.clip_y is not None:
        display["clip"] = {"enabled": True, "axis": "y", "at": view.clip_y}
    out = ROOT / "docs" / "img" / view.path if view.path else out_dir / f"{view.name}.png"
    width, height = view.size
    cadgen.snapshot(str(scene_file), job={
        "camera": camera.request(),
        "display": display,
        "output": {"tightFrame": False, "renderScale": 2},
        "outputs": [{"path": str(out), "width": width, "height": height}],
    }, progress=False, daemon=False)   # the daemon can keep a rewritten scene's old geometry
    draw_labels(out, view, camera, named)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapter", help="a module in tools/assembly_steps")
    parser.add_argument("--only", help="draw only views whose name contains this")
    args = parser.parse_args()

    chapter = importlib.import_module(f"assembly_steps.{args.chapter}")
    leaves = {leaf.label: leaf for leaf in read_scene(str(ROOT / chapter.ASSEMBLY)).leaves()}
    out_dir = ROOT / "docs" / "img" / "assembly" / chapter.NAME
    out_dir.mkdir(parents=True, exist_ok=True)
    drawn = 0
    for step in chapter.STEPS:
        for view in step.views:
            if args.only and args.only not in view.name:
                continue
            print(f"{view.name}: {render(view, chapter, leaves, out_dir).relative_to(ROOT)}", flush=True)
            drawn += 1
    print(json.dumps({"drawn": drawn}))


if __name__ == "__main__":
    main()
