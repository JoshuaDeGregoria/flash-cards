# Flash Cards for the 50 US States
# Comment-only code outline based on Flashcard_Project_Outline.md



# INSTRUCTIONS: Import the standard-library modules needed for the app.
#Use tkinter for the interface.
#Use os for portable file paths.
#Use time for session timing.
#Use random if the deck should be shuffled.
#Use csv or plain text handling for rankings, or sqlite3 only if the group chooses that path.

import os
import sys
import time
import random
import csv

try:
    import tkinter as tk
except ModuleNotFoundError as exc:
    if exc.name in {"_tkinter", "tkinter"}:
        raise SystemExit(
            "This Python build does not include Tkinter.\n"
            f"Interpreter: {sys.executable}\n"
            f"Try: /usr/bin/python3 {os.path.abspath(__file__)}\n"
            "The Homebrew Python at /opt/homebrew/bin/python3 on this Mac is missing _tkinter."
        ) from None
    raise



# INSTRUCTIONS: Create constants for the app configuration.
# Define the maximum session length as 300 seconds.
# Define scoring values for typed answers and drop-down or multiple-choice answers.
# Define visible colors for map highlighting, selected states, and normal states.
# Define portable file paths based on the current script location.
# Keep the rankings file in the same folder as this Python file so the project is transferable to any laptop.

MAX_SESSION_LENGTH = 300  # seconds
TYPED_ANSWER_POINTS = 2 / 6
MULTIPLE_CHOICE_POINTS = 1 / 6
MAP_HIGHLIGHT_COLOR = "yellow"
SELECTED_STATE_COLOR = "lightblue"
NORMAL_STATE_COLOR = "white"
RANKINGS_FILE = os.path.join(os.path.dirname(__file__), "rankings.csv")

