# 0003: A tool role is proved by its pipeline and its judge

**Decision:** A tool role (Blender, Godot) states its reliability as a count: the clean runs of the tool's own pipeline that a program judged `pass`, with the Wilson interval. It adds the faults its judge must refuse.

**Status:** proposed, 2026-11-16, for the maintainer to accept or change. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics/blob/030e4f21a151dca21366dc98923e6285f5f6e5ba/shapes/decision-record.md).

## Context

- [Decision 0002](0002-the-pilot-role-extends-skill-md-and-is-judged-by-a-program.md) gave the first role a pass rate over N repositories against the same model without the procedure.
- A tool role holds knowledge that a machine's notes carry: which flag, which order of calls, which trap fails silently. The notes can be stale, and the procedure is useless if its first command no longer works.
- On 2026-11-16 the notes said that two GLX variables put a background Blender on the discrete GPU; a run showed they do not in Blender 5.2, and the Vulkan backend does (see [reliability.md](../blender-render/reliability.md)).

## Decision

- A tool role keeps the `ROLE.md` shape of 0002 (`SKILL.md` front matter plus a `role` table), a `judge.py` that reads files and asks the tool itself, a `trial.py`, and a `reliability.md`.
- Its statistic is `passed of N` clean runs of the reference pipeline, from an empty folder, each judged by the program, and `caught of M` faults the judge must refuse. Both carry the Wilson 95% interval.
- The judge asks the tool, never the environment or a log: for Blender the renderer string of a background run, for Godot the files of `build/web`.
- The statement says that it measures the pipeline and the judge, not a model that follows the procedure. Measuring the model is the pilot's design and a later trial.

## Consequences

- **Good:** a stale note fails the trial the day it goes stale, as the offload recipe did.
- **Bad:** two runs give an interval of 0.34 to 1.00. The statement is a smoke test with a proof of its judge, not a rate. More runs are cheap, and a procedure written by a model needs the arms of 0002.
- The verification level stays `tested`: no Lean file backs a tool role.

## See also

- [blender-render](../blender-render/ROLE.md) and [godot-web-build](../godot-web-build/ROLE.md).
- [decision 0001](0001-a-role-is-defined-by-its-proof.md), what a role is.
