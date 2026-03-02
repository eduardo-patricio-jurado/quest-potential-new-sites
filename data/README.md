Satellite tower detection (prototype)

Small Python toolkit to run object detection on satellite/Google Earth images to detect and measure cell towers and billboard towers.

Key ideas:
- Use a pre-trained YOLO model (Ultralytics) for detection; fine-tune on labeled samples for better accuracy.
- Provide measurement helpers that convert pixel sizes to meters using a user-supplied scale or a known reference object.

Files of interest:
- `requirements.txt` — Python dependencies
- `src/detect_towers/` — detection and measurement modules
- `src/detect_towers/cli.py` — simple command-line wrapper

Quick start
1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run detection on an image (saves annotated image to `runs/detect`):

```bash
python -m detect_towers.cli detect --image path/to/image.jpg --model yolov8n.pt --save-dir runs/detect
```

3. Convert detections to real-world sizes by providing `--meters-per-pixel`:

```bash
python -m detect_towers.cli measure --image path/to/image.jpg --model yolov8n.pt --meters-per-pixel 0.2
```

Notes & next steps:
- For accurate meters-per-pixel you can compute scale from a known object visible in the image using `compute_scale_from_known_object`.
- For automated satellite downloads consider integrating Google Earth Engine or manual exports from Google Earth Pro.
