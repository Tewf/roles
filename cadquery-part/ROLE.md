---
name: cadquery-part
description: Builds a parametric solid with CadQuery in this machine's cad venv, exports STEP and STL, and proves it by reading the files back; a program judges the result.
role:
  autonomy: acts on a scratch folder; the person keeps the part
  verification: tested
  unit-of-proof: clean runs of the reference pipeline judged by a program, each counted pass or fail, with the Wilson interval; five faults the judge must refuse
  judge: ~/.venvs/cad/bin/python cadquery-part/judge.py OUTDIR
  statement: cadquery-part/reliability.md
---

# cadquery-part

CadQuery is installed in one place here, `~/.venvs/cad`, and a script that is judged by its own exit code can pass with a broken solid. This role makes the checks the CAD work of this machine learned a procedure with a judge. Its level is `tested`, and its proof follows [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md).

## What it does

Given parameters, it builds one solid and leaves `part.step`, `part.stl` and `params.json` in a scratch folder. The reference pipeline is a 40 by 30 by 6 mm plate with an 8 mm through-hole, [reference_part.py](reference_part.py).

## Procedure

1. Run with `~/.venvs/cad/bin/python`. Never install CadQuery into conda `base` or the system Python.
2. Write the numbers in the program, not in the model's text: the volume, the heights and the radii come from `params.json`, and the judge recomputes the volume from it. In the route study, 0 of 25 first attempts of small and medium models passed when the model wrote both the code and the numbers.
3. Export STEP for the solid and STL for the mesh, both from the same `Workplane`.
4. Measure a wall from face to face (`BRepExtrema_DistShapeShape` on two faces), never from sampled vertices. The first checker read a wall of w as w times the square root of 2 at the corners and rejected good bottles.
5. Disarm any `signal.alarm` in a `finally`: one checker left its alarm armed and killed the process that called it.
6. Run `~/.venvs/cad/bin/python cadquery-part/judge.py OUTDIR`. The role has passed only when it prints `pass`.

## What it must not do

- Trust the script that wrote the file: the judge re-imports the STEP and reads the STL.
- Let a model do the arithmetic of a shape it will be judged on.
- Run a long boolean on the whole card or a recording: CadQuery is CPU only, but the machine runs hot.

## Not covered

- That the part is the right design, or that a given process can make it. The bottle's targets are a vendor page's, not a glassmaker's standard, and live in the `cadpipe` of the Design repository.
- Assemblies, drawings, and any format other than STEP and STL.
