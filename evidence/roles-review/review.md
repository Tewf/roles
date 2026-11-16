# Review: six strands

Step 2 of the review, read on 2026-11-16. It groups the 67 sources cited by strand and answers Q1 to Q5 of [frame](frame.md). Surveys first in each strand.

**Shape:** [review](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/review.md)

- Each key is in the [bibliography](references.md).
- Grades are the standard's four: measured, supported with caveat, convention, not supported.
- A figure read in an abstract is marked (secondary). A statement about a repository is a statement about what GitHub code search and the README showed on 2026-11-16.

## Strand 0: existing reviews

- Guo 2024 surveys LLM-based multi-agent systems along their domains and settings, the profiling and communication methods of the agents, and how they develop skills (Guo 2024, abstract, secondary). Descriptive.
- Wang 2024b surveys LLM-based autonomous agents: construction, applications, evaluation (Wang 2024b, abstract, secondary). Descriptive.
- He 2025 reviews multi-agent systems for software engineering and states that specialised agents enable autonomous problem solving and robustness (He 2025, abstract, secondary). Descriptive; the claim is the authors', not a measurement.
- Xu 2026 surveys agent skills on four axes (architecture, acquisition, deployment, security) and reports that 26.1% of community-contributed skills contain vulnerabilities (Xu 2026, abstract, secondary). Descriptive; the figure is quoted from other work.
- Hou 2025 gives the Model Context Protocol a lifecycle of four phases and 16 activities and a threat taxonomy by four attacker types (Hou 2025, abstract, secondary). Descriptive.
- Coordination between agents and delegation are reviewed in the family's [multi-agent-teams](https://github.com/Tewf/ai-augmented-agents/blob/8a05e7eb88a41cfb53c8188fc9faacac94e79d02/evidence/multi-agent-teams/review.md), not redone here.
- No review was found that joins roles, autonomy and a proof of reliability, in these searches (strings F3, F6, F10, F11, O9, O10).

## Strand 1: what a role is, and how it is defined (Q1)

- MetaGPT encodes standard operating procedures into prompt sequences so that agents with human-like expertise verify intermediate results (Hong 2023, abstract, secondary). Its repository holds a folder of roles: product manager, architect, project manager, engineer, QA engineer and others (MetaGPT 2026, `metagpt/roles/`). Descriptive, on the authors' own tasks.
- ChatDev guides specialised agents by a chat chain and by communicative dehallucination (Qian 2023, abstract, secondary). Its version 2.0 is a zero-code platform where a user defines agents, workflows and tasks by configuration (ChatDev 2026, README). Descriptive.
- CAMEL defines a role by role-playing with inception prompting, in a module `camel/societies/role_playing.py` (Li 2023, abstract, secondary; CAMEL 2026, README). Descriptive.
- AutoGen lets the developer define conversation patterns between conversable agents in language or in code (Wu 2023, abstract, secondary). Descriptive.
- A role can be a decision graph: SOP-agent writes the procedure as pseudocode in natural language and represents it as a graph the agent traverses (Ye 2025, abstract, secondary). Descriptive.
- A skill is a unit of executable code kept in a library that grows: Voyager stores and retrieves programs it has written and checked against the environment (Wang 2023, abstract, secondary). Descriptive.
- A persona in a system prompt brings no measured gain: 162 roles, four model families and 2,410 factual questions showed no improvement against no persona (Zheng 2024, abstract, secondary). Measured, on factual questions only.
- With the model and the tools fixed, over 13 enterprise SOPs and four designs in eight arms, no architecture was statistically separable in aggregate. Coordinated arms cost 1.4 to 4.7 times the tokens and 2.6 to 5.8 times the latency of the single agent. High-quality skills lifted success from 67.4% to 73.1% and degraded skills fell below the baseline (Nandi 2026, abstract, secondary). Measured.
- None of the six frameworks read ships a statement of reliability with its roles (MetaGPT 2026; ChatDev 2026; CAMEL 2026; CrewAI 2026; AutoGen 2026; OpenHands 2026, code scan). Descriptive, a run on `search/absence.tsv`.
  - Zero files for `lean4`, for `"formal verification"` and for `"autonomy level"`, in all six repositories.
  - At most one file for `"confidence interval"`, none about a role.
  - One file for `wilson` in three repositories and 56 in CrewAI 2026, whose first six hits are changelog pages.
  - The MetaGPT file for `"confidence interval"` is the convergence test of its workflow optimiser, `aflow/convergence_utils.py`. It stops the search for a better workflow when scores stop moving.
- CrewAI's README calls its platform "reliable" and gives no figure; CAMEL's lists benchmarks for evaluating agents in general (CrewAI 2026, README; CAMEL 2026, README). Descriptive.

## Strand 2: autonomy, and loops that close (Q2)

- Autonomy is graded by the role the person takes. Feng 2025 defines five levels: operator, collaborator, consultant, approver, observer. The level is a design decision separate from capability, and autonomy certificates are proposed for single and multi-agent systems (Feng 2025, abstract, secondary). Convention.
- Zheng 2026 separates the autonomy an agent is allowed from the autonomy it is capable of, with five levels from reactive execution to delegated operational authority (Zheng 2026, abstract, secondary). Convention.
- The older scale of levels of automation across the stages of information acquisition, analysis, decision and action is Parasuraman 2000 (located only, not read).
- The AI Scientist generates ideas, writes code, runs experiments, writes a paper and reviews it (Lu 2024, abstract, secondary). Version 2 produced the first entirely AI-generated workshop paper to pass peer review (Yamada 2025, abstract, secondary). Descriptive, one result.
- A mathematics agent generated a research paper on structure constants in arithmetic geometry with no human intervention. The same report separates this from a human-AI paper and a semi-autonomous evaluation (Feng 2026, abstract, secondary). Descriptive.
- Two agents, one informal and one that formalises, resolved an open problem of commutative algebra and the proof was verified in Lean 4 with essentially no human involvement (Ju 2026, abstract, secondary). Descriptive, one case.
- Program search with an evaluator is the loop closest to maths as the backbone, algorithmics as the engine and a model as the heuristic. AlphaEvolve improves an algorithm by code changes under continuous feedback from evaluators. It reports algorithms it calls provably correct (Novikov 2025, abstract, secondary). FunSearch is its predecessor (Romera-Paredes 2023, located only). Descriptive.
- Finding the problem is the weak link. Over 100 NLP researchers judged LLM-generated ideas more novel than experts' ideas (p < 0.05) and slightly weaker on feasibility, and the study found failures of LLM self-evaluation and little diversity (Si 2024, abstract, secondary). Measured. A position paper adds that problem selection is influenced by the McNamara fallacy (Bisht 2026, abstract, secondary). Convention.

## Strand 3: proofs of reliability, and what can be pinned to a package (Q3)

Formal proof:

- A language model cannot by itself plan or verify; it works as a source of candidates beside external model-based verifiers, in an LLM-Modulo framework (Kambhampati 2024, abstract, secondary). Convention, a position paper.
- Lean checks a proof "leaving no room for hallucination", and Lean Copilot runs model inference inside Lean to build proof tools (Song 2024, abstract, secondary). Descriptive.
- A skill manifest carries a verification level (unverified, declared, tested, formal). The runtime asks a person to approve each irreversible call of an unverified skill and relaxes that as the level rises (Metere 2026a, abstract, secondary). Convention.
- What the top level proves is **capability containment**: the behaviour of a skill stays inside the capabilities its manifest declares. Three methods show it: static analysis over an effect lattice, a refinement type system for tool calls and SMT-bounded model checking. They are bundled in a proof-carrying skill that the runtime re-checks (Metere 2026b, sections 1, 8 and 12). Supported with caveat: three methods and a bundle layout; no evaluation on a set of skills was read in the sections read. It does not prove that the skill does its task, nor how often.

Statistics:

- Pass^k measures reliability over repeated trials, and even gpt-4o-class agents succeed on under half of the tasks of tau-bench (Yao 2024, abstract, secondary). Measured.
- Under semantically equivalent perturbations the success rate fell from 96.9% to 88.1% at intensity 0.2, over 1,280 episodes (Gupta 2026, abstract, secondary). Measured.
- Pass@k, pass^k and the reliability decay curve are projections of one success-time distribution, fitted as an absorbing Markov chain with credible and bootstrap intervals. On seven frameworks the fit was accepted by a two-sample test on 7 of 7 (Tran-Truong 2026, abstract, secondary). Supported with caveat: controlled frameworks, not field traces.
- A single run is a noisy estimate. Over 60,000 trajectories on SWE-Bench-Verified, pass@1 varied by 2.2 to 6.0 points depending on the run chosen. Standard deviations were above 1.5 points at temperature 0 (Bjarnason 2026, abstract, secondary). Measured.
- Benchmarks of agents that report accuracy alone, with no holdout set, make agents fragile and costly (Kapoor 2024, abstract, secondary). Supported with caveat.
- A skill is measured by pairing runs with and without it under deterministic verifiers. Over 87 tasks in eight domains and 18 configurations, curated skills raised the pass rate from 33.9% to 50.5%. Skills with at most three modules beat larger bundles (Li 2026, abstract, secondary). Measured. This is the nearest published form of a reliability statistic pinned to a skill.
- A guarantee on the rate of error of a tool call holds per semantic role of an argument, with a finite-sample bound. The word role there means the part of a call's arguments (recipient, command), not an agent's function (Rahman 2026, abstract, secondary). Supported with caveat.
- Collective certification by a quorum of diverse validator agents cut unsafe approvals from 18.5% to 0.3% on 500 scenarios (He 2026, abstract, secondary). Supported with caveat: simulated scenarios.

Arguments by reference:

- A safety case is a structured argument with four categories (inability, control, trustworthiness, deference to credible advisors) that a system is safe to deploy (Clymer 2024, abstract, secondary). A control safety case rests on a red-team evaluation and three claims about it (Korbak 2025, abstract, secondary). Convention.
- A proof can travel with the code it is about: proof-carrying code is the foundation that Metere 2026b adapts to skills (Necula 1997, located only; Metere 2026b, section 8).
- No source was found that gives a role or a skill a Lean theorem together with a statistic of its task success, in these searches (strings O9, O10, B6, B7).

## Strand 4: error amplification and where the check sits (Q4)

- In a controlled evaluation of 260 configurations, independent agents amplified trace-level errors 17.2 times and centralised coordination contained it to 4.4 times by validation bottlenecks. Relative performance ranged from +80.8% on a decomposable task to -70.0% on sequential planning, and once a single agent exceeds 45% accuracy more agents give negative returns (Kim 2025, introduction). Measured.
- Failures of multi-agent systems fall into 14 modes in three categories: system design, inter-agent misalignment and task verification. They were annotated on more than 1,600 traces of seven frameworks, with an agreement of kappa 0.88 (Cemri 2025, abstract, secondary). Measured.
- Errors solidify into a false consensus by propagating along message dependencies (Xie 2026, abstract, secondary). Uncertainty is lost at the handoff between components and local doubt becomes system-level error (Shi 2026, abstract, secondary). A role-based software pipeline can carry an early hallucination to every later agent (Ogunsusi 2026, abstract, secondary). Supported with caveat, three papers of 2026.
- A verifier role is not a central check. With roles enforced by the operating system, verifiers approved 49% of the submissions that failed the deterministic grader. Removing the verifier improved the mean partial score. Prompt-only and enforced teams had pass rates that were statistically indistinguishable, but prompt-only runs had 3.6 times more cases where the verifier tried to edit the executor's code (Kim 2026a, abstract, secondary). Measured.

## Strand 5: packaging and serving roles (Q5)

- A skill is a folder with a `SKILL.md` that holds a name, a description and instructions, and optionally scripts, references and assets (AgentSkills 2026, README). Specification, first tier.
- MCP standardises how an agent reaches tools and context; A2A governs coordination between agents, discovered by Agent Cards that list capabilities and connection details (Adimulam 2026, abstract, secondary; A2A 2026, README). Convention.
- Skills and MCP complement each other: skills carry procedure, MCP carries access (Xu 2026, abstract, secondary).
- Invoked as subagents with clear input-output contracts, skill packages beat loading their instructions into the main context, at the cost of extra tokens (Piriyakulkij 2026, abstract, secondary). Measured.
- Packaging quality is poor: 91.8% of 138,133 public `SKILL.md` files from 20,556 repositories contain at least one detected defect, mostly weak routing metadata and bloated bodies (Zhang 2026, abstract, secondary). Measured. Skill dependencies are implicit, and a skill alone hides security signals found in its dependencies (Jia 2026, abstract, secondary). Supported with caveat.
- One tool server per piece of software exists already. MCP for Blender has 34,652 stars on 2026-11-16 (Blender-MCP 2026, README, top section). Godot MCP has 6,676 stars and its last push is 2026-04-16 (Godot-MCP 2026, README, top section). Unity MCP has 16,013 stars (Unity-MCP 2026, README, top section). Each exposes editor tools to a model. Descriptive. None of the three READMEs states a success rate or a proof.
- A reliability statement is shipped by a gateway repository in another sense. enclawed-oss reports Wilson intervals in the files of its adversarial test reports. They concern the security properties of the gateway (Enclawed 2026, file paths from code search; content not read). Descriptive.
