"""Compare a recreated part with its Fusion original ("replica done" gate).

Single comparison (from CAD/):
    python checks/compare_to_fusion.py STEP/gearbox/ring_gear.step \
        "STEP/imported/fusion/Joint 1 and 2.step" "#o1.12.9" [--align center]

All mapped parts:
    python checks/compare_to_fusion.py --map checks/fusion_map.json

The Fusion part is taken in its own local frame (its assembly placement is
undone), which is the frame the recreation models in. ``--transform
x,y,z,rx,ry,rz`` (degrees, applied rotate-then-translate) moves the
generated part into that frame; ``--align center`` instead translates it so
the bounding-box centres coincide.

Pass criteria (defaults): bounding box within 0.1 mm per side, volume within
0.5 %, symmetric-difference volume within 0.5 % of the Fusion volume.
Exit status is 1 if any comparison fails.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cadgen import build123d as bd
from cadgen import read_scene, read_step


def _fusion_part(path: str, ref: str) -> bd.Shape:
    (sel,) = read_scene(path).resolve(ref)
    shape = sel.shape()
    return shape.moved(shape.location.inverse())


# OCCT's boolean returns an empty result for some exactly coincident faces
# (e.g. a recreated pin against the Fusion pin). A failed common only ever
# under-reports, so also evaluate it with the generated part nudged by
# NUDGE mm and keep the larger volume; the nudge adds at most about
# surface_area * NUDGE of apparent difference.
NUDGE = 1e-4


def _common_volume(a: bd.Shape, b: bd.Shape) -> float:
    best = 0.0
    for shift in ((0.0, 0.0, 0.0), (NUDGE, 0.7 * NUDGE, 0.3 * NUDGE)):
        common = (bd.Pos(*shift) * a) & b
        if common:
            best = max(best, common.volume)
    return best


def _solid(shape: bd.Shape) -> bd.Shape:
    solids = shape.solids()
    if len(solids) == 1:
        return solids[0]
    return bd.Compound(solids)


def compare(generated: str, fusion: str, ref: str, transform=None, align=None,
            bbox_tol=0.1, vol_tol=0.5, symdiff_tol=0.5) -> dict:
    ref_part = _solid(_fusion_part(fusion, ref))
    gen = _solid(read_step(generated))
    if transform:
        x, y, z, rx, ry, rz = transform
        gen = bd.Pos(x, y, z) * bd.Rot(rx, ry, rz) * gen
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
    symdiff = max(0.0, vol_r + vol_g - 2.0 * _common_volume(gen, ref_part))
    symdiff_pct = 100.0 * symdiff / vol_r

    return {
        "generated": generated,
        "ref": f"{Path(fusion).name}{ref}",
        "bbox_err": bbox_err,
        "vol_fusion": vol_r,
        "vol_generated": vol_g,
        "vol_err_pct": vol_err,
        "symdiff": symdiff,
        "symdiff_pct": symdiff_pct,
        "pass": bbox_err <= bbox_tol and vol_err <= vol_tol and symdiff_pct <= symdiff_tol,
    }


def _report(rows):
    print(f"{'result':6s} {'bbox mm':>8s} {'vol %':>7s} {'symdiff %':>9s}  generated  <-  fusion ref")
    for r in rows:
        print(
            f"{'PASS' if r['pass'] else 'FAIL':6s} {r['bbox_err']:8.3f} {r['vol_err_pct']:7.3f} "
            f"{r['symdiff_pct']:9.3f}  {r['generated']}  <-  {r['ref']}"
        )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("generated", nargs="?")
    ap.add_argument("fusion", nargs="?")
    ap.add_argument("ref", nargs="?")
    ap.add_argument("--map", help="JSON list of {generated, fusion, ref, transform?, align?, tolerances?}")
    ap.add_argument("--transform", help="x,y,z,rx,ry,rz")
    ap.add_argument("--align", choices=["center"])
    ap.add_argument("--bbox-tol", type=float, default=0.1)
    ap.add_argument("--vol-tol", type=float, default=0.5)
    ap.add_argument("--symdiff-tol", type=float, default=0.5)
    args = ap.parse_args(argv)

    if args.map:
        jobs = json.loads(Path(args.map).read_text())
    elif args.generated and args.fusion and args.ref:
        jobs = [{
            "generated": args.generated, "fusion": args.fusion, "ref": args.ref,
            "transform": [float(v) for v in args.transform.split(",")] if args.transform else None,
            "align": args.align,
        }]
    else:
        ap.error("give GENERATED FUSION REF, or --map")

    rows = []
    for job in jobs:
        tol = job.get("tolerances", {})
        rows.append(compare(
            job["generated"], job["fusion"], job["ref"],
            transform=job.get("transform"), align=job.get("align"),
            bbox_tol=tol.get("bbox", args.bbox_tol),
            vol_tol=tol.get("vol_pct", args.vol_tol),
            symdiff_tol=tol.get("symdiff_pct", args.symdiff_tol),
        ))
    _report(rows)
    return 0 if all(r["pass"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
