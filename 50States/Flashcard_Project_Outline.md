# Flash Cards for the 50 US States

## Project Goal

Create one Python file that launches a local `tkinter` interface for a US states flashcard application. The program should let the user choose what information is shown, what information must be answered, how answers are entered, and then save rankings across sessions.

This outline is written to fit the coding patterns already present in this repo: functions, loops, dictionaries, file handling, and `try/except`. A more advanced approach is allowed in a few places, but the safest plan is still a clean single-file procedural program.

## Core Requirements

The final program must:

- Be written in one `.py` file only
- Use Python and `tkinter`
- Run locally on another laptop without needing edits
- Cover all 50 US states
- Associate each state with:
  - map location
  - full name
  - initials
  - capital city
- Let the user choose, before the session starts:
  - which 1-3 items are shown on each flashcard
  - which 1-3 different, non-overlapping items the user must answer
  - whether name, initials, and capital answers are entered with text boxes or drop-downs
- Require the user to enter 3-character initials before starting
- Limit the session to 300 seconds
- End when:
  - all cards are completed, or
  - time expires, or
  - the user ends the session
- Show top 10 rankings after the session
- Rank by:
  - higher score first
  - shorter time first when scores tie
- Save rankings to a file that can be reused later
- Allow smooth navigation between settings, flashcards, and rankings
- Avoid crashing on bad input or normal UI usage

## Recommended Scope

Build the project in a way that matches what has already been practiced in this repo:

- dictionaries for state data
- lists for deck order and rankings
- functions for each part of the program
- loops for checking answers and processing records
- `try/except` for file loading and input safety
- local file storage for rankings

Do not make the design more complex than needed. You can use advanced features if they truly help, but they should not hurt portability.

## Best Technical Direction

### Recommended

Use only the Python standard library:

- `tkinter`
- `random`
- `time`
- `os`
- `csv` or plain text file handling

This is the safest choice for transferability because another laptop with Python installed can usually run the file without package installs.

### Optional Advanced Choice

You may use `sqlite3` for rankings because it is part of the standard library. This is acceptable if your group wants slightly cleaner ranking storage, but it is not required.

If you use `sqlite3`:

- create the database file automatically if it does not exist
- keep the database file in the same folder as the `.py` file
- do not require setup steps from the user

If your group is unsure, use a plain text or CSV rankings file instead. That is simpler and easier to debug.

## Portability Rules

This part matters a lot. The program must run on another laptop without adjustment.

### Always Do

- Use relative file paths, not hard-coded personal paths
- Keep generated files in the same folder as the `.py` file
- Use only standard-library modules if possible
- Create missing files automatically
- Handle missing or empty rankings files without crashing
- Use `if __name__ == "__main__":` to start the app cleanly

### Never Do

- Do not hard-code paths like `/Users/name/Desktop/...`
- Do not require manually changing the working directory
- Do not depend on files stored elsewhere on your laptop
- Do not require internet access
- Do not require external Python packages unless your instructor clearly allows setup steps

### Safe File Pattern

Use a path built from the script location, not the current terminal location:

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RANKINGS_FILE = os.path.join(BASE_DIR, "state_rankings.csv")
```

That makes the program much more likely to run correctly on any laptop.

## Program Structure

Keep everything in one file, but divide it into clear sections.

### Suggested File Layout

1. imports
2. constants
3. state data dictionary
4. rankings load/save functions
5. scoring functions
6. map drawing and map click functions
7. settings screen functions
8. flashcard screen functions
9. rankings screen functions
10. app startup

## Data Design

### State Dictionary

Store all map and state information in one large dictionary.

Suggested format:

```python
states = {
    "AL": {
        "name": "Alabama",
        "initials": "AL",
        "capital": "Montgomery",
        "map_points": [(x1, y1), (x2, y2), (x3, y3)],
        "center": (cx, cy)
    }
}
```

### Why This Works

- one place for all state information
- easy to read and update
- easy to loop through
- supports both drawing and answer checking

### Notes About the Map

Since the prompt requires map information inside the `.py` file, the simplest safe design is:

- draw the map on a `tkinter.Canvas`
- store each state's drawing coordinates in the dictionary
- fill the selected state with a visible color
- optionally draw a ring around the selected state's center

Avoid relying on an external image file unless your group can embed everything safely in the one-file rule.

## User Flow

### Screen 1: Settings

The user should:

- enter 3-character initials
- choose which fields are shown as prompts
- choose which different fields must be answered
- choose answer style for name, initials, and capital
- start the deck
- navigate to rankings

Validation rules:

- initials must be exactly 3 characters
- prompt count must be 1, 2, or 3
- answer count must be 1, 2, or 3
- prompt and answer selections must not overlap
- there must be at least one answer field

### Screen 2: Flashcards

For each state:

- display the selected prompt items
- show answer widgets that match the chosen settings
- allow submission
- move to the next card
- show current score
- show remaining time
- allow ending the session early

If map location is part of the prompt:

- show the map with the current state highlighted

If map location is part of the answer:

- let the user click the correct state on the map

### Screen 3: Rankings

Show:

- top 10 attempts
- user initials
- session time
- session score

Allow:

- return to settings
- optionally start a new session

## Scoring Rules

The assignment gives a weighted scoring system.

- `2/6` point for each correct typed answer
- `1/6` point for each correct drop-down or other multiple-choice answer

Recommended interpretation:

- text entry for name, initials, or capital counts as typed
- drop-down answer counts as multiple-choice
- clicking a state on the map should be treated as multiple-choice unless your instructor says otherwise

### Practical Tip

Track score as a float during the session, then format it cleanly for display.

Example:

```python
score = round(score, 2)
```

## Screen Management

The cleanest `tkinter` approach is to use one root window and swap frames.

Recommended pattern:

- create one main root window
- create a frame for settings
- create a frame for flashcards
- create a frame for rankings
- destroy or hide the old frame when switching screens

This is easier to manage than opening many new windows.

## Timer Design

Use `tkinter`'s `after()` method instead of freezing the app with `time.sleep()`.

Why:

- the UI stays responsive
- the countdown updates smoothly
- buttons and clicks still work

Track:

- session start time
- elapsed time
- remaining time

End the session automatically at 300 seconds.

## Rankings Storage

### Simplest Option

Use a CSV or text file such as:

- `state_rankings.csv`

Each row can contain:

- initials
- elapsed time
- final score

Example row:

```text
ABC,184.2,17.33
```

### Ranking Logic

When loading rankings:

1. read all past attempts
2. add the current attempt
3. sort by score descending
4. break ties by time ascending
5. keep the top 10
6. save the trimmed list back to the file

### Safety Rules

- if the file does not exist, create it
- if the file is empty, treat it as no rankings yet
- if one row is malformed, skip it instead of crashing

## Suggested Function List

You do not need these exact names, but this is a good one-file outline.

- `load_rankings()`
- `save_rankings(rankings)`
- `sort_rankings(rankings)`
- `validate_initials(text)`
- `validate_settings(prompt_fields, answer_fields)`
- `build_settings_screen()`
- `start_session()`
- `build_flashcard_screen()`
- `show_current_card()`
- `check_answers()`
- `score_answer(answer_type, is_correct)`
- `next_card()`
- `update_timer()`
- `end_session()`
- `build_rankings_screen()`
- `draw_map(canvas)`
- `highlight_state(state_code)`
- `handle_map_click(event)`

## Recommended Build Order

### Phase 1: Core Data

- define the 50-state dictionary
- decide how map coordinates will be stored
- create a simple rankings file design

### Phase 2: Settings Screen

- initials input
- prompt selections
- answer selections
- answer mode selections
- validation checks

### Phase 3: Flashcard Engine

- create the 50-state deck
- track current card
- track score
- track time
- switch to next card cleanly

### Phase 4: Map Logic

- draw all states
- highlight one prompt state
- detect clicks for answer mode

### Phase 5: Ranking Logic

- save results
- sort results
- trim to top 10
- display rankings

### Phase 6: Testing and Cleanup

- click through every screen
- test invalid inputs
- test missing rankings file
- test timer expiration
- test ranking ties

## Team Plan

### For a 2-Person Group

Person 1:

- settings screen
- flashcard flow
- scoring and timer

Person 2:

- state dictionary
- map drawing and click logic
- rankings file and rankings screen

### For a 3-Person Group

Person 1:

- settings UI
- input validation
- screen navigation

Person 2:

- flashcard logic
- answer checking
- scoring and timer

Person 3:

- state data
- map drawing/clicking
- rankings storage and display

## Tips and Tricks

### Keep the First Version Simple

Make a working version before polishing the interface. A program that fully works is better than a fancy app with missing features.

### Test One Feature at a Time

Do not try to build everything at once. Finish:

1. settings
2. one flashcard
3. many flashcards
4. timer
5. rankings

### Reuse Small Functions

If you repeat logic more than once, put it in a function. This will help during quizzes when you need to explain your code.

### Validate Early

Reject bad settings before the session begins. This prevents confusing errors later.

### Normalize Text Answers

When checking typed answers:

- strip spaces
- consider lowercasing

Example:

```python
user_answer.strip().lower()
```

This reduces false wrong answers caused by capitalization or extra spaces.

### Keep the UI Responsive

Avoid blocking code during the session. Prefer `after()` callbacks in `tkinter`.

### Save Carefully

Write rankings only when the session ends. That reduces accidental corruption.

### Build for Quiz Readiness

Since students may be quizzed on their code:

- keep functions short
- use clear variable names
- add a few short comments where logic is not obvious
- make sure each group member understands the part they wrote

## Common Mistakes to Avoid

- overlapping prompt and answer fields
- forgetting to stop the timer when the session ends
- using absolute file paths
- assuming the rankings file already exists
- crashing when the user leaves a text box blank
- not resetting values when starting a new session
- sorting rankings incorrectly
- freezing the interface with long-running code
- making map clicks register the wrong state

## Advanced Options That Are Still Reasonable

These are acceptable only if your group can explain and maintain them.

### `sqlite3` for Rankings

Useful if you want cleaner structured storage. Still portable because it is built into Python.

### Shuffle the Deck

Using `random.shuffle()` makes sessions less predictable.

### Small Helper Classes

Allowed if they truly simplify the program, but they are not necessary. Given this repo, functions are probably the better fit.

### Lightweight Multiple Choice

For drop-down answers, you can generate options from the state data dynamically instead of typing lists by hand.

## Minimum Quality Checklist

Before submission, confirm:

- the app launches with `python your_file.py`
- it works without changing any paths
- the rankings file is created automatically
- settings validation works
- all 50 states are included
- the timer ends the session at 300 seconds
- scores are calculated correctly
- ties are ranked by shorter time
- top 10 rankings display correctly
- the user can return to settings and run another session
- normal mistakes by the user do not crash the program

## Final Recommendation

The strongest version of this project is not the most advanced version. The strongest version is:

- complete
- stable
- easy to explain
- portable to any laptop
- built with clean functions and solid validation

If your group adds advanced features, only do so after the required version already works.
