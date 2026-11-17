#!/usr/bin/env python3
"""The trial of the runpod-pod-guard role: the guard pipeline run twice from an empty folder, then six faults the judge must refuse.

    python3 trial.py [--runs 2] [--out trial-1]

Writes OUT/scores.json. No pod is created and nothing is spent. A run counts as passed only when judge.py prints `pass`;
a control counts as caught only when judge.py fails it. This measures the pipeline and the judge, not a model that follows the procedure.
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


def wilson(passed: int, n: int, z: float = 1.96) -> tuple[float, float]:
    p = passed / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(centre - half, 2), round(centre + half, 2)


def judge(folder: Path) -> str:
    out = subprocess.run([sys.executable, str(HERE / "judge.py"), str(folder)], capture_output=True, text=True)
    return out.stdout.strip().splitlines()[-1] if out.stdout.strip() else "no verdict"


def controls(good: Path, scratch: Path) -> list[dict]:
    rows = []

    def record(name: str, folder: Path) -> None:
        verdict = judge(folder)
        rows.append({"control": name, "verdict": verdict, "caught": verdict.startswith("fail")})

    def copy(name: str) -> Path:
        case = scratch / name
        shutil.copytree(good, case)
        return case

    case = copy("no-guard"); (case / "guard_armed.txt").write_text(""); record("no-guard", case)
    case = copy("stop-not-delete")
    text = (case / "guard_armed.txt").read_text().replace('"delete"', '"stop"'); (case / "guard_armed.txt").write_text(text); record("stop-not-delete", case)
    case = copy("wrong-version"); (case / "version.txt").write_text("runpodctl 1.14.0\n"); record("wrong-version", case)
    case = copy("no-eu"); (case / "datacenters.json").write_text(json.dumps([{"id": "US-TX-1", "gpuAvailability": [{"gpuId": "x"}]}])); record("no-eu", case)
    case = copy("state-moved"); (case / "state_after.txt").write_text("0" * 64 + "\n"); record("state-moved", case)
    case = copy("still-armed")  # a real timer for this folder's id, left running for the judge to find
    pod_id = (case / "guard_id.txt").read_text().strip()
    subprocess.run(["systemd-run", "--user", "--on-active=3600", "--unit", f"studio-pod-{pod_id}", "true"], capture_output=True, text=True)
    try:
        record("still-armed", case)
    finally:
        subprocess.run(["systemctl", "--user", "stop", f"studio-pod-{pod_id}.timer"], capture_output=True, text=True)
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
            subprocess.run([sys.executable, str(HERE / "guard_pipeline.py"), str(folder)], capture_output=True, text=True, timeout=120)
            verdict = judge(folder)
            runs.append({"run": i, "verdict": verdict, "passed": verdict == "pass"})
            last = folder
        scratch = Path(tmp) / "controls"; scratch.mkdir()
        caught = controls(last, scratch) if last else []
    passed = sum(r["passed"] for r in runs)
    scores = {"role": "runpod-pod-guard", "runs": runs, "passed": passed, "n": args.runs, "wilson95": wilson(passed, args.runs),
              "controls": caught, "controls_caught": sum(c["caught"] for c in caught), "controls_n": len(caught)}
    (args.out / "scores.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: scores[k] for k in ("passed", "n", "wilson95", "controls_caught", "controls_n")}))
    return 0 if passed == args.runs and scores["controls_caught"] == scores["controls_n"] else 1


if __name__ == "__main__":
    sys.exit(main())
