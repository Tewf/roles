#!/usr/bin/env python3
"""The judge of the blender-render role: a program decides whether a headless render passes.

    python3 judge.py SCRIPT OUTDIR [--frames N]

SCRIPT is the Blender Python file the role wrote and ran, OUTDIR the folder it rendered into. It passes when all four hold:
  1. SCRIPT uses no Blender 4.x name that 5.x removed (`.sequences`, `.fcurves`, a `bl_info` add-on), and sets
     `image_settings.media_type` before it first names FFMPEG;
  2. OUTDIR/still.png is a PNG with a real size, and OUTDIR/clip.mp4 holds N video frames (default 2), counted by ffprobe;
  3. a background Blender started with the Vulkan offload (`--gpu-backend vulkan` and the two variables) reports an NVIDIA
     renderer, run here by this file; the GLX variables alone leave Blender 5.2 on the Intel iGPU on this machine (measured 2026-11-16);
  4. nothing is claimed from a log: only the files and the renderer string count.
Exit 0 on pass, 1 on fail; the last line is `pass` or `fail: <reason>`.
What it does not decide: that the picture shows what was asked, or that Cycles picks the right device (it has its own setting).
"""
from __future__ import annotations

import argparse
import io
import os
import re
import struct
import subprocess
import sys
import tokenize
from pathlib import Path

REMOVED = {r"\.sequences\b": "`.sequences` is `.strips` in Blender 5.x",
           r"\.fcurves\b": "`Action.fcurves` was removed in Blender 5.x (slotted actions)",
           r"\bbl_info\b": "a legacy `bl_info` add-on does not load in Blender 5.2"}
OFFLOAD = {"__NV_PRIME_RENDER_OFFLOAD": "1", "__VK_LAYER_NV_optimus": "NVIDIA_only"}
RENDERER_PROBE = "import gpu; gpu.init(); print('RENDERER=' + gpu.platform.renderer_get())"


def code_only(text: str) -> str:
    """The script without its comments: a comment may name what the code must not use."""
    try:
        kept = [t for t in tokenize.generate_tokens(io.StringIO(text).readline) if t.type != tokenize.COMMENT]
        return tokenize.untokenize(kept)
    except (tokenize.TokenError, IndentationError):
        return text


def script_problems(text: str) -> list[str]:
    text = code_only(text)
    found = [why for pattern, why in REMOVED.items() if re.search(pattern, text)]
    ffmpeg, media = text.find("FFMPEG"), text.find("media_type")
    if ffmpeg != -1 and (media == -1 or media > ffmpeg):
        found.append("FFMPEG is named before `image_settings.media_type = \"VIDEO\"`, which Blender 5.x raises on")
    return found


def png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", data[16:24])


def video_frames(path: Path) -> int | None:
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                          "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True)
    return int(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip().isdigit() else None


def renderer() -> str:
    out = subprocess.run(["blender", "--background", "--gpu-backend", "vulkan", "--python-expr", RENDERER_PROBE],
                         capture_output=True, text=True, env={**os.environ, **OFFLOAD}, timeout=120)
    match = re.search(r"RENDERER=(.*)", out.stdout)
    return match.group(1).strip() if match else ""


def judge(script: Path, outdir: Path, frames: int) -> str:
    problems = script_problems(script.read_text(encoding="utf-8"))
    if problems:
        return "fail: " + "; ".join(problems)
    still, clip = outdir / "still.png", outdir / "clip.mp4"
    if not still.is_file() or png_size(still) is None or min(png_size(still)) < 1:
        return "fail: still.png is missing or is not a PNG with a size"
    if not clip.is_file() or video_frames(clip) != frames:
        return f"fail: clip.mp4 is missing or does not hold {frames} video frames"
    name = renderer()
    if "nvidia" not in name.lower():
        return f"fail: the offloaded Blender renders on `{name or 'no renderer'}`, not the discrete GPU"
    return "pass"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("script", type=Path)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--frames", type=int, default=2)
    args = parser.parse_args()
    verdict = judge(args.script, args.outdir, args.frames)
    print(verdict)
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
