# 0002: The pilot role extends SKILL.md and is judged by a program

**Decision:** The first role, `doc-editor`, is a folder with a `ROLE.md` whose front matter is a `SKILL.md` front matter plus a `role` table, a program that judges the result, and a `reliability.md` that holds the statistic.

**Status:** proposed, 2026-11-16, for the maintainer to accept or change. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/030e4f21a151dca21366dc98923e6285f5f6e5ba/shapes/decision-record.md).

## Context

- The review's position leaves the manifest open: extend `SKILL.md` and the verification levels of Metere 2026a, or state its own ([position](../evidence/roles-review/position.md), "What the shapes must decide").
- The unit of proof was proposed as a pass rate with a Wilson interval over N tasks, against the single agent without the role.
- The check at the centre must be a program, not a model: a model as verifier approved 49% of failing submissions (Kim 2026a, as held by the review).

## Decision

- `ROLE.md` keeps the `name` and `description` fields of a skill, so any reader of skills can load it, and adds a `role` table: `autonomy`, `verification`, `unit-of-proof`, `judge`, `statement`.
- The verification level is `tested` until a Lean file backs a part of the role. The word follows Metere 2026a's four levels: unverified, declared, tested, formal.
- The judge is a Python file that runs the standard's own checks and three more tests (no file removed, no non-Markdown file changed, every number, address and code span kept). The agent never declares success.
- The first trial seeds faults into copies of ten repositories: a benchmark, not a field observation.

## Consequences

- **Good:** a skill-aware tool can load the role, and the statement is checkable by running one command.
- **Bad:** seeded faults measure repair of what the checks name, not how often real documentation breaks. The statistic says so in its first lines.
- A manifest that needs more than a table in the front matter is a new record.

## See also

- [ROLE.md](../doc-editor/ROLE.md) and [reliability.md](../doc-editor/reliability.md).
- [decision 0001](0001-a-role-is-defined-by-its-proof.md), what a role is.
