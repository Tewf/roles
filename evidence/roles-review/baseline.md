# Baseline

Step 5 of the review: the baseline the work is compared against. Evidence is in [review](review.md).

**Shape:** [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/baseline.md)

## B1: a role as MetaGPT, ChatDev and CAMEL define it, with no reliability statement

1. A role is a function given to an agent by a prompt and a procedure. MetaGPT encodes an SOP in prompt sequences (Hong 2023). ChatDev uses a chat chain with communicative dehallucination (Qian 2023). CAMEL uses a role-playing prompt with inception prompting (Li 2023).
2. It is run inside the framework that defines it, with roles specified by prompts and not enforced (Kim 2026a).
3. It is judged by a pass rate from a single run on the framework's own tasks (Bjarnason 2026). It ships no Lean file, no interval and no reference list. The scan of the three repositories found no file for `lean4`, `"formal verification"` or `"autonomy level"`.
4. It is not served: it lives in the framework's process, and a package form exists only where the framework adopts `SKILL.md` or an MCP wrapper.

The nearest neighbour to beat on the proof, kept apart from B1: **B2, a skill with a verification level** (Metere 2026a, Metere 2026b), which proves capability containment and not task success.

## Compared with what the review found

| Item | In B1 | Fit |
|---|---|---|
| a function with a named procedure | yes: SOP, chat chain or role-play prompt | matches |
| the person's role and the level of autonomy stated | none | lacks (Feng 2025; Zheng 2026) |
| a loop from problem to result | the framework's tasks give the problem; software projects are finished, problem finding is not | in part (Si 2024) |
| a statistic on task success with an interval | single-run pass@1 on its own tasks | lacks (Bjarnason 2026; Li 2026) |
| a formal proof of the deterministic part | none | lacks (Ju 2026; Metere 2026b) |
| references for the claims | the papers, not carried with the role | in part |
| a check outside the model before use | a verifier role by prompt | lacks (Kim 2025; Kim 2026a) |
| packaged and served like a tool | not as such | lacks (AgentSkills 2026; MCP 2026) |
| a tool role per software | not part of the frameworks | lacks (Blender-MCP 2026; Godot-MCP 2026; Unity-MCP 2026) |

## What B1 lacks

- A reliability statement that travels with the role: no Lean theorem, no interval, no references in the three repositories (strand 1, scan).
- An outside check at the centre: a model verifier approved 49% of failing submissions (Kim 2026a), and a central validation cut error amplification from 17.2 to 4.4 times (Kim 2025).
- A package and a server: the roles live in frameworks, while skills and MCP servers are the field's served forms (strand 5).
- A level of autonomy that a program reads (Feng 2025).
- A statement of what the role does not cover: the formal level of B2 leaves the model's freedom to refuse (Metere 2026b).

## How it is measured

- The pass rate of a role on N tasks judged by deterministic verifiers, with its Wilson 95% interval. Each task is repeated k times for the pass^k (Yao 2024). The comparator is the single agent without the role on the same tasks (Li 2026; Nandi 2026). The count is made by a program.
- The proof's checks that pass: Lean builds (`lake build`), the interval is computed by a program from the run's log, each reference resolves. A role is served only if all pass.
- The pilot role of the DAG (`f-pilot-role`) measures this on ten repositories.

## The review is finished

The baseline is named, B1 with B2 as the neighbour to beat on the proof, and the next work is the `Tewf/roles` repository and the pilot role.
