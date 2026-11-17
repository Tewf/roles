---
name: comfyui-graph-check
description: Boots ComfyUI on the CPU, reads its version and node schema, validates every studio graph and any new one before a run, and proves it by files; a program judges the result.
role:
  autonomy: starts and stops its own server on port 8189; the person keeps the report
  verification: tested
  unit-of-proof: clean runs of the reference pipeline judged by a program, each counted pass or fail, with the Wilson interval; six faults the judge must refuse
  judge: python3 comfyui-graph-check/judge.py OUTDIR [--graph GRAPH.json]
  statement: comfyui-graph-check/reliability.md
---

# comfyui-graph-check

ComfyUI's website is not the authority on what this install can do; the running server is. This role is the cheap check that asks the server, before a graph spends GPU time. Its level is `tested`, and its proof follows [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## What it does

Starts ComfyUI with `--cpu` on port 8189, so no weight loads, reads `/system_stats` and `/object_info`, runs `studio validate` over the 17 graphs the studio can build, and stops the server. With `--graph` the judge also validates one graph a person or model wrote.

## Procedure

1. Check the port first. A server that finds its port held logs it and exits while `curl` keeps answering from the old one: the same node count, a green report, the wrong build. The pipeline writes `ss` output before it starts, and the judge refuses a folder where the port was held.
2. Start `main.py --cpu --port 8189` from `~/opt/ComfyUI` with the `comfyui` conda env. Never start it on the GPU for a check, and never while Cycles, a lecture recording or a generation holds the 8 GB card.
3. Read the version from `/system_stats` and compare it with `comfyui_version.py`. The judge does.
4. Read the shipped template in `comfyui_workflow_templates_json/templates/` before writing a graph by hand, and write node ids as registered, not as class names: `ReferenceTimbreAudio`, not `ReferenceAudio`.
5. Validate a new graph: `python3 comfyui-graph-check/judge.py OUTDIR --graph graph.json`.
6. Open ComfyUI's page in Firefox, never Brave (`firefox URL`), when a person needs to see it.

## What it must not do

- Trust the docs page over `/object_info`.
- Call a graph valid because the server answered: the answer must come from the server this run started.
- Generate anything: that is the studio's job, and costs the card.

## Not covered

- That a graph draws a good picture, or that its weights are on disk (the report lists the missing ones as notes).
- Generation itself, the RunPod pod and its tunnel.
