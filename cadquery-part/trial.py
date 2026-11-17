#!/usr/bin/env python3
"""The trial of the cadquery-part role: the reference plate built twice from an empty folder, then five faults the judge must refuse.

    ~/.venvs/cad/bin/python trial.py [--runs 2] [--out trial-1]

Writes OUT/scores.json. A run counts as passed only when judge.py prints `pass`; a control counts as caught only when
judge.py fails it. This measures the pipeline and the judge, not a model that follows the procedure.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def wilson(passed: int, n: int, z: float = 1.96) -> tuple[float, float]:
    p = passed / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(centre - half, 2), round(centre + half, 2)


def judge(folder: Path) -> str:
    out = subprocess.run([sys.executable, str(HERE / "judge.py"), str(folder)], capture_output=True, text=True)
    return out.stdout.strip().splitlines()[-1] if out.stdout.strip() else "no verdict"


def pipeline(folder: Path, *extra: str) -> None:
    subprocess.run([sys.executable, str(HERE / "reference_part.py"), str(folder), *extra], capture_output=True, text=True, timeout=300)


def controls(good: Path, scratch: Path) -> list[dict]:
    rows = []

    def record(name: str, folder: Path) -> None:
        verdict = judge(folder)
        rows.append({"control": name, "verdict": verdict, "caught": verdict.startswith("fail")})

    def copy(name: str) -> Path:
        case = scratch / name
        shutil.copytree(good, case)
        return case

    case = copy("no-step"); (case / "part.step").unlink(); record("no-step", case)
    case = copy("empty-stl"); (case / "part.stl").write_bytes(b""); record("empty-stl", case)
    case = copy("wrong-hole")  # a 10 mm hole exported under parameters that say 8 mm: the volume is off
    wide = scratch / "wide"; pipeline(wide, "--hole", "10"); shutil.copy(wide / "part.step", case / "part.step"); record("wrong-hole", case)
    case = copy("two-solids")
    import cadquery as cq
    two = cq.Workplane("XY").box(40, 30, 6).union(cq.Workplane("XY").workplane(offset=20).box(5, 5, 5))
    cq.exporters.export(two, str(case / "part.step")); record("two-solids", case)
    case = copy("open-mesh")  # the last triangle of the binary STL removed
    data = (case / "part.stl").read_bytes(); count = struct.unpack("<I", data[80:84])[0]
    (case / "part.stl").write_bytes(data[:80] + struct.pack("<I", count - 1) + data[84:84 + 50 * (count - 1)]); record("open-mesh", case)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--out", type=Path, default=HERE / "trial-1")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    runs, last = [], None
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(1, args.runs + 1):
            folder = Path(tmp) / f"run{i}"
            pipeline(folder)
            verdict = judge(folder)
            runs.append({"run": i, "verdict": verdict, "passed": verdict == "pass"})
            last = folder
        scratch = Path(tmp) / "controls"; scratch.mkdir()
        caught = controls(last, scratch) if last else []
    passed = sum(r["passed"] for r in runs)
    scores = {"role": "cadquery-part", "runs": runs, "passed": passed, "n": args.runs, "wilson95": wilson(passed, args.runs),
              "controls": caught, "controls_caught": sum(c["caught"] for c in caught), "controls_n": len(caught)}
    (args.out / "scores.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: scores[k] for k in ("passed", "n", "wilson95", "controls_caught", "controls_n")}))
    return 0 if passed == args.runs and scores["controls_caught"] == scores["controls_n"] else 1


if __name__ == "__main__":
    sys.exit(main())
