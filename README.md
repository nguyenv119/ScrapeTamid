# ScrapeTamid
A webscraper to view all of tamids groups projects as one of their PMs in an easily digestable html file

Issue: Tamid by default will show Tech consulting PM's 3 projects at a time, and rerolling projects takes too much time

Solution: This scraper will crawl all pages within the specified ID range, and add all projects for the given semester to a nicely formatted HTML file

### How to Use

1. install dependencies

Run the following commands in bash / zsh / wsl (pretty much anything but powershell)
``` bash
  python -m venv .venv # or python3.10 / python3 if this gives you an error
  . .venv/bin/activate # or . .venv/scripts/activate if you are on windows
  pip install -r requirements.txt # or pip3.10 / pip3 if this gives you an error
```

2. Configure settings

Since you have to be authenticated to see projects, put your credentials in a .env file as such

``` bash
#### .env ####
email="youremail"
password="yourpassword"
```

Update the start and end page Ids you would like to scan in config.py
You can get a good sense of what numbers are good by checking the projects you can see on the dashboard, and check their ids in the url. 

Eg. https://apps.tamidgroup.org/Consulting/Company/posting?id=11397 has id 11397. Find the max and min values and then have it range around 2000 projects.

``` python
#### config.py ####
config = Config(
    # Edit start and end here, and email / password in .env
    start=9000,
    end=11000,
    ...
)
 ```

### Running the script
Assuming you did everything correctly, you can now run the script

``` bash
python scraper.py
```

You will be prompted for if you would like to scrape consulting or tech consulting, and then
for the name of the output file. Just give it a name without a file extension

Once the script has run, you can view the html file by opening it in your file explorer, right clicking, and opening with chrome/firefox/safari.

### Notes: 
 - To avoid getting rate limited, a request is sent every .5 seconds, this means to scan all 2000 possible projects in the default range,
 - this will take ~16.6 repeating minutes. Although this seems like a long time, it pales in comparison to trying to reroll, especially since you aren't guarenteed to find all projects. 
