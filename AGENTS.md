# Contributing to this repository

For anyone changing this repository, person or language model. To apply the reader-ergonomics standard elsewhere, read its [standard.md](https://github.com/Tewf/reader-ergonomics/blob/030e4f21a151dca21366dc98923e6285f5f6e5ba/standard.md). This file is about this repository only.

## Before writing

1. Read the front page's scope: what is in, what is out, and which neighbour holds what is out.
2. Read the review's [position](evidence/roles-review/position.md) and [baseline](evidence/roles-review/baseline.md). A role that claims more than B1 carries its proof.
3. A fact that belongs to a neighbour is linked, never copied. A choice that shapes the repository gets a record in [decisions/](decisions/).

## Rules for claims

- Every claim carries a grade: **measured**, **supported with caveat**, **convention** or **not supported**. A grade moves only with a cited source.
- Cite as `Author Year`. The entry goes once into the review's `references.md`, with a DOI, an arXiv id or a stable URL.
- Evidence against a rule goes into `against.md`, never deleted to make a rule look stronger.
- A number read in a summary rather than in the source is marked "(secondary)".
- A role's reliability claim names its witness: a Lean file and theorem, a statistic with its sample and the run that made it, or a reference with its section.

## The model's place

- A model explains, proposes, translates and drafts. It decides nothing. Its output is checked by a program or read by the maintainer.
- Nothing is pushed, published or sent without the maintainer's go.

## Checks

- `python3 checks/run.py .` from a checkout of reader-ergonomics, as CI does ([checks.yml](.github/workflows/checks.yml)). Fix every error and every warning, or say in one line why a warning is false.
