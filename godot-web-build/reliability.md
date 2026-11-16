# godot-web-build: reliability statement

The reliability statement of [godot-web-build](ROLE.md). **Status (2026-11-16):** the starter's export ran twice from a copy without `build/` and a program judged both `pass`; four faults given to the judge were all refused. This counts the export and the judge. It does not say how often a model produces a passing project from the procedure.

## The claim

Run as written on the starter project, the export leaves `build/web/` with the four files a page needs, each non-empty, and the launcher still exports the three discrete-GPU variables. [judge.py](judge.py) decides, and reads no log.

## The statistic

| What | Count | Wilson 95% interval |
|---|---|---|
| clean runs of the export, judged `pass` | 2 of 2 | 0.34 to 1.00 |
| faults refused by the judge | 4 of 4 | 0.51 to 1.00 |

Verdicts, one per run and per fault, are in [trial-1/scores.json](trial-1/scores.json). The four faults: a C# file in the project, a project with no `build/`, an empty `index.wasm`, and a launcher that is a symlink.

## The sample

- Run on 2026-11-16 with Godot 4.7.1 and its export templates in `~/.local/share/godot`, on a copy of `~/Desktop/GameDev/projects/starter` with its `build/` removed.
- Each run takes about 6 s and is started by `python3 godot-web-build/trial.py`.

## What this does and does not show

- **Shows:** the export runs on this machine and is judged by files, and the judge turns away the four faults it was handed.
- **Is not a rate.** Two runs, one machine and one day give an interval from 0.34 to 1.00.
- **Has no rival arm.** No run was made without the procedure, so no gain over a plain agent is claimed.
- **Does not show that a game plays.** The judge sees files; only a browser sees the game.
- **Leaves the snap trap untested.** The trial ran from a plain terminal, so no run kept the export templates out of reach.

## To rerun

```bash
python3 godot-web-build/trial.py --runs 2
```
