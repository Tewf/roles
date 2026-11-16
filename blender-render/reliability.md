# blender-render: reliability statement

The reliability statement of [blender-render](ROLE.md). **Status (2026-11-16):** the reference pipeline ran twice from an empty folder and a program judged both `pass`; four faults given to the judge were all refused. This counts the pipeline and the judge. It does not say how often a model writes a passing scene from the procedure.

## The claim

Run as written, the reference pipeline leaves a PNG with a size and an MP4 of two video frames, and the Blender it ran on reports the NVIDIA card. [judge.py](judge.py) decides, and refuses a script that uses a name Blender 5.x removed.

## The statistic

| What | Count | Wilson 95% interval |
|---|---|---|
| clean runs of the pipeline, judged `pass` | 2 of 2 | 0.34 to 1.00 |
| faults refused by the judge | 4 of 4 | 0.51 to 1.00 |

Verdicts, one per run and per fault, are in [trial-1/scores.json](trial-1/scores.json). The four faults: a script using `.sequences`, one using `Action.fcurves`, one naming FFMPEG before `media_type`, and a result with no clip.

## The sample

- Run on 2026-11-16 on Blender 5.2.0 LTS, a Wayland session, an RTX 4060 Laptop GPU with 13 MiB of the card in use before the trial.
- Each run starts from an empty folder, takes about 2 s, and is started by `python3 blender-render/trial.py`.

## A measurement that corrected the notes

The machine's notes say that `__NV_PRIME_RENDER_OFFLOAD` and `__GLX_VENDOR_LIBRARY_NAME` put a background Blender on the discrete GPU. Today they do not. One frame at 1920 by 1080 and 256 EEVEE samples, `trial` of 2026-11-16:

| Launch | Renderer reported | Seconds |
|---|---|---|
| no variable | Mesa Intel(R) Graphics (ADL GT2), OpenGL | 18.37 |
| the two GLX variables | Mesa Intel(R) Graphics (ADL GT2), OpenGL | 18.37 |
| `--gpu-backend vulkan` and the Vulkan variable | NVIDIA GeForce RTX 4060 Laptop GPU, Vulkan | 5.15 |

So the role names the Vulkan line, and its judge asks a background Blender for its renderer instead of trusting the environment. The command `studio`, which sets only the GLX variables, is not changed by this role.

## What this does and does not show

- **Shows:** the steps run and are judged on this machine, and the judge refuses the four faults it was given.
- **Does not show a rate.** With 2 runs the interval runs from 0.34 to 1.00, on one machine and one day.
- **Does not show a gain over the single agent.** No arm without the procedure was run.
- **Not covered:** the look of the picture, Cycles, the MCP route.

## To rerun

```bash
python3 blender-render/trial.py --runs 2
```
