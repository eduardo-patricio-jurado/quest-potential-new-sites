"""Detection utilities using Ultralytics YOLO.

Functions:
- detect: run detection on a single image and return parsed bounding boxes.
"""
from typing import List, Optional, Dict
import os

try:
    from ultralytics import YOLO
except Exception as e:
    YOLO = None

import numpy as np


def detect(image_path: str, model: str = "yolov8n.pt", conf: float = 0.25, classes: Optional[List[int]] = None, save: bool = True, save_dir: str = "runs/detect") -> List[Dict]:
    """Run YOLO detection on a single image.

    Returns a list of detections with keys: `label`, `confidence`, `x1,y1,x2,y2`, `w`,`h`, `area_px`.
    If Ultralytics is not installed, raises ImportError.
    """
    if YOLO is None:
        raise ImportError("Ultralytics YOLO not available. Install via `pip install ultralytics`.")

    os.makedirs(save_dir, exist_ok=True)
    model_obj = YOLO(model)
    results = model_obj.predict(source=image_path, conf=conf, save=save, save_dir=save_dir, classes=classes)

    parsed = []
    # results is a list-like (one per image)
    for r in results:
        boxes = getattr(r, "boxes", None)
        names = getattr(r, "names", {})
        if boxes is None:
            continue
        # boxes.xyxy, boxes.conf, boxes.cls
        xyxy = boxes.xyxy.cpu().numpy() if hasattr(boxes.xyxy, "cpu") else np.array(boxes.xyxy)
        confs = boxes.conf.cpu().numpy() if hasattr(boxes.conf, "cpu") else np.array(boxes.conf)
        cls = boxes.cls.cpu().numpy() if hasattr(boxes.cls, "cpu") else np.array(boxes.cls)

        for (x1, y1, x2, y2), c, ci in zip(xyxy, confs, cls):
            w = float(x2 - x1)
            h = float(y2 - y1)
            parsed.append({
                "label": names.get(int(ci), str(int(ci))),
                "confidence": float(c),
                "x1": float(x1),
                "y1": float(y1),
                "x2": float(x2),
                "y2": float(y2),
                "w": w,
                "h": h,
                "area_px": w * h,
            })

    return parsed
