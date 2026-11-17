#!/usr/bin/env python3
"""The reference pipeline of the unity-batch-build role: a Unity project created and driven in batch mode from an empty folder.

    python3 smoke_pipeline.py OUTDIR

Creates OUTDIR/project with `-createProject`, adds Smoke.cs, runs `-executeMethod Smoke.Run`, and copies the three files
the judge reads to OUTDIR: smoke.json, Smoke.unity and ProjectVersion.txt. The logs are kept for a person; no verdict reads them.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
UNITY = Path.home() / "Unity/Hub/Editor/6000.6.9f1/Editor/Unity"
FLAGS = ["-batchmode", "-nographics", "-quit"]


def run(args: list[str], log: Path, cwd: Path, timeout: int) -> int:
    done = subprocess.run([str(UNITY), *FLAGS, *args, "-logFile", str(log)], cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return done.returncode


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: smoke_pipeline.py OUTDIR")
        return 2
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    project = out / "project"
    if run(["-createProject", str(project)], out / "create.log", out, 900) != 0:
        return 3
    (project / "Assets/Editor").mkdir(parents=True, exist_ok=True)
    shutil.copy(HERE / "Smoke.cs", project / "Assets/Editor/Smoke.cs")
    code = run(["-projectPath", str(project), "-executeMethod", "Smoke.Run"], out / "run.log", project, 900)
    for source, name in ((project / "smoke.json", "smoke.json"), (project / "Assets/Smoke.unity", "Smoke.unity"),
                         (project / "ProjectSettings/ProjectVersion.txt", "ProjectVersion.txt")):
        if source.is_file():
            shutil.copy(source, out / name)
    (out / "exit_code.txt").write_text(f"{code}\n", encoding="utf-8")
    shutil.rmtree(project, ignore_errors=True)  # a project is hundreds of megabytes of Library
    return 0


if __name__ == "__main__":
    sys.exit(main())
