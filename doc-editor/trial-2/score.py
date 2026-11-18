#!/usr/bin/env python3
"""Score trial 2: each arm's pass rate, and the role against the single agent by McNemar's paired test.

    python3 score.py RUNS [--out scores.json]

The unit of pairing is one fault, one model and one run index: the role's run i and the single agent's run i on the
same fault with the same model. Of n pairs, b are passed by the role alone and c by the single agent alone.

- Pass rate of an arm: passed over runs, with the Wilson score interval (Wilson 1927).
- McNemar's exact test (McNemar 1947): under no difference, b is Binomial(b + c, 1/2); the two-sided p is
  min(1, 2 P(X <= min(b, c))).
- The share of discordant pairs the role wins, b / (b + c), with its exact Clopper-Pearson interval (1934).
- The difference in paired pass rates, (b - c) / n, with the Wald interval of a paired difference,
  standard error sqrt(b + c - (b - c)^2 / n) / n (Agresti 2013, section 10.1).
Per model, and both models pooled. Verdicts come from each run's verdict.json, written by run_trial.py from the judge.

Two more readings, named before the trial's data was in (17 Nov. 2026), because the 900 s limit cut 8 of 14 pilot runs:
- the share of each arm's runs cut at the limit (`outcome` "deadline" in the verdict, from the sandbox's export),
  with its Wilson interval;
- secondary: the same paired analysis restricted to the pairs where neither run was cut.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

Z = 1.96


def wilson(k: int, n: int, z: float = Z) -> list[float]:
    if n == 0:
        return [0.0, 1.0]
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 3), round((c + h) / d, 3)]


def binom_cdf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def mcnemar_p(b: int, c: int) -> float:
    m = b + c
    return 1.0 if m == 0 else min(1.0, 2 * binom_cdf(min(b, c), m, 0.5))


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> list[float]:
    """Exact interval of a binomial share, by bisection on the binomial tails."""
    if n == 0:
        return [0.0, 1.0]

    def solve(f, lo=0.0, hi=1.0):
        for _ in range(100):
            mid = (lo + hi) / 2
            if f(mid):
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda p: 1 - binom_cdf(k - 1, n, p) >= alpha / 2)
    upper = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p) <= alpha / 2)
    return [round(lower, 3), round(upper, 3)]


def paired(b: int, c: int, n: int) -> dict:
    out = {"pairs": n, "role_only": b, "base_only": c, "mcnemar_p": float(f"{mcnemar_p(b, c):.3g}"),
           "role_wins_share": None if b + c == 0 else round(b / (b + c), 3),
           "role_wins_share_ci95": clopper_pearson(b, b + c)}
    if n:
        d = (b - c) / n
        se = math.sqrt(max(b + c - (b - c) ** 2 / n, 0)) / n
        out.update(difference=round(d, 3), difference_ci95=[round(d - Z * se, 3), round(d + Z * se, 3)])
    return out


def cut(v: dict) -> bool:
    """A run the sandbox stopped at its time limit."""
    return v.get("outcome") == "deadline"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("runs", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    verdicts = [json.loads(p.read_text(encoding="utf-8")) for p in args.runs.glob("*/*/*/r*/verdict.json")]
    by = {(v["name"], v["model"], v["run"], v["arm"]): v["passed"] for v in verdicts}
    was_cut = {(v["name"], v["model"], v["run"], v["arm"]): cut(v) for v in verdicts}
    report: dict = {"arms": {}, "paired": {}, "paired_neither_cut": {}}
    for model in sorted({v["model"] for v in verdicts}) + ["pooled"]:
        sel = [v for v in verdicts if model == "pooled" or v["model"] == model]
        for arm in ("role", "base"):
            runs = [v for v in sel if v["arm"] == arm]
            k = sum(v["passed"] for v in runs)
            report["arms"][f"{model}/{arm}"] = {"passed": k, "runs": len(runs), "rate": round(k / len(runs), 3) if runs else None,
                                                "wilson95": wilson(k, len(runs)),
                                                "stray_writes": sum("outside its folder" in v["verdict"] for v in runs),
                                                "cut_at_limit": sum(cut(v) for v in runs),
                                                "cut_wilson95": wilson(sum(cut(v) for v in runs), len(runs))}
        keys = {(n, m, r) for (n, m, r, a) in by if model == "pooled" or m == model}
        pairs = [(by[(n, m, r, "role")], by[(n, m, r, "base")]) for (n, m, r) in keys
                 if (n, m, r, "role") in by and (n, m, r, "base") in by]
        b = sum(1 for x, y in pairs if x and not y)
        c = sum(1 for x, y in pairs if y and not x)
        report["paired"][model] = paired(b, c, len(pairs))
        whole = [(by[(n, m, r, "role")], by[(n, m, r, "base")]) for (n, m, r) in keys
                 if (n, m, r, "role") in by and (n, m, r, "base") in by
                 and not was_cut[(n, m, r, "role")] and not was_cut[(n, m, r, "base")]]
        report["paired_neither_cut"][model] = paired(sum(1 for x, y in whole if x and not y),
                                                     sum(1 for x, y in whole if y and not x), len(whole))
    print(json.dumps(report, indent=1))
    if args.out:
        args.out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
