import sys
import os
import pandas as pd
from dotenv import load_dotenv
from .download import download_image
from .detect import detect_towers

# Load environment variables from .env if present
load_dotenv()


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
            # ensure images directory exists and save the downloaded image
            os.makedirs('images', exist_ok=True)
            lat_str = f"{lat:.6f}".replace('.', 'p').replace('-', 'm')
            lon_str = f"{lon:.6f}".replace('.', 'p').replace('-', 'm')
            filename = os.path.join('images', f"{lat_str}_{lon_str}.png")
            with open(filename, 'wb') as fh:
                fh.write(img)
            print(f"Saved image to {filename}")
            detection = detect_towers(img)
            print(f"Result: {detection}")
        except Exception as e:
            print(f"Error processing {lat}, {lon}: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m src.cli <locations.xlsx>")
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.environ.get('GOOGLE_API_KEY'):
        print('Warning: GOOGLE_API_KEY not set. Set it in your environment or in .env to download images.')
    process_locations(file_path)
