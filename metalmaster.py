import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree


def url_master(url):
    ua = UserAgent()
    headers = {
        'Accept': '*/*',
        'User-Agent': ua.random
    }
    response = requests.get(url, headers=headers, verify=False, timeout=240)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    return soup


def metal_list(url):
    soup_s = url_master(url)
    offer = soup_s.find_all('li', class_='col-lg-4 col-md-4 col-sm-6')
    pages = ['https://sankt-peterburg.metalmaster.ru' + i.find('a', class_="item-name").get('href') for i in offer]
    for j in pages:
        metal_offer(j)


def metal_offer(url):
    soup = url_master(url)
    print(url)
    product_card = soup.find('div', class_='top__product clearfix')
    if soup.find('h1', class_='catolog__caption') is not None:
        name = soup.find('h1', class_='catolog__caption').text.strip()
    else:
        name = ''
    if soup.find('span', class_='product__right-price') is not None:
        price = soup.find('span', class_='product__right-price').text.strip().replace(' ', '').replace('руб.', '')
    else:
        price = ''
    if soup.find('a', class_='fancybox') is not None:
        image = 'https://sankt-peterburg.metalmaster.ru' + soup.find('a', class_='fancybox').get('href')
    else:
        image = ''
    response = requests.get(url, verify=False, timeout=240)
    html = response.text
    tree = etree.HTML(html)
    breadcrumbs = tree.xpath('//ul[@class="track__munu clearfix"]/li[@itemprop="itemListElement"]//span[@itemprop="name"]/text()')

    with open('metalmaster.csv', 'a', encoding='utf-8', newline="") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                [name] + [price] + [image] + ['1000']
                + ['0'] + ['metalmaster'] + breadcrumbs
            )
        )


def main():
    with open('metalmaster.txt') as file:
        urls = [line.rstrip() for line in file]
    for url in urls:
        metal_list(url)


if __name__ == '__main__':
    main()