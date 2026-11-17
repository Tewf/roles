#!/usr/bin/env python3
"""The reference pipeline of the cadquery-part role: one parametric plate, built, exported to STEP and STL.

    ~/.venvs/cad/bin/python reference_part.py OUTDIR [--hole 8]

Writes OUTDIR/params.json, part.step and part.stl. The numbers are the program's; the judge recomputes the volume from them.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cadquery as cq

PARAMS = {"length_mm": 40.0, "width_mm": 30.0, "thickness_mm": 6.0, "hole_diameter_mm": 8.0}


def build(params: dict) -> cq.Workplane:
    plate = cq.Workplane("XY").box(params["length_mm"], params["width_mm"], params["thickness_mm"])
    return plate.faces(">Z").workplane().hole(params["hole_diameter_mm"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out", type=Path)
    parser.add_argument("--hole", type=float, default=PARAMS["hole_diameter_mm"])
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    params = dict(PARAMS, hole_diameter_mm=args.hole)
    part = build(params)
    (args.out / "params.json").write_text(json.dumps(params, indent=2) + "\n", encoding="utf-8")
    cq.exporters.export(part, str(args.out / "part.step"))
    cq.exporters.export(part, str(args.out / "part.stl"), tolerance=0.01, angularTolerance=0.05)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
