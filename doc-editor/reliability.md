# doc-editor: reliability statement

The statement of the role [doc-editor](ROLE.md), as [decision 0001](../decisions/0001-a-role-is-defined-by-its-proof.md) asks of a role: a statistic with its sample and the run that made it. **Status (2026-11-16):** one trial, ten repositories; the role passed 10 of 10, and so did the same model without the procedure, so this trial shows no gain from the role.

## The claim

On a copy of a repository whose Markdown has link errors or duplicated passages, the role brings the `links` and `duplication` checks of the reader-ergonomics standard to zero errors. It loses no number, web address or code span, and it changes no file that is not Markdown. A program, [judge.py](judge.py), decides each run.

## The statistic

| Arm | What the model got | Passed | Pass rate | Wilson 95% interval |
|---|---|---|---|---|
| role | the procedure of [ROLE.md](ROLE.md), the checks, the judge | 10 of 10 | 100% | 0.72 to 1.00 |
| single agent | the task in plain words, no procedure, no checks | 10 of 10 | 100% | 0.72 to 1.00 |

Runs where only one arm passed: 0 (the role only: 0; the single agent only: 0). Every verdict is in [trial-1/scores.json](trial-1/scores.json); the seeded faults of each repository are in `trial-1/<repository>.seeded.json`.

## The sample

- Ten repositories of the author's own family, checked out on 2026-11-16, each with 0 errors of the two checks before seeding: business, business-pricing, business-market, business-model, business-finance, business-customer, ai-augmented-cases, reader-ergonomics-project, ai-augmented-practice and ai-augmented-data-gathering.
- Seeded by [seed.py](seed.py) with seed 1: three relative links broken (`-old` added to the target) and two paragraphs of 30 words or more copied into another file. Each seeded copy held 5 to 8 errors of the two checks.
- One run per repository and arm (k = 1), the same model (Claude Sonnet) in both arms, run in parallel.
- Scored by `python3 score.py`, which calls the judge on each result.

## What this does and does not show

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

The next trial should make the task harder for the single agent. It can seed faults that the checks name but the task text does not, and give each arm k = 3 runs per repository.
