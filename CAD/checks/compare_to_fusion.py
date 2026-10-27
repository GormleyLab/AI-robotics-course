"""Compare a recreated part with its Fusion original ("replica done" gate).

Single comparison (from CAD/):
    python checks/compare_to_fusion.py STEP/gearbox/ring_gear.step \
        "STEP/imported/fusion/Joint 1 and 2.step" "#o1.12.9" [--align center]

All mapped parts:
    python checks/compare_to_fusion.py --map checks/fusion_map.json

The Fusion part is taken in its own local frame (its assembly placement is
undone), which is the frame the recreation models in. ``--transform
x,y,z,rx,ry,rz`` (degrees, applied rotate-then-translate; map entries may
instead give a list of ``["rot", rx, ry, rz]`` / ``["pos", x, y, z]`` steps
applied in order) moves the generated part into that frame; ``--align center`` instead translates it so
the bounding-box centres coincide. ``--frame world`` (map key ``frame``)
compares against the part as placed in the Fusion assembly instead; the
gearbox parts use it with transform 0,0,0,-90,0,0 (part +Z = gearbox +Y).
``--explain`` lists the largest extra and missing regions. If the 3D
boolean fails (as it does for helical gears), the symmetric difference is
integrated from thin sections along the map entry's ``slice_axis``. Map
entries for helical gears set ``"method": "sliced"`` to skip the 3D boolean
(and its nudged retries) entirely; ``slices`` (default 20) sets the count.

Pass criteria (defaults): bounding box within 0.1 mm per side, volume within
0.5 %, symmetric-difference volume within 0.5 % of the Fusion volume.
Exit status is 1 if any comparison fails.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from cadgen import build123d as bd
from cadgen import read_scene, read_step


def _fusion_part(path: str, ref: str, frame: str = "local") -> bd.Shape:
    (sel,) = read_scene(path).resolve(ref)
    shape = sel.shape()
    if frame == "world":
        return shape
    return shape.moved(shape.location.inverse())


# OCCT's boolean returns an empty or partial result for some exactly or
# nearly coincident faces (a recreated pin against the Fusion pin; twisted
# helical flanks against Fusion's B-spline flanks). A failed common only
# ever under-reports, so it is also evaluated with the generated part nudged
# and the largest volume is kept. A nudge of d mm adds at most about
# surface_area * d of apparent difference (< 0.05 % for these parts).
NUDGES = (
    bd.Location(),
    bd.Pos(1e-4, 0.7e-4, 0.3e-4),
    bd.Pos(1e-3, 0.7e-3, 0.3e-3),
    bd.Rot(0, 0, 1e-3),
)


def _common_volume(a: bd.Shape, b: bd.Shape, target: float | None = None) -> float:
    best = 0.0
    for nudge in NUDGES:
        try:
            common = (nudge * a) & b
        except Exception:
            continue
        if common:
            best = max(best, common.volume)
        if target and best >= 0.995 * target:
            break  # good enough; skip the remaining nudges
    return best


SLICES = 20  # default; uniform helices make the section difference nearly constant along the axis


def _in_plane_nudges(axis: int) -> list[bd.Location]:
    """Small translations/rotation that keep a section in its own plane."""
    out = [bd.Location()]
    for d in (1e-4, 1e-3):
        v = [d, 0.7 * d, 0.3 * d]
        v[axis] = 0.0
        out.append(bd.Pos(*v))
    rot = [0.0, 0.0, 0.0]
    rot[axis] = 1e-3
    out.append(bd.Rot(*rot))
    return out


POLY_STEP = 0.2  # mm between points when polygonising section wires (chord error ~0.01 mm on R0.5 arcs)


def _polygonise(shape) -> list[bd.Face]:
    """Section faces rebuilt from evenly spaced points on their wires.

    Exact section edges through B-spline flanks defeat OCCT's 2D booleans
    (the common comes back empty), while polygon faces work; both sides are
    polygonised the same way, so the chord error largely cancels.
    """
    def poly(w):
        n = max(8, int(w.length / POLY_STEP))
        return bd.Wire.make_polygon([w.position_at(k / n) for k in range(n)], close=True)

    return [bd.Face(poly(f.outer_wire()), [poly(w) for w in f.inner_wires()])
            for f in (shape.faces() if shape else [])]


def _area(shape) -> float:
    return sum(f.area for f in shape.faces()) if shape else 0.0


def _common_area(fa, fb, aa: float, ab: float, nudges) -> float:
    common = 0.0
    if aa <= 0 or ab <= 0:
        return common
    for nudge in nudges:
        try:
            common = max(common, _area((nudge * fa) & fb))
        except Exception:
            continue
        if common >= 0.995 * min(aa, ab):
            break
    return common


def _sliced_symdiff(a: bd.Shape, b: bd.Shape, axis: str, slices: int = SLICES) -> float:
    """Symmetric-difference volume integrated from planar sections.

    Each section is cut with a plane normal to ``axis`` (fast even through
    B-spline helical flanks); the section difference is
    area(A) + area(B) - 2 area(A & B), with the 2D common retried under
    in-plane nudges and, if it still fails, on polygonised sections. A failed common only under-reports, so errors lean to FAIL.
    """
    i = "xyz".index(axis)
    normal = [0.0, 0.0, 0.0]
    normal[i] = 1.0
    nudges = _in_plane_nudges(i)
    bb = a.bounding_box().add(b.bounding_box())
    lo, hi = bb.min.to_tuple()[i], bb.max.to_tuple()[i]
    extent = 4 * max(bb.size.X, bb.size.Y, bb.size.Z)
    step = (hi - lo) / slices
    total = 0.0
    for k in range(slices):
        origin = list(bb.center().to_tuple())
        origin[i] = lo + (k + 0.5) * step
        sheet = bd.Plane(origin=origin, z_dir=normal) * bd.Rectangle(extent, extent)
        sa, sb = a & sheet, b & sheet
        aa, ab = _area(sa), _area(sb)
        common = _common_area(sa, sb, aa, ab, nudges)
        if aa > 0 and ab > 0 and common < 0.5 * min(aa, ab):
            # exact 2D boolean failed on B-spline section edges: compare polygons
            pa, pb = bd.Compound(_polygonise(sa)), bd.Compound(_polygonise(sb))
            aa, ab = _area(pa), _area(pb)
            common = _common_area(pa, pb, aa, ab, nudges)
        total += max(0.0, aa + ab - 2.0 * common) * step
    return total


def _transform(spec) -> bd.Location:
    """[x,y,z,rx,ry,rz] (rotate, then translate), or a list of steps
    [["rot", rx, ry, rz] | ["pos", x, y, z], ...] applied in order."""
    if not isinstance(spec[0], (list, tuple)):
        x, y, z, rx, ry, rz = spec
        return bd.Pos(x, y, z) * bd.Rot(rx, ry, rz)
    loc = bd.Location()
    for kind, *v in spec:
        loc = (bd.Rot(*v) if kind == "rot" else bd.Pos(*v)) * loc
    return loc


def _solid(shape: bd.Shape) -> bd.Shape:
    solids = shape.solids()
    if len(solids) == 1:
        return solids[0]
    return bd.Compound(solids)


def _explain(gen: bd.Shape, ref_part: bd.Shape, top: int = 6) -> None:
    """Print the largest extra / missing regions (generated minus Fusion and vice versa)."""
    for name, (x, y) in (("extra (generated only)", (gen, ref_part)), ("missing (Fusion only)", (ref_part, gen))):
        try:
            diff = x - y
        except Exception as e:  # OCCT can fail on near-coincident faces
            print(f"    {name}: boolean failed ({e})")
            continue
        pieces = sorted(diff.solids() if diff else [], key=lambda p: -p.volume)
        print(f"    {name}: {len(pieces)} regions, {sum(p.volume for p in pieces):.2f} mm^3")
        for p in pieces[:top]:
            b = p.bounding_box()
            print(f"      {p.volume:9.2f} mm^3  min=({b.min.X:.2f},{b.min.Y:.2f},{b.min.Z:.2f}) max=({b.max.X:.2f},{b.max.Y:.2f},{b.max.Z:.2f})")


def compare(generated: str, fusion: str, ref: str, transform=None, align=None,
            bbox_tol=0.1, vol_tol=0.5, symdiff_tol=0.5, frame="local", explain=False,
            slice_axis="z", method="auto", slices=SLICES) -> dict:
    """method: "auto" (3D boolean, sliced fallback if it fails) or "sliced"
    (skip the 3D boolean; use for helical gears, where it always fails)."""
    t0 = time.monotonic()
    ref_part = _solid(_fusion_part(fusion, ref, frame))
    gen = _solid(read_step(generated))
    if transform:
        gen = _transform(transform) * gen
    if align == "center":
        gen = bd.Pos(ref_part.bounding_box().center() - gen.bounding_box().center()) * gen

    bb_r, bb_g = ref_part.bounding_box(), gen.bounding_box()
    bbox_err = max(
        abs(a - b)
        for va, vb in ((bb_r.min, bb_g.min), (bb_r.max, bb_g.max))
        for a, b in zip(va, vb)
    )
    vol_r, vol_g = ref_part.volume, gen.volume
    vol_err = 100.0 * abs(vol_g - vol_r) / vol_r
    if method == "sliced":
        symdiff = _sliced_symdiff(gen, ref_part, slice_axis, slices)
        method = f"sliced-{slice_axis}x{slices}"
    else:
        symdiff = max(0.0, vol_r + vol_g - 2.0 * _common_volume(gen, ref_part, min(vol_r, vol_g)))
        method = "boolean"
        if symdiff > 0.5 * vol_r:  # the 3D boolean clearly failed; fall back to sections
            symdiff = _sliced_symdiff(gen, ref_part, slice_axis, slices)
            method = f"sliced-{slice_axis}x{slices} (fallback)"
    symdiff_pct = 100.0 * symdiff / vol_r
    if explain:
        print(f"  {generated}:")
        _explain(gen, ref_part)

    return {
        "generated": generated,
        "ref": f"{Path(fusion).name}{ref}",
        "bbox_err": bbox_err,
        "vol_fusion": vol_r,
        "vol_generated": vol_g,
        "vol_err_pct": vol_err,
        "symdiff": symdiff,
        "symdiff_pct": symdiff_pct,
        "method": method,
        "seconds": time.monotonic() - t0,
        "pass": bbox_err <= bbox_tol and vol_err <= vol_tol and symdiff_pct <= symdiff_tol,
    }


def _report(rows):
    print(f"{'result':6s} {'bbox mm':>8s} {'vol %':>7s} {'symdiff %':>9s}  generated  <-  fusion ref")
    for r in rows:
        print(
            f"{'PASS' if r['pass'] else 'FAIL':6s} {r['bbox_err']:8.3f} {r['vol_err_pct']:7.3f} "
            f"{r['symdiff_pct']:9.3f}  {r['generated']}  <-  {r['ref']}"
            + ("" if r["method"] == "boolean" else f"  ({r['method']})")
            + f"  [{r['seconds']:.0f}s]"
        )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("generated", nargs="?")
    ap.add_argument("fusion", nargs="?")
    ap.add_argument("ref", nargs="?")
    ap.add_argument("--map", help="JSON list of {generated, fusion, ref, transform?, align?, tolerances?}")
    ap.add_argument("--transform", help="x,y,z,rx,ry,rz")
    ap.add_argument("--align", choices=["center"])
    ap.add_argument("--frame", choices=["local", "world"], default="local",
                    help="compare against the Fusion part's local frame (default) or its assembly placement")
    ap.add_argument("--only", help="with --map: only entries whose generated path contains this text")
    ap.add_argument("--explain", action="store_true", help="list the largest extra/missing regions")
    ap.add_argument("--bbox-tol", type=float, default=0.1)
    ap.add_argument("--vol-tol", type=float, default=0.5)
    ap.add_argument("--symdiff-tol", type=float, default=0.5)
    args = ap.parse_args(argv)

    if args.map:
        jobs = json.loads(Path(args.map).read_text())
        if args.only:
            jobs = [j for j in jobs if args.only in j["generated"]]
    elif args.generated and args.fusion and args.ref:
        jobs = [{
            "generated": args.generated, "fusion": args.fusion, "ref": args.ref,
            "transform": [float(v) for v in args.transform.split(",")] if args.transform else None,
            "align": args.align, "frame": args.frame,
        }]
    else:
        ap.error("give GENERATED FUSION REF, or --map")

    rows = []
    for job in jobs:
        tol = job.get("tolerances", {})
        rows.append(compare(
            job["generated"], job["fusion"], job["ref"],
            transform=job.get("transform"), align=job.get("align"),
            frame=job.get("frame", "local"), explain=args.explain,
            slice_axis=job.get("slice_axis", "z"),
            method=job.get("method", "auto"), slices=job.get("slices", SLICES),
            bbox_tol=tol.get("bbox", args.bbox_tol),
            vol_tol=tol.get("vol_pct", args.vol_tol),
            symdiff_tol=tol.get("symdiff_pct", args.symdiff_tol),
        ))
    _report(rows)
    return 0 if all(r["pass"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
