from bs4 import BeautifulSoup

def get_consulting_content(id: int, html_file, base_url) -> dict:
    content = dict()

    soup = BeautifulSoup(html_file, 'lxml')

    box = soup.find_all('div', class_= 'u-shadow-v11 rounded g-pa-30')
    if len(box) < 2:
        print('\terror - redirect')
        return {}
    else:
        box1 = box[0]
        box2 = box[1]
    # contains: name, rating, industry, website, company description, company size, point of 
    # contact
    # contains: deliverable description and work time 
    list_group_items = box1.find_all('li', class_= 'list-group-item')
    if not (9 == len(list_group_items)):
        print('\terror - not consulting')
        return {}
    proj_desc = box1.find('p', class_='margin-bottom-40')
    if len(proj_desc) == 0:
        print('\terror - not consulting')
        return {}
    if len(box2) < 2:
        print('\terror - not consulting')
        return {}
    start_date = box2.find_all('div', class_='col-xs-6')
    start_date = start_date[1].text.strip()
    if not("2023" in start_date):
        print('\tWrong year')
        return {}
    

    content['name'] = f"{list_group_items[0].find('div', class_='col-xs-8').text.strip()}"
    content['start_date'] = f"{start_date}"
    content['industry'] = f"{list_group_items[2].find('div', class_='col-xs-8').text.strip()}" 
    content['url'] = f'{base_url}{id}'
    content['website'] = f"{list_group_items[3].find('div', class_='col-xs-8').text.strip()}"
    print()
    return content
