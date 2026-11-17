#!/usr/bin/env python3
"""The trial of the comfyui-graph-check role: the validation pipeline run twice from an empty folder, then six faults the judge must refuse.

    python3 trial.py [--runs 2] [--out trial-1]

Writes OUT/scores.json. A run counts as passed only when judge.py prints `pass`; a control counts as caught only when
judge.py fails it. This measures the pipeline and the judge, not a model that follows the procedure.
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
GOOD_GRAPH = {"1": {"class_type": "EmptyLatentImage", "inputs": {"width": 512, "height": 512, "batch_size": 1}}}
TRAP_GRAPH = {"1": {"class_type": "ReferenceAudio", "inputs": {}}}  # the class name, not the registered id ReferenceTimbreAudio
MISSING_GRAPH = {"1": {"class_type": "EmptyLatentImage", "inputs": {"width": 512, "batch_size": 1}}}  # height missing


def wilson(passed: int, n: int, z: float = 1.96) -> tuple[float, float]:
    p = passed / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(centre - half, 2), round(centre + half, 2)


def judge(folder: Path, graph: Path | None = None) -> str:
    cmd = [sys.executable, str(HERE / "judge.py"), str(folder)] + (["--graph", str(graph)] if graph else [])
    out = subprocess.run(cmd, capture_output=True, text=True)
    return out.stdout.strip().splitlines()[-1] if out.stdout.strip() else "no verdict"


def controls(good: Path, scratch: Path) -> list[dict]:
    rows = []

    def record(name: str, verdict: str) -> None:
        rows.append({"control": name, "verdict": verdict, "caught": verdict.startswith("fail")})

    def copy(name: str) -> Path:
        case = scratch / name
        shutil.copytree(good, case)
        return case

    case = copy("port-held"); (case / "port_before.txt").write_text("LISTEN 0 2048 127.0.0.1:8189 0.0.0.0:*\n"); record("port-held", judge(case))
    case = copy("stale-version")
    stats = json.loads((case / "system_stats.json").read_text()); stats["system"]["comfyui_version"] = "0.28.0"
    (case / "system_stats.json").write_text(json.dumps(stats)); record("stale-version", judge(case))
    case = copy("empty-schema"); (case / "object_info.json").write_text("{}"); record("empty-schema", judge(case))
    case = copy("error-report")
    report = (case / "report.md").read_text().replace("7 nodes, OK", "7 nodes, 2 errors, 0 weights missing", 1)
    (case / "report.md").write_text(report); record("error-report", judge(case))
    graph = scratch / "trap.json"; graph.write_text(json.dumps(TRAP_GRAPH)); record("class-name-trap", judge(good, graph))
    graph = scratch / "missing.json"; graph.write_text(json.dumps(MISSING_GRAPH)); record("missing-input", judge(good, graph))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", type=int, default=2)
    parser.add_argument("--out", type=Path, default=HERE / "trial-1")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    runs, last = [], None
    with tempfile.TemporaryDirectory() as tmp:
        good_graph = Path(tmp) / "good.json"; good_graph.write_text(json.dumps(GOOD_GRAPH))
        for i in range(1, args.runs + 1):
            folder = Path(tmp) / f"run{i}"
            subprocess.run([sys.executable, str(HERE / "validate_pipeline.py"), str(folder)], capture_output=True, text=True, timeout=600)
            verdict = judge(folder, good_graph)
            runs.append({"run": i, "verdict": verdict, "passed": verdict == "pass"})
            last = folder
        scratch = Path(tmp) / "controls"; scratch.mkdir()
        caught = controls(last, scratch) if last else []
    passed = sum(r["passed"] for r in runs)
    scores = {"role": "comfyui-graph-check", "runs": runs, "passed": passed, "n": args.runs, "wilson95": wilson(passed, args.runs),
              "controls": caught, "controls_caught": sum(c["caught"] for c in caught), "controls_n": len(caught)}
    (args.out / "scores.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: scores[k] for k in ("passed", "n", "wilson95", "controls_caught", "controls_n")}))
    return 0 if passed == args.runs and scores["controls_caught"] == scores["controls_n"] else 1


if __name__ == "__main__":
    sys.exit(main())
