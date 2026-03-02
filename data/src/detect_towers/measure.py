"""Measurement utilities for pixel -> real-world conversions.

Functions:
- compute_scale_from_known_object: compute meters per pixel from a known object length.
- measure_bboxes: convert bbox sizes (px) to meters given meters_per_pixel.
- estimate_height_from_shadow: estimate tower height from shadow length and sun elevation.
"""
from typing import List, Dict
import math


def compute_scale_from_known_object(known_length_m: float, pixel_length: float) -> float:
    """Return meters per pixel given a known real-world length and measured pixel length.

    Example: a road lane known to be 3.5 m that measures 50 px => meters_per_pixel = 3.5 / 50
    """
    if pixel_length <= 0:
        raise ValueError("pixel_length must be positive")
    return float(known_length_m) / float(pixel_length)


def measure_bboxes(bboxes: List[Dict], meters_per_pixel: float) -> List[Dict]:
    """Convert a list of bbox dicts (with `w` and `h` in px) to meters.

    Returns the same dicts with added keys: `w_m`, `h_m`, `area_m2`.
    """
    if meters_per_pixel <= 0:
        raise ValueError("meters_per_pixel must be positive")

    out = []
    for b in bboxes:
        w_m = b.get("w", 0) * meters_per_pixel
        h_m = b.get("h", 0) * meters_per_pixel
        area_m2 = w_m * h_m
        nb = dict(b)
        nb.update({"w_m": float(w_m), "h_m": float(h_m), "area_m2": float(area_m2)})
        out.append(nb)
    return out


def estimate_height_from_shadow(shadow_length_px: float, sun_elevation_deg: float, meters_per_pixel: float) -> float:
    """Estimate object height from shadow length and sun elevation angle.

    height_m = shadow_length_m * tan(sun_elevation)
    where shadow_length_m = shadow_length_px * meters_per_pixel
    `sun_elevation_deg` is degrees above horizon.
    """
    if shadow_length_px < 0:
        raise ValueError("shadow_length_px must be non-negative")
    if meters_per_pixel <= 0:
        raise ValueError("meters_per_pixel must be positive")

    shadow_m = float(shadow_length_px) * float(meters_per_pixel)
    # Convert degrees to radians
    elev_rad = math.radians(float(sun_elevation_deg))
    height_m = shadow_m * math.tan(elev_rad)
    return float(height_m)
