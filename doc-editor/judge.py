#!/usr/bin/env python3
"""The judge of the doc-editor role: a program decides whether a result passes.

    python3 judge.py BEFORE AFTER [--re PATH_TO_READER_ERGONOMICS]

BEFORE is the repository as given, AFTER the role's result. It passes when all four hold:
  1. BEFORE has at least one error of `links` or `duplication` (otherwise the task was empty);
  2. AFTER has none (the reader-ergonomics checks, program tier, run by this file, never by the model);
  3. AFTER has every file of BEFORE and changed no file that is not Markdown;
  4. every number, web address and code span of BEFORE's Markdown appears somewhere in AFTER's Markdown.
Exit 0 on pass, 1 on fail; the last line is `pass` or `fail: <reason>`.
What it does not decide: that the result reads well, or that a fact kept as a number is kept in the right place.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CHECKS = "links,duplication"
TOKEN = re.compile(r"https?://[^\s)>\]]+|`[^`\n]+`|\b\d[\d.,]*\d\b|\b\d\b")


def errors(repo: Path, re_root: Path) -> list[str]:
    out = subprocess.run(
        [sys.executable, str(re_root / "checks/run.py"), "--only", CHECKS, "--tiers", "program",
         "--judge", "none", str(repo)],
        capture_output=True, text=True, timeout=600)
    return [l for l in out.stdout.splitlines() if l.startswith("error")]


def markdown(repo: Path) -> dict[str, str]:
    return {str(p.relative_to(repo)): p.read_text(encoding="utf-8", errors="replace")
            for p in repo.rglob("*.md") if ".git" not in p.parts}


def tokens(texts: dict[str, str]) -> set[str]:
    return {t.strip(".,") for text in texts.values() for t in TOKEN.findall(text)}


def judge(before: Path, after: Path, re_root: Path) -> str:
    if not errors(before, re_root):
        return "fail: BEFORE has no links or duplication error, the task is empty"
    left = errors(after, re_root)
    if left:
        return f"fail: {len(left)} error(s) left, first: {left[0][:120]}"
    for p in before.rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            q = after / p.relative_to(before)
            if not q.exists():
                return f"fail: file removed: {p.relative_to(before)}"
            if p.suffix != ".md" and p.read_bytes() != q.read_bytes():
                return f"fail: non-Markdown file changed: {p.relative_to(before)}"
    lost = sorted(tokens(markdown(before)) - tokens(markdown(after)))
    if lost:
        return f"fail: {len(lost)} number, address or code span lost, first: {lost[0][:80]}"
    return "pass"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("before", type=Path)
    ap.add_argument("after", type=Path)
    ap.add_argument("--re", type=Path, default=Path.home() / "Desktop/Tewf/reader-ergonomics")
    a = ap.parse_args()
    verdict = judge(a.before.resolve(), a.after.resolve(), a.re)
    print(verdict)
    sys.exit(0 if verdict == "pass" else 1)
