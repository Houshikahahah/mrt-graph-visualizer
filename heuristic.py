# def build_line_heuristic(graph, goal):
#     """
#     h(n) = 0 if n is goal
#            1 if n shares a line with goal
#            2 otherwise
#     """
#     goal_lines = graph.stations[goal].lines
#     h = {}

#     for code, station in graph.stations.items():
#         if code == goal:
#             h[code] = 0
#         elif not station.lines.isdisjoint(goal_lines):
#             h[code] = 1
#         else:
#             h[code] = 2
#     return h




# heuristic.py
#
# Heuristics for MRT routing:
# 1) Simple line-based heuristic (your original)
# 2) Euclidean (straight-line) heuristic using station lat/lon JSON

import os
import json
import math
import re
from typing import Dict, Tuple


# -----------------------------
# 1) Line heuristic (unchanged)
# -----------------------------
def build_line_heuristic(graph, goal: str) -> Dict[str, int]:
    """
    h(n) = 0 if n is goal
           1 if n shares a line with goal
           2 otherwise
    """
    goal_lines = graph.stations[goal].lines
    h = {}

    for code, station in graph.stations.items():
        if code == goal:
            h[code] = 0
        elif not station.lines.isdisjoint(goal_lines):
            h[code] = 1
        else:
            h[code] = 2
    return h


# --------------------------------------------------------
# 2) Euclidean heuristic helpers (lat/lon -> local x,y)
# --------------------------------------------------------
_CODE_RE = re.compile(r"^([A-Z]+)(\d+)$")


def _ensure_upper(code: str) -> str:
    return code.strip().upper()


def _candidate_codes(line: str, n: int) -> Tuple[str, str]:
    """
    Return both non-padded and zero-padded station codes.
    Examples: (EW7, EW07), (TE2, TE02)
    """
    line = line.strip().upper()
    return f"{line}{n}", f"{line}{n:02d}"


def load_station_coords_latlon(json_path: str) -> Dict[str, Tuple[float, float]]:
    """
    Supports TWO JSON row formats:

    A) station_code format (your FUTURE json):
       {"station_code":"TE32","latitude":..,"longitude":..}

    B) line + station_number format:
       {"line":"EW","station_number":7,"latitude":..,"longitude":..}

    Returns: {CODE: (lat, lon)} and also adds zero-padded variant if applicable.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Coords JSON not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    coords: Dict[str, Tuple[float, float]] = {}

    for row in data:
        if not isinstance(row, dict):
            continue

        lat = row.get("latitude") or row.get("lat")
        lon = row.get("longitude") or row.get("lon") or row.get("lng")
        if lat is None or lon is None:
            continue

        try:
            lat = float(lat)
            lon = float(lon)
        except (TypeError, ValueError):
            continue

        # --- Case A: station_code provided ---
        code = row.get("station_code") or row.get("code") or row.get("stationCode")
        if code:
            code = _ensure_upper(str(code))
            coords[code] = (lat, lon)

            # also store zero/non-zero padded variants if it matches pattern
            m = _CODE_RE.match(code)
            if m:
                line, digits = m.group(1), m.group(2)
                n = int(digits)
                c1, c2 = _candidate_codes(line, n)
                coords[c1] = (lat, lon)
                coords[c2] = (lat, lon)
            continue

        # --- Case B: line + station_number ---
        line = row.get("line")
        station_number = row.get("station_number")

        if line is None or station_number in (None, ""):
            continue

        try:
            n = int(station_number)
        except (TypeError, ValueError):
            continue

        line = str(line).strip().upper()
        c1, c2 = _candidate_codes(line, n)
        coords[c1] = (lat, lon)
        coords[c2] = (lat, lon)

    if not coords:
        raise ValueError(f"No valid station coordinates loaded from {json_path}")

    return coords




def _latlon_to_xy_m(lat: float, lon: float, lat0_deg: float) -> Tuple[float, float]:
    """
    Equirectangular projection -> (x,y) in meters.
    Good approximation for Singapore-scale distances.
    """
    R = 6_371_000.0  # meters
    phi = math.radians(lat)
    lam = math.radians(lon)
    phi0 = math.radians(lat0_deg)

    x = R * lam * math.cos(phi0)
    y = R * phi
    return x, y


def build_euclidean_distance_heuristic(
    graph,
    goal: str,
    station_coords_latlon: Dict[str, Tuple[float, float]],
    *,
    missing_value: float = 0.0,
) -> Dict[str, float]:
    """
    h(n) = straight-line distance in METERS from n to goal.

    - station_coords_latlon: dict {station_code: (lat, lon)}
    - If a station is missing coords, we set h to missing_value (default 0.0)
      so A* remains correct (it just becomes less informed for that node).
    """
    goal = _ensure_upper(goal)
    if goal not in station_coords_latlon:
        raise KeyError(
            f"Goal '{goal}' not found in station_coords_latlon. "
            f"Check your JSON line/station_number mapping."
        )

    # Use goal latitude as reference for projection (stable for small area)
    goal_lat, goal_lon = station_coords_latlon[goal]
    lat0 = goal_lat

    gx, gy = _latlon_to_xy_m(goal_lat, goal_lon, lat0)

    h: Dict[str, float] = {}
    for code in graph.stations.keys():
        c = _ensure_upper(code)
        if c == goal:
            h[c] = 0.0
            continue

        ll = station_coords_latlon.get(c)
        if ll is None:
            h[c] = float(missing_value)
            continue

        lat, lon = ll
        x, y = _latlon_to_xy_m(lat, lon, lat0)
        h[c] = math.hypot(x - gx, y - gy)

    return h


def build_euclidean_time_heuristic(
    graph,
    goal: str,
    station_coords_latlon: Dict[str, Tuple[float, float]],
    *,
    minutes_per_km: float = 2.5,
    missing_value: float = 0.0,
) -> Dict[str, float]:
    """
    h(n) = straight-line distance converted into MINUTES
         = (distance_km * minutes_per_km)

    This matches your edge weights better if your edges are "time-like"
    (you currently bake 1 + transfer + crowding into edge weights).
    """
    dist_m = build_euclidean_distance_heuristic(
        graph, goal, station_coords_latlon, missing_value=missing_value
    )
    h: Dict[str, float] = {}
    for k, d_m in dist_m.items():
        h[k] = (d_m / 1000.0) * float(minutes_per_km)
    h[_ensure_upper(goal)] = 0.0
    return h


# --------------------------------------------------------
# Convenience wrapper: build directly from a coords JSON
# --------------------------------------------------------
def build_euclidean_time_heuristic_from_json(
    graph,
    goal: str,
    coords_json_path: str,
    *,
    minutes_per_km: float = 2.5,
    missing_value: float = 0.0,
) -> Dict[str, float]:
    coords = load_station_coords_latlon(coords_json_path)
    if goal not in coords:
        # show something close to TE32 if present with padding or odd chars
        keys = list(coords.keys())
    return build_euclidean_time_heuristic(
        graph,
        goal,
        coords,
        minutes_per_km=minutes_per_km,
        missing_value=missing_value,
    )


