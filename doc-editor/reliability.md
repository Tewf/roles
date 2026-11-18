# doc-editor: reliability statement

The statement of the role [doc-editor](ROLE.md), as [decision 0001](../decisions/0001-a-role-is-defined-by-its-proof.md) asks of a role: a statistic with its sample and the run that made it. **Status (2026-11-18):** two trials.

- Trial 2, 14 real faults from the family's history, two models, three runs each: the role passed 84 of 84, the same model without the procedure 43 of 84. McNemar's test on the 84 pairs gives p below 1e-11. Most of the gain is finishing within the time limit.
- Trial 1, seeded faults: both arms at the ceiling.

## The claim


On a copy of a repository whose Markdown has link errors or duplicated passages, the role brings the `links` and `duplication` checks of the reader-ergonomics standard to zero errors. It loses no number, web address or code span, and it changes no file that is not Markdown. A program, [judge.py](judge.py), decides each run.

## Trial 2: real faults, two models, three runs (2026-11-17)

### The statistic

| Model, arm | Passed | Wilson 95% | Cut at the 900 s limit | Median seconds |
|---|---|---|---|---|
| Mistral Large 4, role | 42 of 42 | 0.92 to 1.00 | 0 | 115 |
| Mistral Large 4, single agent | 15 of 42 | 0.23 to 0.51 | 30 | 901 |
| GLM 5.3 Flash, role | 42 of 42 | 0.92 to 1.00 | 0 | 39 |
| GLM 5.3 Flash, single agent | 28 of 42 | 0.52 to 0.79 | 3 | 343 |

| Paired reading (one fault, one model, one run index) | Pairs | Role only, agent only | McNemar p | Paired difference, 95% |
|---|---|---|---|---|
| primary, Mistral | 42 | 27, 0 | 1.5e-08 | 0.64, 0.50 to 0.79 |
| primary, GLM | 42 | 14, 0 | 1.2e-04 | 0.33, 0.19 to 0.48 |
| primary, both models | 84 | 41, 0 | 9.1e-13 | 0.49, 0.38 to 0.60 |
| secondary, neither run cut, both models | 51 | 12, 0 | 4.9e-04 | 0.24, 0.12 to 0.35 |

- McNemar's exact test (McNemar 1947) on the discordant pairs; the paired difference with the Wald interval of Agresti (2013, section 10.1).
- The secondary reading was named before the data, in the trial's notes. Its pairs are chosen by an outcome, so it is reported as secondary only.
- Every verdict summary is in [trial-2/scores.json](trial-2/scores.json), made by [trial-2/score.py](trial-2/score.py).

### The sample

- 14 commits, mined by [trial-2/mine.py](trial-2/mine.py) from the first-parent history of the family's repositories ([trial-2/instances.json](trial-2/instances.json)). The parent has errors of the `links` or `duplication` check, at reader-ergonomics `65e4247`. The commit has none, and the judge passes it against its parent. 14 kept of 825 tried. The faulty tree is the parent.
- Two models free on the plan, `mistral-large-4-0-3` and `zai-glm-5-3-flash`, three runs per fault, arm and model: 168 runs, one at a time, by [trial-2/run_trial.py](trial-2/run_trial.py).
- Each run confined to its own folder by a sandbox with no web; anything written in the folder outside the repository copy fails the run. The role arm also saw the standard's checks and the role read-only.

### What this does and does not show

- **Shows:** on real faults, the role repaired every one, with both models, in a fraction of the time. The single agent left errors, ran out of time, or wrote outside its folder.
- **Most of the gain is speed.** The check's list of errors tells the role what to fix. It finished in 39 to 115 seconds at the median; the single agent was cut at 900 s in 33 of 84 runs, 4 of which still passed.
  - Of the 41 pairs the single agent lost, 29 are cuts at the limit: 26 of 27 on Mistral Large 4, 3 of 14 on GLM 5.3 Flash.
  - Where neither run was cut, the gain is 12 pairs against 0, and it is almost all GLM's: 11 against 0 on 39 pairs. On Mistral Large 4 only 12 pairs had both runs finish, and they split 1 against 0, so on that model the trial cannot separate a better repair from a faster one.
- **The judge accepts a reworded duplicate.** A duplicated passage passes the 20-word check once it is rewritten, though the task asks for one copy and a link. Read by hand, 3 of the role's 12 repairs of a duplication and both of the single agent's 2 are of this kind, or link a file to itself. Counted as failures, the result is 81 of 84 against 41 of 84, 40 pairs against 0.
- **One channel of leakage:** the role arm saw the reader-ergonomics checkout, which holds the repaired tree of its two faults. Its runs on them read nothing there outside `checks/`, and no benchmark tree carries a `.git`.
- **Stray writes:** 2 single-agent runs on GLM wrote a scratch file beside the repository copy and failed; no role run did.
- **One stalled run:** a single-agent run waited on the API for six hours past its limit; it was stopped by hand and counted as cut and failed.
- **One family, one week.** The faults come from repositories written by one author with the same checks; the statement does not say it holds elsewhere.

## Trial 1: seeded faults (2026-11-16)

### The statistic

| Arm | What the model got | Passed | Pass rate | Wilson 95% interval |
|---|---|---|---|---|
| role | the procedure of [ROLE.md](ROLE.md), the checks, the judge | 10 of 10 | 100% | 0.72 to 1.00 |
| single agent | the task in plain words, no procedure, no checks | 10 of 10 | 100% | 0.72 to 1.00 |

Runs where only one arm passed: 0 (the role only: 0; the single agent only: 0). Every verdict is in [trial-1/scores.json](trial-1/scores.json); the seeded faults of each repository are in `trial-1/<repository>.seeded.json`.

### The sample

- Ten repositories of the author's own family, checked out on 2026-11-16, each with 0 errors of the two checks before seeding: business, business-pricing, business-market, business-model, business-finance, business-customer, ai-augmented-cases, reader-ergonomics-project, ai-augmented-practice and ai-augmented-data-gathering.
- Seeded by [seed.py](seed.py) with seed 1: three relative links broken (`-old` added to the target) and two paragraphs of 30 words or more copied into another file. Each seeded copy held 5 to 8 errors of the two checks.
- One run per repository and arm (k = 1), the same model (Claude Sonnet) in both arms, run in parallel.
- Scored by `python3 score.py`, which calls the judge on each result.

### What this does and does not show

- **Shows:** with its procedure and judge, the role repaired all ten seeded repositories, and it did it in 1 to 3 rounds of the checks (the agents' own reports).
- **Does not show a gain over the single agent.** Both arms are at the ceiling. With 10 pairs and no discordant pair, the data cannot separate a role that helps a little from one that does not help. The task was too easy for this model, and the single agent was told the two kinds of error, which is most of what the checker says.
- **Does not show reliability on real documentation.** The faults are seeded and mechanical. Real documentation breaks in other ways, and two checks that matter for readers (`tree-shape`, `long-sentences`) are out of scope.
- **Not blind to the judge's tokens.** The single agent was told not to lose a number, address or code span, which is the judge's own preservation test.
- **One model, one day.** The statement does not say it survives a change of model or harness (the review's third question).
- **Two stray writes:** two single-agent runs wrote a helper script one directory above their folder, in the scratch area of the trial, not in a repository. No result file was affected (the judge compares the repositories only).

## To rerun

```bash
python3 doc-editor/seed.py ~/Desktop/Tewf/<repository> <scratch>/seeded/<repository> --seed 1
# copy to <scratch>/work/role/<repository> and <scratch>/work/base/<repository>, give each to an agent, then
python3 doc-editor/score.py <scratch>
```

Trial 2:

```bash
python3 doc-editor/trial-2/mine.py <bench>                      # the real faults and their faulty trees
python3 doc-editor/trial-2/run_trial.py <bench> <runs> --k 3     # both arms, both models, confined
python3 doc-editor/trial-2/score.py <runs> --out doc-editor/trial-2/scores.json
```
