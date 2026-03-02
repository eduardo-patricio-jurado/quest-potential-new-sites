import os
import math
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
        "markers": f"color:blue|label:L|{lat},{lon}",
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.content


def _destination_point(lat: float, lon: float, distance_m: float, bearing_deg: float) -> tuple:
    """Return destination point from start lat/lon having travelled the given
    distance (in meters) on the given initial bearing (degrees).
    Uses the haversine/geodesic formula on a spherical Earth.
    """
    R = 6371000.0  # Earth radius in meters
    br = math.radians(bearing_deg)
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    dr = distance_m / R

    lat2 = math.asin(math.sin(lat1) * math.cos(dr) + math.cos(lat1) * math.sin(dr) * math.cos(br))
    lon2 = lon1 + math.atan2(math.sin(br) * math.sin(dr) * math.cos(lat1), math.cos(dr) - math.sin(lat1) * math.sin(lat2))

    return (math.degrees(lat2), math.degrees(lon2))


def download_image_with_radius(lat: float, lon: float, radius_m: float, zoom: int = 16, size: str = "640x640", points: int = 36) -> bytes:
    """Download a static map image with a circle (approximated by a polygon) drawn around the location.

    - `radius_m` is the circle radius in meters.
    - `points` is how many points will be used to approximate the circle.
    """
    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set")

    # build path parameter as lat,lon pairs around the circle
    coords = []
    for i in range(points + 1):
        bearing = (i / points) * 360.0
        p_lat, p_lon = _destination_point(lat, lon, radius_m, bearing)
        coords.append(f"{p_lat},{p_lon}")

    path = "color:0xff0000ff|weight:2|" + "|".join(coords)

    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": size,
        "maptype": "satellite",
        "key": key,
        "markers": f"color:blue|label:L|{lat},{lon}",
        "path": path,
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.content


def google_maps_link(lat: float, lon: float, zoom: int = 17) -> str:
    """Return a URL to open the location in Google Maps (interactive)."""
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}&zoom={zoom}"
