import os
import argparse
import pandas as pd
from dotenv import load_dotenv
from .download import download_image, download_image_with_radius, google_maps_link
from .detect import detect_towers

# Load environment variables from .env if present
load_dotenv()


def process_locations(file_path: str, radius_m: float | None = None):
    """Read Excel file and process each coordinate.

    If the spreadsheet contains a column named `radius` it is interpreted as a
    meter value and used for that row. Otherwise `radius_m` from the command
    line (or `None`) is used.
    """
    df = pd.read_excel(file_path)
    # expecting columns 'latitude' and 'longitude'; optional 'radius'
    for idx, row in df.iterrows():
        lat = row.get('latitude')
        lon = row.get('longitude')
        if pd.isna(lat) or pd.isna(lon):
            continue
        # determine radius for this row
        row_radius = None
        if 'radius' in df.columns:
            val = row.get('radius')
            if not pd.isna(val):
                try:
                    row_radius = float(val)
                except Exception:
                    print(f"Warning: invalid radius value '{val}' at row {idx}, ignoring")
        radius_to_use = row_radius if row_radius is not None else radius_m

        print(f"Processing {lat}, {lon} (radius={radius_to_use})")
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

            # print interactive Google Maps link
            maps_url = google_maps_link(lat, lon)
            print(f"Open in Google Maps: {maps_url}")

            # optionally download an image with radius drawn
            if radius_to_use:
                try:
                    rad_img = download_image_with_radius(lat, lon, radius_to_use)
                    rad_filename = os.path.join('images', f"{lat_str}_{lon_str}_r{int(radius_to_use)}m.png")
                    with open(rad_filename, 'wb') as fh:
                        fh.write(rad_img)
                    print(f"Saved radius image to {rad_filename}")
                except Exception as re:
                    print(f"Error downloading radius image: {re}")

            detection = detect_towers(img)
            print(f"Result: {detection}")
        except Exception as e:
            print(f"Error processing {lat}, {lon}: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process locations and download satellite images')
    parser.add_argument('locations', help='Excel file with latitude and longitude columns')
    parser.add_argument('--radius', type=float, default=None, help='Radius in meters to draw around each location')
    args = parser.parse_args()

    if not os.environ.get('GOOGLE_API_KEY'):
        print('Warning: GOOGLE_API_KEY not set. Set it in your environment or in .env to download images.')

    process_locations(args.locations, radius_m=args.radius)
