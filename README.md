# Satellite Imagery Tower Detector

This Python project downloads Google Earth imagery for given latitude/longitude pairs and attempts to detect and estimate the height of billboard or cell tower structures.

## Features

- Read locations from an Excel spreadsheet (`.xlsx`) or other sources
- Download satellite images for each coordinate using Google Static Maps API
- Analyze images to detect towers and provide a height estimate (stubbed for now)

## Setup

1. Clone or open this repository.
2. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Obtain a Google Maps API key and set it in your environment:
   ```bash
   export GOOGLE_API_KEY="your_key_here"
   ```

## Usage

Prepare an Excel/CSV/JSON file with at least latitude and longitude.
The loader understands either `lat`/`lon` or `latitude`/`longitude` column names
(case doesn’t matter).  You also need a radius column – it can be named
`radius` or any name containing "radius".  If you use kilometers (e.g. a
`radius_km` column) the values will be converted to metres automatically.  Any
extra fields such as `id`, `name` or `tower_date` are preserved and can be
shown in the popups.

Run the CLI tool:

```bash
python -m src.cli path/to/locations.xlsx
```

To also draw a radius (in meters) around each location and save that image, pass `--radius`:

```bash
python -m src.cli path/to/locations.xlsx --radius 200
```

Output will print each location, an interactive Google Maps link for the location, and detection result.  Extend the detection logic in `src/detect.py`.

- Downloaded images are saved to the `images/` folder (created automatically).  Radius images are saved as `*_r{radius}m.png`.

## Project Structure

```
/quest-potential-new-sites
├── README.md
├── requirements.txt
├── src
    ├── __init__.py
    ├── cli.py
    ├── download.py
    ├── detect.py
```
