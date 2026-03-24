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


# INSTRUCTIONS: Create the full state data dictionary for all 50 states.
# INSTRUCTIONS: Use state initials as dictionary keys.
# INSTRUCTIONS: For each state, store the full name, initials, capital city, map drawing data, and center point for optional highlight rings.
# INSTRUCTIONS: Keep all map information inside this file to match the project requirement.
STATE_DATA = {
    "AL": {
        "name": "Alabama",
        "initials": "AL",
        "capital": "Montgomery",
        "map_data": [(x1, y1), (x2, y2), ...],  # Replace with actual coordinates for the state border
        "center": (cx, cy)  # Replace with actual center coordinates for the state
    },
    "AK": {
        "name": "Alaska",
        "initials": "AK",
        "capital": "Juneau",        
        "map_data": [(x1, y1), (x2, y2), ...],  # Replace with actual coordinates for the state border
        "center": (cx, cy)  # Replace with actual center coordinates for the state
    },
    
}   


# INSTRUCTIONS: Create global app-state variables or one shared state dictionary.
# INSTRUCTIONS: Track the current screen, selected settings, deck order, current card index, score, timer values, and map selection state.
# INSTRUCTIONS: Track the user's 3-character initials and the ranking data loaded from file.
app_state = {
    "current_screen": "settings",
    "selected_prompt_fields": [],
    "selected_answer_fields": [],
    "answer_modes": {},  # e.g., {"name": "text", "capital": "dropdown", ...}
    "deck_order": [],
    "current_card_index": 0,
    "score": 0,
    "session_start_time": None,
    "elapsed_time": 0,
    "selected_map_state": None,
    "user_initials": "",
    "rankings": []
}


# INSTRUCTIONS: Write a function that creates the rankings file automatically if it does not exist yet.
# INSTRUCTIONS: Make sure missing files do not crash the program.
# INSTRUCTIONS: Keep the file format simple and easy to debug.
def initialize_rankings_file():
    if not os.path.exists(RANKINGS_FILE):
        with open(RANKINGS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Initials", "Elapsed Time", "Score"])  # Header row


# INSTRUCTIONS: Write a function to load past rankings from the local file.
# INSTRUCTIONS: Read each stored attempt and convert it into a list or dictionary record.
# INSTRUCTIONS: Skip malformed rows safely instead of crashing.
# INSTRUCTIONS: Return an empty list if no rankings are stored yet.

def load_rankings():
    rankings = []
    if os.path.exists(RANKINGS_FILE):
        with open(RANKINGS_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                try:
                    initials, elapsed_time, score = row
                    rankings.append((initials, float(elapsed_time), int(score)))
                except (ValueError, IndexError):
                    pass  # Skip malformed rows
    return rankings

# INSTRUCTIONS: Write a function to save rankings back to the local file.
# INSTRUCTIONS: Save initials, elapsed session time, and final session score.
# INSTRUCTIONS: Save only the top 10 records after sorting.


# INSTRUCTIONS: Write a function to sort ranking records.
# INSTRUCTIONS: Sort by score from highest to lowest.
# INSTRUCTIONS: When scores are tied, rank the shorter elapsed time higher.


# INSTRUCTIONS: Write a function to validate the user's initials.
# INSTRUCTIONS: Require exactly 3 characters before starting a session.
# INSTRUCTIONS: Decide whether initials should be forced to uppercase and trimmed.


# INSTRUCTIONS: Write a function to validate the flashcard settings.
# INSTRUCTIONS: Require 1 to 3 prompt items.
# INSTRUCTIONS: Require 1 to 3 answer items.
# INSTRUCTIONS: Make sure prompt items and answer items do not overlap.
# INSTRUCTIONS: Make sure the selected answer style only applies to the allowed answer fields.


# INSTRUCTIONS: Write a function to calculate the score for one answer field.
# INSTRUCTIONS: Award 2/6 point for each correct typed answer.
# INSTRUCTIONS: Award 1/6 point for each correct drop-down or other multiple-choice answer.
# INSTRUCTIONS: Treat map-click answers according to the scoring rule your group decides to follow.


# INSTRUCTIONS: Write a function to normalize typed answers before checking them.
# INSTRUCTIONS: Strip extra spaces and handle capitalization consistently.
# INSTRUCTIONS: Use this for name, initials, and capital comparisons where appropriate.


# INSTRUCTIONS: Write a function to build the main tkinter window.
# INSTRUCTIONS: Create one root window only.
# INSTRUCTIONS: Set the window title and any basic sizing rules.
# INSTRUCTIONS: Prepare the app to switch between settings, flashcards, and rankings without opening extra windows.


# INSTRUCTIONS: Write a helper function to clear, hide, or replace the current screen frame.
# INSTRUCTIONS: Use this whenever the program moves from one screen to another.
# INSTRUCTIONS: Keep screen switching simple so the interface stays stable.


# INSTRUCTIONS: Write the function that builds the settings screen.
# INSTRUCTIONS: Add the initials input.
# INSTRUCTIONS: Add controls for selecting which items appear as prompts.
# INSTRUCTIONS: Add controls for selecting which different items must be answered.
# INSTRUCTIONS: Add controls for choosing text-entry or drop-down mode for name, initials, and capital answers.
# INSTRUCTIONS: Add buttons for starting the session and viewing rankings.


# INSTRUCTIONS: On the settings screen, add clear labels that explain the rules.
# INSTRUCTIONS: Explain that prompt and answer selections cannot overlap.
# INSTRUCTIONS: Explain that the session lasts at most 300 seconds.


# INSTRUCTIONS: Write the function that reads the settings screen values.
# INSTRUCTIONS: Collect the chosen prompt fields, answer fields, answer modes, and user initials.
# INSTRUCTIONS: Validate everything before starting the deck.
# INSTRUCTIONS: Show a user-friendly error message if a setting is invalid.


# INSTRUCTIONS: Write the function that starts a new flashcard session.
# INSTRUCTIONS: Reset the score, timer, current card index, and any previous answer state.
# INSTRUCTIONS: Build the 50-state deck.
# INSTRUCTIONS: Shuffle the deck only if your group wants that behavior.
# INSTRUCTIONS: Record the session start time.


# INSTRUCTIONS: Write the function that builds the flashcard screen.
# INSTRUCTIONS: Show the current card number, the running score, and the time remaining.
# INSTRUCTIONS: Add a place for prompt content.
# INSTRUCTIONS: Add a place for answer widgets.
# INSTRUCTIONS: Add submit, next, end-session, and navigation controls as needed.


# INSTRUCTIONS: Write the function that displays the current flashcard.
# INSTRUCTIONS: Look up the current state in the state dictionary.
# INSTRUCTIONS: Show the selected prompt items for that state.
# INSTRUCTIONS: Build answer widgets that match the selected answer settings.
# INSTRUCTIONS: Reset any old answer widgets from the previous card.


# INSTRUCTIONS: Write the function that creates text-entry answer widgets.
# INSTRUCTIONS: Use these for typed name, initials, and capital answers when the settings require text input.


# INSTRUCTIONS: Write the function that creates drop-down answer widgets.
# INSTRUCTIONS: Populate the options from the state data.
# INSTRUCTIONS: Use these for multiple-choice style answers when the settings require drop-downs.


# INSTRUCTIONS: Write the function that draws the map on a tkinter Canvas.
# INSTRUCTIONS: Use the map data stored in the state dictionary.
# INSTRUCTIONS: Make all state borders clear enough to see.
# INSTRUCTIONS: Make it possible to redraw or recolor a state when needed.


# INSTRUCTIONS: Write the function that highlights the current state on the map.
# INSTRUCTIONS: Fill the selected state with a noticeable color.
# INSTRUCTIONS: Optionally draw a thin circular ring around the selected state's center point.
# INSTRUCTIONS: Use this when map location is part of the prompt.


# INSTRUCTIONS: Write the function that handles map clicks.
# INSTRUCTIONS: Detect which state the user clicked.
# INSTRUCTIONS: Store the selected state as the user's answer when map location is part of the answer.
# INSTRUCTIONS: Give visual feedback so the user knows which state was selected.


# INSTRUCTIONS: Write the function that checks the user's answers for the current flashcard.
# INSTRUCTIONS: Compare each required answer field against the current state's correct data.
# INSTRUCTIONS: Score each field using the correct rule for typed or drop-down or map-click answers.
# INSTRUCTIONS: Add the earned points to the running session score.
# INSTRUCTIONS: Prevent crashes when fields are blank or incomplete.


# INSTRUCTIONS: Write the function that moves to the next flashcard.
# INSTRUCTIONS: Advance the card index only after the current card has been submitted or handled correctly.
# INSTRUCTIONS: End the session automatically when all 50 states have been completed.


# INSTRUCTIONS: Write the timer-update function using tkinter's after() method.
# INSTRUCTIONS: Recalculate elapsed time and remaining time without freezing the interface.
# INSTRUCTIONS: Update the on-screen timer display.
# INSTRUCTIONS: End the session automatically when the timer reaches 300 seconds.


# INSTRUCTIONS: Write the function that ends the session.
# INSTRUCTIONS: Stop timer updates.
# INSTRUCTIONS: Compute the final elapsed time.
# INSTRUCTIONS: Round or format the final score cleanly for display.
# INSTRUCTIONS: Save the session result into the rankings data.
# INSTRUCTIONS: Switch to the rankings screen.


# INSTRUCTIONS: Write the function that builds the rankings screen.
# INSTRUCTIONS: Load or refresh the top 10 attempts.
# INSTRUCTIONS: Display user initials, elapsed session time, and session score.
# INSTRUCTIONS: Keep the ranking order consistent with the project rules.
# INSTRUCTIONS: Add buttons to return to settings or start a new session.


# INSTRUCTIONS: Write a helper function to format ranking rows for display.
# INSTRUCTIONS: Make score and time values easy to read.
# INSTRUCTIONS: Keep the ranking presentation clean and simple.


# INSTRUCTIONS: Write error-handling around file access and user input where needed.
# INSTRUCTIONS: The program should not crash from empty inputs, missing files, or normal interface actions.
# INSTRUCTIONS: Show helpful messages instead of failing silently.


# INSTRUCTIONS: Write a setup function that launches the first screen when the app opens.
# INSTRUCTIONS: Load rankings first, then show the settings screen by default.


# INSTRUCTIONS: Add the main program entry point.
# INSTRUCTIONS: Create the app window, initialize shared state, build the initial screen, and start the tkinter event loop.
# INSTRUCTIONS: Use if __name__ == "__main__": so the file runs cleanly on any laptop.
