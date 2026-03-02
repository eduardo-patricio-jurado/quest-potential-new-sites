import cv2
import numpy as np


def detect_towers(image_bytes: bytes) -> dict:
    """Stub for tower detection algorithm.

    Currently returns an empty result; extend with computer vision logic.
    """
    # convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # placeholder logic
    result = {
        "found": False,
        "type": None,
        "estimated_height_m": None,
    }
    return result
