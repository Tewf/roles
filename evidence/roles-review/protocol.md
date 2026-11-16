# Protocol: how the pool was built

A first pass, run on 2026-11-16 by one reviewer (a Claude model, with a Mistral model for the first reading of abstracts). Terms are in [frame](frame.md).

**Shape:** [protocol](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/protocol.md)

## 1. Why grey literature

Garousi's seven questions: one yes suggests including grey sources.

| Question | Answer |
|---|---|
| Is there a lack of volume or quality in the formal literature on this point? | yes: the roles, skills and servers of the frameworks live in repositories and specifications before they reach a paper |
| Is the context important in the outcome? | yes: a role is defined by the framework that runs it |
| Is the goal to corroborate science with practice? | yes: whether any framework ships a reliability proof is read in its repository |
| Is the subject new, with practice ahead of research? | yes: the Agent Skills format dates from late 2025 and the first formal papers on it from 2026 |
| Does practice need guidance from research? | yes: a package is served with no statement of how reliable it is |

## 2. Questions

- Q1 What is a role: how do the frameworks define it, name it and package it?
- Q2 How is autonomy graded, and which systems close the loop of finding a problem, proposing a solution and finishing it?
- Q3 What counts as a proof of reliability for an agent, and which kinds could be pinned to a package?
- Q4 What does coordination between agents add and cost, and where must a check sit?
- Q5 How are roles and skills packaged and served, and is there a tool role per piece of software?

## 3. Existing reviews

- Found: surveys of LLM multi-agent systems (Guo 2024, Wang 2024b, He 2025), a survey of agent skills (Xu 2026), a survey of the Model Context Protocol (Hou 2025). The family holds a review of coordination between agents, [multi-agent-teams](https://github.com/Tewf/ai-augmented-agents/blob/8a05e7eb88a41cfb53c8188fc9faacac94e79d02/evidence/multi-agent-teams/review.md), which this review does not redo.
- Not found: a review that joins roles, autonomy and a proof of reliability in one question (strings F3, F6, F10, F11, O9, O10).

## 4. Formal search

Counts are of 2026-11-16. No key and no identity was sent to either service.

- Databases: arXiv (search_query, sorted by relevance) and OpenAlex (title and abstract, sorted by citations).
- The first three strings used `all:`, which ORs the terms. They were kept and not screened.
- The scripts are in `search/`: `search.py`, `forward.py` and `lookup.py`.
- The log of the results screened is `search/log.csv`, with one row per result and the concepts it carries.
- A concept is a closed-list slug assigned by the reviewer from the title and, where read, the abstract.

| Id | String as run | Count | New concept |
|---|---|---|---|
| F0a | arXiv: `all:LLM-based multi-agent systems survey` | 1010072 | not run: `all:` ORs the terms, 10^6 results; none screened |
| F0b | arXiv: `all:role-playing agents software development standard operating procedures` | 1041982 | not run: same fault; none screened |
| F0c | arXiv: `all:levels of autonomy AI agents framework` | 743044 | not run: same fault; none screened |
| F1 | arXiv: `abs:"multi-agent" AND abs:"large language model" AND ti:survey` | 59 | nnyyynnnnn |
| F2 | arXiv: `abs:"standard operating procedures" AND abs:"agents" AND abs:"language model"` | 26 | yyyynnny |
| F3 | arXiv: `ti:"levels of autonomy" OR ti:"autonomy levels" AND abs:"agents"` | 7 | yyynnnn |
| F4 | arXiv: `ti:"multi-agent" AND ti:fail AND abs:"language model"` | 5 | nnyny |
| F5 | arXiv: `abs:"software development" AND abs:"role" AND abs:"multi-agent" AND abs:"language model"` | 21 | ynnnnnnn |
| F6 | arXiv: `abs:"reliability" AND abs:"agents" AND (abs:"pass^k" OR abs:"consistency across trials")` | 26 | ynnnnyny |
| F7 | arXiv: `abs:"Lean" AND abs:"agent" AND abs:"proof" AND abs:"language model" AND ti:verif*` | 15 | yyynnnnn |
| F8 | arXiv: `abs:"error amplification" AND abs:"agents"` | 8 | nnnynnnn |
| F9 | arXiv: `abs:"Model Context Protocol" AND (ti:survey OR ti:landscape OR ti:security)` | 74 | ynnnnnnn |
| F10 | arXiv: `abs:"agent skills" AND abs:"language model" AND abs:"packag*"` | 26 | yynynnnn |
| F11 | arXiv: `abs:"safety case" AND abs:"AI" AND abs:"argument"` | 19 | ynnnnnyn |
| F12 | arXiv: `ti:"scientist" AND abs:"autonomous" AND abs:"language model" AND abs:"discovery"` | 18 | ynynynnn |
| F13 | arXiv: `abs:"evaluator" AND abs:"program search" AND abs:"language model" AND abs:"mathematical discoveries"` | 0 | no result |
| F14 | arXiv: `abs:"LLM-Modulo" OR (abs:"verifier" AND abs:"language models cannot plan")` | 9 | yynynnnn |
| O1 | OpenAlex: `"Agent2Agent" OR "agent card" OR "A2A protocol"` | 262 | yynnn |
| O2 | OpenAlex: `"Agent Skills" "language model" skill package` | 48 | yynnyn |
| O3 | OpenAlex: `"Blender" "Model Context Protocol" OR "Godot" "Model Context Protocol" OR "Unity" "Model Context Protocol"` | 30 | ynnnn |
| O4 | OpenAlex: `"confidence interval" "agent" "success rate" "language model" evaluation statistical` | 1 | n |
| O5 | OpenAlex: `"conformal" "language model agents" guarantee` | 2 | yn |
| O6 | OpenAlex: `"formal verification" "multi-agent" "language model" "guarantee"` | 10 | nnny |
| O7 | OpenAlex: `"agent" "assurance" OR "certification" "language model" "trustworthy autonomous" role` | 7128 | nnnnnnnn |
| O8 | OpenAlex: `"role-playing" "persona" "language model" "does not improve" OR "helpful assistant"` | 128 | nn |
| O9 | OpenAlex: `"agent skills" "formal verification"` | 1 | y |
| O10 | OpenAlex: `"LLM agents" "reliability" "certificate"` | 4 | nyn |
| O11 | OpenAlex: `"multi-agent" "role" "language model" "Lean 4"` | 1 | n |
| O12 | OpenAlex: `"autonomous" "closed-loop" "problem finding" "language model" "mathematics"` | 0 | no result |
| B1 | OpenAlex: `cites MetaGPT, then "reliability OR verification OR proof OR guarantee"` | 596 | nynnnnnn |
| B2 | OpenAlex: `cites MetaGPT, then "survey OR taxonomy OR systematic"` | 469 | nnnnnnn |
| B3 | OpenAlex: `cites MetaGPT, then "autonomy levels OR levels of autonomy OR fully autonomous"` | 62 | ynnny |
| B4 | OpenAlex: `cites MetaGPT, then "role specialization" OR "roles" AND "standard operating"` | 17 | nnnny |
| B6 | OpenAlex: `cites Kim 2025, then "certificate OR guarantee OR formal OR proof OR verified"` | 59 | nynnnnnn |
| B7 | OpenAlex: `cites Cemri 2025, then "formal OR certificate OR guarantee OR proof OR lean"` | 25 | nyyynnnnn |
| B8 | OpenAlex: `"agent" "skills" "formal verification" OR "proof" OR "certified" "package"` | 906587 | not run: operators ignored, count meaningless; none screened |
| B9 | OpenAlex: `"certified" OR "certification" "LLM agents" reliability "statistical guarantee" OR "confidence bound"` | 251943 | not run: operators ignored, count meaningless; none screened |
| R1 | OpenAlex: `"role-playing" "language model" agents society` | 11 | nynnn |
| R2 | OpenAlex: `"SKILL.md" agent skills` | 104 | nynynn |
| R3 | OpenAlex: `"Model Context Protocol" servers tools` | 868 | nnynnn |
| R4 | OpenAlex: `"levels of autonomy" agents` | 268 | ynnynn |
| R5 | OpenAlex: `"pass^k" reliability agent` | 27 | nnynnn |
| R6 | OpenAlex: `"safety case" agents` | 120 | nnynnn |
| R7 | OpenAlex: `"Lean 4" autoformalization agent` | 13 | ynynnn |
| R8 | OpenAlex: `"software company" "multi-agent" "language model" roles` | 1 | y |
| R9 | OpenAlex: `"evolutionary" "program search" "language model" discovery` | 11 | nnnnnn |
| R10 | OpenAlex: `"autonomous" "scientific discovery" agent "language model" end-to-end` | 45 | nynnnn |

B5 is not used: it was a title lookup, moved to the named leads below. The rows of F1 to F14, the named leads and the first rows of the O and B strings were logged in the order seen. The rows of O4, O7, O11 and the later rows of the B strings were added afterwards. Their letters are computed in file order, not in the order of reading.

Named leads are not strings. They were looked up by title on OpenAlex on 2026-11-16, and are these:

- Systems: MetaGPT, ChatDev, CAMEL, AutoGen, AgentVerse, SWE-agent, OpenHands, Voyager, Self-collaboration.
- Evaluation and failures: AI Agents That Matter, Why Do Multi-Agent LLM Systems Fail, Towards a Science of Scaling Agent Systems.
- Autonomy and discovery: The AI Scientist, FunSearch, AlphaEvolve, Levels of Automation (Parasuraman 2000).
- Proof: Proof-carrying code, Lean Copilot, Personas in system prompts.

Agentless and the Anthropic text on building agents returned no work on OpenAlex and are not cited.

## 5. Grey search

Repositories and specifications were read on 2026-11-16 through the GitHub API. For each: the README, and the folder of roles where there is one. The code was scanned with GitHub code search for six terms, 7 seconds apart: `lean4`, `wilson`, `"confidence interval"`, `"formal verification"`, `"autonomy level"` and `"standard operating procedure"`. The raw counts are in `search/absence.tsv`.

| Id | Producer or engine | String or what was read | Result | New concept |
|---|---|---|---|---|
| G1 | FoundationAgents/MetaGPT | README, `metagpt/roles/`, scan of six terms, `aflow/convergence_utils.py` | screened 1, included | not recorded |
| G2 | OpenBMB/ChatDev | README, scan of six terms | screened 1, included | not recorded |
| G3 | camel-ai/camel | README, scan of six terms, the files that hold `reliability` | screened 1, included | not recorded |
| G4 | crewAIInc/crewAI | README, scan of six terms | screened 1, included | not recorded |
| G5 | microsoft/autogen | README, scan of six terms | screened 1, included | not recorded |
| G6 | OpenHands/OpenHands | README, scan of six terms | screened 1, included | not recorded |
| G7 | modelcontextprotocol/modelcontextprotocol | README | screened 1, included | not recorded |
| G8 | a2aproject/A2A | README, the Agent Card passages | screened 1, included | not recorded |
| G9 | agentskills/agentskills, anthropics/skills | READMEs, the `SKILL.md` layout | screened 2, included | not recorded |
| G10 | ahujasid/mcp-for-blender (formerly blender-mcp) | README | screened 1, included | not recorded |
| G11 | Coding-Solo/godot-mcp | README | screened 1, included | not recorded |
| G12 | CoplayDev/unity-mcp | README | screened 1, included | not recorded |
| G13 | enclawed/enclawed-oss (and its archived mirror metereconsulting/enclawed) | README, scan of four terms, the files that hold `wilson` and `"confidence interval"` | screened 2, included | not recorded |

## 6. Stopping rule

- Stated in the job's brief before the search: the stopping estimator's line must end on `stop`, or the review says the coverage reached. The family's rule k = 5 leaves a string after five results with no new concept.
- Result: the estimator ended on `keep searching`, at coverage 0.79 against the target 0.95, after 40 strings and 255 results, 236 from strings and 19 from named leads (`search/log.csv`). The review stops under an effort bound, not on saturation. Each of the five questions was searched with at least two names (the field's name, the acronym or the author). The forward citations were run for MetaGPT, Kim 2025 and Cemri 2025, and the repositories were read. What the coverage of 0.79 leaves out is discussed in section 10.

## 7. Selection

- Include: a work or repository that defines or packages a role, a skill or a server, or grades autonomy. Also one that closes a loop from problem to result, or states a proof of reliability, a verification or a failure rate of agents.
- Exclude: work on one domain's agent with no general claim, and works from before 2022 except named foundations. Security papers on MCP and skills are excluded too, apart from the ones that set the verification level of a skill (kept for position).
- A work is cited only when its abstract or text was read in this pass, or marked located only.

## 8. Quality of grey sources

Garousi's 20 criteria in eight groups (authority 4, methodology 6, objectivity 4, date 1, position 1, novelty 2, impact 1, outlet 1); the threshold is 10 of 20. Scores are in [sources](sources.md), given by one reviewer.

## 9. Extraction and synthesis

- Abstracts of 54 works were fetched from OpenAlex and read. Two more came back empty: Xi 2025 and a survey of agents in software engineering.
- A first extraction of kind, role mechanism, autonomy and reliability evidence went to a Mistral model (`mistral-small-latest`, 38 abstracts). Its output was coarse, most cells reading "partial". No finding rests on it: each figure was read again in the abstract and is marked (secondary).
- Two papers were read in the text: Kim 2025 (introduction and section 6, for the error figures) and Metere 2026b (sections 1, 8 and 12, for the scope of the proof).
- Repositories: the figures are counts of files returned by GitHub code search, which indexes the default branch only and skips large files. A zero is a statement about that search.
- The synthesis follows the five questions; evidence against goes to [against](against.md).

## 10. Not searched, and limits

- Not searched: Google Scholar, Semantic Scholar, DBLP, the ACL Anthology and the ACM digital library directly. Also the forums and blogs of practitioners, Devin and other closed products, and the documentation sites of the frameworks beyond their READMEs. The code of the frameworks was not read beyond the scan above.
- Not recorded: the New concept cells of G1 to G13 say `not recorded`, because a repository was read as a whole and no result list was lettered.
- Limits: one reviewer, no second rater. The arXiv API throttled the requests (HTTP 429) during the session, so the title lookups and abstracts of the second half went through OpenAlex. The concept list is open and wide. Of 81 concepts, 43 were seen once, mostly tail topics (MCP security, skill supply chains, benchmarks of one domain). That is why the estimator's coverage stays at 0.79 although the core questions were searched twice. A second pass restricted to the core concepts would raise it; it was not run. The abstract of Xi 2025 could not be retrieved, so that survey is located only. OpenAlex dates some works a year after their arXiv date; keys follow the first public version where known.
