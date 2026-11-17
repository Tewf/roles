#!/usr/bin/env python3
"""The judge of the comfyui-graph-check role: a program decides whether a ComfyUI graph check can be trusted.

    python3 judge.py OUTDIR [--graph GRAPH.json]

OUTDIR is the folder validate_pipeline.py wrote. It passes when all six hold:
  1. port_before.txt is empty: the port was free, so the server that answered is the one this run started;
  2. system_stats.json names the version installed in ~/opt/ComfyUI (comfyui_version.py) and a CPU device;
  3. object_info.json serves at least 800 node classes;
  4. report.md says at least 10 graphs were built, none failed to build, and no graph has a hard error
     (a weight file the server does not hold yet is only a note);
  5. port_after.txt is empty: the server was stopped;
  6. with --graph, the graph is validated against the saved object_info by the studio's own validate(): no unknown class,
     no missing required input, no input that does not exist, no value outside a combo's options (weight names excepted).
Exit 0 on pass, 1 on fail; the last line is `pass` or `fail: <reason>`.
What it does not decide: that a graph makes a good picture, or that its weights exist (the report lists those it lacks).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import re
import sys
from pathlib import Path

COMFY_VERSION_FILE = Path.home() / "opt/ComfyUI/comfyui_version.py"
MODULES = Path(os.environ.get("STUDIO_MODULES") or Path(shutil.which("studio") or "studio").resolve().parent / "modules")  # beside the `studio` launcher


def installed_version() -> str:
    match = re.search(r'__version__\s*=\s*"([^"]+)"', COMFY_VERSION_FILE.read_text(encoding="utf-8"))
    return match.group(1) if match else "unknown"


def judge(out: Path, graph: Path | None) -> str:
    for name in ("port_before.txt", "system_stats.json", "object_info.json", "report.md", "port_after.txt"):
        if not (out / name).is_file():
            return f"fail: {name} is missing: the pipeline did not finish"
    if (out / "port_before.txt").read_text(encoding="utf-8").strip():
        return "fail: the port was held before the server started: the answers may come from an older server"
    stats = json.loads((out / "system_stats.json").read_text(encoding="utf-8"))
    version, devices = stats.get("system", {}).get("comfyui_version"), stats.get("devices", [])
    if version != installed_version():
        return f"fail: the server says ComfyUI {version}, the install is {installed_version()}"
    if not devices or "cpu" not in str(devices[0].get("name", "")).lower():
        return "fail: the server did not run with --cpu: the check would load weights"
    try:
        schema = json.loads((out / "object_info.json").read_text(encoding="utf-8"))
    except ValueError:
        return "fail: object_info.json is not JSON"
    if not isinstance(schema, dict) or len(schema) < 800:
        return f"fail: object_info.json serves {len(schema) if isinstance(schema, dict) else 0} node classes, fewer than 800"
    report = (out / "report.md").read_text(encoding="utf-8")
    built = re.search(r"(\d+) graphs built, (\d+) failed to build", report)
    if not built or int(built.group(1)) < 10 or int(built.group(2)) != 0:
        return f"fail: report.md does not show 10 or more graphs built with none failing ({built.group(0) if built else 'no count'})"
    hard = [m for m in re.findall(r"(\d+) errors", report) if int(m) > 0]
    if hard or "could not build" in report:
        return "fail: report.md lists a graph with a hard error or one that could not be built"
    if (out / "port_after.txt").read_text(encoding="utf-8").strip():
        return "fail: the server still holds the port after the run"
    if graph is not None:
        sys.path.insert(0, str(MODULES))
        import comfy_validate
        issues = [m for kind, m in comfy_validate.validate(json.loads(graph.read_text(encoding="utf-8")), schema) if kind == "error"]
        if issues:
            return f"fail: the graph is refused by the server's schema: {issues[0]}"
    return "pass"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out", type=Path)
    parser.add_argument("--graph", type=Path)
    args = parser.parse_args()
    verdict = judge(args.out, args.graph)
    print(verdict)
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
