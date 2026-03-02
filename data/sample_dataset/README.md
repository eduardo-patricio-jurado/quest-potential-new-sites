# Sample Dataset

This folder contains a minimal YOLO-format dataset with placeholder images and labels. It's intended to demonstrate the layout needed for training.

Structure:

```
sample_dataset/
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

Each image is a plain white PNG and each corresponding label file contains one fake bounding box (class 0).

To generate the files yourself run the helper script from the repository root:

```bash
python data/scripts/create_sample_dataset.py
```

After running the script you can train a model with:

```bash
python -m detect_towers.train --data sample_data.yaml --epochs 3
```
