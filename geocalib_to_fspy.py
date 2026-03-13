import json
from typing import Union, List, Dict, Any


class GeoCalibToFSpy:
    """
    Converts GeoCalib camera calibration output to fSpy JSON format.
    Takes camera calibration data (intrinsics and extrinsics) and converts it
    to the fSpy JSON format for use with Blender's fSpy importer.
    """

    CATEGORY = "GeoCalib"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("fspy_json",)
    FUNCTION = "convert_to_fspy"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "geocalib_data": ("DICT",),
            },
            "optional": {
                "sensor_width_mm": ("FLOAT", {"default": 36.0, "min": 0.1, "max": 100.0, "step": 0.1}),
                "transform_orientation": ("STRING", {"default": "Y_UP"}),
            }
        }

    def convert_to_fspy(self, geocalib_data: Dict[str, Any], sensor_width_mm: float = 36.0, transform_orientation: str = "Y_UP") -> tuple:
        """
        Convert GeoCalib camera calibration to fSpy JSON format.

        Args:
            geocalib_data: Dictionary containing GeoCalib output with keys:
                - width: image width in pixels
                - height: image height in pixels
                - fx: focal length in pixels (x-axis)
                - fy: focal length in pixels (y-axis) [optional, uses fx if not present]
                - cx: principal point x in pixels
                - cy: principal point y in pixels
                - R: 3x3 rotation matrix (list of lists or flat list of 9 values)
            sensor_width_mm: Sensor width in millimeters (default: 36.0)
            transform_orientation: Coordinate system orientation (default: "Y_UP")

        Returns:
            Tuple containing the fSpy JSON string.

        Raises:
            KeyError: If required keys are missing from geocalib_data.
            ValueError: If data types or shapes are invalid.
        """
        # Extract required fields
        try:
            image_width = int(geocalib_data["width"])
            image_height = int(geocalib_data["height"])
            fx = float(geocalib_data["fx"])
            fy = float(geocalib_data.get("fy", fx))  # Use fx if fy not provided
            cx = float(geocalib_data["cx"])
            cy = float(geocalib_data["cy"])
            R = geocalib_data["R"]
        except KeyError as e:
            raise KeyError(f"Missing required key in geocalib_data: {e}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid data type in geocalib_data: {e}")

        # Parse rotation matrix (handle both nested list and flat list formats)
        rotation_matrix = self._parse_rotation_matrix(R)

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
    def _parse_rotation_matrix(R: Union[List[List[float]], List[float]]) -> List[List[float]]:
        """
        Parse rotation matrix from either nested list or flat list format.

        Args:
            R: Rotation matrix as either:
                - Nested list: [[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]]
                - Flat list: [r11, r12, r13, r21, r22, r23, r31, r32, r33]

        Returns:
            Rotation matrix as nested list of lists.

        Raises:
            ValueError: If matrix shape or size is invalid.
        """
        try:
            # Check if it's a nested list (list of lists)
            if isinstance(R, list) and len(R) == 3 and all(isinstance(row, list) for row in R):
                # Verify each row has 3 elements
                if all(len(row) == 3 for row in R):
                    # Convert all values to float
                    return [[float(val) for val in row] for row in R]

            # Check if it's a flat list of 9 elements
            if isinstance(R, list) and len(R) == 9:
                R_float = [float(val) for val in R]
                # Reshape to 3x3 (row-major)
                return [
                    [R_float[0], R_float[1], R_float[2]],
                    [R_float[3], R_float[4], R_float[5]],
                    [R_float[6], R_float[7], R_float[8]],
                ]

            raise ValueError(f"Rotation matrix must be 3x3 nested list or flat list of 9 values, got: {R}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to parse rotation matrix: {e}")


# ComfyUI node registration
NODE_CLASS_MAPPINGS = {
    "GeoCalibToFSpy": GeoCalibToFSpy,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeoCalibToFSpy": "GeoCalib → fSpy JSON",
}
