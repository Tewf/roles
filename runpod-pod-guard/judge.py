#!/usr/bin/env python3
"""The judge of the runpod-pod-guard role: a program decides whether the cost guard is proved before any pod is rented.

    python3 judge.py OUTDIR

OUTDIR is the folder guard_pipeline.py wrote. It passes when all six hold:
  1. version.txt is the version runpodctl reports now, and it is 2.x;
  2. datacenters.json lists at least one EU- datacenter that has a GPU in its availability: data of clients stays in the EU;
  3. guard_armed.txt shows a transient timer with OnActiveSec=1h whose service runs `runpodctl pod delete <the id>`: a
     deadline that deletes, not stops (a stopped pod still bills for its disk);
  4. systemd, asked now, holds no active unit for that id (the guard of a pod that was never rented is gone: `down` disarms);
  5. guard_after.txt is empty, as recorded by the run;
  6. the studio's pod state is the same before and after: the run rented nothing.
Exit 0 on pass, 1 on fail; the last line is `pass` or `fail: <reason>`.
What it does not decide: that a pod can be created (the key may be refused at GraphQL), what a rental costs, or that the tunnel works.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def judge(out: Path) -> str:
    names = ("version.txt", "datacenters.json", "guard_id.txt", "guard_armed.txt", "guard_after.txt", "state_before.txt", "state_after.txt")
    for name in names:
        if not (out / name).is_file():
            return f"fail: {name} is missing: the pipeline did not finish"
    version = (out / "version.txt").read_text(encoding="utf-8").strip()
    live = subprocess.run(["runpodctl", "--version"], capture_output=True, text=True).stdout.strip()
    if not version.startswith("runpodctl 2.") or version != live:
        return f"fail: version.txt says `{version}`, runpodctl says `{live}`"
    try:
        centres = json.loads((out / "datacenters.json").read_text(encoding="utf-8"))
    except ValueError:
        return "fail: datacenters.json is not JSON"
    if not any(str(c.get("id", "")).startswith("EU-") and c.get("gpuAvailability") for c in centres):
        return "fail: datacenters.json lists no EU datacenter with a GPU"
    pod_id = (out / "guard_id.txt").read_text(encoding="utf-8").strip()
    armed = (out / "guard_armed.txt").read_text(encoding="utf-8")
    if "OnActiveSec=1h" not in armed:
        return "fail: guard_armed.txt shows no timer with OnActiveSec=1h: no deadline was armed"
    if f'"pod" "delete" "{pod_id}"' not in armed:
        return f"fail: the guard's service does not run `runpodctl pod delete {pod_id}`"
    active = subprocess.run(["systemctl", "--user", "is-active", f"studio-pod-{pod_id}.timer"], capture_output=True, text=True).stdout.strip()
    if active == "active":
        return f"fail: the timer studio-pod-{pod_id} is still active: the guard was not disarmed"
    if (out / "guard_after.txt").read_text(encoding="utf-8").strip():
        return "fail: guard_after.txt still lists a unit for the pod id"
    if (out / "state_before.txt").read_text(encoding="utf-8") != (out / "state_after.txt").read_text(encoding="utf-8"):
        return "fail: the studio's pod state changed during the run: something was rented"
    return "pass"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: judge.py OUTDIR")
        return 2
    verdict = judge(Path(sys.argv[1]))
    print(verdict)
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
