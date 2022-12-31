from bs4 import BeautifulSoup
START = 9219
# END = 9327
END = START
OUTPUT_FILE = 'output.txt'
BASE_URL = 'https://apps.tamidgroup.org/Consulting/Company/posting?id='

def main():

    companies = set()

    with open(OUTPUT_FILE, 'w') as f:
        for i in range(START, END + 1):
            html = get_html(i)
            company:dict = get_content(i, html)
            if 'name' in company.keys() and company['name'] not in companies:
                print_to_output_file(company, f)
                companies.add(company['name'].lower())

def get_html(i: int) -> str:
    f = open('test2.html', 'r')
    return f.read()


def get_content(id: int, html_file) -> dict:
    content = dict()

    soup = BeautifulSoup(html_file, 'lxml')

    box = soup.find_all('div', class_= 'u-shadow-v11 rounded g-pa-30')[0]

    

    # contains: name, rating, industry, website, company description, company size, point of 
    # contact
    # contains: deliverable description and work time 
    list_group_items = box.find_all('li', class_= 'list-group-item')
    proj_desc = box.find('p', class_='margin-bottom-40')
    if len(list_group_items) < 14:
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
    return content

def print_to_output_file(content: dict, f):
    """Takes dict as input and writes the content to output file"""
    for key, value in content.items():
        f.write(f"{key}: {value}\n")
    f.write("\n")

if __name__ == '__main__':
    main()


