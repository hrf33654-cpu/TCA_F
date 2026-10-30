# TCA · 探索样板

Project memory for AI assistants (read by Godot Forge). Keep it short and current.

## Game
- Genre / pitch: 
- Core loop: 

## Conventions
- Scenes in res://scenes, scripts next to their scene, assets in res://assets.
- Typed GDScript, signals up / calls down.

## Art & audio
- Style: HD2D with pixel-textured 3D architecture and illustrated alpha-cutout leaf crowns. Warm inn courtyard transitions to cooler woodland. Keep the teal pointed roof and building silhouette.

## Decisions
- 2026-10-27 depth-of-field v4 corrects weak upper blur: closer far-clear thresholds (3.5..6m) and shorter far transitions (10..13m), plus prototype/upper_field_softness.gdshader on CanvasLayer 0. The upper shoulder tapers to zero at y=.34 (overview .28), scales mip blur with resolution, and stays below review UI on layer 1. Mode 0 enables both effects; legacy/off must hide UpperField. v3 evidence is preserved; current validator outputs to research/depth_of_field_v4/.
- 2026-10-27 depth-of-field v3: runtime observer owns a duplicate of the v2 camera attributes. Six profiles in world/maps/lanternbrook_hd2d/depth_profiles.json blend spatially while panning; camera-space focus depth and zoom set the clear band. High-quality circular bokeh, no jitter. D cycles tuned / exact v2 / disabled without moving camera. Keep v2 optics resource as comparison baseline. Evidence: art/lanternbrook_hd2d/research/depth_of_field_v3/; tools/validate_depth_of_field.gd captured 61 images and checked modes, zoom/rotation, pan continuity. Existing renders/ remain texture-v2 evidence.
- 2026-10-27: User chose an Octopath Traveler visual reference, fixed oblique camera and small horizontal rotation. New art preview: scenes/lanternbrook_hd2d_preview.tscn. Do not revert to 360-degree orbit or change the existing world instance transform.
- HD2D observer clamps yaw to base 0.56 radians +/- 12 degrees. User requested lower and longer lens: 20-degree pitch, distance 96, perspective projection, default FOV about 9.53 degrees (effective view size 16). Zoom range 14..27. Original v1 scene remains available as a comparison. No characters or gameplay acceptance yet.
- Complete outdoor map now covers six regions (keys 1..6), including willow river lookout and return loop. Authoritative metadata: world/maps/lanternbrook_hd2d/complete_data.json. Editable source: art/lanternbrook_hd2d/Lanternbrook_HD2D_Complete.blend. See that directory's README for rebuild and evidence.
- Collision masks: walking surfaces layer 1, blocking world layer 2, camera-only distant terrain/water layer 3 (bit 4). Character mask 3, camera mask 5. Never include camera-only terrain in walking navigation. Fine terrain/apron seam is explicitly closed.
- Scene lamps use stable unique names; avoid automatic @ names when adding to loaded legacy scenes, as duplicate serialized names caused orphan lights on reload.
- Material pass v2 uses original generated timber/limestone/groundcover *_handpainted_v2.png (true alpha on groundcover), native authored supporting textures, per-material relief/roughness, map-local weathering, 322 litter patches and slight near/far focus falloff. See art/lanternbrook_hd2d/research/TEXTURE_PASS_V2.md. Do not regenerate these images with Python.
- IMPORTANT: run author_hd2d_pass.gd with the rendering backend, without --headless. Dummy rendering serializes MultiMesh transforms as zero. Pack art partitions only once, after finishing; CACHE_MODE_REPLACE on a live MultiMesh resource also clears its transform data. Texture .import files must generate mipmaps to avoid grain flicker.
