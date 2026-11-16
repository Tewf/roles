"""The reference pipeline of the blender-render role: one lit cube, one still, one two-frame clip.

    __NV_PRIME_RENDER_OFFLOAD=1 __VK_LAYER_NV_optimus=NVIDIA_only \
      blender --background --gpu-backend vulkan --python render_smoke.py -- OUTDIR

Writes OUTDIR/still.png and OUTDIR/clip.mp4. Written for Blender 5.x: the moves that 4.x code gets wrong are marked 5.x.
"""
import sys
from pathlib import Path

import bpy

out = Path(sys.argv[sys.argv.index("--") + 1])
out.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 160, 90
scene.render.fps = 12
scene.frame_start, scene.frame_end = 1, 2

bpy.ops.mesh.primitive_cube_add(size=1.5)
cube = bpy.context.object
bpy.ops.object.light_add(type="SUN", location=(2, -2, 4))
bpy.ops.object.camera_add(location=(3, -3, 2.2), rotation=(1.1, 0, 0.785))
scene.camera = bpy.context.object

# A move between the two frames, set through the object, never through Action.fcurves (removed in 5.x).
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert("rotation_euler", frame=1)
cube.rotation_euler = (0, 0, 0.8)
cube.keyframe_insert("rotation_euler", frame=2)

# Flat colour for 2D artwork would need view_transform = "Standard"; this lit scene keeps the default.
scene.render.image_settings.media_type = "IMAGE"        # 5.x: set the media type first when going back to stills
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(out / "still")
scene.frame_set(1)
bpy.ops.render.render(write_still=True)
Path(out / "still.png").exists() or Path(str(out / "still") + ".png").rename(out / "still.png")

scene.render.image_settings.media_type = "VIDEO"        # 5.x: FFMPEG raises unless this comes first
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.filepath = str(out / "clip")
bpy.ops.render.render(animation=True)
clips = list(out.glob("clip*.mp4"))
clips and clips[0].rename(out / "clip.mp4")
