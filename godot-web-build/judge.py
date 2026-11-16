#!/usr/bin/env python3
"""The judge of the godot-web-build role: a program decides whether a Godot Web export passes.

    python3 judge.py PROJECT [--godot PATH]

PROJECT is a Godot 4.7 project folder the role exported. It passes when all five hold:
  1. no C# file (`.cs`, `.csproj`, `.sln`): the standard build has no C# Web export;
  2. the Godot launcher is a wrapper, not a symlink, and exports the three discrete-GPU variables;
  3. `export_presets.cfg` holds a Web preset;
  4. `build/web` holds `index.html`, `index.js`, `index.wasm` and `index.pck`, each non-empty, and the page is HTML;
  5. nothing is read from a log: a build is proved by files on disk, never by the absence of a word.
Exit 0 on pass, 1 on fail; the last line is `pass` or `fail: <reason>`.
What it does not decide: that the game runs in a browser (webapp-testing does), or that its assets may ship (their licences).
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

CS_SUFFIXES = {".cs", ".csproj", ".sln"}
GPU_VARIABLES = ("__NV_PRIME_RENDER_OFFLOAD", "__GLX_VENDOR_LIBRARY_NAME", "__VK_LAYER_NV_optimus")
ARTEFACTS = ("index.html", "index.js", "index.wasm", "index.pck")


def csharp_files(project: Path) -> list[str]:
    return sorted(str(p.relative_to(project)) for p in project.rglob("*")
                  if p.suffix in CS_SUFFIXES and ".godot" not in p.parts and "build" not in p.parts)


def wrapper_problem(godot: Path) -> str | None:
    if godot.is_symlink():
        return f"`{godot}` is a symlink: Godot would run on the Intel iGPU with no error"
    text = godot.read_text(encoding="utf-8", errors="replace") if godot.is_file() else ""
    missing = [v for v in GPU_VARIABLES if f"export {v}=" not in text]
    return f"`{godot}` lacks the exports {', '.join(missing)}" if missing else None


def judge(project: Path, godot: Path) -> str:
    cs = csharp_files(project)
    if cs:
        return f"fail: C# files ({cs[0]}): the standard build cannot export C# to the Web"
    problem = wrapper_problem(godot)
    if problem:
        return f"fail: {problem}"
    presets = project / "export_presets.cfg"
    if not presets.is_file() or 'platform="Web"' not in presets.read_text(encoding="utf-8", errors="replace"):
        return "fail: export_presets.cfg has no Web preset"
    web = project / "build" / "web"
    for name in ARTEFACTS:
        path = web / name
        if not path.is_file() or path.stat().st_size == 0:
            return f"fail: build/web/{name} is missing or empty: the build is not proved"
    if "<html" not in (web / "index.html").read_text(encoding="utf-8", errors="replace").lower():
        return "fail: build/web/index.html is not an HTML page"
    return "pass"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("project", type=Path)
    parser.add_argument("--godot", type=Path, default=Path(shutil.which("godot") or "godot"))
    args = parser.parse_args()
    verdict = judge(args.project, args.godot)
    print(verdict)
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
