import requests as rq
from bs4 import BeautifulSoup as bs
import csv


URL = 'https://www.beboss.ru/rating-tc'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.126 Yowser/2.5 Safari/537.36',
           'accept': '*/*'}
FILE = 'molls.csv'
# HOST = 'https://auto.ria.com'


def get_html(url, params=None):
    r = rq.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('tr', valign='top')
    molls = []

    for item in items:
        molls.append({
            'title': item.find('p', class_='rlist__name').get_text(strip=True),
            'area': item.find('p', class_='rlist__area').get_text(strip=True),
            'address': item.find('p', class_='rlist__address').get_text(strip=True).replace('На карте', ''),
            'rate': item.find('span', class_='w-rstars__text').get('data-score')
        })
    return molls


def get_pages_count(html):
    soup = bs(html, 'html.parser')
    pagination = soup.find_all('span', class_='b-paginator__link-shadow')
    pages = int(pagination[-2].get_text())
    return pages


def save_file(molls, path):
    with open (path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Площадь', 'Адрес', 'Рейтинг'])
        for item in molls:
            writer.writerow([item['title'], item['area'], item['address'], item['rate']])


def parse():
    html = get_html(URL)
    if html.status_code:
        pages = get_pages_count(html.text)
        molls = []
        for page in range(pages + 1):
            print(f'It is parsing page #{page} of {pages}...')
            html = get_html(URL, params={'page': page})
            molls.extend(get_content(html.text))
        save_file(molls, FILE)
        print(f'There are {len(molls)} molls')
    else:
        print('Error')


parse()