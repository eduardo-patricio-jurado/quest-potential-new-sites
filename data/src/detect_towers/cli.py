"""Simple CLI to run detection and measurement.

Usage examples:
  python -m detect_towers.cli detect --image img.jpg --model yolov8n.pt --save-dir runs/detect
  python -m detect_towers.cli measure --image img.jpg --model yolov8n.pt --meters-per-pixel 0.2
"""
import argparse
import json
import logging
import sys
from pathlib import Path

from .detect import detect
from .measure import measure_bboxes, compute_scale_from_known_object, estimate_height_from_shadow

# configure simple logging for CLI
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("detect_towers")


def cmd_detect(args):
    try:
        dets = detect(args.image, model=args.model, conf=args.conf, save=True, save_dir=args.save_dir)
        out_path = Path(args.save_dir) / "detections.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(dets, f, indent=2)
        print(f"Wrote {len(dets)} detections to {out_path}")
    except Exception as e:
        logger.exception("detect command failed")
        print(f"Error running detect: {e}", file=sys.stderr)


def cmd_measure(args):
    try:
        dets = detect(args.image, model=args.model, conf=args.conf, save=False)
        if args.meters_per_pixel is None:
            print("meters-per-pixel is required for measurement. Either pass --meters-per-pixel or compute it from a known object.")
            return
        measured = measure_bboxes(dets, args.meters_per_pixel)
        print(json.dumps(measured, indent=2))
    except Exception as e:
        logger.exception("measure command failed")
        print(f"Error running measure: {e}", file=sys.stderr)


def cmd_map(args):
    try:
        from .map import plot_locations
        # auto-detect format
        from .map import load_locations_from_file

        # ensure input exists before proceeding
        if not Path(args.input).exists():
            raise FileNotFoundError(args.input)

        pts = load_locations_from_file(args.input)

        # ensure output directory exists
        out_path = Path(args.output)
        if out_path.parent and not out_path.parent.exists():
            out_path.parent.mkdir(parents=True, exist_ok=True)

        plot_locations(pts, args.output, tiles=args.tiles, attr=args.attr, api_key=args.api_key)
    except FileNotFoundError as e:
        # distinguish between input missing and output directory issues
        logger.exception("map file not found")
        print(f"File not found: {e}", file=sys.stderr)
    except Exception as e:
        logger.exception("map command failed")
        print(f"Error running map: {e}", file=sys.stderr)


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

    # map command to plot latitude/longitude points with radius
    pmap = sub.add_parser("map")
    pmap.add_argument("--input", required=True,
                      help="Path to JSON, CSV, or Excel file with columns lat, lon, radius, optional name")
    pmap.add_argument("--output", default="map.html",
                      help="Output HTML file (uses folium)")
    pmap.add_argument("--tiles", default="OpenStreetMap",
                      help="Tile URL or name (use Google template with key)")
    pmap.add_argument("--attr", default=None,
                      help="Attribution for custom tiles")
    pmap.add_argument("--api-key", default=None,
                      help="API key for tile service if required (e.g. Google)")
    pmap.set_defaults(func=cmd_map)

    args = p.parse_args()
    if not hasattr(args, "func"):
        p.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception in CLI")
        sys.exit(1)
