import tkinter as tk
from tkinter import ttk

# =============================================================================
#  US STATE CAPITALS — Flash Card App
# =============================================================================
#  Two views:
#    Table  →  scrollable list of every state, abbreviation, and capital
#    Map    →  clickable outline map of the US; click a state to see details
# =============================================================================


# ── STATE DATA ────────────────────────────────────────────────────────────────
# Dictionary keyed by full state name.
# Each value holds the capital city and the 2-letter abbreviation.

states = {
    "Alabama":        {"capital": "Montgomery",    "abbreviation": "AL"},
    "Alaska":         {"capital": "Juneau",        "abbreviation": "AK"},
    "Arizona":        {"capital": "Phoenix",       "abbreviation": "AZ"},
    "Arkansas":       {"capital": "Little Rock",   "abbreviation": "AR"},
    "California":     {"capital": "Sacramento",    "abbreviation": "CA"},
    "Colorado":       {"capital": "Denver",        "abbreviation": "CO"},
    "Connecticut":    {"capital": "Hartford",      "abbreviation": "CT"},
    "Delaware":       {"capital": "Dover",         "abbreviation": "DE"},
    "Florida":        {"capital": "Tallahassee",   "abbreviation": "FL"},
    "Georgia":        {"capital": "Atlanta",       "abbreviation": "GA"},
    "Hawaii":         {"capital": "Honolulu",      "abbreviation": "HI"},
    "Idaho":          {"capital": "Boise",         "abbreviation": "ID"},
    "Illinois":       {"capital": "Springfield",   "abbreviation": "IL"},
    "Indiana":        {"capital": "Indianapolis",  "abbreviation": "IN"},
    "Iowa":           {"capital": "Des Moines",    "abbreviation": "IA"},
    "Kansas":         {"capital": "Topeka",        "abbreviation": "KS"},
    "Kentucky":       {"capital": "Frankfort",     "abbreviation": "KY"},
    "Louisiana":      {"capital": "Baton Rouge",   "abbreviation": "LA"},
    "Maine":          {"capital": "Augusta",       "abbreviation": "ME"},
    "Maryland":       {"capital": "Annapolis",     "abbreviation": "MD"},
    "Massachusetts":  {"capital": "Boston",        "abbreviation": "MA"},
    "Michigan":       {"capital": "Lansing",       "abbreviation": "MI"},
    "Minnesota":      {"capital": "Saint Paul",    "abbreviation": "MN"},
    "Mississippi":    {"capital": "Jackson",       "abbreviation": "MS"},
    "Missouri":       {"capital": "Jefferson City","abbreviation": "MO"},
    "Montana":        {"capital": "Helena",        "abbreviation": "MT"},
    "Nebraska":       {"capital": "Lincoln",       "abbreviation": "NE"},
    "Nevada":         {"capital": "Carson City",   "abbreviation": "NV"},
    "New Hampshire":  {"capital": "Concord",       "abbreviation": "NH"},
    "New Jersey":     {"capital": "Trenton",       "abbreviation": "NJ"},
    "New Mexico":     {"capital": "Santa Fe",      "abbreviation": "NM"},
    "New York":       {"capital": "Albany",        "abbreviation": "NY"},
    "North Carolina": {"capital": "Raleigh",       "abbreviation": "NC"},
    "North Dakota":   {"capital": "Bismarck",      "abbreviation": "ND"},
    "Ohio":           {"capital": "Columbus",      "abbreviation": "OH"},
    "Oklahoma":       {"capital": "Oklahoma City", "abbreviation": "OK"},
    "Oregon":         {"capital": "Salem",         "abbreviation": "OR"},
    "Pennsylvania":   {"capital": "Harrisburg",    "abbreviation": "PA"},
    "Rhode Island":   {"capital": "Providence",    "abbreviation": "RI"},
    "South Carolina": {"capital": "Columbia",      "abbreviation": "SC"},
    "South Dakota":   {"capital": "Pierre",        "abbreviation": "SD"},
    "Tennessee":      {"capital": "Nashville",     "abbreviation": "TN"},
    "Texas":          {"capital": "Austin",        "abbreviation": "TX"},
    "Utah":           {"capital": "Salt Lake City","abbreviation": "UT"},
    "Vermont":        {"capital": "Montpelier",    "abbreviation": "VT"},
    "Virginia":       {"capital": "Richmond",      "abbreviation": "VA"},
    "Washington":     {"capital": "Olympia",       "abbreviation": "WA"},
    "West Virginia":  {"capital": "Charleston",    "abbreviation": "WV"},
    "Wisconsin":      {"capital": "Madison",       "abbreviation": "WI"},
    "Wyoming":        {"capital": "Cheyenne",      "abbreviation": "WY"},
}

# Quick lookup: "AL" → "Alabama"
abbrev_to_name = {info["abbreviation"]: name for name, info in states.items()}


# ── STATE OUTLINE DATA ────────────────────────────────────────────────────────
# Each state's border is stored as a list of (longitude, latitude) points.
#   • Longitude: negative numbers, larger magnitude = further west
#   • Latitude:  positive numbers, larger = further north
#
# Simple rectangular states only need 4 corner points.
# States with complex coastlines or river borders need more points.
#
# Michigan is a special case — it has two separate land masses
# (upper and lower peninsula), so its value is a LIST of two point-lists.
#
# Alaska and Hawaii are stored separately below because they need
# their own projection (they're far outside the main map area).

state_shapes = {

    # ── NORTHWEST ────────────────────────────────────────────
    "WA": [(-124.73, 48.48), (-117.03, 49.00), (-117.03, 46.00),
           (-119.00, 45.80), (-124.14, 45.56), (-124.73, 46.20)],

    "OR": [(-124.55, 46.23), (-123.72, 46.18), (-117.03, 46.00),
           (-117.03, 42.00), (-124.55, 42.00)],

    "CA": [
        (-124.41, 42.00), (-124.30, 41.50), (-124.20, 41.00),
        (-124.10, 40.50), (-124.00, 40.00), (-123.90, 39.50),
        (-123.70, 39.00), (-123.50, 38.50), (-123.20, 38.00),
        (-122.90, 37.70), (-122.60, 37.40), (-122.40, 37.10),
        (-122.30, 36.80), (-122.00, 36.50), (-121.80, 36.20),
        (-121.50, 35.80), (-121.20, 35.40), (-120.90, 35.00),
        (-120.50, 34.70), (-120.00, 34.40), (-119.50, 34.10),
        (-119.00, 33.80), (-118.50, 33.50), (-118.00, 33.20),
        (-117.60, 32.90), (-117.30, 32.70), (-117.24, 32.53),

        (-114.63, 32.53), (-114.63, 35.00), (-119.99, 39.00),
        (-120.00, 42.00)
    ],

    # ── MOUNTAIN ─────────────────────────────────────────────
    "NV": [(-120.00, 42.00), (-114.05, 42.00), (-114.05, 37.00),
           (-114.63, 35.00), (-120.00, 39.00)],

    "ID": [(-117.03, 44.00), (-117.03, 49.00), (-111.05, 49.00),
           (-111.05, 42.00), (-114.05, 42.00), (-116.05, 44.00)],

    "MT": [(-116.05, 49.00), (-104.04, 49.00),
           (-104.04, 44.36), (-116.05, 44.36)],

    "WY": [(-111.05, 45.00), (-104.05, 45.00),
           (-104.05, 41.00), (-111.05, 41.00)],

    "CO": [(-109.05, 41.00), (-102.05, 41.00),
           (-102.05, 37.00), (-109.05, 37.00)],

    "UT": [(-114.05, 42.00), (-111.05, 42.00), (-111.05, 41.00),
           (-109.05, 41.00), (-109.05, 37.00), (-114.05, 37.00)],

    "AZ": [(-114.82, 37.00), (-109.05, 37.00), (-109.05, 31.33),
           (-111.07, 31.33), (-114.82, 32.49)],

    # New Mexico has a notched bottom-left corner (the "boot heel")
    "NM": [(-109.05, 37.00), (-103.00, 37.00), (-103.00, 32.00),
           (-106.62, 32.00), (-106.62, 31.78), (-108.21, 31.78),
           (-108.21, 31.33), (-109.05, 31.33)],

    # ── GREAT PLAINS ─────────────────────────────────────────
    "ND": [(-104.05, 49.00), (-96.56, 48.99), (-97.00, 46.93),
           (-96.56, 46.63), (-104.05, 45.93)],

    "SD": [(-104.05, 45.93), (-96.44, 45.93),
           (-96.44, 43.00), (-104.05, 43.00)],

    "NE": [(-104.05, 43.00), (-102.05, 43.00), (-102.05, 40.00),
           (-95.31, 40.00), (-95.37, 42.49), (-96.48, 43.00)],

    "KS": [(-102.05, 40.00), (-94.62, 40.00),
           (-94.62, 37.00), (-102.05, 37.00)],

    # Oklahoma has a rectangular panhandle sticking out to the west
    "OK": [(-103.00, 37.00), (-100.00, 37.00), (-100.00, 36.50),
           (-94.43, 36.50), (-94.43, 33.64), (-103.00, 33.64)],

    # Texas is one of the most complex shapes: panhandle at top,
    # wide body, Gulf Coast at bottom, and the Rio Grande on the west
    "TX": [
        (-106.62, 32.00), (-105.50, 31.80), (-104.50, 31.50),
        (-103.50, 31.00), (-102.50, 30.50), (-101.50, 30.00),
        (-100.50, 29.50), (-99.50, 28.80), (-98.50, 27.80),
        (-97.80, 26.80), (-97.20, 25.90), (-97.00, 25.84),

        (-96.50, 26.50), (-96.00, 27.50), (-95.50, 28.50),
        (-95.00, 29.50), (-94.50, 30.00), (-94.00, 30.00),

        (-94.43, 36.50), (-100.00, 36.50), (-100.00, 37.00),
        (-103.00, 37.00), (-103.00, 32.00)
    ],

    # ── MIDWEST ──────────────────────────────────────────────
    "MN": [(-97.24, 43.50), (-89.49, 43.50), (-89.49, 45.30),
           (-92.01, 46.71), (-89.49, 48.00), (-90.00, 49.00),
           (-97.24, 49.00)],

    "IA": [(-96.60, 43.50), (-90.15, 43.50), (-90.15, 40.38),
           (-95.86, 40.38), (-96.60, 43.10)],

    "MO": [(-95.77, 40.59), (-91.73, 40.61), (-89.52, 37.00),
           (-89.13, 36.62), (-94.62, 36.50), (-95.77, 36.50)],

    "AR": [(-94.62, 36.50), (-90.15, 36.50), (-90.30, 35.43),
           (-90.07, 35.00), (-91.09, 33.00), (-94.04, 33.01)],

    "LA": [(-94.04, 33.01), (-89.73, 33.00), (-89.73, 30.20),
           (-89.00, 29.00), (-90.00, 29.00), (-90.40, 29.88),
           (-91.40, 29.30), (-92.60, 29.60), (-93.80, 29.84),
           (-93.90, 30.20), (-94.04, 30.00)],

    # ── GREAT LAKES ──────────────────────────────────────────
    "WI": [(-92.89, 47.08), (-86.81, 47.08), (-87.03, 45.50),
           (-87.80, 45.20), (-87.03, 42.50), (-90.64, 42.50),
           (-92.89, 44.00)],

    # Michigan has two separate land masses, so we store TWO point lists
    "MI": [
        # Lower Peninsula (the "mitten")
        [(-86.60, 41.77), (-82.43, 41.77), (-82.43, 43.00),
         (-83.45, 44.00), (-83.80, 44.77), (-84.00, 45.77),
         (-85.56, 45.77), (-86.60, 44.50)],
        # Upper Peninsula
        [(-90.42, 45.77), (-84.50, 45.77), (-84.50, 46.00),
         (-84.00, 46.50), (-84.50, 47.00), (-88.00, 48.19),
         (-90.42, 48.19)],
    ],

    "IL": [(-91.51, 42.51), (-87.80, 42.49), (-87.80, 37.00),
           (-89.20, 37.00), (-91.51, 40.00)],

    "IN": [(-88.10, 41.77), (-84.81, 41.77),
           (-84.81, 37.77), (-88.10, 37.77)],

    "OH": [(-84.82, 42.00), (-80.52, 42.00),
           (-80.52, 38.40), (-84.82, 38.40)],

    # ── SOUTH ────────────────────────────────────────────────
    "MS": [(-91.65, 35.00), (-88.10, 34.99), (-88.10, 30.24),
           (-88.47, 30.24), (-91.65, 30.99)],

    "AL": [(-88.47, 34.99), (-85.61, 34.99), (-85.18, 32.87),
           (-84.89, 32.26), (-88.10, 30.24), (-88.47, 31.00)],

    "TN": [(-90.31, 36.50), (-81.65, 36.59),
           (-81.65, 35.00), (-90.31, 35.00)],

    # Kentucky's north border follows the Ohio River (hence the curves)
    "KY": [(-89.57, 36.50), (-89.57, 37.90), (-87.50, 37.90),
           (-84.82, 39.10), (-82.60, 38.60), (-81.97, 37.54),
           (-84.30, 36.60)],

    "GA": [(-85.61, 34.99), (-83.11, 35.00), (-83.00, 34.00),
           (-81.00, 32.00), (-81.00, 30.36), (-84.90, 30.36),
           (-85.18, 32.87)],

    # Florida has a long peninsula — needs many points to look right
    "FL": [
        (-87.63, 30.99), (-86.80, 30.90), (-86.00, 30.80),
        (-85.20, 30.70), (-84.90, 30.10), (-84.50, 29.80),
        (-84.00, 29.60), (-83.50, 29.40), (-83.00, 29.20),
        (-82.50, 28.90), (-82.00, 28.50), (-81.50, 28.00),
        (-81.00, 27.50), (-80.60, 27.00), (-80.30, 26.50),
        (-80.10, 26.00), (-80.03, 25.13),

        (-80.30, 25.50), (-80.80, 26.00), (-81.50, 26.50),
        (-82.30, 27.00), (-82.65, 28.00), (-83.00, 29.50),
        (-84.00, 30.00), (-85.00, 31.00)
    ],

    "SC": [(-83.36, 35.20), (-78.55, 33.85), (-79.68, 32.00),
           (-81.12, 31.00), (-81.40, 31.70), (-83.36, 32.00)],

    "NC": [(-84.32, 36.59), (-75.46, 36.55), (-75.46, 35.20),
           (-76.50, 34.80), (-77.50, 34.20), (-78.00, 33.90),
           (-84.32, 35.00)],

    "VA": [(-83.68, 37.30), (-76.00, 38.00), (-75.24, 37.89),
           (-75.24, 36.55), (-79.00, 36.54), (-83.68, 36.60)],

    # West Virginia is one of the most irregular shapes in the US
    "WV": [(-82.64, 40.64), (-80.52, 40.64), (-79.46, 39.72),
           (-77.72, 39.46), (-77.72, 37.40), (-79.00, 37.00),
           (-81.97, 37.24), (-82.64, 38.18)],

    # ── MID-ATLANTIC ─────────────────────────────────────────
    "MD": [(-79.49, 39.72), (-75.79, 39.72), (-75.25, 38.45),
           (-76.00, 38.00), (-77.00, 38.35), (-79.49, 39.20)],

    "PA": [(-80.52, 42.27), (-74.70, 42.27),
           (-74.70, 39.72), (-80.52, 39.72)],

    "NJ": [(-75.56, 41.36), (-74.01, 41.36),
           (-74.01, 39.00), (-75.56, 39.00)],

    "DE": [(-75.79, 39.84), (-75.05, 39.84),
           (-75.05, 38.45), (-75.79, 38.45)],

    "NY": [(-79.76, 43.00), (-73.77, 45.01), (-71.51, 45.01),
           (-73.54, 40.75), (-74.25, 41.00), (-76.00, 42.00),
           (-79.76, 42.27)],

    # ── NEW ENGLAND ──────────────────────────────────────────
    "CT": [(-73.73, 42.05), (-71.80, 42.02),
           (-71.80, 41.00), (-73.73, 41.00)],

    "RI": [(-71.86, 42.02), (-71.12, 42.02),
           (-71.12, 41.30), (-71.86, 41.30)],

    "MA": [(-73.51, 42.79), (-69.93, 42.09),
           (-69.93, 41.50), (-73.51, 41.50)],

    "VT": [(-73.44, 45.01), (-71.51, 45.01),
           (-72.46, 43.58), (-73.44, 43.58)],

    "NH": [(-72.56, 45.31), (-70.70, 43.73),
           (-70.70, 43.00), (-72.56, 43.00)],

    "ME": [(-71.08, 43.08), (-71.08, 45.31), (-70.65, 47.40),
           (-69.23, 47.45), (-67.79, 47.06), (-67.00, 44.00)],
}

# Alaska — drawn in its own small inset box in the bottom-left corner.
# Uses real coordinates but a different (smaller) projection.
alaska_shape = [
    (-167.00, 55.00), (-160.00, 54.50), (-153.00, 56.50),
    (-148.00, 59.50), (-136.00, 57.00), (-130.00, 55.50),
    (-141.00, 60.00), (-141.00, 70.50), (-156.00, 71.50),
    (-163.00, 67.50), (-168.00, 66.00),
]

# Hawaii — multiple islands, so each island is its own mini-polygon.
# Listed roughly east (Big Island) to west (Kauai).
hawaii_islands = [
    [(-156.05, 18.92), (-154.82, 18.92), (-154.82, 20.27), (-156.05, 20.27)],  # Big Island
    [(-156.70, 20.52), (-155.95, 20.52), (-155.95, 21.03), (-156.70, 21.03)],  # Maui
    [(-157.30, 21.00), (-156.70, 21.00), (-156.70, 21.22), (-157.30, 21.22)],  # Molokai
    [(-158.30, 21.23), (-157.65, 21.23), (-157.65, 21.72), (-158.30, 21.72)],  # Oahu
    [(-159.79, 21.84), (-159.28, 21.84), (-159.28, 22.23), (-159.79, 22.23)],  # Kauai
]

# Manual label positions (lon, lat) for states whose centroid looks off.
# For most states the centroid is calculated automatically (see polygon_center).
LABEL_OVERRIDES = {
    "OK": (-97.50, 35.30),  # panhandle pulls automatic center too far west
    "TX": (-99.30, 31.20),  # very large state; manual is more readable
    "FL": (-83.50, 28.00),  # peninsula shape throws off the centroid
    "ME": (-69.20, 45.30),  # jagged coast; centroid ends up in the ocean
    "MI": (-85.00, 43.50),  # use lower-peninsula center, not the average of both
    "MN": (-94.30, 46.40),  # northern arm pulls center too high
    "KY": (-85.30, 37.50),  # irregular shape
    "WV": (-80.60, 38.80),  # very irregular shape
    "VA": (-79.40, 37.50),  # long narrow state
    "NC": (-80.00, 35.50),  # long narrow state
    "TN": (-86.30, 35.90),  # long narrow state
    "NY": (-75.80, 43.00),  # panhandle pulls center east
    "LA": (-92.40, 31.00),  # Gulf Coast shape
    "MD": (-77.00, 39.30),  # small and irregular
}


# ── PROJECTION FUNCTIONS ──────────────────────────────────────────────────────
# A "projection" converts real-world longitude/latitude into canvas x/y pixels.
#
# For the main map we stretch the contiguous US to fit a rectangle.
# Think of it like pressing a world map flat into a box.

# The bounding box of the contiguous 48 states (in degrees)
WEST,  EAST  = -125.0, -66.5   # leftmost / rightmost longitude
SOUTH, NORTH =   24.0,  50.0   # southernmost / northernmost latitude

# Where on the canvas the map is drawn
MAP_LEFT, MAP_TOP    =  15,  10   # top-left corner (pixels)
MAP_WIDTH, MAP_HEIGHT = 720, 430  # size of the map area (pixels)


def to_canvas(lon, lat):
    """
    Convert (longitude, latitude) to canvas (x, y) pixel coordinates.

    Longitude increases east  → maps to increasing x (left → right).
    Latitude  increases north → maps to decreasing y (top  → bottom),
    because on a canvas y=0 is at the TOP, not the bottom.
    """
    x = MAP_LEFT + (lon - WEST)   / (EAST  - WEST)  * MAP_WIDTH
    y = MAP_TOP  + (NORTH - lat)  / (NORTH - SOUTH) * MAP_HEIGHT
    return x, y


def points_to_flat(point_list):
    """
    Tkinter's create_polygon expects a flat list: [x1, y1, x2, y2, ...].
    This converts our (lon, lat) pairs into that format.
    """
    flat = []
    for lon, lat in point_list:
        x, y = to_canvas(lon, lat)
        flat.append(x)
        flat.append(y)
    return flat


def polygon_center(point_list):
    """
    Return the average longitude and latitude of a polygon's points.
    Used to decide where to place the state abbreviation label.
    """
    avg_lon = sum(lon for lon, _ in point_list) / len(point_list)
    avg_lat = sum(lat for _, lat in point_list) / len(point_list)
    return avg_lon, avg_lat


# ── ALASKA & HAWAII INSET PROJECTIONS ────────────────────────────────────────
# These states sit far outside the main map, so we draw them in small
# corner boxes with their own separate coordinate ranges.

# Alaska inset — bottom-left corner of the canvas
AK_LEFT,  AK_TOP    =  15, 450   # inset box position
AK_WIDTH, AK_HEIGHT = 150,  90   # inset box size
AK_WEST,  AK_EAST   = -170.0, -130.0
AK_SOUTH, AK_NORTH  =   54.0,   72.0


def to_canvas_ak(lon, lat):
    x = AK_LEFT + (lon - AK_WEST)   / (AK_EAST  - AK_WEST)  * AK_WIDTH
    y = AK_TOP  + (AK_NORTH - lat)  / (AK_NORTH - AK_SOUTH) * AK_HEIGHT
    return x, y


# Hawaii inset — just to the right of Alaska
HI_LEFT,  HI_TOP    = 174, 458   # inset box position
HI_WIDTH, HI_HEIGHT = 100,  68   # inset box size
HI_WEST,  HI_EAST   = -161.0, -154.5
HI_SOUTH, HI_NORTH  =   18.8,   22.5


def to_canvas_hi(lon, lat):
    x = HI_LEFT + (lon - HI_WEST)   / (HI_EAST  - HI_WEST)  * HI_WIDTH
    y = HI_TOP  + (HI_NORTH - lat)  / (HI_NORTH - HI_SOUTH) * HI_HEIGHT
    return x, y


def inset_flat(point_list, proj_fn):
    """Same as points_to_flat but uses a custom projection function."""
    flat = []
    for lon, lat in point_list:
        x, y = proj_fn(lon, lat)
        flat.append(x)
        flat.append(y)
    return flat


# ── COLORS ───────────────────────────────────────────────────────────────────
BG_DARK       = "#1e1e2e"   # main window background
BG_DARKER     = "#181825"   # nav bar / alternating table rows / map canvas
ACCENT_BLUE   = "#89b4fa"   # highlighted button / column headers
ACCENT_GREEN  = "#a6e3a1"   # info bar text
TEXT_LIGHT    = "#cdd6f4"   # general text
TEXT_DIM      = "#585b70"   # secondary / muted text
TILE_DEFAULT  = "#313244"   # state fill color (normal)
TILE_HOVER    = "#45475a"   # state fill color (mouse-over)
TILE_OUTLINE  = "#585b70"   # border between states


# ── WINDOW ───────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("US State Capitals")
root.geometry("780x700")
root.configure(bg=BG_DARK)
root.resizable(False, False)


# ── NAVIGATION BAR ───────────────────────────────────────────────────────────
nav_frame = tk.Frame(root, bg=BG_DARKER, pady=6)
nav_frame.pack(fill="x")

# Two content frames; only one is visible at a time
table_frame = tk.Frame(root, bg=BG_DARK)
map_frame   = tk.Frame(root, bg=BG_DARK)


def show_table():
    """Switch to the table view."""
    map_frame.pack_forget()
    table_frame.pack(fill="both", expand=True)
    table_btn.configure(bg=ACCENT_BLUE, fg=BG_DARK)
    map_btn.configure(bg=TILE_DEFAULT, fg=TEXT_LIGHT)


def show_map():
    """Switch to the map view."""
    table_frame.pack_forget()
    map_frame.pack(fill="both", expand=True)
    map_btn.configure(bg=ACCENT_BLUE, fg=BG_DARK)
    table_btn.configure(bg=TILE_DEFAULT, fg=TEXT_LIGHT)


table_btn = tk.Button(nav_frame, text="  Table  ", command=show_table,
                      bg=ACCENT_BLUE, fg=BG_DARK, font=("Helvetica", 11, "bold"),
                      relief="flat", cursor="hand2", padx=10)
table_btn.pack(side="left", padx=(12, 4))

map_btn = tk.Button(nav_frame, text="  Map  ", command=show_map,
                    bg=TILE_DEFAULT, fg=TEXT_LIGHT, font=("Helvetica", 11, "bold"),
                    relief="flat", cursor="hand2", padx=10)
map_btn.pack(side="left", padx=4)


# ── TABLE VIEW ───────────────────────────────────────────────────────────────
tk.Label(table_frame, text="US State Capitals", font=("Helvetica", 20, "bold"),
         bg=BG_DARK, fg=TEXT_LIGHT).pack(pady=(16, 8))

# Outer container for the canvas + scrollbar pair
table_container = tk.Frame(table_frame, bg=BG_DARK)
table_container.pack(fill="both", expand=True, padx=16, pady=8)

table_canvas = tk.Canvas(table_container, bg=BG_DARK, highlightthickness=0)
table_scroll  = ttk.Scrollbar(table_container, orient="vertical",
                               command=table_canvas.yview)
table_inner   = tk.Frame(table_canvas, bg=BG_DARK)

# When rows are added, update how far the user can scroll
table_inner.bind("<Configure>",
                 lambda e: table_canvas.configure(
                     scrollregion=table_canvas.bbox("all")))

table_canvas.create_window((0, 0), window=table_inner, anchor="nw")
table_canvas.configure(yscrollcommand=table_scroll.set)

table_canvas.pack(side="left", fill="both", expand=True)
table_scroll.pack(side="right", fill="y")

# Column header row
headers    = ["#", "State", "Abbreviation", "Capital"]
col_widths = [3, 22, 14, 20]

for col, (header, width) in enumerate(zip(headers, col_widths)):
    tk.Label(table_inner, text=header, font=("Helvetica", 11, "bold"),
             bg=TILE_DEFAULT, fg=ACCENT_BLUE, width=width, anchor="w",
             padx=8, pady=6).grid(row=0, column=col, sticky="ew",
                                  padx=1, pady=(0, 2))

# One row per state, sorted A–Z, with alternating row backgrounds
for i, (state_name, info) in enumerate(sorted(states.items()), start=1):
    row_bg   = BG_DARK if i % 2 == 0 else BG_DARKER
    row_data = [str(i), state_name, info["abbreviation"], info["capital"]]

    for col, (value, width) in enumerate(zip(row_data, col_widths)):
        tk.Label(table_inner, text=value, font=("Helvetica", 10),
                 bg=row_bg, fg=TEXT_LIGHT, width=width, anchor="w",
                 padx=8, pady=5).grid(row=i, column=col, sticky="ew",
                                      padx=1, pady=1)

# Mouse-wheel scrolling for the table
root.bind("<MouseWheel>",
          lambda e: table_canvas.yview_scroll(-1 * (e.delta // 120), "units"))


# ── MAP VIEW ─────────────────────────────────────────────────────────────────
tk.Label(map_frame, text="US State Map", font=("Helvetica", 18, "bold"),
         bg=BG_DARK, fg=TEXT_LIGHT).pack(pady=(12, 4))

# Info bar — updated when the user clicks a state
info_var = tk.StringVar(value="Click a state to see its capital")
tk.Label(map_frame, textvariable=info_var, font=("Helvetica", 12),
         bg=TILE_DEFAULT, fg=ACCENT_GREEN, padx=12, pady=6).pack(
    fill="x", padx=20, pady=(0, 6))

# The canvas is where all the state polygons are drawn
map_canvas = tk.Canvas(map_frame, bg=BG_DARKER, highlightthickness=0,
                       width=755, height=555)
map_canvas.pack(padx=10)

# This dictionary maps each abbreviation to the list of canvas items
# that belong to that state (polygons + label text).
# We need it so we can highlight all pieces of a state on hover.
state_items = {}   # e.g. {"FL": [polygon_id, text_id], "MI": [poly1, poly2, text_id]}


# ── MAP EVENT HANDLERS ───────────────────────────────────────────────────────

def on_state_click(abbrev):
    """Show the clicked state's full name and capital in the info bar."""
    full_name = abbrev_to_name[abbrev]
    capital   = states[full_name]["capital"]
    info_var.set(f"  {full_name}  ({abbrev})  —  Capital: {capital}")


def on_enter(abbrev):
    """Highlight the state when the mouse moves over it."""
    for item_id in state_items[abbrev]:
        if map_canvas.type(item_id) == "polygon":
            map_canvas.itemconfig(item_id, fill=TILE_HOVER)


def on_leave(abbrev):
    """Remove the highlight when the mouse leaves the state."""
    for item_id in state_items[abbrev]:
        if map_canvas.type(item_id) == "polygon":
            map_canvas.itemconfig(item_id, fill=TILE_DEFAULT)


def attach_events(abbrev, item_ids):
    """Connect the three mouse events to every canvas item for one state."""
    for item_id in item_ids:
        # tkinter always passes an event object to callbacks,
        # but we don't need it here — so we name it _ to show that.
        map_canvas.tag_bind(item_id, "<Button-1>",
                            lambda _, a=abbrev: on_state_click(a))
        map_canvas.tag_bind(item_id, "<Enter>",
                            lambda _, a=abbrev: on_enter(a))
        map_canvas.tag_bind(item_id, "<Leave>",
                            lambda _, a=abbrev: on_leave(a))


# ── DRAW CONTIGUOUS 48 STATES ────────────────────────────────────────────────

for abbrev, shape in state_shapes.items():

    # Michigan stores a list of TWO point-lists (two peninsulas).
    # Every other state stores a single flat list of points.
    # We normalise both cases into a list-of-polygons so the loop below
    # works the same way for every state.
    if isinstance(shape[0], list):
        polygons = shape            # Michigan: already [[points], [points]]
    else:
        polygons = [shape]          # Normal state: wrap in a list → [[points]]

    items = []

    for point_list in polygons:
        flat_coords = points_to_flat(point_list)
        poly_id = map_canvas.create_polygon(flat_coords,
                                            fill=TILE_DEFAULT,
                                            outline=TILE_OUTLINE,
                                            width=1)
        items.append(poly_id)

    # Place the abbreviation label at the state's center.
    # Use a manual override if one is defined; otherwise compute the centroid.
    if abbrev in LABEL_OVERRIDES:
        label_lon, label_lat = LABEL_OVERRIDES[abbrev]
    else:
        label_lon, label_lat = polygon_center(polygons[0])

    lx, ly   = to_canvas(label_lon, label_lat)
    label_id = map_canvas.create_text(lx, ly, text=abbrev,
                                      fill=TEXT_LIGHT,
                                      font=("Helvetica", 7, "bold"))
    items.append(label_id)

    state_items[abbrev] = items
    attach_events(abbrev, items)


# ── DRAW ALASKA INSET ────────────────────────────────────────────────────────

# Dashed border box so it's clear this is an inset, not part of the main map
map_canvas.create_rectangle(AK_LEFT - 2, AK_TOP - 2,
                            AK_LEFT + AK_WIDTH + 2, AK_TOP + AK_HEIGHT + 2,
                            fill="", outline=TEXT_DIM, width=1, dash=(3, 3))

ak_flat   = inset_flat(alaska_shape, to_canvas_ak)
ak_poly   = map_canvas.create_polygon(ak_flat, fill=TILE_DEFAULT,
                                      outline=TILE_OUTLINE, width=1)
ak_label  = map_canvas.create_text(AK_LEFT + AK_WIDTH // 2,
                                   AK_TOP  + AK_HEIGHT // 2,
                                   text="AK", fill=TEXT_LIGHT,
                                   font=("Helvetica", 8, "bold"))
map_canvas.create_text(AK_LEFT + AK_WIDTH // 2, AK_TOP + AK_HEIGHT + 9,
                       text="Alaska", fill=TEXT_DIM, font=("Helvetica", 7))

state_items["AK"] = [ak_poly, ak_label]
attach_events("AK", state_items["AK"])


# ── DRAW HAWAII INSET ────────────────────────────────────────────────────────

map_canvas.create_rectangle(HI_LEFT - 2, HI_TOP - 2,
                            HI_LEFT + HI_WIDTH + 2, HI_TOP + HI_HEIGHT + 2,
                            fill="", outline=TEXT_DIM, width=1, dash=(3, 3))

hi_items = []
for island_points in hawaii_islands:
    hi_flat  = inset_flat(island_points, to_canvas_hi)
    island_poly = map_canvas.create_polygon(hi_flat, fill=TILE_DEFAULT,
                                            outline=TILE_OUTLINE, width=1)
    hi_items.append(island_poly)

hi_label = map_canvas.create_text(HI_LEFT + HI_WIDTH // 2,
                                  HI_TOP  + HI_HEIGHT // 2,
                                  text="HI", fill=TEXT_LIGHT,
                                  font=("Helvetica", 8, "bold"))
hi_items.append(hi_label)
map_canvas.create_text(HI_LEFT + HI_WIDTH // 2, HI_TOP + HI_HEIGHT + 9,
                       text="Hawaii", fill=TEXT_DIM, font=("Helvetica", 7))

state_items["HI"] = hi_items
attach_events("HI", hi_items)


# ── START ─────────────────────────────────────────────────────────────────────
show_table()        # open on the table view by default
root.mainloop()     # hand control to tkinter; keeps the window open
