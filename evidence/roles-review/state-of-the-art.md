# State of the art

Step 3 of the review. For each question, the best evidence, kept apart from the practice most adopted. Upper bounds (what was achieved) are kept apart from limits (what was shown not to work). Sources are in [review](review.md).

**Shape:** [state of the art](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/state-of-the-art.md)

## Q1 What is a role, and how is it defined and packaged?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Nandi 2026 | with model and tools fixed, over 13 SOPs the architecture matters less than the quality of the skill and of the implementation | measured |
| Upper bound | Li 2026 | curated skills raised the pass rate from 33.9% to 50.5% over 87 tasks and 18 configurations | measured |
| Limit | Zheng 2024 | a persona in a system prompt gave no gain on 2,410 factual questions | measured |
| Most adopted | Hong 2023 | roles with SOPs in prompts, in a framework with 71,301 stars on 2026-11-16 (MetaGPT 2026) | descriptive |

## Q2 How is autonomy graded, and which systems close the loop?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Si 2024 | a human study of 100+ researchers on the first step, ideas: more novel, slightly less feasible, self-evaluation fails | measured |
| Upper bound | Ju 2026 | an open problem resolved and verified in Lean 4 with essentially no human involvement | descriptive, one case |
| Limit | Bisht 2026 | agentic AI scientists are not built for autonomous discovery; problem selection is the first obstacle | convention |
| Most adopted | Feng 2025 | five levels by the role of the person, with autonomy certificates proposed | convention |

## Q3 What counts as a proof of reliability, and what can be pinned to a package?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Li 2026 | a statistic pinned to a skill: paired pass rate with and without it, deterministic verifiers | measured |
| Upper bound | Metere 2026b | a formal level for a skill: three methods and a proof-carrying bundle for capability containment | supported with caveat |
| Limit | Bjarnason 2026 | a single run is noisy: pass@1 varies by 2.2 to 6.0 points over 60,000 trajectories | measured |
| Limit | Kambhampati 2024 | a language model cannot by itself verify; the verifier is outside | convention |
| Most adopted | Bjarnason 2026 | most papers report a pass@1 from a single run per task | measured |

## Q4 What does coordination add and cost, and where must the check sit?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Kim 2025 | 260 configurations: centralised validation contained error amplification from 17.2 to 4.4 times | measured |
| Upper bound | Kim 2025 | +80.8% against a single agent on a decomposable task | measured |
| Limit | Kim 2026a | a verifier role approved 49% of submissions that failed the deterministic grader | measured |
| Most adopted | Kim 2026a | roles specified by prompts and not enforced | measured, descriptive of practice |

## Q5 How are roles and skills packaged and served, and is there a tool role per software?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Piriyakulkij 2026 | skills invoked as subagents with input-output contracts beat loading them into the context | measured |
| Upper bound | Metere 2026b | a skill bundle that carries its proof and is re-checked at load | supported with caveat |
| Limit | Zhang 2026 | 91.8% of 138,133 public skill files hold at least one defect | measured |
| Most adopted | AgentSkills 2026 | `SKILL.md` folders (195,964 stars for the anthropics/skills repository) and MCP servers, among them Blender (34,652 stars), Unity (16,013) and Godot (6,676) | descriptive |
