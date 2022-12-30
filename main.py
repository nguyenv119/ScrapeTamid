from bs4 import BeautifulSoup
START = 9219
END = 9327
OUTPUT_FILE = 'output.txt'
BASE_URL = 'https://apps.tamidgroup.org/Consulting/Company/posting?id='

def main():

    companies = set()

    with open(OUTPUT_FILE, 'w') as f:
        for i in range(START, END + 1):
            html = get_html(i)
            company:dict = get_content(i, html)
            if company.has_key('name') and company.name not in companies:
                print_to_output_file(company, f)
            companies.add(company.name.lower())

def get_html(i: int) -> str:
    f = open('test.html', 'r')
    return f.read()


def get_content(i: int, html_file) -> dict:
    content = dict()

    soup = BeautifulSoup(html_file, 'lxml')
    soup.find('div', class_='row')

def print_to_output_file(content: dict, f):
    """Takes dict as input and writes the content to output file"""
    for key, value in content.items():
        f.write(f"{key}: {value}\n")
    f.write("\n")

if __name__ == '__main__':
    main()


