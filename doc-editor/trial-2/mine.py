#!/usr/bin/env python3
"""Find real faults for the doc-editor role in the history of the family's repositories.

    python3 mine.py OUT [--repos DIR] [--re PATH]

A real fault is a commit C whose parent P has errors of the `links` or `duplication` check of reader-ergonomics, and
whose own tree has none of them: a person fixed them, so the task is solvable. It is kept only when the role's own
judge, given P as BEFORE and C as AFTER, says pass: the fix lost no number, address or code span, removed no file and
changed no file that is not Markdown. Every first-parent commit of every repository is tried, not only those whose
message names a fix, since a fix often rides along with other work.

The checks are those of the reader-ergonomics checkout at PATH (its HEAD), run on both trees, so P and C are judged by
the same rules; the commit at which the checks ran is written in OUT/instances.json. Each kept fault leaves
OUT/<repo>-<C>/before (the tree of P, Markdown and all) and the record of its errors.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import judge  # noqa: E402


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def export(repo: Path, rev: str, into: Path) -> None:
    """The tree of `rev`, as files, into `into` (no .git)."""
    into.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(["git", "-C", str(repo), "archive", rev], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(into)], input=archive, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out", type=Path)
    parser.add_argument("--repos", type=Path, default=Path.home() / "Desktop/Tewf")
    parser.add_argument("--re", type=Path, default=Path.home() / "Desktop/Tewf/reader-ergonomics")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    kept, tried = [], 0
    for repo in sorted(p for p in args.repos.iterdir() if (p / ".git").exists()):
        for line in git(repo, "log", "--first-parent", "--format=%H %P").splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue        # the first commit has no parent
            commit, parent = parts[0], parts[1]
            changed = git(repo, "diff", "--name-only", parent, commit).split()
            if not any(name.endswith(".md") for name in changed):
                continue
            tried += 1
            with tempfile.TemporaryDirectory() as scratch:
                before, after = Path(scratch) / "before", Path(scratch) / "after"
                export(repo, parent, before)
                export(repo, commit, after)
                faults = judge.errors(before, args.re)
                if not faults or judge.errors(after, args.re):
                    continue
                verdict = judge.judge(before, after, args.re)
                if verdict != "pass":
                    continue
                name = f"{repo.name}-{commit[:7]}"
                shutil.copytree(before, args.out / name / "before")
                kept.append({"name": name, "repo": repo.name, "parent": parent, "commit": commit,
                             "subject": git(repo, "log", "-1", "--format=%s", commit).strip(),
                             "errors": faults, "n_errors": len(faults)})
                print(f"kept {name}: {len(faults)} error(s)", flush=True)
    record = {"checks_at": git(args.re, "rev-parse", "HEAD").strip(), "tried": tried, "kept": kept}
    (args.out / "instances.json").write_text(json.dumps(record, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(kept)} faults kept of {tried} commits that touch Markdown")
    return 0


if __name__ == "__main__":
    sys.exit(main())
