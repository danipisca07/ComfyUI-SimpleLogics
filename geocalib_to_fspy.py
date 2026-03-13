import json
import math
from typing import Union, List, Dict, Any


class GeoCalibToFSpy:
    """
    Converts GeoCalib camera calibration output to fSpy JSON format.
    Takes camera calibration data from the GeoCalib Estimator node outputs
    and converts it to the fSpy JSON format for use with Blender's fSpy importer.
    """

    CATEGORY = "GeoCalib"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("fspy_json",)
    FUNCTION = "convert_to_fspy"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_width": ("INT", {"default": 1920, "min": 1, "max": 65536}),
                "image_height": ("INT", {"default": 1080, "min": 1, "max": 65536}),
                "focal_length_px": ("FLOAT", {"default": 1500.0, "min": 0.1}),
                "principal_point_x": ("FLOAT", {"default": 960.0, "min": -10000.0, "max": 10000.0}),
                "principal_point_y": ("FLOAT", {"default": 540.0, "min": -10000.0, "max": 10000.0}),
                "roll": ("FLOAT", {"default": 0.0, "min": -180.0, "max": 180.0}),
                "pitch": ("FLOAT", {"default": 0.0, "min": -180.0, "max": 180.0}),
                "yaw": ("FLOAT", {"default": 0.0, "min": -180.0, "max": 180.0}),
            },
            "optional": {
                "sensor_width_mm": ("FLOAT", {"default": 36.0, "min": 0.1, "max": 100.0, "step": 0.1}),
                "transform_orientation": ("STRING", {"default": "Y_UP"}),
            }
        }

    def convert_to_fspy(
        self,
        image_width: int,
        image_height: int,
        focal_length_px: float,
        principal_point_x: float,
        principal_point_y: float,
        roll: float,
        pitch: float,
        yaw: float,
        sensor_width_mm: float = 36.0,
        transform_orientation: str = "Y_UP",
    ) -> tuple:
        """
        Convert GeoCalib camera calibration parameters to fSpy JSON format.

        Args:
            image_width: Image width in pixels
            image_height: Image height in pixels
            focal_length_px: Focal length in pixels
            principal_point_x: Principal point X coordinate in pixels
            principal_point_y: Principal point Y coordinate in pixels
            roll: Camera roll rotation in degrees (Z-axis)
            pitch: Camera pitch rotation in degrees (X-axis)
            yaw: Camera yaw rotation in degrees (Y-axis)
            sensor_width_mm: Sensor width in millimeters (default: 36.0)
            transform_orientation: Coordinate system orientation (default: "Y_UP")

        Returns:
            Tuple containing the fSpy JSON string.
        """
        try:
            image_width = int(image_width)
            image_height = int(image_height)
            fx = float(focal_length_px)
            cx = float(principal_point_x)
            cy = float(principal_point_y)
            roll_deg = float(roll)
            pitch_deg = float(pitch)
            yaw_deg = float(yaw)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid input data types: {e}")

        # Convert rotation angles from degrees to radians
        roll_rad = math.radians(roll_deg)
        pitch_rad = math.radians(pitch_deg)
        yaw_rad = math.radians(yaw_deg)

        # Build rotation matrix from Euler angles (ZXY order: roll, pitch, yaw)
        # This corresponds to rotations around Z, X, Y axes respectively
        rotation_matrix = self._euler_to_rotation_matrix(roll_rad, pitch_rad, yaw_rad)

        # Compute focal length in millimeters
        # f_mm = f_px * sensor_width_mm / image_width_px
        focal_length_mm = (fx * sensor_width_mm) / image_width

        # Compute sensor height from aspect ratio
        # sensor_height = sensor_width * image_height / image_width
        sensor_height_mm = (sensor_width_mm * image_height) / image_width

        # Build fSpy JSON structure
        fspy_dict = {
            "version": 1,
            "imageWidth": image_width,
            "imageHeight": image_height,
            "camera": {
                "focalLength": focal_length_mm,
                "focalLengthPx": fx,
                "sensorWidth": sensor_width_mm,
                "sensorHeight": sensor_height_mm,
                "principalPoint": [cx, cy],
                "position": [0.0, 0.0, 0.0],
                "rotation": rotation_matrix,
            },
            "transformOrientation": transform_orientation,
        }

        # Serialize to JSON string with indentation
        fspy_json = json.dumps(fspy_dict, indent=4)
        return (fspy_json,)

    @staticmethod
    def _euler_to_rotation_matrix(roll: float, pitch: float, yaw: float) -> List[List[float]]:
        """
        Convert Euler angles (roll, pitch, yaw) to a 3x3 rotation matrix.
        Uses ZXY rotation order (roll around Z, pitch around X, yaw around Y).

        Args:
            roll: Rotation around Z-axis in radians
            pitch: Rotation around X-axis in radians
            yaw: Rotation around Y-axis in radians

        Returns:
            3x3 rotation matrix as nested list of lists.
        """
        # Precompute sin and cos values
        cr = math.cos(roll)
        sr = math.sin(roll)
        cp = math.cos(pitch)
        sp = math.sin(pitch)
        cy = math.cos(yaw)
        sy = math.sin(yaw)

        # Rotation matrix from ZXY Euler angles
        # R = Rz(roll) * Rx(pitch) * Ry(yaw)
        R = [
            [cy * cr - sy * sp * sr, -sy * cp, cy * sr + sy * sp * cr],
            [sy * cr + cy * sp * sr, cy * cp, sy * sr - cy * sp * cr],
            [-cp * sr, sp, cp * cr],
        ]

        return R


# ComfyUI node registration
NODE_CLASS_MAPPINGS = {
    "GeoCalibToFSpy": GeoCalibToFSpy,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeoCalibToFSpy": "GeoCalib → fSpy JSON",
}
