<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Ok I will use the geocalib node. Give me a prompt to give to claude code to write a comfyui custom node to convert from the output of the geocalib node to a fspy json format.

Here’s a prompt you can paste into Claude to get a solid ComfyUI node implementation:

***

I want you to write a ComfyUI custom node in Python.

Goal:
Take the output of a GeoCalib node (single-image camera calibration) and convert it to an fSpy-compatible JSON string (same structure as a `.fspy` file) so I can save it and import it in Blender via the fSpy importer.

Assumptions and inputs:

- I already have a node in the graph that runs GeoCalib and outputs a Python dict (or JSON-like object) with at least:
    - `image_width` (int, pixels)
    - `image_height` (int, pixels)
    - `focal_length_px` (float, focal length in pixels)
    - `principal_point_x` (float, pixels)
    - `principal_point_y` (float, pixels)
    - `R` (3×3 rotation matrix as nested list or flat list of 9 floats, row-major)
- If you need to choose exact key names, **define them clearly** in the node’s INPUT_TYPES and assume the upstream GeoCalib node can be adapted. For example, assume the GeoCalib node outputs a dict like:

```python
{
    "width": 1920,
    "height": 1080,
    "fx": 1500.0,
    "fy": 1500.0,
    "cx": 960.0,
    "cy": 540.0,
    "R": [[r11, r12, r13],
          [r21, r22, r23],
          [r31, r32, r33]]
}
```

- The node should **not** call GeoCalib itself, just accept this dict as an input from another node.

Target fSpy JSON format:

Use the standard fSpy JSON format that Blender’s fSpy importer expects. Base the structure on fSpy’s exported JSON files, something like:

```json
{
  "version": 1,
  "imageWidth": 1920,
  "imageHeight": 1080,
  "camera": {
    "focalLength": 35.0,
    "focalLengthPx": 1500.0,
    "sensorWidth": 36.0,
    "sensorHeight": 20.25,
    "principalPoint": [960.0, 540.0],
    "position": [0.0, 0.0, 0.0],
    "rotation": [
      [r11, r12, r13],
      [r21, r22, r23],
      [r31, r32, r33]
    ]
  },
  "transformOrientation": "Y_UP"
}
```

Notes:

- Use focal length in **pixels** directly from GeoCalib for `focalLengthPx`.
- For `focalLength` in millimeters and sensor size, choose reasonable defaults and derive one from the other so they’re consistent:
    - Assume a default 36mm sensor width.
    - Compute `focalLength` in mm from `focalLengthPx` as
`f_mm = focalLengthPx * sensorWidth_mm / imageWidth_px`.
    - Compute `sensorHeight` from the aspect ratio:
`sensorHeight_mm = sensorWidth_mm * imageHeight_px / imageWidth_px`.
- `principalPoint` is `[cx, cy]` from GeoCalib.
- Use the provided rotation matrix `R` directly in the JSON, in row-major order, as a 3×3 array named `rotation`.
- Set `position` to `[0, 0, 0]` and `transformOrientation` to `"Y_UP"` as defaults.
- Add any minimal other fields that fSpy usually includes, but keep the JSON lean and focused on what the importer needs to reconstruct the camera.

ComfyUI node requirements:

- Put everything in a single Python file, e.g. `geocalib_to_fspy.py`.
- Implement as a standard ComfyUI node class with:
    - `CATEGORY` set to `"GeoCalib"`
    - `INPUT_TYPES` that accept:
        - a `DICT` or `STRING` input for the GeoCalib result:
            - option 1: `geocalib_data` (type `"DICT"`) containing the dict above
            - option 2: `geocalib_json` (type `"STRING"`) and parse JSON
    - `RETURN_TYPES` = (`"STRING"`,)
    - `RETURN_NAMES` = (`"fspy_json"`,)
    - `FUNCTION` pointing to your processing method.
- The node’s function should:

1. Read the GeoCalib data from the input.
2. Extract width, height, fx, cx, cy, and R.
3. Compute `focalLength`, `sensorWidth`, `sensorHeight` as described.
4. Build a Python dict that matches the fSpy JSON structure.
5. Serialize it with `json.dumps(..., indent=4)` and return the string.
- At the bottom of the file, define `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS` properly so ComfyUI detects the node:

```python
NODE_CLASS_MAPPINGS = {
    "GeoCalibToFSpy": GeoCalibToFSpy,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeoCalibToFSpy": "GeoCalib → fSpy JSON",
}
```


What I want from you:

1. The complete, ready-to-drop-in Python file content for this node.
2. Robust handling of:
    - Missing keys with clear exceptions.
    - Both nested-list and flat-list 3×3 matrices for `R`.
3. Inline comments where the fSpy-specific structure is built, so I can tweak field names if needed.

Output only the Python code (no explanations), so I can paste it directly into a file.
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^2][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://github.com/cvg/geocalib

[^2]: https://arxiv.org/html/2409.06704v2

[^3]: https://pix4d.github.io/opf-spec/specification/calibrated_cameras.html

[^4]: https://community.opendronemap.org/t/how-to-use-opencv-camera-calibration-xlm-parameters-in-odm-as-cameras-json-input/12912

[^5]: https://camera-calibrator.com/blogs/blog/json-output-values-from-calibration-software

[^6]: https://www.youtube.com/watch?v=7pgDrQzThH0

[^7]: https://www.reddit.com/r/comfyui/comments/18wp6oj/tutorial_create_a_custom_node_in_5_minutes/

[^8]: https://solarframework.github.io/use/tools/

[^9]: https://www.youtube.com/watch?v=TMKmSsAj1jQ

[^10]: https://aayushgarg.dev/posts/2025-09-10-build-custom-comfyui-node.html

[^11]: https://docs.nvidia.com/drive/driveworks-3.5/dwx_calibration_graph_cli.html

[^12]: https://discourse.mcneel.com/t/fspy-camera-importer/87072

[^13]: https://docs.comfy.org/custom-nodes/walkthrough

[^14]: https://www.iis.fraunhofer.de/content/dam/iis/de/doc/profil/zukunftsinitiativen/künstliche-intelligenz/dsai/2022/Camorph A Toolbox for Conversion between Camera Parameter Conventions.pdf

[^15]: https://devforum.roblox.com/t/using-fspy-to-camera-match-images-to-help-building/3132390

