Satellite tower detection (prototype)

Small Python toolkit to run object detection on satellite/Google Earth images to detect and measure cell towers and billboard towers.

Key ideas:
- Use a pre-trained YOLO model (Ultralytics) for detection; fine-tune on labeled samples for better accuracy.
- Provide measurement helpers that convert pixel sizes to meters using a user-supplied scale or a known reference object.

Files of interest:
- `requirements.txt` — Python dependencies (includes folium for mapping)
- `src/detect_towers/` — detection, measurement, and mapping modules
- `src/detect_towers/cli.py` — simple command-line wrapper with `detect`, `measure`, `train`, and `map` commands

Quick start
1. Create a virtualenv at the workspace root and install requirements:

```bash
cd /workspaces/quest-potential-new-sites
python -m venv venv
source venv/bin/activate
pip install -r data/requirements.txt  # or install minimal packages like Pillow for dataset scripts
```

2. Run detection on an image (saves annotated image to `runs/detect`):

```bash
python -m detect_towers.cli detect --image path/to/image.jpg --model yolov8n.pt --save-dir runs/detect
```

3. Plot geolocated points on a map with radius overlays:

```bash
python -m detect_towers.cli map --input locations.json --output towers_map.html
```

`locations.json` (or CSV/Excel) should be a list/table with columns `lat`, `lon`, `radius` (meters) and optional `name`.

Example:
```json
[
  {"lat":40.0, "lon":-105.3, "radius":50, "name":"Tower A"},
  {"lat":39.9, "lon":-105.2, "radius":30}
]
```

By default the map uses OpenStreetMap tiles. To use Google Maps (or another service) pass a tile URL template and your API key, e.g.:

```bash
python -m detect_towers.cli map --input locations.json --tiles "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}&key={key}" \
    --api-key YOUR_GOOGLE_KEY --output google_map.html
```

Note that Google requires an API key and billing enabled for its service.

4. Convert detections to real-world sizes by providing `--meters-per-pixel`:

```bash
python -m detect_towers.cli measure --image path/to/image.jpg --model yolov8n.pt --meters-per-pixel 0.2
```

3. Convert detections to real-world sizes by providing `--meters-per-pixel`:

```bash
python -m detect_towers.cli measure --image path/to/image.jpg --model yolov8n.pt --meters-per-pixel 0.2
```

Notes & next steps:
- For accurate meters-per-pixel you can compute scale from a known object visible in the image using `compute_scale_from_known_object`.
- For automated satellite downloads consider integrating Google Earth Engine or manual exports from Google Earth Pro.

Training
- Provide a YOLO-format dataset YAML (example below) with `train` and `val` image folders and a `names` list mapping class IDs to labels.

Example `data.yaml` (a ready-made sample is provided as `data/data.yaml` pointing at the `sample_dataset`):

```yaml
train: data/sample_dataset/images/train
val: data/sample_dataset/images/val
names: ["cell_tower", "billboard_tower"]
```

Run a training job (uses Ultralytics YOLOv8 API):

```bash
python -m detect_towers.train --data data.yaml --model yolov8n.pt --epochs 100 --imgsz 640 --batch 8 --project runs/train
```

The `train` script wraps `YOLO(model).train(...)` and saves results to the specified project folder.
