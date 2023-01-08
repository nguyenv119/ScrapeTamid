# ScrapeTamid
A webscraper to view all of tamids groups projects as one of their PMs in an easily digestable html file

Issue: Tamid by default will show Tech consulting PM's 3 projects at a time, and rerolling projects takes too much time

Solution: This scraper will crawl all pages within the specified ID range, and add all projects for the given semester to a nicely formatted HTML file

To use, create a .env folder with contents: 

EMAIL="youremail"
PASSWORD="yourpassword"

By default, this will scan in the range of id's 9000-11000 although at later points in time, projects might be in a different ID range
Additionally to avoid irritating Tamid's servers, a request is sent every .5 seconds, this means to scan all 2000 possible projects in the default range,
this will take ~16.6 repeating minutes. Although this seems like a long time, it pales in comparison to trying to reroll, especially since you aren't
guarenteed to find all projects. 
