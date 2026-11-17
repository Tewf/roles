# 0001: A role is defined by the proof it carries

**Decision:** The word role is kept. The first lines of the front page define it as an autonomous AI-augmented project with a proof of reliability, which tells it apart from a persona and from a skill.

**Status:** proposed, 2026-11-16, for the maintainer to accept or change. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/030e4f21a151dca21366dc98923e6285f5f6e5ba/shapes/decision-record.md).

## Context

- The review's frame finds that the field uses role for a persona in a prompt (Li 2023) and for a position in a team with an SOP (Hong 2023). The first has no measured gain on factual questions (Zheng 2024).
- The field's closest word for what the maintainer means is a skill with a verification level above `tested` (Metere 2026a, Metere 2026b).
- The review finds no source that gives such a package a task-success proof, so the word that names it has no competing meaning to collide with beyond the two above.

## Decision

- Keep the repository name `roles`.
- State the definition once, on the front page, and link it from the review's frame.
- Say plainly on the front page that the field's nearest name is a verified skill, so a reader who searches for that finds this.

## Consequences

- **Good:** the name the maintainer uses everywhere stays, and its meaning is checked by the proof it carries.
- **Bad:** a reader who knows role as persona may expect a prompt. The first lines of the front page answer that.
- If the manifest later extends the `SKILL.md` format, the repository may be renamed to say so. That is a new record.

## See also

- [position](../evidence/roles-review/position.md), what the shapes must decide.
- [frame](../evidence/roles-review/frame.md), the section on whether the name matches.
