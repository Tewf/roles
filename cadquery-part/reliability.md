# cadquery-part: reliability statement

The reliability statement of [cadquery-part](ROLE.md), as of 2026-11-17: the plate was exported twice and judged `pass` both times, and the judge refused each of five seeded faults.

## The claim

Run as written, the pipeline leaves a STEP that re-imports as one valid solid. That solid's volume equals the closed form of its parameters within 0.1%. The STL is a closed mesh within 1% of that volume. The verdict comes from [judge.py](judge.py), which opens files and no log.

## The statistic

| What | Count | Wilson 95% interval |
|---|---|---|
| clean runs of the pipeline, judged `pass` | 2 of 2 | 0.34 to 1.00 |
| faults refused by the judge | 5 of 5 | 0.57 to 1.00 |

Verdicts, one per run and per fault, are in [trial-1/scores.json](trial-1/scores.json). The seeded faults:

- no STEP
- an empty STL
- a 10 mm hole exported under parameters that say 8 mm
- a second solid unioned in apart from the plate
- an STL with its last triangle removed

## The sample

- Run on 2026-11-17 with CadQuery 2.8.0 in `~/.venvs/cad`, through `maestro/heavy.py`, by `~/.venvs/cad/bin/python cadquery-part/trial.py`.
- One part, one machine, one day.

## What this does and does not show

- **Shows:** the export runs here and is judged by files read back; the judge turns away the five faults it was handed.
- **Does not show that a part is good.** The judge compares the file with its own parameters, not with a need.
- The shared limits, two runs and no rival arm, are in [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## To rerun

```bash
~/.venvs/cad/bin/python cadquery-part/trial.py --runs 2
```
