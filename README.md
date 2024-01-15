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

### Running the script
``` bash
python scraper.py <output_file> <email> <password> <start_id> <end_id>
```

Once the script has run, you can view the html file by opening it in your file explorer, right clicking, and opening with chrome/firefox/safari.

### Options
For additional options and help, run `python scraper.py -help`
