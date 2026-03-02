"""Simple CLI to run detection and measurement.

Usage examples:
  python -m detect_towers.cli detect --image img.jpg --model yolov8n.pt --save-dir runs/detect
  python -m detect_towers.cli measure --image img.jpg --model yolov8n.pt --meters-per-pixel 0.2
"""
import argparse
import json
from pathlib import Path

from .detect import detect
from .measure import measure_bboxes, compute_scale_from_known_object, estimate_height_from_shadow


def cmd_detect(args):
    dets = detect(args.image, model=args.model, conf=args.conf, save=True, save_dir=args.save_dir)
    out_path = Path(args.save_dir) / "detections.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(dets, f, indent=2)
    print(f"Wrote {len(dets)} detections to {out_path}")


def cmd_measure(args):
    dets = detect(args.image, model=args.model, conf=args.conf, save=False)
    if args.meters_per_pixel is None:
        print("meters-per-pixel is required for measurement. Either pass --meters-per-pixel or compute it from a known object.")
        return
    measured = measure_bboxes(dets, args.meters_per_pixel)
    print(json.dumps(measured, indent=2))


def main():
    p = argparse.ArgumentParser(prog="detect_towers")
    sub = p.add_subparsers(dest="cmd")

    pd = sub.add_parser("detect")
    pd.add_argument("--image", required=True)
    pd.add_argument("--model", default="yolov8n.pt")
    pd.add_argument("--conf", type=float, default=0.25)
    pd.add_argument("--save-dir", default="runs/detect")
    pd.set_defaults(func=cmd_detect)

    pm = sub.add_parser("measure")
    pm.add_argument("--image", required=True)
    pm.add_argument("--model", default="yolov8n.pt")
    pm.add_argument("--conf", type=float, default=0.25)
    pm.add_argument("--meters-per-pixel", type=float, default=None)
    pm.set_defaults(func=cmd_measure)

    args = p.parse_args()
    if not hasattr(args, "func"):
        p.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
