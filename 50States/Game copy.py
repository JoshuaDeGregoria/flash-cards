# Flash Cards for the 50 US States
# Complete single-file tkinter implementation.

# This file is organized by responsibility:
# 1) static data and map geometry,
# 2) pure helper functions,
# 3) application state,
# 4) UI building and interaction handlers,
# 5) session/ranking flow.
# Keeping everything in one file makes it easy to study control flow end-to-end.

import csv
import os
import random
import sys
import time

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError as exc:
    if exc.name in {"_tkinter", "tkinter"}:
        raise SystemExit(
            "This Python build does not include Tkinter.\n"
            f"Interpreter: {sys.executable}\n"
            f"Try: /usr/bin/python3 {os.path.abspath(__file__)}"
        ) from None
    raise


MAX_SESSION_LENGTH = 300  # seconds
TYPED_ANSWER_POINTS = 2 / 6
MULTIPLE_CHOICE_POINTS = 1 / 6
MAP_HIGHLIGHT_COLOR = "#f9e27d"
SELECTED_STATE_COLOR = "#7fd1b9"
NORMAL_STATE_COLOR = "#d8dee9"
MAP_BORDER_COLOR = "#4c566a"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RANKINGS_FILE = os.path.join(BASE_DIR, "rankings.csv")

FIELD_LABELS = {
    "name": "State Name",
    "initials": "State Initials",
    "capital": "Capital City",
    "map": "Map Location",
}

# --- Reference data section -------------------------------------------------
# STATE_INFO is the canonical source for each state's core quiz facts.
# Shapes/centers are kept separate so factual data can be reused independently
# from map rendering logic.

# (abbr, full_name, capital)
STATE_INFO = {
    "AL": ("Alabama", "Montgomery"),
    "AK": ("Alaska", "Juneau"),
    "AZ": ("Arizona", "Phoenix"),
    "AR": ("Arkansas", "Little Rock"),
    "CA": ("California", "Sacramento"),
    "CO": ("Colorado", "Denver"),
    "CT": ("Connecticut", "Hartford"),
    "DE": ("Delaware", "Dover"),
    "FL": ("Florida", "Tallahassee"),
    "GA": ("Georgia", "Atlanta"),
    "HI": ("Hawaii", "Honolulu"),
    "ID": ("Idaho", "Boise"),
    "IL": ("Illinois", "Springfield"),
    "IN": ("Indiana", "Indianapolis"),
    "IA": ("Iowa", "Des Moines"),
    "KS": ("Kansas", "Topeka"),
    "KY": ("Kentucky", "Frankfort"),
    "LA": ("Louisiana", "Baton Rouge"),
    "ME": ("Maine", "Augusta"),
    "MD": ("Maryland", "Annapolis"),
    "MA": ("Massachusetts", "Boston"),
    "MI": ("Michigan", "Lansing"),
    "MN": ("Minnesota", "Saint Paul"),
    "MS": ("Mississippi", "Jackson"),
    "MO": ("Missouri", "Jefferson City"),
    "MT": ("Montana", "Helena"),
    "NE": ("Nebraska", "Lincoln"),
    "NV": ("Nevada", "Carson City"),
    "NH": ("New Hampshire", "Concord"),
    "NJ": ("New Jersey", "Trenton"),
    "NM": ("New Mexico", "Santa Fe"),
    "NY": ("New York", "Albany"),
    "NC": ("North Carolina", "Raleigh"),
    "ND": ("North Dakota", "Bismarck"),
    "OH": ("Ohio", "Columbus"),
    "OK": ("Oklahoma", "Oklahoma City"),
    "OR": ("Oregon", "Salem"),
    "PA": ("Pennsylvania", "Harrisburg"),
    "RI": ("Rhode Island", "Providence"),
    "SC": ("South Carolina", "Columbia"),
    "SD": ("South Dakota", "Pierre"),
    "TN": ("Tennessee", "Nashville"),
    "TX": ("Texas", "Austin"),
    "UT": ("Utah", "Salt Lake City"),
    "VT": ("Vermont", "Montpelier"),
    "VA": ("Virginia", "Richmond"),
    "WA": ("Washington", "Olympia"),
    "WV": ("West Virginia", "Charleston"),
    "WI": ("Wisconsin", "Madison"),
    "WY": ("Wyoming", "Cheyenne"),
}

# Contiguous US state border data in lon/lat points.
STATE_SHAPES = {
    "WA": [(-124.73, 48.48), (-117.03, 49.00), (-117.03, 46.00), (-119.00, 45.80), (-124.14, 45.56), (-124.73, 46.20)],
    "OR": [(-124.55, 46.23), (-123.72, 46.18), (-117.03, 46.00), (-117.03, 42.00), (-124.55, 42.00)],
    "CA": [(-124.41, 42.00), (-120.00, 42.00), (-119.99, 39.00), (-114.63, 35.00), (-114.63, 32.53), (-117.24, 32.53), (-117.34, 33.10), (-118.52, 34.00), (-120.51, 35.14), (-120.90, 35.47), (-122.40, 37.36), (-122.50, 37.71), (-124.18, 38.97), (-124.35, 40.26)],
    "NV": [(-120.00, 42.00), (-114.05, 42.00), (-114.05, 37.00), (-114.63, 35.00), (-120.00, 39.00)],
    "ID": [(-117.03, 44.00), (-117.03, 49.00), (-111.05, 49.00), (-111.05, 42.00), (-114.05, 42.00), (-116.05, 44.00)],
    "MT": [(-116.05, 49.00), (-104.04, 49.00), (-104.04, 44.36), (-116.05, 44.36)],
    "WY": [(-111.05, 45.00), (-104.05, 45.00), (-104.05, 41.00), (-111.05, 41.00)],
    "CO": [(-109.05, 41.00), (-102.05, 41.00), (-102.05, 37.00), (-109.05, 37.00)],
    "UT": [(-114.05, 42.00), (-111.05, 42.00), (-111.05, 41.00), (-109.05, 41.00), (-109.05, 37.00), (-114.05, 37.00)],
    "AZ": [(-114.82, 37.00), (-109.05, 37.00), (-109.05, 31.33), (-111.07, 31.33), (-114.82, 32.49)],
    "NM": [(-109.05, 37.00), (-103.00, 37.00), (-103.00, 32.00), (-106.62, 32.00), (-106.62, 31.78), (-108.21, 31.78), (-108.21, 31.33), (-109.05, 31.33)],
    "ND": [(-104.05, 49.00), (-96.56, 48.99), (-97.00, 46.93), (-96.56, 46.63), (-104.05, 45.93)],
    "SD": [(-104.05, 45.93), (-96.44, 45.93), (-96.44, 43.00), (-104.05, 43.00)],
    "NE": [(-104.05, 43.00), (-102.05, 43.00), (-102.05, 40.00), (-95.31, 40.00), (-95.37, 42.49), (-96.48, 43.00)],
    "KS": [(-102.05, 40.00), (-94.62, 40.00), (-94.62, 37.00), (-102.05, 37.00)],
    "OK": [(-103.00, 37.00), (-100.00, 37.00), (-100.00, 36.50), (-94.43, 36.50), (-94.43, 33.64), (-103.00, 33.64)],
    "TX": [(-103.00, 36.50), (-94.43, 36.50), (-94.00, 30.00), (-96.40, 28.30), (-97.00, 25.84), (-99.45, 26.45), (-100.50, 28.00), (-104.02, 29.45), (-104.57, 30.08), (-106.62, 32.00), (-103.00, 32.00)],
    "MN": [(-97.24, 43.50), (-89.49, 43.50), (-89.49, 45.30), (-92.01, 46.71), (-89.49, 48.00), (-90.00, 49.00), (-97.24, 49.00)],
    "IA": [(-96.60, 43.50), (-90.15, 43.50), (-90.15, 40.38), (-95.86, 40.38), (-96.60, 43.10)],
    "MO": [(-95.77, 40.59), (-91.73, 40.61), (-89.52, 37.00), (-89.13, 36.62), (-94.62, 36.50), (-95.77, 36.50)],
    "AR": [(-94.62, 36.50), (-90.15, 36.50), (-90.30, 35.43), (-90.07, 35.00), (-91.09, 33.00), (-94.04, 33.01)],
    "LA": [(-94.04, 33.01), (-89.73, 33.00), (-89.73, 30.20), (-89.00, 29.00), (-90.00, 29.00), (-90.40, 29.88), (-91.40, 29.30), (-92.60, 29.60), (-93.80, 29.84), (-93.90, 30.20), (-94.04, 30.00)],
    "WI": [(-92.89, 47.08), (-86.81, 47.08), (-87.03, 45.50), (-87.80, 45.20), (-87.03, 42.50), (-90.64, 42.50), (-92.89, 44.00)],
    "MI": [[(-86.60, 41.77), (-82.43, 41.77), (-82.43, 43.00), (-83.45, 44.00), (-83.80, 44.77), (-84.00, 45.77), (-85.56, 45.77), (-86.60, 44.50)], [(-90.42, 45.77), (-84.50, 45.77), (-84.50, 46.00), (-84.00, 46.50), (-84.50, 47.00), (-88.00, 48.19), (-90.42, 48.19)]],
    "IL": [(-91.51, 42.51), (-87.80, 42.49), (-87.80, 37.00), (-89.20, 37.00), (-91.51, 40.00)],
    "IN": [(-88.10, 41.77), (-84.81, 41.77), (-84.81, 37.77), (-88.10, 37.77)],
    "OH": [(-84.82, 42.00), (-80.52, 42.00), (-80.52, 38.40), (-84.82, 38.40)],
    "MS": [(-91.65, 35.00), (-88.10, 34.99), (-88.10, 30.24), (-88.47, 30.24), (-91.65, 30.99)],
    "AL": [(-88.47, 34.99), (-85.61, 34.99), (-85.18, 32.87), (-84.89, 32.26), (-88.10, 30.24), (-88.47, 31.00)],
    "TN": [(-90.31, 36.50), (-81.65, 36.59), (-81.65, 35.00), (-90.31, 35.00)],
    "KY": [(-89.57, 36.50), (-89.57, 37.90), (-87.50, 37.90), (-84.82, 39.10), (-82.60, 38.60), (-81.97, 37.54), (-84.30, 36.60)],
    "GA": [(-85.61, 34.99), (-83.11, 35.00), (-83.00, 34.00), (-81.00, 32.00), (-81.00, 30.36), (-84.90, 30.36), (-85.18, 32.87)],
    "FL": [(-87.63, 30.99), (-85.00, 31.00), (-84.90, 29.70), (-83.30, 29.45), (-81.50, 28.50), (-80.40, 27.00), (-80.03, 25.13), (-80.35, 26.30), (-81.00, 27.00), (-82.30, 27.00), (-82.65, 28.00), (-83.00, 29.50), (-84.00, 30.00), (-84.90, 30.10), (-87.63, 30.40)],
    "SC": [(-83.36, 35.20), (-78.55, 33.85), (-79.68, 32.00), (-81.12, 31.00), (-81.40, 31.70), (-83.36, 32.00)],
    "NC": [(-84.32, 36.59), (-75.46, 36.55), (-75.46, 35.20), (-76.50, 34.80), (-77.50, 34.20), (-78.00, 33.90), (-84.32, 35.00)],
    "VA": [(-83.68, 37.30), (-76.00, 38.00), (-75.24, 37.89), (-75.24, 36.55), (-79.00, 36.54), (-83.68, 36.60)],
    "WV": [(-82.64, 40.64), (-80.52, 40.64), (-79.46, 39.72), (-77.72, 39.46), (-77.72, 37.40), (-79.00, 37.00), (-81.97, 37.24), (-82.64, 38.18)],
    "MD": [(-79.49, 39.72), (-75.79, 39.72), (-75.25, 38.45), (-76.00, 38.00), (-77.00, 38.35), (-79.49, 39.20)],
    "PA": [(-80.52, 42.27), (-74.70, 42.27), (-74.70, 39.72), (-80.52, 39.72)],
    "NJ": [(-75.56, 41.36), (-74.01, 41.36), (-74.01, 39.00), (-75.56, 39.00)],
    "DE": [(-75.79, 39.84), (-75.05, 39.84), (-75.05, 38.45), (-75.79, 38.45)],
    "NY": [(-79.76, 43.00), (-73.77, 45.01), (-71.51, 45.01), (-73.54, 40.75), (-74.25, 41.00), (-76.00, 42.00), (-79.76, 42.27)],
    "CT": [(-73.73, 42.05), (-71.80, 42.02), (-71.80, 41.00), (-73.73, 41.00)],
    "RI": [(-71.86, 42.02), (-71.12, 42.02), (-71.12, 41.30), (-71.86, 41.30)],
    "MA": [(-73.51, 42.79), (-69.93, 42.09), (-69.93, 41.50), (-73.51, 41.50)],
    "VT": [(-73.44, 45.01), (-71.51, 45.01), (-72.46, 43.58), (-73.44, 43.58)],
    "NH": [(-72.56, 45.31), (-70.70, 43.73), (-70.70, 43.00), (-72.56, 43.00)],
    "ME": [(-71.08, 43.08), (-71.08, 45.31), (-70.65, 47.40), (-69.23, 47.45), (-67.79, 47.06), (-67.00, 44.00)],
}

ALASKA_SHAPE = [
    (-167.00, 55.00), (-160.00, 54.50), (-153.00, 56.50),
    (-148.00, 59.50), (-136.00, 57.00), (-130.00, 55.50),
    (-141.00, 60.00), (-141.00, 70.50), (-156.00, 71.50),
    (-163.00, 67.50), (-168.00, 66.00),
]

HAWAII_ISLANDS = [
    [(-156.05, 18.92), (-154.82, 18.92), (-154.82, 20.27), (-156.05, 20.27)],
    [(-156.70, 20.52), (-155.95, 20.52), (-155.95, 21.03), (-156.70, 21.03)],
    [(-157.30, 21.00), (-156.70, 21.00), (-156.70, 21.22), (-157.30, 21.22)],
    [(-158.30, 21.23), (-157.65, 21.23), (-157.65, 21.72), (-158.30, 21.72)],
    [(-159.79, 21.84), (-159.28, 21.84), (-159.28, 22.23), (-159.79, 22.23)],
]

LABEL_OVERRIDES = {
    "OK": (-97.50, 35.30),
    "TX": (-99.30, 31.20),
    "FL": (-83.50, 28.00),
    "ME": (-69.20, 45.30),
    "MI": (-85.00, 43.50),
    "MN": (-94.30, 46.40),
    "KY": (-85.30, 37.50),
    "WV": (-80.60, 38.80),
    "VA": (-79.40, 37.50),
    "NC": (-80.00, 35.50),
    "TN": (-86.30, 35.90),
    "NY": (-75.80, 43.00),
    "LA": (-92.40, 31.00),
    "MD": (-77.00, 39.30),
}

# Projection constants for map rendering.
WEST, EAST = -125.0, -66.5
SOUTH, NORTH = 24.0, 50.0
MAP_LEFT, MAP_TOP = 10, 10
MAP_WIDTH, MAP_HEIGHT = 690, 420

AK_LEFT, AK_TOP = 10, 440
AK_WIDTH, AK_HEIGHT = 140, 85
AK_WEST, AK_EAST = -170.0, -130.0
AK_SOUTH, AK_NORTH = 54.0, 72.0

HI_LEFT, HI_TOP = 165, 447
HI_WIDTH, HI_HEIGHT = 95, 64
HI_WEST, HI_EAST = -161.0, -154.5
HI_SOUTH, HI_NORTH = 18.8, 22.5


def to_canvas(lon, lat):
    """Convert contiguous-US longitude/latitude into canvas pixel coordinates.

    Why: map shape data is stored in geographic coordinates for readability and
    reuse, but tkinter polygons need x/y pixels in the window coordinate system.
    """
    x = MAP_LEFT + (lon - WEST) / (EAST - WEST) * MAP_WIDTH
    y = MAP_TOP + (NORTH - lat) / (NORTH - SOUTH) * MAP_HEIGHT
    return x, y


def to_canvas_ak(lon, lat):
    """Project Alaska coordinates into its inset map rectangle.

    Why: Alaska's true position/scale does not fit well in a contiguous map, so
    it is rendered in a dedicated inset with its own projection bounds.
    """
    x = AK_LEFT + (lon - AK_WEST) / (AK_EAST - AK_WEST) * AK_WIDTH
    y = AK_TOP + (AK_NORTH - lat) / (AK_NORTH - AK_SOUTH) * AK_HEIGHT
    return x, y


def to_canvas_hi(lon, lat):
    """Project Hawaii coordinates into its inset map rectangle.

    Why: like Alaska, Hawaii is intentionally moved into an inset so all states
    are visible in a compact classroom-friendly layout.
    """
    x = HI_LEFT + (lon - HI_WEST) / (HI_EAST - HI_WEST) * HI_WIDTH
    y = HI_TOP + (HI_NORTH - lat) / (HI_NORTH - HI_SOUTH) * HI_HEIGHT
    return x, y


def polygon_center(point_list):
    """Return a simple centroid approximation by averaging polygon vertices.

    Why: label placement does not require geometric-perfect centroids; averaging
    is fast and easy to understand for a teaching project.
    """
    avg_lon = sum(lon for lon, _ in point_list) / len(point_list)
    avg_lat = sum(lat for _, lat in point_list) / len(point_list)
    return avg_lon, avg_lat


def normalize_polygons(shape_data):
    """Normalize shape data to a list-of-polygons format.

    Why: most states have one polygon, while some (for example Michigan) have
    multiple disjoint polygons. Normalization gives drawing code one format.
    """
    if not shape_data:
        return []
    if isinstance(shape_data[0], tuple):
        return [shape_data]
    return shape_data


def points_to_flat(point_list, projector):
    """Convert [(lon, lat), ...] into [x1, y1, x2, y2, ...] for tkinter.

    Why: tkinter's create_polygon expects a flattened numeric sequence.
    """
    flat = []
    for lon, lat in point_list:
        x, y = projector(lon, lat)
        flat.extend([x, y])
    return flat


def projector_for_state(abbr):
    """Choose which coordinate projector to use for a state abbreviation.

    Why: AK and HI use inset projections; every other state uses the contiguous
    map projection. Centralizing this keeps drawing code clean.
    """
    if abbr == "AK":
        return to_canvas_ak
    if abbr == "HI":
        return to_canvas_hi
    return to_canvas


def build_state_data():
    """Build the unified STATE_DATA structure used by gameplay and UI.

    Why: a single normalized dictionary avoids repeated lookups and keeps each
    card generation step simple (name, initials, capital, polygons, label point).
    """
    shape_by_abbr = dict(STATE_SHAPES)
    shape_by_abbr["AK"] = ALASKA_SHAPE
    shape_by_abbr["HI"] = HAWAII_ISLANDS

    result = {}
    for abbr, (name, capital) in STATE_INFO.items():
        polygons = normalize_polygons(shape_by_abbr[abbr])

        if abbr in LABEL_OVERRIDES:
            center_lon, center_lat = LABEL_OVERRIDES[abbr]
        else:
            center_lon, center_lat = polygon_center(polygons[0])

        result[abbr] = {
            "name": name,
            "initials": abbr,
            "capital": capital,
            "map_data": polygons,
            "center": (center_lon, center_lat),
        }

    return result


STATE_DATA = build_state_data()


# --- Runtime state section --------------------------------------------------
# app_state acts as a simple in-memory state store for this single-file app.
# This avoids global scattered variables and makes transitions explicit.
app_state = {
    "current_screen": "settings",
    "selected_prompt_fields": [],
    "selected_answer_fields": [],
    "answer_modes": {},
    "deck_order": [],
    "current_card_index": 0,
    "current_state_abbr": None,
    "current_answer_vars": {},
    "score": 0.0,
    "session_start_time": None,
    "elapsed_time": 0.0,
    "timer_after_id": None,
    "selected_map_state": None,
    "submitted_current": False,
    "user_initials": "",
    "rankings": [],
    "map_polygon_items": {},
    "ui": {},
}


def initialize_rankings_file():
    """Create rankings CSV with headers if it does not exist.

    Why: bootstrap once so later reads/writes can assume a valid file shape.
    """
    if os.path.exists(RANKINGS_FILE):
        return

    try:
        with open(RANKINGS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Initials", "Elapsed Time", "Score"])
    except OSError:
        pass


def load_rankings():
    """Load persisted rankings from CSV, skipping malformed rows.

    Why: defensive parsing lets the app keep working even if a row was edited
    manually or partially written.
    """
    rankings = []

    if not os.path.exists(RANKINGS_FILE):
        return rankings

    try:
        with open(RANKINGS_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                try:
                    initials, elapsed_time, score = row
                    rankings.append((initials, float(elapsed_time), float(score)))
                except (ValueError, IndexError):
                    continue
    except OSError:
        return []

    return rankings


def save_rankings(rankings):
    """Persist the top 10 ranking rows to disk.

    Why: saving only the leaderboard cap keeps file size small and read logic
    straightforward for beginners.
    """
    try:
        with open(RANKINGS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Initials", "Elapsed Time", "Score"])
            for initials, elapsed, score in rankings[:10]:
                writer.writerow([initials, f"{elapsed:.3f}", f"{score:.3f}"])
    except OSError:
        return


def sort_rankings(rankings):
    """Sort by highest score first, then fastest time as tie-breaker.

    Why: this rewards accuracy primarily while still distinguishing equal-score
    runs by speed.
    """
    return sorted(rankings, key=lambda record: (-record[2], record[1]))


def validate_initials(initials):
    """Return True when initials are exactly three alphabetic letters.

    Why: fixed-length initials keep leaderboard display aligned and readable.
    """
    cleaned = initials.strip().upper()
    return len(cleaned) == 3 and cleaned.isalpha()


def validate_settings(prompt_fields, answer_fields, answer_modes):
    """Validate user-selected quiz configuration.

    Why: central validation ensures all entry points enforce the same rules
    (count limits, no overlap, and mode constraints).
    """
    if not (1 <= len(prompt_fields) <= 3):
        return False, "Select 1 to 3 prompt items."
    if not (1 <= len(answer_fields) <= 3):
        return False, "Select 1 to 3 answer items."

    overlap = set(prompt_fields) & set(answer_fields)
    if overlap:
        joined = ", ".join(FIELD_LABELS[key] for key in sorted(overlap))
        return False, f"Prompt and answer items cannot overlap ({joined})."

    for field in answer_fields:
        if field == "map":
            if answer_modes.get(field) != "map-click":
                return False, "Map answers must use map click mode."
            continue

        if answer_modes.get(field) not in {"text", "dropdown"}:
            return False, f"Choose a valid answer mode for {FIELD_LABELS[field]}."

    return True, ""


def normalize_answer(answer):
    """Normalize user input for case-insensitive comparison.

    Why: grading should focus on knowledge, not capitalization differences.
    """
    return answer.strip().lower()


def calculate_score(field, user_answer, correct_answer, answer_mode):
    """Compute earned points for one answer field.

    Why: scoring weights typed answers higher than assisted modes (dropdown/map)
    to reflect increased recall difficulty.
    """
    if answer_mode == "text":
        return TYPED_ANSWER_POINTS if normalize_answer(user_answer) == normalize_answer(correct_answer) else 0.0
    if answer_mode in {"dropdown", "multiple-choice", "map-click"}:
        return MULTIPLE_CHOICE_POINTS if normalize_answer(user_answer) == normalize_answer(correct_answer) else 0.0
    return 0.0


# --- UI and interaction section ---------------------------------------------
# The functions below construct screens and mediate user interaction. Keeping
# view construction and event handlers grouped together makes state flow easier
# to follow when learning tkinter apps.

def create_main_window():
    """Create and configure the root tkinter window.

    Why: centralizing window setup ensures every app launch starts with the
    same dimensions/title and keeps startup code in __main__ minimal.
    """
    root = tk.Tk()
    root.title("50 States Flash Cards")
    root.geometry("1060x760")
    root.minsize(980, 700)
    return root


def clear_screen(root):
    """Remove all widgets from the root window.

    Why: this app swaps full screens (settings, gameplay, rankings) by
    destroying and rebuilding widgets rather than using multiple windows.
    """
    for widget in root.winfo_children():
        widget.destroy()


def dropdown_options_for_field(field):
    """Return sorted drop-down values for the requested quiz field.

    Why: generating options from STATE_DATA avoids duplicated hardcoded lists
    and automatically stays in sync with the canonical data source.
    """
    if field == "name":
        return sorted(STATE_DATA[abbr]["name"] for abbr in STATE_DATA)
    if field == "initials":
        return sorted(STATE_DATA)
    if field == "capital":
        return sorted({STATE_DATA[abbr]["capital"] for abbr in STATE_DATA})
    return []


def field_value_for_state(field, state_abbr):
    """Read one field value for a specific state abbreviation.

    Why: prompt rendering and answer checking both rely on the same mapping,
    so this helper prevents duplicate branching in multiple call sites.
    """
    state = STATE_DATA[state_abbr]
    if field == "name":
        return state["name"]
    if field == "initials":
        return state["initials"]
    if field == "capital":
        return state["capital"]
    if field == "map":
        return state["initials"]
    return ""


def set_settings_error(message):
    """Write a validation message into the settings error label.

    Why: one helper keeps all settings-screen error updates consistent and
    avoids repetitive UI lookup logic.
    """
    error_var = app_state.get("ui", {}).get("settings_error_var")
    if error_var is not None:
        error_var.set(message)


def build_settings_screen(root):
    """Render the configuration screen where a session is customized.

    What it does: builds initials input, prompt/answer selectors, and answer
    mode radio buttons, then stores Tk variables into app_state['ui'].
    Why: UI variables are retained in app_state so later handlers can read
    choices without passing many widget references between functions.
    """
    clear_screen(root)
    app_state["current_screen"] = "settings"

    container = tk.Frame(root, padx=20, pady=20)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="US States Flash Cards", font=("Helvetica", 24, "bold")).pack(anchor="w")
    tk.Label(
        container,
        text="Choose 1-3 prompt items and 1-3 non-overlapping answer items. Session time limit: 300 seconds.",
        font=("Helvetica", 11),
    ).pack(anchor="w", pady=(8, 18))

    initials_row = tk.Frame(container)
    initials_row.pack(fill="x", pady=(0, 14))

    tk.Label(initials_row, text="Your 3-letter initials:", font=("Helvetica", 12, "bold")).pack(side="left")
    initials_var = tk.StringVar(value=app_state["user_initials"])
    tk.Entry(initials_row, textvariable=initials_var, width=8, font=("Helvetica", 12)).pack(side="left", padx=10)

    selector_row = tk.Frame(container)
    selector_row.pack(fill="x", pady=(8, 8))

    prompt_box = tk.LabelFrame(selector_row, text="Prompt Items", padx=10, pady=8)
    prompt_box.pack(side="left", fill="both", expand=True, padx=(0, 8))

    answer_box = tk.LabelFrame(selector_row, text="Answer Items", padx=10, pady=8)
    answer_box.pack(side="left", fill="both", expand=True, padx=(8, 0))

    prompt_vars = {}
    answer_vars = {}

    for field in ("name", "initials", "capital", "map"):
        prompt_var = tk.BooleanVar(value=(field in app_state["selected_prompt_fields"]))
        answer_var = tk.BooleanVar(value=(field in app_state["selected_answer_fields"]))
        prompt_vars[field] = prompt_var
        answer_vars[field] = answer_var

        tk.Checkbutton(prompt_box, text=FIELD_LABELS[field], variable=prompt_var, anchor="w").pack(fill="x")
        tk.Checkbutton(answer_box, text=FIELD_LABELS[field], variable=answer_var, anchor="w").pack(fill="x")

    mode_box = tk.LabelFrame(container, text="Answer Mode (for name, initials, and capital)", padx=10, pady=8)
    mode_box.pack(fill="x", pady=(10, 8))

    mode_vars = {}
    for field in ("name", "initials", "capital"):
        previous_mode = app_state["answer_modes"].get(field, "text")
        mode_var = tk.StringVar(value=previous_mode)
        mode_vars[field] = mode_var

        row = tk.Frame(mode_box)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=f"{FIELD_LABELS[field]}:", width=20, anchor="w").pack(side="left")
        tk.Radiobutton(row, text="Typed", variable=mode_var, value="text").pack(side="left", padx=(0, 10))
        tk.Radiobutton(row, text="Drop-down", variable=mode_var, value="dropdown").pack(side="left")

    settings_error_var = tk.StringVar(value="")
    tk.Label(container, textvariable=settings_error_var, fg="#b00020", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(10, 4))

    action_row = tk.Frame(container)
    action_row.pack(fill="x", pady=(10, 0))

    tk.Button(action_row, text="Start Session", width=16, command=lambda: start_session(root)).pack(side="left")
    tk.Button(action_row, text="View Rankings", width=16, command=lambda: build_rankings_screen(root)).pack(side="left", padx=8)
    tk.Button(action_row, text="Quit", width=10, command=root.destroy).pack(side="right")

    app_state["ui"] = {
        "initials_var": initials_var,
        "prompt_vars": prompt_vars,
        "answer_vars": answer_vars,
        "mode_vars": mode_vars,
        "settings_error_var": settings_error_var,
    }


def read_settings_screen(root):
    """Validate and persist settings-screen selections into app_state.

    Why: session startup should only proceed with clean, reusable config, so
    this function is the single gatekeeper for initials/options validity.
    """
    ui = app_state.get("ui", {})
    initials_var = ui.get("initials_var")
    prompt_vars = ui.get("prompt_vars", {})
    answer_vars = ui.get("answer_vars", {})
    mode_vars = ui.get("mode_vars", {})

    if initials_var is None:
        return False

    initials = initials_var.get().strip().upper()
    if not validate_initials(initials):
        set_settings_error("Initials must be exactly 3 letters.")
        return False

    prompt_fields = [field for field, var in prompt_vars.items() if var.get()]
    answer_fields = [field for field, var in answer_vars.items() if var.get()]

    answer_modes = {}
    for field in answer_fields:
        if field == "map":
            answer_modes[field] = "map-click"
        else:
            answer_modes[field] = mode_vars[field].get()

    valid, message = validate_settings(prompt_fields, answer_fields, answer_modes)
    if not valid:
        set_settings_error(message)
        return False

    app_state["user_initials"] = initials
    app_state["selected_prompt_fields"] = prompt_fields
    app_state["selected_answer_fields"] = answer_fields
    app_state["answer_modes"] = answer_modes
    set_settings_error("")
    return True


def start_session(root):
    """Initialize a new flashcard session and transition to gameplay.

    Why: resetting score, timer, deck order, and per-card flags in one place
    prevents stale data from a prior run affecting a new session.
    """
    if app_state["current_screen"] == "settings" and not read_settings_screen(root):
        return

    if app_state.get("timer_after_id") is not None:
        try:
            root.after_cancel(app_state["timer_after_id"])
        except tk.TclError:
            pass

    app_state["score"] = 0.0
    app_state["elapsed_time"] = 0.0
    app_state["current_card_index"] = 0
    app_state["session_start_time"] = time.time()
    app_state["selected_map_state"] = None
    app_state["submitted_current"] = False
    app_state["current_state_abbr"] = None

    app_state["deck_order"] = list(STATE_DATA)
    random.shuffle(app_state["deck_order"])

    build_flashcard_screen(root)
    display_flashcard(root)
    update_timer(root)


def build_flashcard_screen(root):
    """Build the main play screen with prompt/answer panes and map canvas.

    Why: this creates stable UI containers once, while display_flashcard only
    swaps card-specific content for efficiency and clearer control flow.
    """
    clear_screen(root)
    app_state["current_screen"] = "flashcards"

    outer = tk.Frame(root, padx=14, pady=14)
    outer.pack(fill="both", expand=True)

    top = tk.Frame(outer)
    top.pack(fill="x")

    card_var = tk.StringVar(value="Card 1 / 50")
    score_var = tk.StringVar(value="Score: 0.00")
    timer_var = tk.StringVar(value="Time Left: 05:00")

    tk.Label(top, textvariable=card_var, font=("Helvetica", 12, "bold")).pack(side="left")
    tk.Label(top, textvariable=score_var, font=("Helvetica", 12, "bold")).pack(side="left", padx=18)
    tk.Label(top, textvariable=timer_var, font=("Helvetica", 12, "bold")).pack(side="right")

    body = tk.Frame(outer)
    body.pack(fill="both", expand=True, pady=(12, 6))

    left = tk.Frame(body)
    left.pack(side="left", fill="both", expand=True, padx=(0, 10))

    prompt_frame = tk.LabelFrame(left, text="Prompt", padx=10, pady=8)
    prompt_frame.pack(fill="x")

    answer_frame = tk.LabelFrame(left, text="Your Answers", padx=10, pady=8)
    answer_frame.pack(fill="x", pady=(10, 0))

    feedback_var = tk.StringVar(value="")
    tk.Label(left, textvariable=feedback_var, fg="#1f5f9a", font=("Helvetica", 11, "bold"), justify="left").pack(anchor="w", pady=(10, 0))

    button_row = tk.Frame(left)
    button_row.pack(fill="x", pady=(14, 0))

    submit_btn = tk.Button(button_row, text="Submit", width=12, command=lambda: check_current_answers(root))
    submit_btn.pack(side="left")

    next_btn = tk.Button(button_row, text="Next", width=12, state="disabled", command=lambda: go_to_next_flashcard(root))
    next_btn.pack(side="left", padx=8)

    end_btn = tk.Button(button_row, text="End Session", width=12, command=lambda: end_session(root, timed_out=False))
    end_btn.pack(side="left")

    tk.Button(button_row, text="Back to Settings", width=16, command=lambda: build_settings_screen(root)).pack(side="right")

    right = tk.Frame(body)
    right.pack(side="left", fill="both", expand=True)

    map_hint_var = tk.StringVar(value="Map is interactive. Click a state when map location is an answer item.")
    tk.Label(right, textvariable=map_hint_var, font=("Helvetica", 10), justify="left", wraplength=380).pack(anchor="w", pady=(0, 6))

    map_canvas = tk.Canvas(right, width=720, height=540, bg="#ffffff", highlightthickness=1, highlightbackground="#c0c0c0")
    map_canvas.pack(fill="both", expand=True)

    app_state["ui"] = {
        "card_var": card_var,
        "score_var": score_var,
        "timer_var": timer_var,
        "prompt_frame": prompt_frame,
        "answer_frame": answer_frame,
        "feedback_var": feedback_var,
        "submit_btn": submit_btn,
        "next_btn": next_btn,
        "map_canvas": map_canvas,
        "map_hint_var": map_hint_var,
    }

    draw_map(root)


def draw_map(root):
    """Render all state polygons and wire click handlers on the map canvas.

    Why: map geometry is drawn from STATE_DATA at runtime so map interaction
    stays data-driven and consistent with the same state records used in quiz
    logic.
    """
    canvas = app_state.get("ui", {}).get("map_canvas")
    if canvas is None:
        return

    canvas.delete("all")
    app_state["map_polygon_items"] = {}

    canvas.create_rectangle(AK_LEFT - 2, AK_TOP - 2, AK_LEFT + AK_WIDTH + 2, AK_TOP + AK_HEIGHT + 2, outline="#b0b0b0", dash=(3, 3))
    canvas.create_rectangle(HI_LEFT - 2, HI_TOP - 2, HI_LEFT + HI_WIDTH + 2, HI_TOP + HI_HEIGHT + 2, outline="#b0b0b0", dash=(3, 3))

    for abbr, state in STATE_DATA.items():
        projector = projector_for_state(abbr)
        polygon_ids = []

        for polygon in state["map_data"]:
            flat = points_to_flat(polygon, projector)
            polygon_id = canvas.create_polygon(flat, fill=NORMAL_STATE_COLOR, outline=MAP_BORDER_COLOR, width=1, tags=("state", f"state_{abbr}"))
            polygon_ids.append(polygon_id)

        center_lon, center_lat = state["center"]
        cx, cy = projector(center_lon, center_lat)
        canvas.create_text(cx, cy, text=abbr, fill="#2e3440", font=("Helvetica", 7, "bold"), tags=("state", f"state_{abbr}"))

        app_state["map_polygon_items"][abbr] = polygon_ids
        canvas.tag_bind(f"state_{abbr}", "<Button-1>", lambda _event, a=abbr: handle_map_click(root, a))

    highlight_current_state(root)


def fill_state_on_map(abbr, color):
    """Apply a fill color to every polygon belonging to one state.

    Why: some states are multi-part polygons, so coloring by state abstraction
    avoids repeating polygon-loop details at each caller.
    """
    canvas = app_state.get("ui", {}).get("map_canvas")
    if canvas is None:
        return

    for polygon_id in app_state["map_polygon_items"].get(abbr, []):
        canvas.itemconfig(polygon_id, fill=color)


def highlight_current_state(root):
    """Refresh visual map highlights for prompt and selected answer state.

    Why: resetting all fills first then reapplying active highlights gives a
    predictable visual state and prevents stale highlights between cards.
    """
    for abbr in app_state["map_polygon_items"]:
        fill_state_on_map(abbr, NORMAL_STATE_COLOR)

    current_abbr = app_state.get("current_state_abbr")
    selected_map_state = app_state.get("selected_map_state")

    if "map" in app_state["selected_prompt_fields"] and current_abbr:
        fill_state_on_map(current_abbr, MAP_HIGHLIGHT_COLOR)

    if selected_map_state:
        fill_state_on_map(selected_map_state, SELECTED_STATE_COLOR)

    map_hint_var = app_state.get("ui", {}).get("map_hint_var")
    if map_hint_var is None:
        return

    if "map" in app_state["selected_answer_fields"] and selected_map_state:
        selected_name = STATE_DATA[selected_map_state]["name"]
        map_hint_var.set(f"Selected map answer: {selected_name} ({selected_map_state})")
    elif "map" in app_state["selected_answer_fields"]:
        map_hint_var.set("Map answer required: click a state on the map.")
    elif "map" in app_state["selected_prompt_fields"] and current_abbr:
        name = STATE_DATA[current_abbr]["name"]
        map_hint_var.set(f"Prompt map highlighted for: {name} ({current_abbr})")
    else:
        map_hint_var.set("Map is interactive. Click any state to inspect selection.")


def handle_map_click(root, clicked_state_abbr):
    """Record the clicked state as the map answer and refresh highlights.

    Why: map click handling stays intentionally lightweight so grading logic
    remains centralized in answer-check functions.
    """
    app_state["selected_map_state"] = clicked_state_abbr
    highlight_current_state(root)


def clear_children(widget):
    """Remove all child widgets from a container frame.

    Why: flashcard prompts/answers are rebuilt per card, so clearing only the
    relevant frame avoids reconstructing the whole window.
    """
    for child in widget.winfo_children():
        child.destroy()


def build_text_entry_answer(parent, label_text):
    """Create one labeled text-entry answer row and return its StringVar.

    Why: returning the Tk variable gives callers a simple, uniform way to read
    user input later during scoring.
    """
    row = tk.Frame(parent)
    row.pack(fill="x", pady=4)
    tk.Label(row, text=label_text, width=18, anchor="w").pack(side="left")

    value_var = tk.StringVar(value="")
    tk.Entry(row, textvariable=value_var, width=28).pack(side="left")
    return value_var


def build_dropdown_answer(parent, label_text, options):
    """Create one labeled drop-down answer row and return its StringVar.

    Why: a shared builder keeps text-entry and drop-down rows visually aligned
    while supporting multiple answer modes with minimal duplication.
    """
    row = tk.Frame(parent)
    row.pack(fill="x", pady=4)
    tk.Label(row, text=label_text, width=18, anchor="w").pack(side="left")

    values = ["Select..."] + options
    value_var = tk.StringVar(value="Select...")
    combo = ttk.Combobox(row, textvariable=value_var, values=values, state="readonly", width=25)
    combo.pack(side="left")
    return value_var


def display_flashcard(root):
    """Populate the gameplay UI with the current card's prompt/answer fields.

    What it does: updates counters, clears prior card widgets, prints selected
    prompt fields, and creates answer controls based on configured modes.
    Why: separating card rendering from screen construction keeps per-card
    refresh logic easy to reason about.
    """
    if app_state["current_card_index"] >= len(app_state["deck_order"]):
        end_session(root, timed_out=False)
        return

    current_abbr = app_state["deck_order"][app_state["current_card_index"]]
    app_state["current_state_abbr"] = current_abbr
    app_state["selected_map_state"] = None
    app_state["submitted_current"] = False

    ui = app_state["ui"]
    ui["next_btn"].config(state="disabled")
    ui["submit_btn"].config(state="normal")

    total_cards = len(app_state["deck_order"])
    card_number = app_state["current_card_index"] + 1
    ui["card_var"].set(f"Card {card_number} / {total_cards}")
    ui["score_var"].set(f"Score: {app_state['score']:.2f}")
    ui["feedback_var"].set("")

    prompt_frame = ui["prompt_frame"]
    answer_frame = ui["answer_frame"]
    clear_children(prompt_frame)
    clear_children(answer_frame)

    state = STATE_DATA[current_abbr]

    for field in app_state["selected_prompt_fields"]:
        if field == "map":
            text = "Map Location: highlighted on the map"
        else:
            text = f"{FIELD_LABELS[field]}: {field_value_for_state(field, current_abbr)}"
        tk.Label(prompt_frame, text=text, anchor="w", justify="left", font=("Helvetica", 11)).pack(fill="x", pady=2)

    app_state["current_answer_vars"] = {}

    for field in app_state["selected_answer_fields"]:
        label_text = FIELD_LABELS[field]

        if field == "map":
            tk.Label(answer_frame, text=f"{label_text}: click the map", anchor="w", justify="left", font=("Helvetica", 11)).pack(fill="x", pady=2)
            continue

        mode = app_state["answer_modes"].get(field, "text")
        if mode == "text":
            app_state["current_answer_vars"][field] = build_text_entry_answer(answer_frame, label_text)
        else:
            options = dropdown_options_for_field(field)
            app_state["current_answer_vars"][field] = build_dropdown_answer(answer_frame, label_text, options)

    highlight_current_state(root)


def max_points_for_current_card():
    """Compute the maximum possible score for the active card.

    Why: feedback uses this to show earned versus possible points, helping the
    learner understand scoring expectations per configured answer modes.
    """
    max_points = 0.0
    for field in app_state["selected_answer_fields"]:
        mode = app_state["answer_modes"].get(field, "map-click" if field == "map" else "text")
        if mode == "text":
            max_points += TYPED_ANSWER_POINTS
        else:
            max_points += MULTIPLE_CHOICE_POINTS
    return max_points


def check_current_answers(root):
    """Grade the current card, update score, and expose per-card feedback.

    Why: this keeps all answer extraction, missing-field detection, and point
    calculation in one place so scoring behavior is consistent across cards.
    """
    if app_state["submitted_current"]:
        return

    current_abbr = app_state.get("current_state_abbr")
    if current_abbr is None:
        return

    earned = 0.0
    missing_fields = []

    for field in app_state["selected_answer_fields"]:
        mode = app_state["answer_modes"].get(field, "map-click" if field == "map" else "text")
        correct_answer = field_value_for_state(field, current_abbr)

        if field == "map":
            user_answer = app_state.get("selected_map_state") or ""
        else:
            answer_var = app_state["current_answer_vars"].get(field)
            user_answer = answer_var.get().strip() if answer_var is not None else ""
            if user_answer == "Select...":
                user_answer = ""

        if not user_answer:
            missing_fields.append(FIELD_LABELS[field])

        earned += calculate_score(field, user_answer, correct_answer, mode)

    app_state["score"] += earned
    app_state["submitted_current"] = True

    ui = app_state["ui"]
    ui["score_var"].set(f"Score: {app_state['score']:.2f}")
    ui["submit_btn"].config(state="disabled")
    ui["next_btn"].config(state="normal")

    max_points = max_points_for_current_card()
    feedback = f"Card score: +{earned:.2f} / {max_points:.2f}."
    if missing_fields:
        feedback += " Missing: " + ", ".join(missing_fields)
    ui["feedback_var"].set(feedback)


def go_to_next_flashcard(root):
    """Advance to the next card, auto-submitting if needed.

    Why: forcing submission before advance ensures each card contributes to the
    final score and prevents accidental skipped grading.
    """
    if not app_state["submitted_current"]:
        check_current_answers(root)

    app_state["current_card_index"] += 1

    if app_state["current_card_index"] >= len(app_state["deck_order"]):
        end_session(root, timed_out=False)
        return

    display_flashcard(root)


def update_timer(root):
    """Update countdown display and end the session when time expires.

    Why: scheduled root.after ticks keep the UI responsive while enforcing a
    hard session cap without blocking the tkinter event loop.
    """
    if app_state["current_screen"] != "flashcards":
        return

    start = app_state.get("session_start_time")
    if start is None:
        return

    elapsed = time.time() - start
    app_state["elapsed_time"] = elapsed

    remaining = max(0, MAX_SESSION_LENGTH - int(elapsed))
    minutes, seconds = divmod(remaining, 60)

    timer_var = app_state.get("ui", {}).get("timer_var")
    if timer_var is not None:
        timer_var.set(f"Time Left: {minutes:02d}:{seconds:02d}")

    if remaining <= 0:
        end_session(root, timed_out=True)
        return

    app_state["timer_after_id"] = root.after(250, lambda: update_timer(root))


def end_session(root, timed_out=False):
    """Finalize timing/score, persist leaderboard entry, and show rankings.

    Why: centralizing session teardown guarantees timer cleanup, scoring
    normalization, and ranking writes happen consistently for every exit path.
    """
    timer_after_id = app_state.get("timer_after_id")
    if timer_after_id is not None:
        try:
            root.after_cancel(timer_after_id)
        except tk.TclError:
            pass
        app_state["timer_after_id"] = None

    if app_state["session_start_time"] is None:
        elapsed = app_state.get("elapsed_time", 0.0)
    else:
        elapsed = min(time.time() - app_state["session_start_time"], MAX_SESSION_LENGTH)

    app_state["elapsed_time"] = elapsed
    app_state["score"] = round(app_state["score"], 2)

    if app_state["user_initials"]:
        app_state["rankings"].append((app_state["user_initials"], elapsed, app_state["score"]))
        app_state["rankings"] = sort_rankings(app_state["rankings"])[:10]
        save_rankings(app_state["rankings"])

    if timed_out:
        message = "Time is up. Session ended automatically."
    elif app_state["current_card_index"] >= len(app_state["deck_order"]):
        message = "All flashcards completed."
    else:
        message = "Session ended by user."

    build_rankings_screen(root, result_message=message)


def format_ranking_row(rank, record):
    """Format one ranking tuple into display-ready strings.

    Why: table formatting is isolated so display rules are easy to tweak
    without touching ranking storage logic.
    """
    initials, elapsed, score = record
    return str(rank), initials.upper(), f"{elapsed:.1f}s", f"{score:.2f}"


def build_rankings_screen(root, result_message=""):
    """Render leaderboard and session summary after gameplay.

    Why: this screen combines current-run context with persistent top scores,
    giving immediate performance feedback before the next run.
    """
    clear_screen(root)
    app_state["current_screen"] = "rankings"

    container = tk.Frame(root, padx=20, pady=20)
    container.pack(fill="both", expand=True)

    tk.Label(container, text="Top Rankings", font=("Helvetica", 24, "bold")).pack(anchor="w")

    summary = f"Initials: {app_state['user_initials']}   Score: {app_state['score']:.2f}   Time: {app_state['elapsed_time']:.1f}s"
    tk.Label(container, text=summary, font=("Helvetica", 12)).pack(anchor="w", pady=(8, 4))

    if result_message:
        tk.Label(container, text=result_message, fg="#1f5f9a", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(0, 12))

    table = tk.Frame(container)
    table.pack(fill="x", pady=(0, 12))

    headers = ("Rank", "Initials", "Elapsed Time", "Score")
    widths = (8, 14, 18, 10)

    for idx, (header, width) in enumerate(zip(headers, widths)):
        tk.Label(table, text=header, width=width, anchor="w", font=("Helvetica", 11, "bold")).grid(row=0, column=idx, padx=2, pady=2)

    if not app_state["rankings"]:
        tk.Label(table, text="No rankings yet.", anchor="w", font=("Helvetica", 11)).grid(row=1, column=0, columnspan=4, sticky="w", padx=2, pady=4)
    else:
        for row_index, record in enumerate(app_state["rankings"][:10], start=1):
            row_values = format_ranking_row(row_index, record)
            for col_index, (value, width) in enumerate(zip(row_values, widths)):
                tk.Label(table, text=value, width=width, anchor="w", font=("Helvetica", 11)).grid(row=row_index, column=col_index, padx=2, pady=2)

    action_row = tk.Frame(container)
    action_row.pack(fill="x", pady=(10, 0))

    tk.Button(action_row, text="Back to Settings", width=16, command=lambda: build_settings_screen(root)).pack(side="left")
    tk.Button(action_row, text="Start New Session", width=16, command=lambda: start_session_from_rankings(root)).pack(side="left", padx=8)
    tk.Button(action_row, text="Quit", width=10, command=root.destroy).pack(side="right")


def start_session_from_rankings(root):
    """Start another run from rankings, or route to settings if unconfigured.

    Why: this preserves user-selected quiz configuration for quick retries but
    safely falls back when configuration is missing.
    """
    if not app_state["selected_prompt_fields"] or not app_state["selected_answer_fields"]:
        build_settings_screen(root)
        return

    start_session(root)


def setup_app(root):
    """Initialize persistent data and display the initial settings screen.

    Why: startup orchestration belongs in one function so __main__ stays small
    and the app boot sequence is easy to explain.
    """
    initialize_rankings_file()
    app_state["rankings"] = sort_rankings(load_rankings())[:10]
    build_settings_screen(root)


if __name__ == "__main__":
    app = create_main_window()
    setup_app(app)
    app.mainloop()
