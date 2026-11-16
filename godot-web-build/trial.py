#!/usr/bin/env python3
"""The trial of the godot-web-build role: the starter project exported to the Web twice from a clean copy, then four faults the judge must refuse.

    python3 trial.py [--runs 2] [--starter DIR] [--out trial-1]

Writes OUT/scores.json. A run counts as passed only when judge.py prints `pass`. A control counts as caught only when
judge.py fails it. This trial measures the pipeline and the judge; it does not measure a model that follows the procedure.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STARTER = Path.home() / "Desktop/GameDev/projects/starter"


def wilson(passed: int, n: int, z: float = 1.96) -> tuple[float, float]:
    p = passed / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(centre - half, 2), round(centre + half, 2)


def judge(project: Path, *extra: str) -> str:
    out = subprocess.run([sys.executable, str(HERE / "judge.py"), str(project), *extra], capture_output=True, text=True)
    return out.stdout.strip().splitlines()[-1] if out.stdout.strip() else "no verdict"


def fresh_copy(starter: Path, dest: Path) -> Path:
    shutil.copytree(starter, dest, ignore=shutil.ignore_patterns("build", ".godot"))
    return dest


def export(project: Path) -> None:
    subprocess.run(["bash", "./export-builds.sh", "Web"], cwd=project, capture_output=True, text=True, timeout=600)


def controls(good: Path, scratch: Path) -> list[dict]:
    rows = []

    def record(name: str, verdict: str) -> None:
        rows.append({"control": name, "verdict": verdict, "caught": verdict.startswith("fail")})

    case = scratch / "csharp"; shutil.copytree(good, case); (case / "Player.cs").write_text("class Player {}\n"); record("csharp", judge(case))
    case = scratch / "no-build"; shutil.copytree(good, case); shutil.rmtree(case / "build"); record("no-build", judge(case))
    case = scratch / "empty-wasm"; shutil.copytree(good, case); (case / "build/web/index.wasm").write_bytes(b""); record("empty-wasm", judge(case))
    link = scratch / "godot-symlink"; link.symlink_to(shutil.which("godot") or "/bin/true"); record("symlink-launcher", judge(good, "--godot", str(link)))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--starter", type=Path, default=STARTER)
    parser.add_argument("--out", type=Path, default=HERE / "trial-1")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    runs, last = [], None
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(1, args.runs + 1):
            project = fresh_copy(args.starter, Path(tmp) / f"run{i}")
            export(project)
            verdict = judge(project)
            runs.append({"run": i, "verdict": verdict, "passed": verdict == "pass"})
            last = project
        scratch = Path(tmp) / "controls"; scratch.mkdir()
        caught = controls(last, scratch) if last else []
    passed = sum(r["passed"] for r in runs)
    scores = {"role": "godot-web-build", "runs": runs, "passed": passed, "n": args.runs,
              "wilson95": wilson(passed, args.runs), "controls": caught,
              "controls_caught": sum(c["caught"] for c in caught), "controls_n": len(caught)}
    (args.out / "scores.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: scores[k] for k in ("passed", "n", "wilson95", "controls_caught", "controls_n")}))
    return 0 if passed == args.runs and scores["controls_caught"] == scores["controls_n"] else 1


if __name__ == "__main__":
    sys.exit(main())
