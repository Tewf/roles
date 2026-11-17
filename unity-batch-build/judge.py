#!/usr/bin/env python3
"""The judge of the unity-batch-build role: a program decides whether a batch-mode Unity run passes.

    python3 judge.py OUTDIR

OUTDIR is the folder smoke_pipeline.py wrote. It passes when all five hold:
  1. exit_code.txt is 0 for the `-executeMethod` run, and no file is judged from a log;
  2. smoke.json names the editor version that `Unity -version` reports now, run here by this file;
  3. ProjectVersion.txt names that same version: the project was made and opened by the editor installed here;
  4. Smoke.unity is a text scene (`%YAML`) holding a GameObject named SmokeCube, saved by the editor method;
  5. that scene's MeshFilter points at Unity's built-in cube mesh (fileID 10202): a cube, not an empty object.
Exit 0 on pass, 1 on fail; the last line is `pass` or `fail: <reason>`.
What it does not decide: that a build for a player works, that the licence allows it, or that a package from the registry resolves (no network is needed for this run).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

UNITY = Path.home() / "Unity/Hub/Editor/6000.6.9f1/Editor/Unity"


def installed_version() -> str:
    done = subprocess.run([str(UNITY), "-version"], capture_output=True, text=True, timeout=120)
    return (done.stdout.strip().split() or ["unknown"])[0]


def judge(out: Path) -> str:
    for name in ("exit_code.txt", "smoke.json", "ProjectVersion.txt", "Smoke.unity"):
        if not (out / name).is_file() or (out / name).stat().st_size == 0:
            return f"fail: {name} is missing or empty: the editor method did not run to its end"
    if (out / "exit_code.txt").read_text(encoding="utf-8").strip() != "0":
        return "fail: the -executeMethod run did not exit 0"
    version = installed_version()
    try:
        said = json.loads((out / "smoke.json").read_text(encoding="utf-8")).get("unityVersion")
    except ValueError:
        return "fail: smoke.json is not JSON"
    if said != version:
        return f"fail: smoke.json says Unity {said}, the installed editor is {version}"
    match = re.search(r"m_EditorVersion: (\S+)", (out / "ProjectVersion.txt").read_text(encoding="utf-8"))
    if not match or match.group(1) != version:
        return f"fail: ProjectVersion.txt names {match.group(1) if match else 'no version'}, the installed editor is {version}"
    scene = (out / "Smoke.unity").read_text(encoding="utf-8", errors="replace")
    if not scene.startswith("%YAML"):
        return "fail: Smoke.unity is not a text scene"
    if "m_Name: SmokeCube" not in scene:
        return "fail: Smoke.unity holds no GameObject named SmokeCube"
    if "fileID: 10202" not in scene:
        return "fail: SmokeCube has no MeshFilter on Unity's built-in cube mesh"
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
