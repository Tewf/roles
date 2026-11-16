#!/usr/bin/env python3
"""The trial of the blender-render role: the reference pipeline twice from a clean folder, then four faults the judge must refuse.

    python3 trial.py [--runs 2] [--out trial-1]

Writes OUT/scores.json. A run counts as passed only when judge.py prints `pass`. A control counts as caught only when
judge.py fails it. This trial measures the pipeline and the judge; it does not measure a model that follows the procedure.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV = {**os.environ, "__NV_PRIME_RENDER_OFFLOAD": "1", "__VK_LAYER_NV_optimus": "NVIDIA_only"}


def wilson(passed: int, n: int, z: float = 1.96) -> tuple[float, float]:
    p = passed / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(centre - half, 2), round(centre + half, 2)


def judge(script: Path, outdir: Path) -> str:
    out = subprocess.run([sys.executable, str(HERE / "judge.py"), str(script), str(outdir)], capture_output=True, text=True)
    return out.stdout.strip().splitlines()[-1] if out.stdout.strip() else "no verdict"


def pipeline(outdir: Path) -> None:
    subprocess.run(["blender", "--background", "--gpu-backend", "vulkan", "--python", str(HERE / "render_smoke.py"), "--", str(outdir)],
                   env=ENV, capture_output=True, text=True, timeout=300)


def controls(good: Path, scratch: Path) -> list[dict]:
    source = (HERE / "render_smoke.py").read_text(encoding="utf-8")
    cases = {
        "sequences": ("write", source + "\nbpy.context.scene.sequence_editor.sequences\n"),
        "fcurves": ("write", source + "\nbpy.data.actions[0].fcurves\n"),
        "ffmpeg-before-media-type": ("write", source.replace('image_settings.media_type = "IMAGE"', "pass").replace(
            'scene.render.image_settings.media_type = "VIDEO"', "pass").replace(
            'scene.render.image_settings.file_format = "FFMPEG"', 'scene.render.image_settings.file_format = "FFMPEG"\nscene.render.image_settings.media_type = "VIDEO"')),
        "no-clip": ("noclip", source),
    }
    rows = []
    for name, (kind, text) in cases.items():
        case = scratch / name
        shutil.copytree(good, case / "out")
        (case / "script.py").write_text(text, encoding="utf-8")
        if kind == "noclip":
            (case / "out" / "clip.mp4").unlink()
        verdict = judge(case / "script.py", case / "out")
        rows.append({"control": name, "verdict": verdict, "caught": verdict.startswith("fail")})
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
            outdir = Path(tmp) / f"run{i}"
            pipeline(outdir)
            verdict = judge(HERE / "render_smoke.py", outdir)
            runs.append({"run": i, "verdict": verdict, "passed": verdict == "pass"})
            last = outdir
        caught = controls(last, Path(tmp) / "controls") if last else []
    passed = sum(r["passed"] for r in runs)
    scores = {"role": "blender-render", "runs": runs, "passed": passed, "n": args.runs,
              "wilson95": wilson(passed, args.runs), "controls": caught,
              "controls_caught": sum(c["caught"] for c in caught), "controls_n": len(caught)}
    (args.out / "scores.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: scores[k] for k in ("passed", "n", "wilson95", "controls_caught", "controls_n")}))
    return 0 if passed == args.runs and scores["controls_caught"] == scores["controls_n"] else 1


if __name__ == "__main__":
    sys.exit(main())
