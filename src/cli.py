import sys
import os
import pandas as pd
from .download import download_image
from .detect import detect_towers


def process_locations(file_path: str):
    """Read Excel file and process each coordinate."""
    df = pd.read_excel(file_path)
    # expecting columns 'latitude' and 'longitude'
    for idx, row in df.iterrows():
        lat = row.get('latitude')
        lon = row.get('longitude')
        if pd.isna(lat) or pd.isna(lon):
            continue
        print(f"Processing {lat}, {lon}")
        try:
            img = download_image(lat, lon)
            detection = detect_towers(img)
            print(f"Result: {detection}")
        except Exception as e:
            print(f"Error processing {lat}, {lon}: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m src.cli <locations.xlsx>")
        sys.exit(1)
    file_path = sys.argv[1]
    process_locations(file_path)
