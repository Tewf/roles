---
name: blender-render
description: Renders a still and a short video from a Blender 5.x scene in the background, on the discrete GPU, and proves it with files and a renderer string; a program judges the result.
role:
  autonomy: acts on a scratch folder; the person keeps what it rendered
  verification: tested
  unit-of-proof: clean runs of the reference pipeline judged by a program, each counted pass or fail, with the Wilson interval; four faults the judge must refuse
  judge: python3 blender-render/judge.py SCRIPT OUTDIR
  statement: blender-render/reliability.md
---

# blender-render

The tool role for Blender 5.2, on a laptop whose discrete GPU must be asked for. The machine's Blender notes become a procedure here, with a judge. Level: `tested`. Its proof is a count of judged runs, as [decision 0003](../decisions/0003-a-tool-role-is-proved-by-its-pipeline-and-its-judge.md) sets for a tool role; what a role is, and what the levels mean, is in [decision 0001](../decisions/0001-a-role-is-defined-by-its-proof.md).

## What it does

Given a scene to draw, it writes one Python file for `blender --background`, runs it, and leaves `still.png` and `clip.mp4` in a folder. [render_smoke.py](render_smoke.py) is the reference: one lit cube, one still, a two-frame clip.

## Procedure

1. Write the scene as a Python file that takes the output folder after `--`. Start from [render_smoke.py](render_smoke.py).
2. Use the Blender 5.x names:
   - set `scene.render.image_settings.media_type` to `"VIDEO"` before the file format `"FFMPEG"`, and back to `"IMAGE"` before a still;
   - reach strips through `sequence_editor.strips`, never `.sequences`;
   - set keyframes with `keyframe_insert` on the object, never through `Action.fcurves`;
   - ship an extension with a `blender_manifest.toml`, never a `bl_info` add-on;
   - for flat 2D artwork set `view_settings.view_transform` to `"Standard"`, because the default tone-maps it to washed-out colour.
3. Run it on the discrete GPU:

   ```bash
   __NV_PRIME_RENDER_OFFLOAD=1 __VK_LAYER_NV_optimus=NVIDIA_only \
     blender --background --gpu-backend vulkan --python scene.py -- OUTDIR
   ```

   The GLX variables the machine's notes name leave Blender 5.2 on the Intel iGPU in a background run. The same frame took 18.4 s with and without them, and 5.2 s with the line above ([reliability.md](reliability.md)).
4. Never render while another job holds the GPU: a recording, an image generation, a Cycles render or a local language model.
5. Run `python3 blender-render/judge.py scene.py OUTDIR`. The role has passed only when it prints `pass`.

## What it must not do

- Declare success from a log line. The judge reads the files and a renderer string it fetches itself.
- Write a `.blend` or a render outside the project's own `visuals/` folder, or edit a file it was not given.

## Not covered

- That the picture shows what was asked: no program says so.
- Cycles: it picks its device through its own setting.
- The MCP route (`blender-headless`): a different way to drive the same program.
