from bs4 import BeautifulSoup
START = 9219
# END = 9327
END = START + 1
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
    f = open('uh.html', 'r')
    return f.read()


def get_content(id: int, html_file) -> dict:
    content = dict()

    soup = BeautifulSoup(html_file, 'lxml')

    box = soup.find_all('div', class_= 'u-shadow-v11 rounded g-pa-30')
    list_group_items = box[0].find_all('div', class_= 'list-group-item')

    content['name'] = ''
    content['industry'] = ''
    content['url'] = f'{BASE_URL}{id}'
    content['website'] = ''
    content['company_description'] = ''
    content['project_description'] = ''
    content['deliverable'] = ''
    content['work_time'] = ''
    content['new_or_existing'] = ''
    content['deliverable_type'] = ''
    content['work_type'] = ''
    content['tech_stack'] = ''
    return content

def print_to_output_file(content: dict, f):
    """Takes dict as input and writes the content to output file"""
    for key, value in content.items():
        f.write(f"{key}: {value}\n")
    f.write("\n")

if __name__ == '__main__':
    main()


