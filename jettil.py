import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree


def url_master(url):
    ua = UserAgent()
    headers = {
        'Accept': '*/*',
        'User-Agent': ua.random
    }
    req = requests.get(url=url, headers=headers, timeout=640)
    soup = BeautifulSoup(req.text, "lxml")
    return soup


def Jet_check(url):
    soup_s = url_master(url)
    if soup_s.find('div', 'component-navigation-pagination js-component-navigation-pagination') is None:
        Jet_products(url)
    else:
        pages = soup_s.find('div', 'component-navigation-pagination js-component-navigation-pagination').find_all('li')[
            -1].text.strip()
        for i in range(int(pages)):
            Jet_products(f'{url}?PAGEN_1={i+1}')


def Jet_products(url):
    soup_f = url_master(url)
    lists = soup_f.find_all('div', class_='component-item-product component-wrapper-default js-component-item-product')
    for i in lists:
        if i.find('a', class_='title') is None:
            continue
        else:
            JEJ_offer('https://www.jettools.ru' + i.find('a', class_='title').get('href'))


def JEJ_offer(url):
    soup = url_master(url)
    print(url)
    if soup.find('link') is not None:
        if soup.find('div', class_='page-product__params') is not None:
            article = soup.find('div', class_='page-product__params').text.strip().replace('Артикул: ', '')
        else:
            article = ''

        if soup.find('div', class_='component-wrapper-default mb-gutter').find('h1') is not None:
            name = soup.find('div', class_='component-wrapper-default mb-gutter').find('h1').text.strip()
        else:
            name = ''

        if soup.find('span', class_='actual js-page-product__price-actual') is not None:
            price = soup.find('span', class_='actual js-page-product__price-actual').text.strip().replace(' ', '').replace(
                '₽', '')
        else:
            price = ''

        if soup.find('div', class_="page-product-photo__main-item js-page-product-photo__main-item").find(
                'img') is not None:
            img = 'https://www.jettools.ru' + soup.find('div',
                                                        class_="page-product-photo__main-item js-page-product-photo__main-item").find(
                'img').get('src')
        else:
            img = ''

        if soup.find('div', class_="col-8 content-wrapper js-content-wrapper").find('table') is not None:
            specs = soup.find('div', class_="col-8 content-wrapper js-content-wrapper").find('table')
        else:
            specs = ''

        response = requests.get(url, timeout=640)
        html = response.text
        tree = etree.HTML(html)
        breadcrumbs = tree.xpath('//ul[@class="component-navigation-breadcrumbs"]/li/a/span/text()')[:-1]

        with open('jet.csv', 'a', encoding='utf-8', newline="") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    [article] + [name] + [price] + [specs] + [img] + ['jettools'] + breadcrumbs
                )
            )


def main():
    sp = url_master('https://www.jettools.ru').find_all('div', class_='item js-item')
    for i in sp:
        if i.find('a').text.split() == ['Powermatic']:
            Jet_check('https://www.jettools.ru/catalog/powermatic/')
        else:
            Jet_check('https://www.jettools.ru' + i.find('a').get('href'))


if __name__ == '__main__':
    main()
