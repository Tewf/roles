# Against

The evidence against what the brief assumes, and the disagreements among the sources. Sources are in [review](review.md). None is deleted to make roles look stronger.

**Shape:** [against](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/against.md)

## Against "a role is a project made fully autonomous"

- Autonomy has a cost that coordination does not repay by default. No architecture was statistically separable in aggregate over 13 SOPs. The coordinated designs spent 1.4 to 4.7 times the tokens for gains "usually small and rarely significant" (Nandi 2026, abstract, secondary). Measured. The single agent is the efficient default there.
- Above a capability ceiling more agents hurt. Tasks where a single agent already exceeds 45% accuracy had negative returns from additional agents. The change ranged from +80.8% to -70.0% with the task (Kim 2025, introduction). Measured.
- The first step of autonomy, finding the problem, is the weakest. LLM self-evaluation failed and ideas lacked diversity (Si 2024, abstract, secondary). Agentic AI scientists "are not built for autonomous scientific discovery" (Bisht 2026, abstract, secondary). Measured for the first, convention for the second.
- A fully autonomous loop was shown on a handful of cases (an open problem in Ju 2026, one paper in Feng 2026, one workshop paper in Yamada 2025). One case is a demonstration, not a rate. Descriptive.

## Against "a role has a defined function that a prompt gives it"

- A persona in a system prompt did not improve accuracy on 2,410 factual questions over 162 roles (Zheng 2024, abstract, secondary). Measured, on factual questions: a role in a collaboration is not the same test.
- Roles that frameworks assign by prompt are not enforced. Prompt-only and enforced teams had indistinguishable pass rates. The prompt-only verifier tried to edit the executor's code 3.6 times more often (Kim 2026a, abstract, secondary). Measured.

## Against "a proof of reliability can be pinned to a package"

- A pass rate depends on the run: single-run pass@1 varied by 2.2 to 6.0 points over 60,000 trajectories, so an improvement of 2 to 3 points may be noise (Bjarnason 2026, abstract, secondary). Measured. A statistic pinned to a package needs its repeated runs and its interval.
- A pass rate depends on the conditions: success fell from 96.9% to 88.1% under small perturbations of the task (Gupta 2026, abstract, secondary). Measured. A package proved on its own tasks is not proved on the user's.
- A formal proof covers a property, not the task. The formal level of a skill proves containment of capabilities. It leaves one residual, the model's freedom to refuse to act, to a runtime check (Metere 2026b, abstract, secondary). Supported with caveat. The same holds for Lean: the kernel checks the proof of the statement given. Two titles of 2026 on autoformalization point at the gap between a statement the kernel accepts and the statement meant. They are SHADOWBENCH and a quality audit "beyond kernel acceptance", titles seen in string R7, not read.
- A hypothesis, not a finding: the proof expires when the model changes. The statistics above are measured per model and harness. Gupta 2026 compared two models. Li 2026 gained from +4.1 to +25.7 points by configuration (abstract, secondary).
- Self-checking does not substitute for an outside check. Language models cannot by themselves plan or verify (Kambhampati 2024, abstract, secondary). A verifier role approved 49% of submissions that failed the deterministic grader (Kim 2026a, abstract, secondary). Measured for the second.

## Disagreements

| Point | One side | Other side |
|---|---|---|
| Does a team of role agents beat one agent? | MetaGPT reports more coherent solutions than chat-based systems on its tasks (Hong 2023, abstract, secondary) | no architecture separable in aggregate, single agent efficient (Nandi 2026); negative returns above 45% single-agent accuracy (Kim 2025) |
| Does a verifier or central check help? | centralised validation contains error amplification from 17.2 to 4.4 times (Kim 2025) | a verifier role approved 49% of failing submissions and removing it raised the partial score (Kim 2026a) |
| Does a role prompt help? | role-playing guides agents toward task completion (Li 2023, abstract, secondary) | no gain from personas on factual questions (Zheng 2024) |
| Do skills help? | +16.6 points in pass rate with curated skills (Li 2026) | gains of 5.7 points with high-quality skills and a loss with degraded skills (Nandi 2026); 91.8% of public skills have a defect (Zhang 2026) |

- A possible reason for the first two splits: the benchmarks differ in task structure (decomposable against sequential), and Kim 2025 shows that the sign of the multi-agent effect depends on it. A possible reason for the third: the tasks differ, dialogue and cooperation against factual recall. A possible reason for the fourth: the effect of a skill depends on its quality, which Nandi 2026 varied on purpose. These are hypotheses.
- On the verifier: the validation bottleneck of Kim 2025 may be a program or a design with defined checks, and the verifier role of Kim 2026a a model that is asked to judge. The abstracts do not say, so this is a hypothesis to read in the texts.

## Against the sources themselves

- Of 54 formal works, 48 were read from the abstract only, and 4 were only located; two were read in part of the text. A figure from an abstract is secondary.
- Most are preprints of 2026 with few citations, many under 20 on OpenAlex. Several come from one group: Kim 2025 and Kim 2026a share a first author. Metere 2026a and 2026b have one author, and their code sits in one project.
- The system papers (MetaGPT, ChatDev, CAMEL, AutoGen, AgentVerse) report gains on their own tasks; none is an independent replication.
- The repository scan is a count of files that GitHub code search returns for a term. A zero rules out the term in the indexed files, not the idea under another name, and the scan did not read the code of each framework beyond the READMEs and the files found.
- The model that did the first reading of abstracts was coarse, and no figure rests on it.
- The review has one reviewer and no second rater.
