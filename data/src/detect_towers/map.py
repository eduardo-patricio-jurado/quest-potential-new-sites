"""Utilities for plotting coordinates on a map.

The loader is forgiving about column names: you can use ``lat``/``lon`` or
``latitude``/``longitude`` (case‑insensitive).  The radius column may be
named ``radius`` or anything containing the word "radius"; ``radius_km`` is
also supported, and its values will be converted to metres automatically.
Additional columns (e.g. ``id`` or ``name``) are preserved in the returned
records and may be used for popups or further processing.
"""
from typing import List, Dict, Optional
import folium


def load_locations_from_file(path: str) -> List[Dict]:
    """Load locations list from JSON, CSV, or Excel file.

    For CSV/Excel, columns should include at least `lat`, `lon`, and
    `radius`. An optional `name` column may be present.
    """
    import os
    ext = os.path.splitext(path)[1].lower()
    if ext in (".json",):
        import json
        with open(path, "r") as f:
            return json.load(f)
    else:
        # use pandas for tabular formats
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas required to read CSV/Excel files")

        if ext in (".csv",):
            df = pd.read_csv(path)
        elif ext in (".xls", ".xlsx", ".xlsm", ".odf", ".ods", ".odt"):
            df = pd.read_excel(path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

        # normalize columns to lowercase to help with synonyms
        df.columns = [c.lower() for c in df.columns]

        # locate latitude/longitude columns (support various names)
        lat_col = next((c for c in df.columns if c in ("lat", "latitude")), None)
        lon_col = next((c for c in df.columns if c in ("lon", "longitude", "lng")), None)
        if lat_col is None or lon_col is None:
            raise ValueError(f"Missing required lat/lon columns in {path}."
                             " Use 'lat'/'lon' or 'latitude'/'longitude'.")

        # find a radius column; prefer explicit 'radius', then look for something with 'radius' in the name
        radius_col = None
        for cand in df.columns:
            if cand == "radius":
                radius_col = cand
                break
            if "radius" in cand:
                radius_col = cand
        if radius_col is None:
            raise ValueError(f"Missing required radius column in {path}."
                             " Column name should include the word 'radius'.")

        records = []
        for _, row in df.iterrows():
            lat = row[lat_col]
            lon = row[lon_col]
            rad = row[radius_col]
            # convert from km to meters if the column name suggests it
            if "km" in radius_col:
                rad = float(rad) * 1000
            # cast to float (pandas may use numpy types)
            records.append({
                "lat": float(lat),
                "lon": float(lon),
                "radius": float(rad),
                # preserve any other fields (name, id, etc.) for potential use
                **{k: v for k, v in row.items() if k not in (lat_col, lon_col, radius_col)}
            })
        return records


def plot_locations(locations: List[Dict], output: str = "map.html", start_zoom: int = 12, tiles: str = "OpenStreetMap", attr: Optional[str] = None, api_key: Optional[str] = None) -> None:
    """Create an HTML map with circles for each location.

    `locations` is a list of dicts with keys:
    - lat (float)
    - lon (float)
    - radius (meters or same unit as desired)
    - name (optional string)

    `tiles` may be any folium tile layer name or a custom URL template.
    To use Google Maps you can supply a URL such as
    ``"https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}&key=YOUR_API_KEY"``
    and provide `api_key` separately. An API key is required by Google.

    The resulting HTML is written to `output`.
    """
    if not locations:
        raise ValueError("locations list is empty")

    # center map on first point
    first = locations[0]
    m = folium.Map(location=[first["lat"], first["lon"]], zoom_start=start_zoom, tiles=tiles, attr=attr)
    if api_key and "{key}" in tiles:
        # if template includes {key}, substitute
        m = folium.Map(location=[first["lat"], first["lon"]], zoom_start=start_zoom, tiles=tiles.format(key=api_key), attr=attr)

    for loc in locations:
        lat = loc.get("lat")
        lon = loc.get("lon")
        radius = loc.get("radius", 0)
        name = loc.get("name") or ""
        folium.Circle(
            location=[lat, lon],
            radius=radius,
            popup=name,
            color="blue",
            fill=True,
            fill_opacity=0.2,
        ).add_to(m)
        folium.Marker([lat, lon], popup=name).add_to(m)

    m.save(output)
    print(f"Map saved to {output}")
