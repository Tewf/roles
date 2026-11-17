---
name: unity-batch-build
description: Creates and drives a Unity 6 project in batch mode from an empty folder with the editor installed here, and proves it by the scene and version files it leaves; a program judges the result.
role:
  autonomy: acts on a scratch project it deletes afterwards; the person keeps the files the judge reads
  verification: tested
  unit-of-proof: clean runs of the reference pipeline judged by a program, each counted pass or fail, with the Wilson interval; five faults the judge must refuse
  judge: python3 unity-batch-build/judge.py OUTDIR
  statement: unity-batch-build/reliability.md
---

# unity-batch-build

Unity is proprietary, and the open options (Godot, MuJoCo) do the job when they can; this role is for the work that needs the Unity editor, such as Unity ML-Agents. Its level is `tested`, and its proof follows [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## What it does

With the editor at `~/Unity/Hub/Editor/6000.6.9f1`, it creates a project with `-createProject`, adds one editor method, runs it with `-executeMethod`, and leaves `smoke.json`, `Smoke.unity`, `ProjectVersion.txt` and the exit code. The method builds a scene with one cube. No network is needed for this run.

## Procedure

1. Start the editor with `-batchmode -nographics -quit`, and give `-logFile` a path, so the log can be read after the run by a person.
2. Make a project with `-createProject DIR`, then copy the editor script into `DIR/Assets/Editor/`. The method uses `UnityEditor`, which compiles only inside an `Editor` folder.
3. Run the method with the project as the working directory (`-projectPath DIR`), so a relative path in the method lands inside the project.
4. Ask the editor its version with `Unity -version`. The judge compares that string with the one the method wrote and the one in `ProjectVersion.txt`.
5. Delete the scratch project afterwards: the `Library` folder alone is hundreds of megabytes.
6. Use the Unity MCP bridge only on purpose. In batch mode it starts only with `UNITY_MCP_ALLOW_BATCH=1`. Its default transport waits for a server and opens no port; `MCPForUnity.UseHttpTransport=false` selects stdio. It listens on loopback only and sends telemetry unless `UNITY_MCP_DISABLE_TELEMETRY=1`. Its `execute_code` tool runs C# in the editor. Add it to a project by `file:` path from the reviewed clone, never from the network.
7. Run `python3 unity-batch-build/judge.py OUTDIR`. The role has passed only when it prints `pass`.

## What it must not do

- Declare success from the exit code of `Unity` alone, or from a log: the method's own file is the proof.
- Run while a lecture records or a generation holds the card. Start it through `maestro/heavy.py`, since the editor takes the CPU while it imports; both runs finished in under a minute, by their file times.
- Put the editor on a project that is not a scratch copy without the person's go.

## Not covered

- A build for a player (Windows, Linux, WebGL), and the licence terms: the free Student plan gives the Pro editor while enrolled.
- Package resolution from the registry, which needs the network.
- Unity ML-Agents training, which has its own env, `mlagents`.
