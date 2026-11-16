---
name: doc-editor
description: Fixes the link and duplication errors that the reader-ergonomics checks report in a repository's Markdown, on a copy, without losing a fact; a program judges the result.
role:
  autonomy: acts on a copy of the repository; the person merges
  verification: tested
  unit-of-proof: pass rate with its Wilson interval over N repositories, k = 1 run each, against the same model without this procedure
  judge: python3 doc-editor/judge.py BEFORE AFTER
  statement: doc-editor/reliability.md
---

# doc-editor

A role in the sense of [decision 0001](../decisions/0001-a-role-is-defined-by-its-proof.md): a procedure that also says how often it works. The verification level is `tested` (levels of Metere 2026a: unverified, declared, tested, formal), because its statement is a measured pass rate and no Lean file backs it.

## What it does

Given a directory of Markdown, it brings the checks `links` and `duplication` of the reader-ergonomics standard to zero errors, by editing the Markdown, and keeps every fact.

## Procedure

1. Copy the repository to a working directory. Never edit the original.
2. Run `python3 $RE/checks/run.py --only links,duplication --tiers program --judge none --out before.txt WORK`, where `$RE` is a checkout of reader-ergonomics. Each `error` line names a file and a line.
3. For an error of `links`: point the link to the file that holds the fact, or write the text without a link when no such file exists. Do not invent a file.
4. For an error of `duplication`: keep the passage in the file that owns the fact and replace it in the other file with one sentence and a link to the owner. The owner is the file that holds the longest version, or the one named in the error.
5. Run the checks again. Repeat from 3 until both checks report 0 errors or 6 rounds have passed.
6. Run `python3 doc-editor/judge.py ORIGINAL WORK`. The role has passed only when the judge prints `pass`.

## What it must not do

- Delete a file, edit a file that is not Markdown, or touch the original.
- Drop a number, an address or a code span that the original holds: the judge looks for each of them somewhere in the result.
- Declare success itself. The judge decides.

## Not covered

- The other checks (`tree-shape`, `long-sentences`, `paragraph-length`): they need a split or a rewrite that has no program to say it is right.
- Whether the prose reads better. The checks and the judge do not measure it.
