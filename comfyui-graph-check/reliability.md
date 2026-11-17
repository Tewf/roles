# comfyui-graph-check: reliability statement

The reliability statement of [comfyui-graph-check](ROLE.md), as of 2026-11-17: the validation ran twice against a fresh CPU server and was judged `pass` both times, and the judge refused each of six seeded faults.

## The claim

Run as written, the pipeline leaves the version the install names and a CPU device. The server serves at least 800 node classes, and the report shows at least 10 graphs built with no hard error. The port is free before and after. The verdict comes from [judge.py](judge.py), which opens files and no log.

## The statistic

| What | Count | Wilson 95% interval |
|---|---|---|
| clean runs of the pipeline, judged `pass` | 2 of 2 | 0.34 to 1.00 |
| faults refused by the judge | 6 of 6 | 0.61 to 1.00 |

Verdicts are in [trial-1/scores.json](trial-1/scores.json). The seeded faults:

- a listener on the port before the run
- a server that reports ComfyUI 0.28.0 where the install is 0.34.0
- an empty schema
- a report with a hard error
- a graph using the class name `ReferenceAudio` where the registered id differs (given to `--graph`)
- a graph lacking a required input (given to `--graph`)

## The sample

- Run on 2026-11-17 with ComfyUI 0.34.0, 937 node classes and 17 graphs, through `maestro/heavy.py`, by `python3 comfyui-graph-check/trial.py`.
- The two runs and the faults used the schema of the server that run started; the largest file (`object_info.json`, 1.7 MB) lives in a temporary folder.

## What this does and does not show

- **Shows:** the validation runs here against the live server; the judge turns away the faults it was handed, the node-id trap that once cost a run among them.
- **Does not show that anything is generated.** No graph ran on the GPU; the soft notes in the report list weights this machine lacks.
- The shared limits, two runs and no rival arm, are in [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## To rerun

```bash
python3 comfyui-graph-check/trial.py --runs 2
```
