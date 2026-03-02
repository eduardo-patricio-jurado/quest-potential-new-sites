"""Utilities for plotting coordinates on a map."""
from typing import List, Dict, Optional
import folium


def load_locations_from_file(path: str) -> List[Dict]:
    """Load locations list from JSON, CSV, or Excel file.

    For CSV/Excel, columns should include at least `lat`, `lon`, and
    `radius`. An optional `name` column may be present.
    """
    import os
+    ext = os.path.splitext(path)[1].lower()
+    if ext in (".json",):
+        import json
+        with open(path, "r") as f:
+            return json.load(f)
+    else:
+        # use pandas for tabular formats
+        try:
+            import pandas as pd
+        except ImportError:
+            raise ImportError("pandas required to read CSV/Excel files")
+        if ext in (".csv",):
+            df = pd.read_csv(path)
+        elif ext in (".xls", ".xlsx", ".xlsm", ".odf", ".ods", ".odt"):
+            df = pd.read_excel(path)
+        else:
+            raise ValueError(f"Unsupported file extension: {ext}")
+        # ensure necessary columns exist
+        for col in ("lat", "lon", "radius"):
+            if col not in df.columns:
+                raise ValueError(f"Missing required column '{col}' in {path}")
+        records = df.to_dict(orient="records")
+        return records
+
+
+def plot_locations(locations: List[Dict], output: str = "map.html", start_zoom: int = 12, tiles: str = "OpenStreetMap", attr: Optional[str] = None, api_key: Optional[str] = None) -> None:
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
