# DATA-flash-cards
For the group project:
This is where we can allocate tasks and share info and map out the project. 

- please leave comments on code so we know what your code is and what it does. 


I think the map will be hard to make look good:
 - The core problem is hand-coded coordinates with too few vertices (we cant make it supper huge). A possible fix is to fetch real US state boundary GeoJSON (built-in urllib + json, no pip installs) and draw the actual outlines. This may work if Bartsch is okay with us importing other features like JSON (I do not want to make it too complex but this might be simple enough). 