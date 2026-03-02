"""Generate a tiny YOLO-format dataset with blank images and dummy labels."""
import os
from pathlib import Path
from PIL import Image


def make_blank_image(path: Path, size=(640, 640)):
    img = Image.new("RGB", size, color=(255, 255, 255))
    img.save(path, "PNG")


def make_label(path: Path):
    # one object of class 0 centered with 0.2 width/height
    w, h = 0.2, 0.2
    x, y = 0.5, 0.5
    path.write_text(f"0 {x} {y} {w} {h}\n")


def create(base="data/sample_dataset", count=2):
    base = Path(base)
    for split in ["train", "val"]:
        img_dir = base / "images" / split
        lbl_dir = base / "labels" / split
        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)
        for i in range(count):
            img_path = img_dir / f"img_{split}_{i}.png"
            lbl_path = lbl_dir / f"img_{split}_{i}.txt"
            make_blank_image(img_path)
            make_label(lbl_path)
    print(f"Created sample dataset under {base}")


if __name__ == "__main__":
    create()
