---
name: runpod-pod-guard
description: Proves the cost guard and the read-only facts of renting a RunPod GPU before any pod exists, with no pod created and no money spent; a program judges the result.
role:
  autonomy: acts only on a made-up pod id and read-only calls; creates, starts and stops no pod
  verification: tested
  unit-of-proof: clean runs of the guard pipeline judged by a program, each counted pass or fail, with the Wilson interval; six faults the judge must refuse
  judge: python3 runpod-pod-guard/judge.py OUTDIR
  statement: runpod-pod-guard/reliability.md
---

# runpod-pod-guard

A rented pod bills until someone deletes it, and neither the RunPod MCP's `create-pod` nor `runpodctl` 2.12.0 has a terminate-after, though the plugin's documentation says one exists. The only deadline is a transient systemd user timer on this machine that `studio pod up` arms. This role proves that guard, and the catalogue facts a rental depends on, without renting. Its level is `tested`, and its proof follows [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## What it does

Reads `runpodctl --version` and the datacenter catalogue, arms the studio's own guard on a made-up pod id, reads the timer back, disarms it, and records that the studio's pod state did not move.

## Procedure

1. Rent only for a job written down first that beats bought calls on cost or quality. Do not rent to try a model for its own sake.
2. Rent through `studio pod up --hours N`, never through the plugin's `create-pod`, which arms no deadline. When a session does rent through the plugin, that session deletes the pod and logs both times.
3. Pick an EU region. Data of clients stays in the EU.
4. Reach the pod by the SSH tunnel. The proxy URL is public.
5. Delete, never stop: the guard's service runs `runpodctl pod delete`. A stopped pod still bills for its disk.
6. Fetch models on the pod from Hugging Face and check their sha256, never upload them over this line.
7. Run `python3 runpod-pod-guard/judge.py OUTDIR` after `guard_pipeline.py`. The role has passed only when it prints `pass`.

## What it must not do

- Create a pod, start one or call a paid endpoint: this role is the free part of the work.
- Install `runpodctl` with `curl | bash`: the binary here came from the GitHub release with its checksum.
- Spend over the standing limits: 20 euro per account per request (PROVISIONAL); the two clicks that would let `runpodctl` rent again are the person's.
- Read the account balance into a file: the pipeline never calls `runpodctl user`.

## Not covered

- That a pod can be created: the restricted key has GraphQL read only, and whether `pod create` passes under it was never verified.
- What a rental costs, the tunnel, or the models on the pod.
