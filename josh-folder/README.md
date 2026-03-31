# DATA-flash-cards
For the group project:
This is where we can allocate tasks and share info and map out the project. 

- please leave comments on code so we know what your code is and what it does. 


I think the map will be hard to make look good:
 - The core problem is hand-coded coordinates with too few vertices (we cant make it supper huge). A possible fix is to fetch real US state boundary GeoJSON (built-in urllib + json, no pip installs) and draw the actual outlines. This may work if Bartsch is okay with us importing other features like JSON (I do not want to make it too complex but this might be simple enough). 


## Project Instructions

We will form several small coding groups and learn to design and execute a project collaboratively: 2-3 people.
Each group is tasked with the same project goal and competes with one another. 
For this project, students are welcome to use AI to help edit and generate code. There are no limitations on your use of outside resources. 
Students will evaluate the results of other groups and the output and work of their own group members. 
Students will be be quizzed on excerpts from their code. 

### Prompt: Create Flash Cards for the 50 US States

- Write one *.py file in Python only.
- Use tkinter to launch a local user interface.
- Each US state is associated with a:
  - I. Visual Map location
  - II. Name
  - III. Initials
  - IV. Capital City

### Flash Card Settings

1. Users select settings prior to viewing flashcards.
2. Users choose one, two, or three items from among I-IV above to be displayed for each flashcard.
3. Users choose one, two, or three non-overlapping items from among I-IV that shall be entered by the user for each flash card.
4. Users choose whether they answer from drop-down menus or text entries for each II-IV flashcard user entry.
5. Users enter their 3-character initials prior to viewing flashcards.

### Flash Card Behavior

- The flash card prompt and user entry adjusts according to settings 1-3 above.
- Users have a maximum of 300 seconds to complete the flashcard deck.
- Once the deck is completed, timer is completed, or the user ends the session, then the user views the top-10 attempts by score.

### Scoring

- Users earn two-sixths (2/6) of a point for each correctly typed answer.
- Users earn one-sixth (1/6) of a point for each correct drop-down or otherwise multiple-choice answer.
- For identical scores, the shorter time elapsed ranks higher.

### Rankings

- The rankings include:
  - User initials
  - Session time
  - Session score
- The user should be able to navigate to the settings or rankings seamlessly.
- The program should not crash due to user interface or entries.
- The program should create or access an existing file that maintains the rankings.

### Maps

- If the flashcard prompt includes a US map, then each state border should be clear. An individual state should be clearly filled with a noticeable color to indicate its selection. You may also want to include a thin circular 'ring' around the selected state to further denote its location.
- If the flashcard prompt includes the visual map location as part of the answer, then the user should be able to click the appropriate state on the map.
- Store your map information within your *.py file as a dictionary.
- Your file should run on another computer through VS Code, without adjustment.