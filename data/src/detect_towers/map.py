"""Utilities for plotting coordinates on a map."""
from typing import List, Dict, Optional
import folium


def plot_locations(locations: List[Dict], output: str = "map.html", start_zoom: int = 12) -> None:
    """Create an HTML map with circles for each location.

    `locations` is a list of dicts with keys:
    - lat (float)
    - lon (float)
    - radius (meters or same unit as desired)
    - name (optional string)

    The resulting HTML is written to `output`.
    """
    if not locations:
        raise ValueError("locations list is empty")

    # center map on first point
    first = locations[0]
    m = folium.Map(location=[first["lat"], first["lon"]], zoom_start=start_zoom)

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
