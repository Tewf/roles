#!/usr/bin/env python3
"""The judge of the cadquery-part role: a program decides whether an exported part passes.

    ~/.venvs/cad/bin/python judge.py OUTDIR

OUTDIR holds params.json, part.step and part.stl. It passes when all four hold:
  1. part.step re-imports as exactly one valid solid (the file is read back, never trusted from the script that wrote it);
  2. that solid's volume equals the closed-form volume of the parameters, within 0.1%, and its bounding box matches them;
  3. part.stl is a closed mesh: every edge is shared by exactly two triangles;
  4. the mesh's volume is within 1% of the solid's (the tessellation of a round hole is a little smaller).
Exit 0 on pass, 1 on fail; the last line is `pass` or `fail: <reason>`.
What it does not decide: that the part is the right design, or that it can be made with a given process.
"""
from __future__ import annotations

import json
import math
import struct
import sys
from pathlib import Path


def closed_form_volume(p: dict) -> float:
    return p["length_mm"] * p["width_mm"] * p["thickness_mm"] - math.pi * (p["hole_diameter_mm"] / 2) ** 2 * p["thickness_mm"]


def stl_triangles(path: Path) -> list[tuple]:
    data = path.read_bytes()
    if data[:5].lower() == b"solid" and b"facet" in data[:400]:
        numbers = [float(t) for line in data.decode("ascii", "replace").splitlines()
                   if line.strip().startswith("vertex") for t in line.split()[1:4]]
        return [tuple(tuple(numbers[i + 3 * k: i + 3 * k + 3]) for k in range(3)) for i in range(0, len(numbers), 9)]
    count = struct.unpack("<I", data[80:84])[0]
    triangles = []
    for k in range(count):
        v = struct.unpack("<12fH", data[84 + 50 * k: 84 + 50 * (k + 1)])
        triangles.append(((v[3], v[4], v[5]), (v[6], v[7], v[8]), (v[9], v[10], v[11])))
    return triangles


def mesh_problem(triangles: list[tuple]) -> tuple[str | None, float]:
    """(problem or None, signed volume). Vertices are matched after rounding to 1e-4 mm."""
    if not triangles:
        return "part.stl holds no triangle", 0.0
    edges: dict[tuple, int] = {}
    volume = 0.0
    for a, b, c in triangles:
        keys = [tuple(round(x, 4) for x in v) for v in (a, b, c)]
        for u, v in ((0, 1), (1, 2), (2, 0)):
            edge = tuple(sorted((keys[u], keys[v])))
            edges[edge] = edges.get(edge, 0) + 1
        volume += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
    open_edges = sum(1 for n in edges.values() if n != 2)
    return (f"part.stl is not closed: {open_edges} edges are not shared by exactly two triangles" if open_edges else None), abs(volume)


def judge(out: Path) -> str:
    import cadquery as cq
    for name in ("params.json", "part.step", "part.stl"):
        if not (out / name).is_file() or (out / name).stat().st_size == 0:
            return f"fail: {name} is missing or empty"
    params = json.loads((out / "params.json").read_text(encoding="utf-8"))
    try:
        shape = cq.importers.importStep(str(out / "part.step"))
    except Exception as error:  # noqa: BLE001 - any read failure is a verdict
        return f"fail: part.step does not re-import ({type(error).__name__})"
    solids = shape.solids().vals()
    if len(solids) != 1 or not solids[0].isValid():
        return f"fail: part.step holds {len(solids)} solid(s), valid={all(s.isValid() for s in solids)}: one valid solid is required"
    expected, got = closed_form_volume(params), solids[0].Volume()
    if abs(got - expected) > 0.001 * expected:
        return f"fail: the solid's volume is {got:.1f} mm3, the parameters give {expected:.1f} mm3"
    box = solids[0].BoundingBox()
    for have, want in ((box.xlen, params["length_mm"]), (box.ylen, params["width_mm"]), (box.zlen, params["thickness_mm"])):
        if abs(have - want) > 0.01:
            return f"fail: the bounding box is {have:.3f} mm where the parameters say {want} mm"
    problem, mesh_volume = mesh_problem(stl_triangles(out / "part.stl"))
    if problem:
        return f"fail: {problem}"
    if abs(mesh_volume - got) > 0.01 * got:
        return f"fail: the mesh volume {mesh_volume:.1f} mm3 differs from the solid's {got:.1f} mm3 by more than 1%"
    return "pass"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: judge.py OUTDIR")
        return 2
    verdict = judge(Path(sys.argv[1]))
    print(verdict)
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
