import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv
from lxml import etree


def url_master(url):
    ua = UserAgent()
    headers = {
        'Accept': '*/*',
        'User-Agent': ua.random
    }
    response = requests.get(url, headers=headers, timeout=240)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup


def triton_list(url):
    soup = url_master(url)
    offer_tokens = soup.find_all('a', class_='charact-link') + soup.find_all('a', class_='tab-item-link')
    for u in offer_tokens:
        triton_offer('https:' + u.get('href'))


def triton_offer(url):
    soup = url_master(url)
    print(url)

    if soup.find('div', class_='articul') is not None:
        article = soup.find('div', class_='articul').text.strip().replace('Артикул: ', '')

    else:
        article = ''

    if soup.find('h1', class_='card__main-title') is not None:
        name = soup.find('h1', class_='card__main-title').text.strip()

    else:
        name = ''

    if soup.find('span', class_='v_price') is not None:
        price = soup.find('span', class_='v_price').text.strip().replace(' ', '')

    else:
        price = ''

    if soup.find('img', class_='img-fluid') is not None:
        image = 'https://www.triton-welding.ru/' + soup.find('img', class_='img-fluid').get('src')
    else:
        image = ''
    response = requests.get(url, timeout=240)
    html = response.text
    tree = etree.HTML(html)
    breadcrumbs = tree.xpath('//li[@class="breadcrumb-item"]/a/text()')
    with open('triton.csv', 'a', encoding='utf-8', newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                    [article] + [name] + [price] + [image] + ['1000'] + ['0'] + ['triton'] + breadcrumbs
            )
        )


def main():
    triton_list('https://www.triton-welding.ru/products.html')


if __name__ == '__main__':
    main()
