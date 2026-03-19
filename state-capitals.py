import tkinter as tk
from tkinter import ttk

# --- DATA ---
# Each state is its own dictionary with capital city and 2-letter abbreviation
states = {
    "Alabama":        {"capital": "Montgomery",    "abbreviation": "AL"},
    "Alaska":         {"capital": "Juneau",         "abbreviation": "AK"},
    "Arizona":        {"capital": "Phoenix",        "abbreviation": "AZ"},
    "Arkansas":       {"capital": "Little Rock",    "abbreviation": "AR"},
    "California":     {"capital": "Sacramento",     "abbreviation": "CA"},
    "Colorado":       {"capital": "Denver",         "abbreviation": "CO"},
    "Connecticut":    {"capital": "Hartford",       "abbreviation": "CT"},
    "Delaware":       {"capital": "Dover",          "abbreviation": "DE"},
    "Florida":        {"capital": "Tallahassee",    "abbreviation": "FL"},
    "Georgia":        {"capital": "Atlanta",        "abbreviation": "GA"},
    "Hawaii":         {"capital": "Honolulu",       "abbreviation": "HI"},
    "Idaho":          {"capital": "Boise",          "abbreviation": "ID"},
    "Illinois":       {"capital": "Springfield",    "abbreviation": "IL"},
    "Indiana":        {"capital": "Indianapolis",   "abbreviation": "IN"},
    "Iowa":           {"capital": "Des Moines",     "abbreviation": "IA"},
    "Kansas":         {"capital": "Topeka",         "abbreviation": "KS"},
    "Kentucky":       {"capital": "Frankfort",      "abbreviation": "KY"},
    "Louisiana":      {"capital": "Baton Rouge",    "abbreviation": "LA"},
    "Maine":          {"capital": "Augusta",        "abbreviation": "ME"},
    "Maryland":       {"capital": "Annapolis",      "abbreviation": "MD"},
    "Massachusetts":  {"capital": "Boston",         "abbreviation": "MA"},
    "Michigan":       {"capital": "Lansing",        "abbreviation": "MI"},
    "Minnesota":      {"capital": "Saint Paul",     "abbreviation": "MN"},
    "Mississippi":    {"capital": "Jackson",        "abbreviation": "MS"},
    "Missouri":       {"capital": "Jefferson City", "abbreviation": "MO"},
    "Montana":        {"capital": "Helena",         "abbreviation": "MT"},
    "Nebraska":       {"capital": "Lincoln",        "abbreviation": "NE"},
    "Nevada":         {"capital": "Carson City",    "abbreviation": "NV"},
    "New Hampshire":  {"capital": "Concord",        "abbreviation": "NH"},
    "New Jersey":     {"capital": "Trenton",        "abbreviation": "NJ"},
    "New Mexico":     {"capital": "Santa Fe",       "abbreviation": "NM"},
    "New York":       {"capital": "Albany",         "abbreviation": "NY"},
    "North Carolina": {"capital": "Raleigh",        "abbreviation": "NC"},
    "North Dakota":   {"capital": "Bismarck",       "abbreviation": "ND"},
    "Ohio":           {"capital": "Columbus",       "abbreviation": "OH"},
    "Oklahoma":       {"capital": "Oklahoma City",  "abbreviation": "OK"},
    "Oregon":         {"capital": "Salem",          "abbreviation": "OR"},
    "Pennsylvania":   {"capital": "Harrisburg",     "abbreviation": "PA"},
    "Rhode Island":   {"capital": "Providence",     "abbreviation": "RI"},
    "South Carolina": {"capital": "Columbia",       "abbreviation": "SC"},
    "South Dakota":   {"capital": "Pierre",         "abbreviation": "SD"},
    "Tennessee":      {"capital": "Nashville",      "abbreviation": "TN"},
    "Texas":          {"capital": "Austin",         "abbreviation": "TX"},
    "Utah":           {"capital": "Salt Lake City", "abbreviation": "UT"},
    "Vermont":        {"capital": "Montpelier",     "abbreviation": "VT"},
    "Virginia":       {"capital": "Richmond",       "abbreviation": "VA"},
    "Washington":     {"capital": "Olympia",        "abbreviation": "WA"},
    "West Virginia":  {"capital": "Charleston",     "abbreviation": "WV"},
    "Wisconsin":      {"capital": "Madison",        "abbreviation": "WI"},
    "Wyoming":        {"capital": "Cheyenne",       "abbreviation": "WY"},
}

# Tile grid positions (col, row) for each state on the map
# Arranged to roughly mirror real US geography
tile_positions = {
    "ME": (11, 0),
    "WA": (1, 1), "MT": (2, 1), "ND": (3, 1), "MN": (4, 1), "VT": (9, 1), "NH": (10, 1),
    "OR": (1, 2), "ID": (2, 2), "SD": (3, 2), "WI": (5, 2), "MI": (6, 2), "NY": (8, 2), "MA": (9, 2), "RI": (11, 2),
    "CA": (1, 3), "NV": (2, 3), "WY": (3, 3), "NE": (4, 3), "IA": (5, 3), "IL": (6, 3), "IN": (7, 3), "OH": (8, 3), "PA": (9, 3), "NJ": (10, 3), "CT": (11, 3),
    "UT": (2, 4), "CO": (3, 4), "KS": (4, 4), "MO": (5, 4), "KY": (6, 4), "WV": (7, 4), "VA": (8, 4), "MD": (9, 4), "DE": (10, 4),
    "AZ": (2, 5), "NM": (3, 5), "OK": (4, 5), "AR": (5, 5), "TN": (6, 5), "NC": (7, 5), "SC": (8, 5),
    "TX": (3, 6), "LA": (4, 6), "MS": (5, 6), "AL": (6, 6), "GA": (7, 6),
    "FL": (7, 7),
    "AK": (0, 8), "HI": (2, 8),
}

# Reverse lookup: abbreviation -> full state name (used when a tile is clicked)
abbrev_to_name = {info["abbreviation"]: name for name, info in states.items()}

# --- WINDOW SETUP ---
root = tk.Tk()
root.title("US State Capitals")
root.geometry("780x680")
root.configure(bg="#1e1e2e")
root.resizable(False, False)  # Locks window size so layout stays clean

# --- NAVIGATION BAR ---
# Top bar with buttons to switch between Table and Map views
nav_frame = tk.Frame(root, bg="#181825", pady=6)
nav_frame.pack(fill="x")

# Holds the two content views — only one is visible at a time
table_frame = tk.Frame(root, bg="#1e1e2e")
map_frame   = tk.Frame(root, bg="#1e1e2e")

def show_table():
    """Hides the map view and shows the table view."""
    map_frame.pack_forget()
    table_frame.pack(fill="both", expand=True)
    table_btn.configure(bg="#89b4fa", fg="#1e1e2e")  # Highlight active button
    map_btn.configure(bg="#313244", fg="#cdd6f4")     # Dim inactive button

def show_map():
    """Hides the table view and shows the tile map view."""
    table_frame.pack_forget()
    map_frame.pack(fill="both", expand=True)
    map_btn.configure(bg="#89b4fa", fg="#1e1e2e")
    table_btn.configure(bg="#313244", fg="#cdd6f4")

# Navigation buttons
table_btn = tk.Button(nav_frame, text="  Table  ", command=show_table,
                      bg="#89b4fa", fg="#1e1e2e", font=("Helvetica", 11, "bold"),
                      relief="flat", cursor="hand2", padx=10)
table_btn.pack(side="left", padx=(12, 4))

map_btn = tk.Button(nav_frame, text="  Map  ", command=show_map,
                    bg="#313244", fg="#cdd6f4", font=("Helvetica", 11, "bold"),
                    relief="flat", cursor="hand2", padx=10)
map_btn.pack(side="left", padx=4)

# --- TABLE VIEW ---
# Title label at the top of the table view
tk.Label(table_frame, text="US State Capitals", font=("Helvetica", 20, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").pack(pady=(16, 8))

# Outer container that holds the canvas and scrollbar
table_container = tk.Frame(table_frame, bg="#1e1e2e")
table_container.pack(fill="both", expand=True, padx=16, pady=8)

# Canvas provides a scrollable surface for the table rows
table_canvas   = tk.Canvas(table_container, bg="#1e1e2e", highlightthickness=0)
table_scroll   = ttk.Scrollbar(table_container, orient="vertical", command=table_canvas.yview)
table_inner    = tk.Frame(table_canvas, bg="#1e1e2e")  # Inner frame holds the actual rows

# When table_inner resizes, update the canvas scroll region to match
table_inner.bind("<Configure>", lambda _: table_canvas.configure(scrollregion=table_canvas.bbox("all")))
table_canvas.create_window((0, 0), window=table_inner, anchor="nw")
table_canvas.configure(yscrollcommand=table_scroll.set)

table_canvas.pack(side="left", fill="both", expand=True)
table_scroll.pack(side="right", fill="y")

# Column headers row
headers    = ["#", "State", "Abbreviation", "Capital"]
col_widths = [3, 22, 14, 20]
for col, (header, width) in enumerate(zip(headers, col_widths)):
    tk.Label(table_inner, text=header, font=("Helvetica", 11, "bold"),
             bg="#313244", fg="#89b4fa", width=width, anchor="w",
             padx=8, pady=6).grid(row=0, column=col, sticky="ew", padx=1, pady=(0, 2))

# One row per state, sorted alphabetically, alternating background colors
for i, (state, info) in enumerate(sorted(states.items()), start=1):
    bg       = "#1e1e2e" if i % 2 == 0 else "#181825"
    row_data = [str(i), state, info["abbreviation"], info["capital"]]
    for col, (val, width) in enumerate(zip(row_data, col_widths)):
        tk.Label(table_inner, text=val, font=("Helvetica", 10),
                 bg=bg, fg="#cdd6f4", width=width, anchor="w",
                 padx=8, pady=5).grid(row=i, column=col, sticky="ew", padx=1, pady=1)

# Mouse wheel scrolling for the table
root.bind("<MouseWheel>", lambda e: table_canvas.yview_scroll(-1 * (e.delta // 120), "units"))

# --- MAP VIEW ---
# Title label at the top of the map view
tk.Label(map_frame, text="US State Tile Map", font=("Helvetica", 18, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").pack(pady=(12, 4))

# Info panel below the title — shows state details when a tile is clicked
info_var = tk.StringVar(value="Click a state to see details")
tk.Label(map_frame, textvariable=info_var, font=("Helvetica", 12),
         bg="#313244", fg="#a6e3a1", padx=12, pady=6).pack(fill="x", padx=20, pady=(0, 8))

# Canvas where the tile grid is drawn
TILE_W, TILE_H = 57, 46   # Width and height of each state tile in pixels
PADDING        = 10        # Left/top offset so tiles don't touch the canvas edge

map_canvas = tk.Canvas(map_frame, bg="#181825", highlightthickness=0,
                       width=13 * TILE_W + PADDING, height=10 * TILE_H + PADDING + 20)
map_canvas.pack(padx=10)

# Tracks the currently selected tile rectangle ID so it can be un-highlighted
selected_rect = [None]

def on_tile_click(abbrev):
    """Called when a state tile is clicked — updates the info panel."""
    name    = abbrev_to_name[abbrev]                # Full state name from abbreviation
    capital = states[name]["capital"]               # Capital city from the states dict
    info_var.set(f"  {name}  ({abbrev})  —  Capital: {capital}")

def on_enter(rect_id):
    """Highlights a tile when the mouse hovers over it."""
    map_canvas.itemconfig(rect_id, fill="#45475a")

def on_leave(rect_id, original_color):
    """Restores tile color when the mouse leaves it."""
    map_canvas.itemconfig(rect_id, fill=original_color)

# Draw a tile for every state using its (col, row) position in tile_positions
for abbrev, (col, row) in tile_positions.items():
    # Calculate pixel coordinates of the tile's top-left corner
    x1 = PADDING + col * TILE_W
    y1 = PADDING + row * TILE_H
    x2 = x1 + TILE_W - 3   # -3 leaves a small gap between tiles
    y2 = y1 + TILE_H - 3

    tile_color = "#313244"  # Default tile background color

    # Draw the rectangle for this state tile
    rect = map_canvas.create_rectangle(x1, y1, x2, y2, fill=tile_color,
                                       outline="#585b70", width=1)

    # Draw the state abbreviation text centered inside the tile
    text = map_canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                  text=abbrev, fill="#cdd6f4",
                                  font=("Helvetica", 9, "bold"))

    # Bind click, hover-in, and hover-out events to both the rect and text
    for item in (rect, text):
        map_canvas.tag_bind(item, "<Button-1>",  lambda _, a=abbrev: on_tile_click(a))
        map_canvas.tag_bind(item, "<Enter>",     lambda _, r=rect: on_enter(r))
        map_canvas.tag_bind(item, "<Leave>",     lambda _, r=rect, c=tile_color: on_leave(r, c))

# Start on the table view by default
show_table()

# Starts the tkinter event loop — keeps the window open and responsive
root.mainloop()
