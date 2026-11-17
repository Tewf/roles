#!/usr/bin/env python3
"""The reference pipeline of the comfyui-graph-check role: boot ComfyUI on the CPU, ask it what it is, validate every studio graph, stop it.

    python3 validate_pipeline.py OUTDIR [--port 8189]

Writes OUTDIR/port_before.txt, system_stats.json, object_info.json, report.md and port_after.txt. No weight loads and
nothing is generated: a `--cpu` server serves /object_info in seconds. The port is checked first because a server that
finds its port held exits while curl keeps answering from the old one (memory/comfyui-validate-graphs-offline.md).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

COMFY = Path.home() / "opt/ComfyUI"
PYTHON = Path.home() / "miniforge3/envs/comfyui/bin/python"
MODULES = Path(os.environ.get("STUDIO_MODULES") or Path(shutil.which("studio") or "studio").resolve().parent / "modules")  # beside the `studio` launcher


def listeners(port: int) -> str:
    return subprocess.run(["ss", "-ltnH", f"sport = :{port}"], capture_output=True, text=True).stdout.strip()


def get(port: int, path: str, timeout: float = 30):
    return json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/{path}", timeout=timeout))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out", type=Path)
    parser.add_argument("--port", type=int, default=8189)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "port_before.txt").write_text(listeners(args.port) + "\n", encoding="utf-8")
    if listeners(args.port):
        return 3  # the judge refuses a folder whose port was held
    server = subprocess.Popen([str(PYTHON), "main.py", "--cpu", "--port", str(args.port), "--listen", "127.0.0.1"],
                              cwd=COMFY, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(120):
            try:
                stats = get(args.port, "system_stats", 3)
                break
            except OSError:
                time.sleep(1)
        else:
            return 4
        (args.out / "system_stats.json").write_text(json.dumps(stats), encoding="utf-8")
        (args.out / "object_info.json").write_text(json.dumps(get(args.port, "object_info")), encoding="utf-8")
        env = dict(os.environ, COMFYUI_PORT=str(args.port), PYTHONPATH=str(MODULES))
        subprocess.run([sys.executable, "-c", "import sys, comfy_validate; sys.exit(comfy_validate.main(['--out', sys.argv[1]]))",
                        str(args.out / "report.md")], env=env, capture_output=True, text=True, timeout=300)
    finally:
        server.terminate()
        try:
            server.wait(30)
        except subprocess.TimeoutExpired:
            server.kill()
        (args.out / "port_after.txt").write_text(listeners(args.port) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
