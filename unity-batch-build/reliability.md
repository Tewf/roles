# unity-batch-build: reliability statement

The reliability statement of [unity-batch-build](ROLE.md), as of 2026-11-17: a Unity project was created and driven twice in batch mode and judged `pass` both times, and the judge refused each of five seeded faults.

## The claim

Run as written with Unity 6000.6.9f1, the pipeline leaves an exit code of 0 for the `-executeMethod` run. `smoke.json` and `ProjectVersion.txt` name the version `Unity -version` reports. The scene is text and holds a GameObject named SmokeCube on Unity's built-in cube mesh. [judge.py](judge.py) gives the verdict from the scene and the version files, never from the log.

## The statistic

| What | Count | Wilson 95% interval |
|---|---|---|
| clean runs of the pipeline, judged `pass` | 2 of 2 | 0.34 to 1.00 |
| faults refused by the judge | 5 of 5 | 0.57 to 1.00 |

Verdicts are in [trial-1/scores.json](trial-1/scores.json). The seeded faults:

- no scene file
- an exit code of 1
- a project version of 6000.3.0f1
- a scene whose mesh is the sphere's (fileID 10207) in place of the cube's (fileID 10202)
- an empty `smoke.json`

## The sample

- Run on 2026-11-17 with the editor in `~/Unity/Hub/Editor/6000.6.9f1`, started through `maestro/heavy.py`, by `python3 unity-batch-build/trial.py`. A first run outside the trial, made to check that the licence and the project creation work offline, also passed; it is not counted.
- At that hour the machine had no DNS and the runs still finished: the pipeline needs no network.

## What this does and does not show

- **Shows:** the editor installed here creates a project and runs an editor method in batch mode; the judge turns away the five faults it was handed.
- **Does not show a player build, a package from the registry, or ML-Agents.**
- The shared limits, two runs and no rival arm, are in [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## To rerun

```bash
python3 unity-batch-build/trial.py --runs 2
```
