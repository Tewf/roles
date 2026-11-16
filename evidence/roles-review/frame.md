# Frame: what the field calls a role that carries a proof of reliability

Step 1 of the review, read on 2026-11-16. It states the problem, gives the field's names beside the practitioners', and says whether the repository's name matches. Searches are in [protocol](protocol.md).

**Shape:** [frame](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/frame.md)

## The problem in one sentence

A program finds or receives a problem, proposes a solution and finishes it. How does it carry a proof that it is reliable, so that it can be packaged, named and served to other agents like a tool server?

Terms used below, defined once:

- A **skill** is a packaged procedure that an agent loads on demand.
- A **proof of reliability** is a witness a reader can follow without asking the agent: a Lean file, a statistic with its sample, or a reference.
- An **autonomous project** is one that chooses or receives its problem, proposes a solution and finishes it with no step done by a person.
- A **role** (the maintainer's word) is the extension of a skill. It is an AI-augmented project made fully autonomous, with a proof of reliability. Maths is its backbone, algorithmics its engine and a model its heuristic.

## What the field calls it

| Level | The field's name | First met in |
|---|---|---|
| a function an agent has in a team | **role**, role-based agent; **agent profile** | Li 2023 (role-playing), Hong 2023 (roles with SOPs), Guo 2024 (profiling) |
| the written procedure the role follows | **standard operating procedure**, SOP | Hong 2023; Ye 2025 (SOP as a decision graph) |
| a packaged reusable capability | **agent skill**, `SKILL.md`, skill package | Xu 2026 (survey); AgentSkills 2026 (the specification) |
| how a skill is checked before it is trusted | **verification level** of a skill manifest: unverified, declared, tested, formal | Metere 2026a, Metere 2026b |
| a tool or an agent served over a protocol | **MCP server**, tool server; **Agent Card** of the A2A protocol | Hou 2025; the A2A 2026 |
| how much the agent does alone | **level of autonomy**, level of automation | Parasuraman 2000; Feng 2025 |
| a loop from problem to result with no person | **automated scientific discovery**, AI scientist; **program search with an evaluator** | Lu 2024; Romera-Paredes 2023; Novikov 2025; Feng 2026 |
| a language model beside a verifier | **LLM-Modulo framework** | Kambhampati 2024 |
| reliability of an agent over repeated trials | **pass^k**, reliability decay curve | Yao 2024; Tran-Truong 2026 |
| a structured argument that a system is safe | **safety case** | Clymer 2024 |
| a proof that travels with the code | **proof-carrying code**; proof-carrying skill | Necula 1997; Metere 2026b |
| a guarantee on a rate of error | **conformal risk control** | Rahman 2026 |
| errors growing across agents | **error amplification**, error cascade; failure taxonomy MAST | Kim 2025; Xie 2026; Cemri 2025 |

## What practice calls it

- **Agent**, **crew**, **subagent**: the framework's word for a role with a prompt and tools (CrewAI's `Crews` are "role-based AI agents"; MetaGPT's `metagpt/roles/` holds product manager, architect, engineer and others).
- **Skill**: the packaged procedure; the word of the open Agent Skills format and of the `anthropics/skills` repository.
- **Workflow** and **flow**: a fixed sequence of steps with a model inside; CrewAI's `Flows`, ChatDev 2.0's configured workflows.
- **MCP server**: the word for "a tool you can plug in", used for the tools of Blender (`mcp-for-blender`), Godot (`godot-mcp`) and Unity (`unity-mcp`).
- No practitioner's word for a **role with a reliability proof** was found: the neighbours are "verified skill" (Metere 2026a) and "AI autonomy certificate" (Feng 2025).

## Does the repository's name match?

- In part. **Role** is the field's word for a persona in a prompt (Li 2023) and for a position in a team (Hong 2023). The persona sense has no measured gain (Zheng 2024), and the team sense says nothing about autonomy or proof. The closest field name for what the maintainer means is a **skill with a verification level above `tested`**, served as a tool.
- The finding is stated; the name `Tewf/roles` is not changed here. The maintainer decides, and may keep the word with its own definition, stated in the first lines of the README.

## Sub-questions

| Question | Strand in review.md |
|---|---|
| Q1 What is a role: how do the frameworks define, name and package it? | Strand 1 |
| Q2 How is autonomy graded, and which systems close the loop from problem to result? | Strand 2 |
| Q3 What counts as a proof of reliability for an agent, and which kinds can be pinned to a package? | Strand 3 |
| Q4 What does coordination between agents add and cost, and where must a check sit? | Strand 4 |
| Q5 How are roles and skills packaged and served, and is there a tool role per piece of software? | Strand 5 |

## Held elsewhere

- Coordination between agents, delegation and incentives: [multi-agent-teams](https://github.com/Tewf/ai-augmented-agents/blob/8a05e7eb88a41cfb53c8188fc9faacac94e79d02/evidence/multi-agent-teams/README.md), in the agents repository.
- The company's roles as cards, with their order and their measures: the role-agents design of the AI-augmented company repository.
- The frameworks pass is [frameworks.csv](frameworks.csv). The stopping estimator is that of ai-augmented-data-gathering.
