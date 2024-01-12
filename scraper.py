from bs4 import BeautifulSoup
import requests
import time
from scrapeConsulting import get_consulting_content
from scrapeTech import get_tech_content
from config import config

payload = {
    'Email': config.email, 
    'password': config.password,
    'submit': 'Sign in',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': ''
  }

def main():
  try: 
    which = int(input("Consulting(0)\t\tTech(1)\t\tExit(^c): "))
    output = input("Output file name: ") + ".html"
    if which:
      scraper(get_tech_content, output)
    else: 
      scraper(get_consulting_content, output)

  except KeyboardInterrupt:
    print("\nExiting")
    return


def scraper(scraper_function, output_file):

  valid_count = 0

  with open(output_file, 'w') as f:
    with requests.Session() as s:
      start_time = time.time()

      # login
      if not login(config.login_url, payload, s):
        print('authetication error')
        return
      print("Logged in")

      # Boilerplate
      f.write("""<!DOCTYPE html>
              <html lang="en">
              <head>
                  <meta charset="UTF-8">
                  <meta http-equiv="X-UA-Compatible" content="IE=edge">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <title>Projects</title>
              </head>
            <body>""")


    # Goes through the range of configs 
    for i in range(config.start, config.end + 1):
        print(f"{i - config.start + 1}/{config.end - config.start + 1}", end="")
        internal_start = time.time()

        html = s.get(config.base_url + str(i))
        print(html)
        html = html.text
        print(html)
        
        company = scraper_function(i, html, config.base_url)

        if company:
            print_to_output_file(company, f)
            valid_count += 1

        internal_end = time.time()
        time.sleep(max(0, config.delay - (internal_end - internal_start)))

        # Stats
        f.write("</body></html>")
        if config.debug:
          total_time = time.time() - start_time
          print(f"Complete\nRuntime: {total_time}\nRuntime minus delay: {total_time - config.delay * (config.end - config.start)}\nValid items: {valid_count}")


def login(url, payload, session):
    """Returns boolean if logging in was successful"""
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    viewStateElement = soup.select_one("#__VIEWSTATE")
    viewStateGeneratorElement = soup.select_one("#__VIEWSTATEGENERATOR")
    eventValidationElement = soup.select_one("#__EVENTVALIDATION")
    if not viewStateElement or not viewStateGeneratorElement or not eventValidationElement:
      raise Exception("Could not find __VIEWSTATE, __VIEWSTATEGENERATOR, or __EVENTVALIDATION \
                        This could imply the login page has changed")
    payload["__VIEWSTATE"] = viewStateElement["value"]
    payload["__VIEWSTATEGENERATOR"] = viewStateGeneratorElement["value"]
    payload["__EVENTVALIDATION"] = eventValidationElement["value"] 

    session.post(url, data=payload)

    open_page = session.get("https://apps.tamidgroup.org/Consulting/PMPD/ConsultingDashboard")

    # kinda hacky but it works
    return not page.text[:1000] == open_page.text[:1000]


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