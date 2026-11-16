#!/usr/bin/env python3
"""Score a doc-editor trial: the judge on every repository, for the role arm and the baseline arm, with Wilson intervals.

    python3 score.py ROOT        # ROOT holds seeded/<repo>, work/role/<repo>, work/base/<repo>

The verdicts come from judge.py, never from the agents' own reports. Prints one line per repository and a table.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import judge  # noqa: E402

RE = Path.home() / "Desktop/Tewf/reader-ergonomics"


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main() -> None:
    root = Path(sys.argv[1])
    repos = sorted(p.name for p in (root / "seeded").iterdir() if p.is_dir())
    results: dict[str, dict[str, str]] = {"role": {}, "base": {}}
    for arm in results:
        for r in repos:
            results[arm][r] = judge.judge(root / "seeded" / r, root / "work" / arm / r, RE)
            print(f"{arm:5} {r:32} {results[arm][r]}", flush=True)
    summary = {}
    for arm, res in results.items():
        k = sum(v == "pass" for v in res.values())
        lo, hi = wilson(k, len(res))
        summary[arm] = {"passed": k, "n": len(res), "rate": k / len(res), "wilson95": [round(lo, 3), round(hi, 3)]}
    both = sum(results["role"][r] == "pass" and results["base"][r] != "pass" for r in repos)
    only_base = sum(results["base"][r] == "pass" and results["role"][r] != "pass" for r in repos)
    summary["discordant"] = {"role_only": both, "base_only": only_base}
    print(json.dumps(summary, indent=1))
    (root / "scores.json").write_text(json.dumps({"verdicts": results, "summary": summary}, indent=1))


if __name__ == "__main__":
    main()
