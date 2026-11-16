# Roles

[![Checks against reader-ergonomics](https://github.com/Tewf/roles/actions/workflows/checks.yml/badge.svg)](https://github.com/Tewf/roles/actions/workflows/checks.yml)
[![Site](https://github.com/Tewf/roles/actions/workflows/pages.yml/badge.svg)](https://tewf.github.io/roles/)

A **role** is an AI-augmented project made fully autonomous, with a proof of reliability, and packaged to be served like a tool server.

- The project has maths as its backbone, algorithmics as its engine and a model as its heuristic.
- It finds or receives its problem, proposes a solution and finishes it.
- Its proof is a Lean file, a statistic with its sample, or a reference.
- A role extends a skill. A skill is a packaged procedure. A role is a procedure that also answers for how often it works.

> **Status (2026-11-16):** the literature review is written and ends on a named baseline, B1. No role is published yet; the first one, a documentation editor, is the next job. The name is kept for now: the field's closest word for the same thing is a skill with a verification level above `tested`. This is not an official standard, not a peer-reviewed study and not a new result.
>
> **How it is made:** with Claude, an AI assistant by Anthropic, under the maintainer's direction, the way reader-ergonomics was made. Corrections are welcome as issues.

## What the review found

- No framework among MetaGPT, ChatDev, CAMEL, AutoGen, CrewAI and OpenHands ships a statement of reliability with its roles. The scan of their code found no file for `lean4`, `"formal verification"` or `"autonomy level"`.
- The nearest work gives a skill a verification level, from unverified to formal. What its formal level proves is that the skill stays inside the capabilities it declares, not that it does its task (Metere 2026b).
- What the searches did not find is a **task-success proof** attached to a package that is served. It would hold a Lean theorem for the part that is mathematics, a success rate with its interval over N tasks, and references.
- Some roles cannot be fully automated yet: finding the problem is the weak step (Si 2024; Bisht 2026).

## Scope

| In | Out, and where it lives |
|---|---|
| the definition of a role and its reliability statement | coordination between agents: [multi-agent-teams](https://github.com/Tewf/ai-augmented-agents/blob/8a05e7eb88a41cfb53c8188fc9faacac94e79d02/evidence/multi-agent-teams/README.md) |
| the manifest of a role, and how it is served | the tool servers themselves, one per piece of software (Blender and Godot first), each its own project |
| the standard roles, and the form of a role specific to one company | a company's own instance: its repository |

## Contents

| Folder | Holds |
|---|---|
| [evidence/](evidence/README.md) | the literature review: frame, protocol, sources, review, against, state of the art, position, baseline, references |
| [decisions/](decisions/README.md) | one record per choice that shapes the repository |
| [AGENTS.md](AGENTS.md) | the rules for changing this repository |

## What comes next

- The pilot role, a documentation editor, measured as a pass rate with its Wilson interval over ten repositories, against the single agent without the role.
- The manifest: whether it extends the `SKILL.md` format and its verification levels, and where the autonomy level and the proof fields go (see [position](evidence/roles-review/position.md)).
