"""Training helper using Ultralytics YOLOv8.

This script expects a YOLO-format `data.yaml` that specifies `train`, `val`, and `names`.

Example:
  train: /path/to/images/train
  val: /path/to/images/val
  names: ["cell_tower", "billboard_tower"]

Usage:
  python -m detect_towers.train --data data.yaml --model yolov8n.pt --epochs 100
"""
from typing import Optional
import argparse
import sys
import os

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


def train(data: str, model: str = "yolov8n.pt", epochs: int = 50, imgsz: int = 640, batch: int = 8, project: str = "runs/train", name: str = "exp", lr0: Optional[float] = None):
    """Run a YOLOv8 training job.

    Parameters:
    - data: path to data.yaml
    - model: pretrained model or config (e.g., yolov8n.pt)
    - epochs, imgsz, batch: training hyperparameters
    - project/name: where to save results
    - lr0: initial learning rate (optional)
    """
    if YOLO is None:
        raise ImportError("Ultralytics YOLO not available. Install with `pip install ultralytics`.")

    os.makedirs(project, exist_ok=True)
    model_obj = YOLO(model)
    train_kwargs = {
        "data": data,
        "epochs": int(epochs),
        "imgsz": int(imgsz),
        "batch": int(batch),
        "project": project,
        "name": name,
    }
    if lr0 is not None:
        train_kwargs["lr0"] = float(lr0)

    print("Starting training with:", train_kwargs)
    model_obj.train(**train_kwargs)


def _parse_args(argv):
    p = argparse.ArgumentParser(prog="detect_towers.train")
    p.add_argument("--data", required=True, help="Path to YOLO data.yaml")
    p.add_argument("--model", default="yolov8n.pt", help="Pretrained model or config")
    p.add_argument("--epochs", type=int, default=50)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--project", default="runs/train")
    p.add_argument("--name", default="exp")
    p.add_argument("--lr0", type=float, default=None)
    return p.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    train(data=args.data, model=args.model, epochs=args.epochs, imgsz=args.imgsz, batch=args.batch, project=args.project, name=args.name, lr0=args.lr0)
