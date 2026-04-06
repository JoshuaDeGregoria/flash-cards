# `TestGame.py` Requirements Review

Reviewed against:

- `Testing/TestGame.py`
- `50States/Flashcard_Project_Outline.md`

## Overall Assessment

`TestGame.py` is structurally close to the intended project. It is a single Python file, uses `tkinter`, includes all 50 states, supports configurable prompt/answer roles, runs a timed quiz, supports typed and multiple-choice scoring, and persists rankings locally.

It does **not fully satisfy** every requirement in the outline yet. The biggest gaps are:

1. startup is not protected by `if __name__ == "__main__":`
2. rankings are displayed as top 10 but the saved file is not trimmed to top 10
3. the settings screen does not provide direct navigation to rankings before a quiz starts
4. rankings loading is not defensive enough against malformed saved entries

## What Already Matches the Outline

- Single `.py` file: yes
- Uses Python + `tkinter`: yes
- Includes all 50 US states: yes
- Supports map, name, initials, and capital: yes
- Lets the user choose 1-3 prompt items: yes
- Lets the user choose 1-3 answer items: yes
- Prevents prompt/answer overlap by design using one role per item: yes
- Requires 3-letter initials before starting: yes
- Limits the session to 300 seconds: yes
- Ends on deck completion, timeout, or user-ending the session: yes
- Shows rankings after the session: yes
- Sorts rankings by score descending, then time ascending: yes
- Stores rankings in a reusable local file in the same folder: yes
- Uses one root window and swaps views instead of opening many windows: yes

## Requirement Gaps

### 1. Missing `__main__` startup guard

Relevant code:

- `Testing/TestGame.py:871-875`
- `Testing/TestGame.py:1918-1920`

Problem:

- `root = tk.Tk()` and `root.mainloop()` run at import time.
- The outline explicitly calls for `if __name__ == "__main__":` to start the app cleanly.
- This makes the file harder to test and less safe to import from another file.

Best-practice fix:

- Move startup code into a `main()` function.
- Put `show_map()` and `root.mainloop()` under:

```python
def main():
    show_map()
    root.mainloop()


if __name__ == "__main__":
    main()
```

### 2. Rankings file is not trimmed to top 10 before saving

Relevant code:

- `Testing/TestGame.py:1863-1872`
- `Testing/TestGame.py:1900-1900`

Problem:

- The app displays only `rankings[:10]`.
- But `save_rankings(rankings)` writes the full list, not the trimmed top 10.
- The outline requires keeping and saving only the top 10 after sorting.

Best-practice fix:

```python
rankings = load_rankings()
rankings.append({
    "initials": user_initials,
    "score": score,
    "time": elapsed,
})
rankings.sort(key=lambda r: (-r["score"], r["time"]))
rankings = rankings[:10]
save_rankings(rankings)
```

### 3. No direct rankings navigation from the settings screen

Relevant code:

- `Testing/TestGame.py:1102-1250`
- `Testing/TestGame.py:1911-1912`

Problem:

- The outline says the settings screen should let the user start the deck and navigate to rankings.
- Current flow only exposes rankings after a quiz ends.
- There is no "View Rankings" button on the settings screen.

Best-practice fix:

- Add a `View Rankings` button beside `Start Quiz`.
- Create a rankings-view function that can open the rankings screen without requiring an active quiz result.
- Reuse the existing results layout, but make current-run summary optional.

### 4. Rankings loading is not robust against malformed saved entries

Relevant code:

- `Testing/TestGame.py:1836-1842`
- `Testing/TestGame.py:1870-1872`
- `Testing/TestGame.py:1900-1904`

Problem:

- `load_rankings()` only handles missing file or invalid whole-file JSON.
- If the JSON file exists but contains one malformed record, later code can fail during sort or display with `KeyError`, `TypeError`, or bad formatting.
- The outline explicitly says malformed rows should be skipped instead of crashing.

Best-practice fix:

- Validate each loaded ranking entry before using it.
- Keep only records with:
  - `initials` as a string
  - `score` as a number
  - `time` as a number

Suggested pattern:

```python
def load_rankings():
    try:
        with open(RANKINGS_FILE, "r") as f:
            raw = json_module.load(f)
    except (FileNotFoundError, json_module.JSONDecodeError):
        return []

    rankings = []
    for entry in raw:
        try:
            initials = str(entry["initials"]).upper()[:3]
            score = float(entry["score"])
            elapsed = float(entry["time"])
        except (KeyError, TypeError, ValueError):
            continue
        rankings.append({
            "initials": initials,
            "score": score,
            "time": elapsed,
        })
    return rankings
```

## Best-Practice Reliability Improvement

### Pending `after()` callback is not canceled on manual end

Relevant code:

- `Testing/TestGame.py:1806-1808`
- `Testing/TestGame.py:1811-1822`
- `Testing/TestGame.py:1550-1562`

Why it matters:

- After submit, the app schedules `root.after(1200, show_card)`.
- If the user ends the session during that delay, the delayed callback is not canceled.
- The timer callback is also not stored/canceled explicitly.
- The current code is mostly protected by state checks, but explicit callback cleanup is safer and easier to reason about.

Best-practice fix:

- Store callback ids returned by `root.after(...)`.
- Cancel them in `end_quiz()` with `root.after_cancel(...)`.

## Suggested Compliance Status

- Core feature completeness: mostly met
- Strict outline compliance: not yet complete
- Recommended next fixes, in order:
  1. add `if __name__ == "__main__":`
  2. trim rankings to top 10 before saving
  3. add rankings access from settings
  4. validate loaded ranking records defensively
  5. cancel scheduled callbacks during quiz shutdown

## Bottom Line

`TestGame.py` is a strong partial-to-near-complete implementation of the flashcard project, but it still misses a few explicit outline requirements and a couple of reliability practices. Fixing the items above would bring it much closer to full compliance.
