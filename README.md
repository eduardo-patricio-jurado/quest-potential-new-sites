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

Prepare an Excel file with at least two columns named `latitude` and `longitude`.

Run the CLI tool:

```bash
python -m src.cli path/to/locations.xlsx
```

Output will print each location and detection result.  Extend the detection logic in `src/detect.py`.

- Downloaded images are saved to the `images/` folder (created automatically).

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
