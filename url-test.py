import tkinter as tk        # the main GUI library — windows, buttons, canvas, etc.
from tkinter import ttk    # "Themed Tkinter" — a submodule with nicer-looking widgets (we use it for the scrollbar)
import json                # built-in Python library for reading/writing JSON data
import urllib.request      # built-in library for downloading files from the internet
import threading           # lets us run the download in the background so the window doesn't freeze
import ssl                 # handles secure HTTPS connections; we use it to fix a Mac certificate issue

# On some Macs, Python's SSL certificates aren't set up automatically.
# This creates an unverified context so the download still works.
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode    = ssl.CERT_NONE

# =============================================================================
#  US STATE CAPITALS — Flash Card App  (url-test version)
# =============================================================================
#  Same as state-capitals.py but the map data is fetched from a public URL
#  instead of being embedded in this file.
#
#  Requires: Python 3 (standard library only — no pip installs)
#  Requires: Internet connection (to download the map boundary data once)
# =============================================================================


# ── STATE DATA ────────────────────────────────────────────────────────────────
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

abbrev_to_name = {info["abbreviation"]: name for name, info in states.items()}

# Needed to look up abbreviation from the GeoJSON "name" property
name_to_abbrev = {name: info["abbreviation"] for name, info in states.items()}


# ── PROJECTION FUNCTIONS ──────────────────────────────────────────────────────
WEST,  EAST  = -125.0, -66.5
SOUTH, NORTH =   24.0,  50.0
MAP_LEFT, MAP_TOP    =  15,  10
MAP_WIDTH, MAP_HEIGHT = 720, 430

def to_canvas(lon, lat):
    """Convert (longitude, latitude) → canvas (x, y) pixels for main map."""
    x = MAP_LEFT + (lon - WEST)  / (EAST  - WEST)  * MAP_WIDTH
    y = MAP_TOP  + (NORTH - lat) / (NORTH - SOUTH) * MAP_HEIGHT
    return x, y

# Alaska inset — bottom-left corner
AK_LEFT,  AK_TOP    =  15, 450
AK_WIDTH, AK_HEIGHT = 150,  90
AK_WEST,  AK_EAST   = -170.0, -130.0
AK_SOUTH, AK_NORTH  =   54.0,  72.0

def to_canvas_ak(lon, lat):
    x = AK_LEFT + (lon - AK_WEST)  / (AK_EAST  - AK_WEST)  * AK_WIDTH
    y = AK_TOP  + (AK_NORTH - lat) / (AK_NORTH - AK_SOUTH) * AK_HEIGHT
    return x, y

# Hawaii inset — right of Alaska
HI_LEFT,  HI_TOP    = 174, 458
HI_WIDTH, HI_HEIGHT = 100,  68
HI_WEST,  HI_EAST   = -161.0, -154.5
HI_SOUTH, HI_NORTH  =   18.8,  22.5

def to_canvas_hi(lon, lat):
    x = HI_LEFT + (lon - HI_WEST)  / (HI_EAST  - HI_WEST)  * HI_WIDTH
    y = HI_TOP  + (HI_NORTH - lat) / (HI_NORTH - HI_SOUTH) * HI_HEIGHT
    return x, y


# ── LABEL OVERRIDES ───────────────────────────────────────────────────────────
# States where the automatic centroid puts the label in a bad spot
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


# ── COLORS ───────────────────────────────────────────────────────────────────
BG_DARK      = "#1e1e2e"
BG_DARKER    = "#181825"
ACCENT_BLUE  = "#89b4fa"
ACCENT_GREEN = "#a6e3a1"
TEXT_LIGHT   = "#cdd6f4"
TEXT_DIM     = "#585b70"
TILE_DEFAULT = "#313244"
TILE_HOVER   = "#45475a"
TILE_OUTLINE = "#585b70"


# ── WINDOW ───────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("US State Capitals (url-test)")
root.geometry("780x700")
root.configure(bg=BG_DARK)
root.resizable(False, False)


# ── NAVIGATION BAR ───────────────────────────────────────────────────────────
nav_frame   = tk.Frame(root, bg=BG_DARKER, pady=6)
nav_frame.pack(fill="x")
table_frame = tk.Frame(root, bg=BG_DARK)
map_frame   = tk.Frame(root, bg=BG_DARK)

def show_table():
    map_frame.pack_forget()
    table_frame.pack(fill="both", expand=True)
    table_btn.configure(bg=ACCENT_BLUE, fg=BG_DARK)
    map_btn.configure(bg=TILE_DEFAULT,  fg=TEXT_LIGHT)

def show_map():
    table_frame.pack_forget()
    map_frame.pack(fill="both", expand=True)
    map_btn.configure(bg=ACCENT_BLUE,  fg=BG_DARK)
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

table_container = tk.Frame(table_frame, bg=BG_DARK)
table_container.pack(fill="both", expand=True, padx=16, pady=8)

table_canvas = tk.Canvas(table_container, bg=BG_DARK, highlightthickness=0)
table_scroll  = ttk.Scrollbar(table_container, orient="vertical",
                               command=table_canvas.yview)
table_inner   = tk.Frame(table_canvas, bg=BG_DARK)

table_inner.bind("<Configure>",
                 lambda e: table_canvas.configure(
                     scrollregion=table_canvas.bbox("all")))
table_canvas.create_window((0, 0), window=table_inner, anchor="nw")
table_canvas.configure(yscrollcommand=table_scroll.set)
table_canvas.pack(side="left", fill="both", expand=True)
table_scroll.pack(side="right", fill="y")

headers    = ["#", "State", "Abbreviation", "Capital"]
col_widths = [3, 22, 14, 20]

for col, (header, width) in enumerate(zip(headers, col_widths)):
    tk.Label(table_inner, text=header, font=("Helvetica", 11, "bold"),
             bg=TILE_DEFAULT, fg=ACCENT_BLUE, width=width, anchor="w",
             padx=8, pady=6).grid(row=0, column=col, sticky="ew",
                                  padx=1, pady=(0, 2))

for i, (state_name, info) in enumerate(sorted(states.items()), start=1):
    row_bg   = BG_DARK if i % 2 == 0 else BG_DARKER
    row_data = [str(i), state_name, info["abbreviation"], info["capital"]]
    for col, (value, width) in enumerate(zip(row_data, col_widths)):
        tk.Label(table_inner, text=value, font=("Helvetica", 10),
                 bg=row_bg, fg=TEXT_LIGHT, width=width, anchor="w",
                 padx=8, pady=5).grid(row=i, column=col, sticky="ew",
                                      padx=1, pady=1)

root.bind("<MouseWheel>",
          lambda e: table_canvas.yview_scroll(-1 * (e.delta // 120), "units"))


# ── MAP VIEW ─────────────────────────────────────────────────────────────────
tk.Label(map_frame, text="US State Map", font=("Helvetica", 18, "bold"),
         bg=BG_DARK, fg=TEXT_LIGHT).pack(pady=(12, 4))

info_var = tk.StringVar(value="Click a state to see its capital")
tk.Label(map_frame, textvariable=info_var, font=("Helvetica", 12),
         bg=TILE_DEFAULT, fg=ACCENT_GREEN, padx=12, pady=6).pack(
    fill="x", padx=20, pady=(0, 6))

map_canvas = tk.Canvas(map_frame, bg=BG_DARKER, highlightthickness=0,
                       width=755, height=555)
map_canvas.pack(padx=10)

# Loading message shown while the map data is being downloaded
loading_id = map_canvas.create_text(
    755 // 2, 220,
    text="Loading map data...",
    fill=TEXT_DIM, font=("Helvetica", 14))

# Draw the Alaska and Hawaii inset border boxes right away
for ox, oy, w, h, label in [
    (AK_LEFT, AK_TOP, AK_WIDTH, AK_HEIGHT, "Alaska"),
    (HI_LEFT, HI_TOP, HI_WIDTH, HI_HEIGHT, "Hawaii"),
]:
    map_canvas.create_rectangle(ox - 2, oy - 2, ox + w + 2, oy + h + 2,
                                fill="", outline=TEXT_DIM, width=1, dash=(3, 3))
    map_canvas.create_text(ox + w // 2, oy + h + 9,
                           text=label, fill=TEXT_DIM, font=("Helvetica", 7))

state_items = {}


# ── MAP EVENT HANDLERS ───────────────────────────────────────────────────────

def on_state_click(abbrev):
    full_name = abbrev_to_name[abbrev]
    capital   = states[full_name]["capital"]
    info_var.set(f"  {full_name}  ({abbrev})  —  Capital: {capital}")

def on_enter(abbrev):
    for item_id in state_items[abbrev]:
        if map_canvas.type(item_id) == "polygon":
            map_canvas.itemconfig(item_id, fill=TILE_HOVER)

def on_leave(abbrev):
    for item_id in state_items[abbrev]:
        if map_canvas.type(item_id) == "polygon":
            map_canvas.itemconfig(item_id, fill=TILE_DEFAULT)

def attach_events(abbrev, item_ids):
    for item_id in item_ids:
        map_canvas.tag_bind(item_id, "<Button-1>",
                            lambda _, a=abbrev: on_state_click(a))
        map_canvas.tag_bind(item_id, "<Enter>",
                            lambda _, a=abbrev: on_enter(a))
        map_canvas.tag_bind(item_id, "<Leave>",
                            lambda _, a=abbrev: on_leave(a))


# ── DRAW MAP FROM GEOJSON ────────────────────────────────────────────────────

def draw_from_geojson(geojson):
    """
    Called once the GeoJSON data has been downloaded.
    Loops over every US state feature and draws its real boundary polygon(s).
    """
    map_canvas.delete(loading_id)   # remove the "Loading..." message

    for feature in geojson["features"]:

        # The GeoJSON uses full state names; look up the abbreviation
        name   = feature["properties"]["name"]
        abbrev = name_to_abbrev.get(name)
        if not abbrev:
            continue    # skip territories like Puerto Rico

        geom = feature["geometry"]

        # GeoJSON Polygon:      coordinates = [outer_ring, hole, hole, ...]
        # GeoJSON MultiPolygon: coordinates = [[outer_ring, ...], [outer_ring, ...]]
        # Normalize both to a list of polygons so the loop below is the same
        if geom["type"] == "Polygon":
            polygons = [geom["coordinates"]]   # wrap single polygon in a list
        else:
            polygons = geom["coordinates"]     # already a list of polygons

        # Pick the right projection function for this state
        if abbrev == "AK":
            proj_fn = to_canvas_ak
        elif abbrev == "HI":
            proj_fn = to_canvas_hi
        else:
            proj_fn = to_canvas

        items = []

        for polygon in polygons:
            outer_ring = polygon[0]   # index 0 = exterior; the rest are holes (ignored)

            # AK and HI: skip rings whose points fall outside the inset box
            # (this removes Aleutian islands that wrap past the -180° line)
            if abbrev == "AK" and not any(AK_WEST <= c[0] <= AK_EAST for c in outer_ring):
                continue
            if abbrev == "HI" and not any(HI_WEST <= c[0] <= HI_EAST for c in outer_ring):
                continue

            # Convert [lon, lat] pairs → flat [x1, y1, x2, y2, ...] pixel list
            flat_coords = []
            for coord in outer_ring:
                lon, lat = coord[0], coord[1]   # GeoJSON order is [lon, lat]
                x, y = proj_fn(lon, lat)
                flat_coords.extend([x, y])

            if len(flat_coords) >= 6:   # need at least 3 points to draw a polygon
                poly_id = map_canvas.create_polygon(flat_coords,
                                                    fill=TILE_DEFAULT,
                                                    outline=TILE_OUTLINE,
                                                    width=1)
                items.append(poly_id)

        # Place the abbreviation label
        if abbrev == "AK":
            lx, ly = AK_LEFT + AK_WIDTH // 2, AK_TOP + AK_HEIGHT // 2
        elif abbrev == "HI":
            lx, ly = HI_LEFT + HI_WIDTH // 2, HI_TOP + HI_HEIGHT // 2
        elif abbrev in LABEL_OVERRIDES:
            lx, ly = to_canvas(*LABEL_OVERRIDES[abbrev])
        else:
            # Compute the centroid (average point) of the first polygon
            outer  = polygons[0][0]
            avg_lon = sum(c[0] for c in outer) / len(outer)
            avg_lat = sum(c[1] for c in outer) / len(outer)
            lx, ly  = to_canvas(avg_lon, avg_lat)

        label_id = map_canvas.create_text(lx, ly, text=abbrev,
                                          fill=TEXT_LIGHT,
                                          font=("Helvetica", 7, "bold"))
        items.append(label_id)

        state_items[abbrev] = items
        attach_events(abbrev, items)


# ── FETCH GEOJSON IN THE BACKGROUND ──────────────────────────────────────────
# Running the download in a background thread means the window stays
# open and responsive while the data is loading.

def fetch_geojson():
    """
    Downloads the GeoJSON file from GitHub and passes it to draw_from_geojson.
    Runs in a background thread so the UI doesn't freeze.
    """
    url = ("https://raw.githubusercontent.com/PublicaMundi/MappingAPI"
           "/master/data/geojson/us-states.json")
    try:
        with urllib.request.urlopen(url, timeout=10, context=SSL_CONTEXT) as response:
            data = json.load(response)

        # Schedule drawing on the main thread (tkinter is not thread-safe)
        root.after(0, lambda: draw_from_geojson(data))

    except Exception as error:
        # If the download fails, show the error on the canvas
        message = f"Could not load map data.\n\n{error}\n\nCheck your internet connection."
        root.after(0, lambda: map_canvas.itemconfig(loading_id,
                                                    text=message,
                                                    fill="#f38ba8"))

# Start the background fetch — daemon=True means it stops when the window closes
threading.Thread(target=fetch_geojson, daemon=True).start()


# ── START ─────────────────────────────────────────────────────────────────────
show_table()
root.mainloop()
