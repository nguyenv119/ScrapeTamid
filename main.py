from bs4 import BeautifulSoup
import requests
import time
from dotenv import dotenv_values
config = dotenv_values(".env")


START = 9219
END = 9327
OUTPUT_FILE = 'output.txt'
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

    companies = set()

    with open(OUTPUT_FILE, 'w') as f:
        with requests.Session() as s:
            # login
            start_time = time.time()

            page = s.get(LOGIN_URL)
            soup = BeautifulSoup(page.content, 'lxml')
            payload["__VIEWSTATE"] = soup.select_one("#__VIEWSTATE")["value"]
            payload["__VIEWSTATEGENERATOR"] = soup.select_one("#__VIEWSTATEGENERATOR")["value"]
            payload["__EVENTVALIDATION"] = soup.select_one("#__EVENTVALIDATION")["value"]

            s.post(LOGIN_URL, data=payload)

            open_page = s.get("https://apps.tamidgroup.org/Consulting/PMPD/ConsultingDashboard")

            if page.text[:1000] == open_page.text[:1000]:
                print('authetication error')
                return
            else:
                print("Logged in")

            for i in range(START, END + 1):
                print(f"{i - START + 1}/{END - START + 1}", end="")
                time.sleep(.5)
                html = get_html(i, s)
                company:dict = get_content(i, html)
                if 'name' in company.keys() and company['name'] not in companies:
                    print_to_output_file(company, f)
                    companies.add(company['name'].lower())
            end_time = time.time()
            print(f"Complete\nRuntime: {end_time - start_time}\nValid items: {len(companies)}")

def get_html(id: int, s) -> str:
    response = s.get(BASE_URL + str(id)).text
    return response


def get_content(id: int, html_file) -> dict:
    content = dict()

    soup = BeautifulSoup(html_file, 'lxml')

    box = soup.find_all('div', class_= 'u-shadow-v11 rounded g-pa-30')
    if len(box) == 0:
        print('\terror - redirect')
        return {}
    else:
        box = box[0]
    # contains: name, rating, industry, website, company description, company size, point of 
    # contact
    # contains: deliverable description and work time 
    list_group_items = box.find_all('li', class_= 'list-group-item')
    proj_desc = box.find('p', class_='margin-bottom-40')
    if len(list_group_items) < 14 or len(list_group_items) == 0:
        print('\terror - not tech')
        return {}

    content['name'] = f"{list_group_items[0].find('div', class_='col-xs-8').text.strip()}"
    content['industry'] = f"{list_group_items[2].find('div', class_='col-xs-8').text.strip()}" 
    content['url'] = f'{BASE_URL}{id}'
    content['website'] = f"{list_group_items[3].find('div', class_='col-xs-8').text.strip()}"
    content['company_description'] = f"{list_group_items[4].find('div', class_='col-xs-8').text.strip()}"
    content['project_description'] = f"{proj_desc.text.strip()}"
    content['deliverable_description'] = f"{list_group_items[7].find('div', class_='col-xs-8').text.strip()}" 
    content['work_time'] = f"{list_group_items[9].find('div', class_='col-xs-8').text.strip()}"
    content['new_or_existing'] = f"{list_group_items[10].find('div', class_='col-xs-8').text.strip()}" 
    content['deliverable_type'] = f"{list_group_items[11].find('div', class_='col-xs-8').text.strip()}" 
    content['work_type'] = f"{list_group_items[12].find('div', class_='col-xs-8').text.strip()}" 
    content['tech_stack'] = f"{list_group_items[13].find('div', class_='col-xs-8').text.strip()}" 
    print()
    return content

def print_to_output_file(content: dict, f):
    """Takes dict as input and writes the content to output file"""
    for key, value in content.items():
        f.write(f"{key}: {value}\n")
    f.write("\n")

if __name__ == '__main__':
    main()


