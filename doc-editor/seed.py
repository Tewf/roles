#!/usr/bin/env python3
"""Seed documentation faults into a copy of a repository, reproducibly, so the doc-editor role has something to fix.

    python3 seed.py SOURCE DEST [--seed N]

SOURCE should pass the `links` and `duplication` checks. DEST receives a copy without .git, then:
  - 3 relative Markdown links are broken (the target gets `-old` before its extension);
  - 2 paragraphs of at least 30 words are copied into another Markdown file.
A seeded fault is a benchmark, not a field observation: it measures whether the role repairs what the checks name, not
how often real documentation breaks this way. The seed and the faults are written to DEST/../<name>.seeded.json.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import shutil
from pathlib import Path

LINK = re.compile(r"\]\((?!https?:|#|mailto:)([^)\s#]+\.md)(#[^)\s]*)?\)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("dest", type=Path)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    if a.dest.exists():
        shutil.rmtree(a.dest)
    shutil.copytree(a.source, a.dest, ignore=shutil.ignore_patterns(".git", "_site", "node_modules", "__pycache__", "checks/out"))
    mds = sorted(p for p in a.dest.rglob("*.md") if "checks" not in p.parts)
    log = {"seed": a.seed, "links": [], "duplicates": []}
    # broken links
    candidates = []
    for p in mds:
        for m in LINK.finditer(p.read_text(encoding="utf-8")):
            if (p.parent / m.group(1)).exists():
                candidates.append((p, m.group(1)))
    rng.shuffle(candidates)
    done = set()
    for p, target in candidates:
        if len(log["links"]) == 3:
            break
        if p in done:
            continue
        text = p.read_text(encoding="utf-8")
        new = target[:-3] + "-old.md"
        p.write_text(text.replace(f"]({target}", f"]({new}", 1), encoding="utf-8")
        log["links"].append({"file": str(p.relative_to(a.dest)), "target": target, "now": new})
        done.add(p)
    # duplicated paragraphs
    paras = []
    for p in mds:
        for para in re.split(r"\n\s*\n", p.read_text(encoding="utf-8")):
            para = para.strip()
            if len(para.split()) >= 30 and not para.startswith(("|", "```", "#", "-", "*", ">")) and "\n" not in para:
                paras.append((p, para))
    rng.shuffle(paras)
    used = set()
    for p, para in paras:
        if len(log["duplicates"]) == 2:
            break
        others = [q for q in mds if q != p and q not in used]
        if not others:
            break
        q = rng.choice(others)
        with q.open("a", encoding="utf-8") as f:
            f.write("\n\n" + para + "\n")
        used.add(q)
        log["duplicates"].append({"from": str(p.relative_to(a.dest)), "into": str(q.relative_to(a.dest))})
    (a.dest.parent / f"{a.dest.name}.seeded.json").write_text(json.dumps(log, indent=1))
    print(a.dest.name, len(log["links"]), "links", len(log["duplicates"]), "duplicates")


if __name__ == "__main__":
    main()
