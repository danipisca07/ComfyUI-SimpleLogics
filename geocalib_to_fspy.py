import json
import math
from typing import List


class GeoCalibToFSpy:
    """
    Converts GeoCalib Estimator node outputs (roll, pitch, vfov) to a valid
    fSpy JSON calibration file string for import into Blender via the fSpy addon.

    fSpy format reference (from a real exported .fspy file):
      - principalPoint: normalized coords, {x:0, y:0} = image center
      - relativeFocalLength: 0.5 / tan(vfov/2), normalized to half-image-height
      - horizontalFieldOfView / verticalFieldOfView: in radians
      - cameraTransform / viewTransform: 4x4 matrices (camera-to-world and world-to-camera)
      - vanishingPoints: not estimated by GeoCalib, set to null placeholders
    """

    CATEGORY = "GeoCalib"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("fspy_json",)
    FUNCTION = "convert_to_fspy"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Wire directly from Load Image node or primitive
                "image_width": ("INT", {"default": 1920, "min": 1, "max": 65536}),
                "image_height": ("INT", {"default": 1080, "min": 1, "max": 65536}),
                # Wire directly from GeoCalib Estimator outputs
                "roll": ("FLOAT", {"default": 0.0, "min": -180.0, "max": 180.0}),
                "pitch": ("FLOAT", {"default": 0.0, "min": -90.0, "max": 90.0}),
                "vfov": ("FLOAT", {"default": 60.0, "min": 1.0, "max": 179.0}),
            },
        }

    def convert_to_fspy(
        self,
        image_width: int,
        image_height: int,
        roll: float,
        pitch: float,
        vfov: float,
    ) -> tuple:
        image_width = int(image_width)
        image_height = int(image_height)
        roll_rad = math.radians(float(roll))
        pitch_rad = math.radians(float(pitch))
        vfov_rad = math.radians(float(vfov))

        aspect = image_width / image_height

        # Vertical FoV is given; derive horizontal FoV from aspect ratio
        hfov_rad = 2.0 * math.atan(math.tan(vfov_rad / 2.0) * aspect)

        # relativeFocalLength: focal length normalized to half-image-height
        # f_rel = 0.5 / tan(vfov/2)
        relative_focal_length = 0.5 / math.tan(vfov_rad / 2.0)

        # Build the 3x3 rotation matrix from roll and pitch only.
        # GeoCalib does not estimate yaw (heading), so we leave it at 0.
        # Convention: pitch = Rx, roll = Rz  (camera gravity alignment)
        # R = Rx(pitch) * Rz(roll)
        R = _rotation_matrix_xz(pitch_rad, roll_rad)

        # Expand to 4x4 camera-to-world transform (translation = [0,0,0])
        cam_transform = _to_4x4(R)

        # viewTransform is the inverse (world-to-camera) = R^T for pure rotation
        R_T = _transpose3x3(R)
        view_transform = _to_4x4(R_T)

        fspy_dict = {
            # Principal point at image center (normalized: 0,0 = center)
            "principalPoint": {"x": 0.0, "y": 0.0},
            "viewTransform": {"rows": view_transform},
            "cameraTransform": {"rows": cam_transform},
            "horizontalFieldOfView": hfov_rad,
            "verticalFieldOfView": vfov_rad,
            # Vanishing points are not estimated by GeoCalib
            "vanishingPoints": [None, None, None],
            "vanishingPointAxes": ["xPositive", "zNegative", "yPositive"],
            "relativeFocalLength": relative_focal_length,
            "imageWidth": image_width,
            "imageHeight": image_height,
        }

        return (json.dumps(fspy_dict, indent=2),)


def _rotation_matrix_xz(pitch: float, roll: float) -> List[List[float]]:
    """
    Build a 3x3 rotation matrix R = Rx(pitch) * Rz(roll).
    pitch: rotation around X axis (camera tilt up/down)
    roll:  rotation around Z axis (camera tilt left/right)
    """
    cp = math.cos(pitch)
    sp = math.sin(pitch)
    cr = math.cos(roll)
    sr = math.sin(roll)

    # Rx(pitch)
    Rx = [
        [1,   0,   0 ],
        [0,  cp, -sp ],
        [0,  sp,  cp ],
    ]
    # Rz(roll)
    Rz = [
        [ cr, -sr, 0],
        [ sr,  cr, 0],
        [  0,   0, 1],
    ]
    return _matmul3x3(Rx, Rz)


def _matmul3x3(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    return [
        [sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def _transpose3x3(R: List[List[float]]) -> List[List[float]]:
    return [[R[j][i] for j in range(3)] for i in range(3)]


def _to_4x4(R: List[List[float]]) -> List[List[float]]:
    """Embed a 3x3 rotation into a 4x4 homogeneous matrix with zero translation."""
    return [
        [R[0][0], R[0][1], R[0][2], 0.0],
        [R[1][0], R[1][1], R[1][2], 0.0],
        [R[2][0], R[2][1], R[2][2], 0.0],
        [0.0,     0.0,     0.0,     1.0],
    ]


# ComfyUI node registration
NODE_CLASS_MAPPINGS = {
    "GeoCalibToFSpy": GeoCalibToFSpy,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeoCalibToFSpy": "GeoCalib → fSpy JSON",
}
