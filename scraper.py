from bs4 import BeautifulSoup
import requests
import time
from dotenv import dotenv_values
from scrapeConsulting import get_consulting_content
from scrapeTech import get_tech_content
config = dotenv_values(".env")

START = 9000
END = 11000
# TEST = 9007
DELAY = 0.5
OUTPUT_FILE = 'tech.html'
BASE_URL = 'https://apps.tamidgroup.org/Consulting/Company/posting?id='
LOGIN_URL = 'https://apps.tamidgroup.org/login'


payload = {
    'Email': config["EMAIL"],
    'password': config["PASSWORD"],
    'submit': 'Sign in',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': ''
}

def main():
    which = int(input("Consulting(0)\t\tTech(1)\t\tExit(^c): "))
    if which:
        scraper(get_tech_content)
    else: 
        scraper(get_consulting_content)

def scraper(scraper_function):

    valid_count = 0

    with open(OUTPUT_FILE, 'w') as f:
        with requests.Session() as s:
            start_time = time.time()

            # login
            if not login(LOGIN_URL, payload, s):
                print('authetication error')
                return
            print("Logged in")

            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projects</title>
</head>
<body>""")

            for i in range(START, END + 1):
                print(f"{i - START + 1}/{END - START + 1}", end="")
                internal_start = time.time()
                html = s.get(BASE_URL + str(i))
                html = html.text
                company = scraper_function(i, html, BASE_URL)
                if company:
                    print_to_output_file(company, f)
                    valid_count += 1
                internal_end = time.time()
                time.sleep(max(0, DELAY - (internal_end - internal_start)))

            # Stats
            f.write("</body></html>")
            total_time = time.time() - start_time
            print(f"Complete\nRuntime: {total_time}\nRuntime minus delay: {total_time - DELAY * (END - START)}\nValid items: {valid_count}")


def login(url, payload, session):
    """Returns boolean if logging in was successful"""
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    payload["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
    payload["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
    payload["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]

    session.post(url, data=payload)

    open_page = session.get("https://apps.tamidgroup.org/Consulting/PMPD/ConsultingDashboard")

    if page.text[:1000] == open_page.text[:1000]:
        return False
    else:
        return True


def print_to_output_file(content: dict, f):
    """Takes dict as input and writes the content to output file"""
    for key, value in content.items():
        if key == "url" or key == "website":
            f.write(f"<div><b>{key}</b>: <a href={value}>{value}</a><br><br>")
        else:
            f.write(f"<div><b>{key}</b>: {value}</div><br>")
    f.write("<hr><br>")


if __name__ == '__main__':
    main()