"""Dump the assembly tree and per-part features of a Fusion STEP export.

Usage (from CAD/):
    python checks/inspect/dump_features.py "Belt Drive Arm.step" [more.step ...]

Writes tmp/inspect/<stem>.txt. Features are reported in each part's local
frame (the world placement is undone), which is the frame the Python
recreation should model in.
"""
from __future__ import annotations

import collections
import math
import sys
from pathlib import Path

from cadgen import read_scene

OUT_DIR = Path("tmp/inspect")


def fmt(v, nd=2):
    return "(" + ", ".join(f"{c:.{nd}f}" for c in (v.X, v.Y, v.Z)) + ")"


def axis_key(d):
    d = d.normalized()
    # Fold opposite directions together.
    if d.X < -1e-6 or (abs(d.X) < 1e-6 and (d.Y < -1e-6 or (abs(d.Y) < 1e-6 and d.Z < 0))):
        d = -d
    return (round(d.X, 3) + 0.0, round(d.Y, 3) + 0.0, round(d.Z, 3) + 0.0)


def describe_part(shape, lines):
    bb = shape.bounding_box()
    lines.append(f"    local bbox min={fmt(bb.min)} max={fmt(bb.max)} size={fmt(bb.size)}")
    lines.append(f"    volume={shape.volume:.1f} mm^3  faces={len(shape.faces())}  solids={len(shape.solids())}")

    types = collections.Counter(f.geom_type.name for f in shape.faces())
    lines.append("    face types: " + ", ".join(f"{k}={v}" for k, v in sorted(types.items())))

    # Cylindrical faces grouped by radius + axis; each group lists distinct axis lines.
    cyl = collections.defaultdict(list)
    for f in shape.faces():
        if f.geom_type.name != "CYLINDER":
            continue
        try:
            ax = f.axis_of_rotation
            r = f.radius
        except Exception:
            continue
        k = (round(2 * r, 2), axis_key(ax.direction))
        fb = f.bounding_box()
        cyl[k].append((ax.position, fb, f.area))
    if cyl:
        lines.append("    cylinders (diameter, axis dir): axis points / z-span along axis")
        for (dia, dkey), items in sorted(cyl.items(), key=lambda kv: -kv[0][0]):
            d = (dkey[0], dkey[1], dkey[2])
            seen = []
            for pos, fb, _ in items:
                # project position onto plane normal to axis to dedupe split faces
                p = (pos.X, pos.Y, pos.Z)
                dot = sum(a * b for a, b in zip(p, d))
                q = tuple(round(a - dot * b, 1) + 0.0 for a, b in zip(p, d))
                lo = min(sum(a * b for a, b in zip(c, d)) for c in ((fb.min.X, fb.min.Y, fb.min.Z), (fb.max.X, fb.max.Y, fb.max.Z)))
                hi = max(sum(a * b for a, b in zip(c, d)) for c in ((fb.min.X, fb.min.Y, fb.min.Z), (fb.max.X, fb.max.Y, fb.max.Z)))
                entry = (q, round(lo, 1), round(hi, 1))
                if not any(s[0] == q for s in seen):
                    seen.append(entry)
            pts = "; ".join(f"{s[0]} span[{s[1]},{s[2]}]" for s in seen[:12])
            more = f" (+{len(seen) - 12} more)" if len(seen) > 12 else ""
            lines.append(f"      Ø{dia:g} dir={d} n_axes={len(seen)} n_faces={len(items)}: {pts}{more}")

    # Planar faces: distinct offsets along each normal (gives plate thicknesses / steps).
    planes = collections.defaultdict(set)
    for f in shape.faces():
        if f.geom_type.name != "PLANE":
            continue
        n = f.normal_at()
        k = axis_key(n)
        c = f.center()
        off = c.X * k[0] + c.Y * k[1] + c.Z * k[2]
        planes[k].add(round(off, 2))
    if planes:
        lines.append("    planar levels by normal:")
        for k, offs in sorted(planes.items(), key=lambda kv: -len(kv[1])):
            offs = sorted(offs)
            s = ", ".join(f"{o:g}" for o in offs[:20]) + (" ..." if len(offs) > 20 else "")
            lines.append(f"      n={k}: {s}")

    # Gear heuristic: count non-planar non-cylindrical faces that are repeated.
    other = [f for f in shape.faces() if f.geom_type.name not in ("PLANE", "CYLINDER", "CONE", "TORUS", "SPHERE")]
    if len(other) >= 20:
        areas = collections.Counter(round(f.area, 2) for f in other)
        common = areas.most_common(3)
        lines.append(f"    freeform faces={len(other)}; most common areas (area: count) {common}  -> tooth flank candidates")


def main(paths):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in paths:
        scene = read_scene(p)
        lines = [f"# {p}", ""]

        def walk(node, depth):
            lines.append("  " * depth + f"{node.ref} {node.label} [{node.kind}]" + (f" proto={node.prototype_id}" if node.kind != "group" else ""))
            for c in node.children:
                walk(c, depth + 1)

        lines.append("## Tree")
        for r in scene.roots:
            walk(r, 0)

        lines.append("")
        lines.append("## Occurrence placements (world)")
        protos = {}
        for leaf in scene.leaves():
            sh = leaf.shape()
            loc = sh.location
            bb = sh.bounding_box()
            lines.append(f"  {leaf.ref:10s} {leaf.label:55s} pos={fmt(loc.position)} rot={fmt(loc.orientation, 1)} wbbox_min={fmt(bb.min, 1)} wbbox_max={fmt(bb.max, 1)}")
            protos.setdefault(leaf.prototype_id, (leaf, sh))

        lines.append("")
        lines.append("## Unique parts (local frame)")
        for pid, (leaf, sh) in protos.items():
            count = sum(1 for l in scene.leaves() if l.prototype_id == pid)
            lines.append(f"\n### {leaf.label}  ({pid}, x{count})")
            local = sh.moved(sh.location.inverse())
            try:
                describe_part(local, lines)
            except Exception as e:  # keep going; report the failure
                lines.append(f"    FAILED: {e!r}")

        out = OUT_DIR / (Path(p).stem + ".txt")
        out.write_text("\n".join(lines) + "\n")
        print(f"wrote {out} ({len(protos)} unique parts)")


if __name__ == "__main__":
    main(sys.argv[1:])
