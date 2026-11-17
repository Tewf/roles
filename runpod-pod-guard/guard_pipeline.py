#!/usr/bin/env python3
"""The reference pipeline of the runpod-pod-guard role: everything a rented pod needs before it exists, with no pod and no spend.

    python3 guard_pipeline.py OUTDIR

Writes OUTDIR/version.txt, datacenters.json, guard_id.txt, guard_armed.txt, guard_after.txt, state_before.txt and state_after.txt.
It asks runpodctl for its version and the datacenter catalogue (read-only), arms the studio's cost guard (a transient
systemd user timer) on a made-up pod id, reads the unit back, disarms it, and records whether the studio's pod state moved.
It never calls `pod create`: the deadline is the trap that costs money (neither the MCP nor runpodctl 2.12.0 has a terminate-after).
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

MODULES = Path(os.environ.get("STUDIO_MODULES") or Path(shutil.which("studio") or "studio").resolve().parent / "modules")  # beside the `studio` launcher
STATE = Path.home() / ".local/state/studio/pod.json"


def sh(*args: str) -> str:
    done = subprocess.run(args, capture_output=True, text=True, timeout=60)
    return done.stdout


def state_hash() -> str:
    return hashlib.sha256(STATE.read_bytes()).hexdigest() if STATE.is_file() else "absent"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: guard_pipeline.py OUTDIR")
        return 2
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(MODULES))
    import pod  # the studio's own code: the guard under test is the one `studio pod up` arms
    (out / "version.txt").write_text(sh("runpodctl", "--version"), encoding="utf-8")
    (out / "datacenters.json").write_text(sh("runpodctl", "datacenter", "list", "--output", "json"), encoding="utf-8")
    (out / "state_before.txt").write_text(state_hash() + "\n", encoding="utf-8")
    fake = f"judge{os.getpid()}"
    (out / "guard_id.txt").write_text(fake + "\n", encoding="utf-8")
    deadline = pod._arm_guard(fake, 1)
    unit = pod._guard_unit(fake)
    (out / "guard_armed.txt").write_text(sh("systemctl", "--user", "cat", unit + ".timer", unit + ".service") if deadline else "", encoding="utf-8")
    pod._disarm_guard(fake)
    (out / "guard_after.txt").write_text(sh("systemctl", "--user", "list-units", unit + ".*", "--all", "--no-legend"), encoding="utf-8")
    (out / "state_after.txt").write_text(state_hash() + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
