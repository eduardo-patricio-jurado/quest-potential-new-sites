import os
import requests

API_URL = "https://maps.googleapis.com/maps/api/staticmap"


def download_image(lat: float, lon: float, zoom: int = 18, size: str = "640x640") -> bytes:
    """Download a static map image from Google Maps for the given location.

    Requires environment variable GOOGLE_API_KEY to be set.
    """
    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set")

    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": size,
        "maptype": "satellite",
        "key": key,
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.content
