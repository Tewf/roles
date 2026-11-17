# runpod-pod-guard: reliability statement

The reliability statement of [runpod-pod-guard](ROLE.md), as of 2026-11-17: the cost guard was armed and disarmed twice with no pod and no spend and judged `pass` both times, and the judge refused each of six seeded faults.

## The claim

Run as written, the pipeline leaves a version file equal to what `runpodctl` reports and a catalogue with an EU datacenter that has a GPU. It arms a one-hour transient timer whose service runs `runpodctl pod delete` on the pod id. No unit is active for that id afterwards, and the pod state is unchanged. The verdict comes from [judge.py](judge.py), which opens files and asks `systemctl` itself.

## The statistic

| What | Count | Wilson 95% interval |
|---|---|---|
| clean runs of the pipeline, judged `pass` | 2 of 2 | 0.34 to 1.00 |
| faults refused by the judge | 6 of 6 | 0.61 to 1.00 |

Verdicts are in [trial-1/scores.json](trial-1/scores.json). The seeded faults:

- no guard armed
- a guard that stops where it should delete
- a wrong version
- a catalogue with no EU datacenter
- a changed pod state
- a timer left running for the pod id

## The sample

- Run on 2026-11-17 with `runpodctl` 2.12.0, by `python3 runpod-pod-guard/trial.py`. At that hour the machine had no DNS: the catalogue call still answered and `pod list` did not, so the pipeline asks the network for nothing.
- No pod was created, started or stopped, no endpoint was called, and the account balance was never read.

## What this does and does not show

- **Shows:** the guard the studio arms exists as a one-hour timer that deletes, and disarms; the judge turns away the faults it was handed.
- **Does not show that a pod can be created or that the deadline fires.** A timer was armed and read back. It was never left to elapse on a real pod. A laptop asleep past the hour fires it on wake.
- The shared limits, two runs and no rival arm, are in [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## To rerun

```bash
python3 runpod-pod-guard/trial.py --runs 2
```
