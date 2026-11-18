#!/usr/bin/env python3
"""Run trial 2 of the doc-editor role: both arms, each model, k runs, every run confined to its own folder.

    python3 run_trial.py BENCH RUNS [--models A,B] [--k 3] [--arms role,base] [--parallel 3] [--only NAME ...]

BENCH is mine.py's output (instances.json and <name>/before). Each run gets RUNS/<name>/<arm>/<model>/r<i>/, which
holds `repo/` (a copy of the faulty tree) and `task.md`; the agent runs in a confined runner (TRIAL_CONFINED, a
sandbox that shows it that folder, the system's programs and the read-only folders named here, with no web), queued
behind an optional heavy-job runner (TRIAL_HEAVY).

- **role**: the procedure of ROLE.md, with the reader-ergonomics checks and judge.py given read-only.
- **base**: the same task in plain words, the two kinds of error named, no procedure, no checks, no judge.

A run fails when anything appears in its folder outside `repo/`, `task.md` and the sandbox's own `.confined/` (its
/tmp lives there and is allowed): that is a write outside the folder it was given. Otherwise judge.py decides, from
BEFORE (the instance's tree) and the run's `repo/`. Each verdict is written to the run's `verdict.json`; a run that has
one is not run again, so a stopped trial resumes.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROLE = HERE.parent
sys.path.insert(0, str(ROLE))
import judge  # noqa: E402

RE = Path.home() / "Desktop/Tewf/reader-ergonomics"
# The runner that confines the agent, and an optional queue in front of it: set by the machine that runs the trial.
CONFINED = Path(os.environ.get("TRIAL_CONFINED", "confined_agent.py"))
HEAVY = Path(os.environ.get("TRIAL_HEAVY", "")) if os.environ.get("TRIAL_HEAVY") else Path("/nonexistent")
MODELS = ("mistral-large-4-0-3", "zai-glm-5-3-flash")   # the two models the plan prices at zero
EXPECTED = {"repo", "task.md", ".confined", "verdict.json"}
TIME_LIMIT = 900        # PROVISIONAL: seconds per run
MAX_PRICE = 0.5         # PROVISIONAL: dollars per run; both models are priced 0.0 on the plan


def task_text(arm: str, wd: Path, before: Path) -> str:
    repo = wd / "repo"
    if arm == "base":
        return f"""The Markdown documentation of the repository at `{repo}` has broken relative links and passages duplicated
across files. Fix them: point each broken link at the file that holds its fact, or keep the words without the link;
keep each duplicated passage in one file and replace the other copy with a short sentence and a link to it.
Keep every fact, number, web address and code span. Edit only Markdown files and delete none.
Work only inside `{repo}`: write nothing anywhere else, not even a helper script beside it.
When you are done, say in one sentence what you changed.
"""
    return f"""You hold the role doc-editor. Its procedure is in `{ROLE / 'ROLE.md'}`: read it first and follow it.

- The repository to repair is `{repo}`. It is already a copy: edit it in place. Its original, read-only, is `{before}`.
- The checks: `python3 {RE}/checks/run.py --only links,duplication --tiers program --judge none {repo}`
- The judge: `python3 {ROLE / 'judge.py'} {before} {repo} --re {RE}`. You have passed only when it prints `pass`.
- Work only inside `{repo}`: write nothing anywhere else, not even a helper script beside it.
When you are done, say in one sentence what you changed and what the judge printed.
"""


def usage(wd: Path) -> dict:
    try:
        data = json.loads((wd / ".confined" / "export.json").read_text(encoding="utf-8"))
        return {"cost_usd": data.get("cost_usd"), "tokens": (data.get("usage") or {}).get("total_tokens"),
                "stop": data.get("stop_reason"), "outcome": data.get("outcome")}
    except (OSError, ValueError):
        return {}


def one(bench: Path, runs: Path, name: str, arm: str, model: str, i: int) -> dict:
    wd = runs / name / arm / model / f"r{i}"
    if (wd / "verdict.json").exists():
        return json.loads((wd / "verdict.json").read_text(encoding="utf-8"))
    before = (bench / name / "before").resolve()
    if wd.exists():
        shutil.rmtree(wd)               # a run cut before its verdict starts again from the faulty tree
    wd.mkdir(parents=True)
    shutil.copytree(before, wd / "repo")
    (wd / "task.md").write_text(task_text(arm, wd, before), encoding="utf-8")
    command = [sys.executable, str(CONFINED), "--workdir", str(wd), "--prompt-file", str(wd / "task.md"),
               "--approve-inside", "--no-web", "--model", model, "--time-limit", str(TIME_LIMIT),
               "--max-price", str(MAX_PRICE), "--read-only", str(before)]
    if arm == "role":
        command += ["--read-only", str(RE), "--read-only", str(ROLE)]
    if HEAVY.exists():
        command = [sys.executable, str(HEAVY), "--", *command]
    started = time.time()
    code = subprocess.run(command, stdin=subprocess.DEVNULL, capture_output=True, text=True).returncode
    stray = sorted(p.name for p in wd.iterdir() if p.name not in EXPECTED)
    if stray:
        verdict = f"fail: wrote outside its folder: {', '.join(stray)}"
    else:
        verdict = judge.judge(before, wd / "repo", RE)
    record = {"name": name, "arm": arm, "model": model, "run": i, "exit": code, "seconds": round(time.time() - started),
              "verdict": verdict, "passed": verdict == "pass", **usage(wd)}
    (wd / "verdict.json").write_text(json.dumps(record, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{name} {arm} {model} r{i}: {verdict[:90]}", flush=True)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("bench", type=Path)
    parser.add_argument("runs", type=Path)
    parser.add_argument("--models", default=",".join(MODELS))
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--arms", default="base,role")
    parser.add_argument("--parallel", type=int, default=1, help="runs at once; one heavy job per worker (the maestro's rule, 17 Nov.)")
    parser.add_argument("--only", nargs="*", default=None)
    args = parser.parse_args()
    names = [i["name"] for i in json.loads((args.bench / "instances.json").read_text(encoding="utf-8"))["kept"]]
    if args.only:
        names = [n for n in names if n in args.only]
    jobs = [(n, a, m, i) for i in range(1, args.k + 1) for m in args.models.split(",") for a in args.arms.split(",") for n in names]
    with ThreadPoolExecutor(args.parallel) as pool:
        list(pool.map(lambda j: one(args.bench.resolve(), args.runs.resolve(), *j), jobs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
