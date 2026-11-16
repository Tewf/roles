---
name: godot-web-build
description: Exports a Godot 4.7 project to the Web on this machine and proves the build by the files on disk, never by a log; a program judges the result.
role:
  autonomy: acts on a copy of the project; the person keeps the build
  verification: tested
  unit-of-proof: clean runs of the starter's export judged by a program, each counted pass or fail, with the Wilson interval; four faults the judge must refuse
  judge: python3 godot-web-build/judge.py PROJECT
  statement: godot-web-build/reliability.md
---

# godot-web-build

Godot 4.7.1 here has three traps that fail without an error, and the game-development notes of this machine name them. This role makes those notes a procedure with a judge. Its level is `tested`, and its proof follows [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## What it does

Given a Godot 4.7 project written in GDScript, it exports the `Web` preset and leaves `build/web/` with `index.html`, `index.js`, `index.wasm` and `index.pck`.

## Procedure

1. Copy the project to a working folder. Never export in the original.
2. Write in GDScript. C# has no Web export in the standard build installed here, and the C# skill was removed on purpose.
3. Start from the starter, `~/Desktop/GameDev/projects/starter`, and keep its two scripts, `export-builds.sh` and `serve-web-build.py`. Each fixes a trap, and the first is the one this role runs.
4. Run `bash ./export-builds.sh Web` from a real terminal, not a VS Code snap terminal: the snap moves Godot's data folder, so it finds no export templates. The script creates the export folder, which Godot does not, and claims success only when a file exists.
5. Launch Godot through `~/.local/bin/godot`, the wrapper that exports the three discrete-GPU variables. A symlink there moves the editor to the Intel iGPU with no error.
6. Run `python3 godot-web-build/judge.py PROJECT`. The role has passed only when it prints `pass`.

## What it must not do

- Declare success from a missing error word. One earlier script printed `ok` for three presets while `build/` was empty, because `pipefail` and `grep -q` inverted the test.
- Put a non-commercial asset in the build (MMS-TTS is CC-BY-NC): the licence of an asset is read by a person.
- Run a generation or a 3D scene at the same time, or while a lecture records: the card has 8 GB.

## Not covered

- That the game runs in a browser: `webapp-testing` drives the build.
- The Linux and Windows presets: the starter's script exports them, this role judges Web only.
- Publishing to itch.io.
