# -*- coding: utf-8 -*-
import arrow

from product_info import ProductInfo
from utils import build_soup, get_text_from_child, extract_value_from_url_key


def get_detail_prod_url_by_prod_id(prod_id):
    url = 'http://www.hyundaihmall.com/front/pda/itemPtc.do?slitmCd={0}'.format(
        prod_id,
    )
    return url


def get_image_url_bu_prod_id(prod_id):
    url = 'http://image.hyundaihmall.com/static/{0}/{1}/{2}/{3}/{4}_0_170.jpg'.format(
        prod_id[7],
        prod_id[6],
        prod_id[4:6],
        prod_id[2:4],
        prod_id,
    )
    return url


def parse_table(rows):
    the_time = ''
    category = ''
    for row in rows:
        product_link = ''
        image_url = ''
        product_name = ''
        product_id = ''
        price = ''
        time_item = row.find('th')
        if time_item:
            the_time = get_text_from_child(time_item)
            category = get_text_from_child(time_item.find('span'))
            category = row.get('th', {}).get('span', '') or category
        product_item = row.find('td')
        product_item = product_item.find('div', {'class': 'layerUp'}) or product_item
        price_item = product_item.find('dl', {'class': 'price'})
        product_item = product_item.find('dl', {'class': 'pdtTxts'}) or product_item
        product_item = product_item.find('dd', {'class': 'txt'}) or product_item
        product_link_item = product_item.find('a')
        if product_link_item:
            product_raw_link = product_link_item['href']
            product_name = get_text_from_child(product_link_item)
            product_id = extract_value_from_url_key(product_raw_link, 'slitmCd')
            if product_id:
                product_link = get_detail_prod_url_by_prod_id(product_id)
                image_url = get_image_url_bu_prod_id(product_id)

        if price_item:
            price_item = price_item.find('span', {'class': 'txtStrong'})
            if price_item:
                price = get_text_from_child(price_item)

        # yield the_time.split(' ~ ')[0], category, ''
        yield ProductInfo(
            name=product_name,
            start_time=the_time.split(' ~ ')[0],
            end_time=the_time.split(' ~ ')[1],
            category=category,
            shop_code='7',
            ch_no ='10',
            shop_prod_id=product_id,
            product_id='001811'+product_id,
            detail_product_url=product_link,
            image=image_url,
            price=price,
        )


def hyundai_home_shopping(window_arrow):
    print('H  MALL')
    url = 'http://www.hyundaihmall.com/front/bmc/brodPordPbdv.do?cnt=0&date={0}'.format(window_arrow.format('YYYYMMDD'))
    soup = build_soup(url)
    table = soup.find('table')
    rows = table.find('tbody').find_all('tr')
    product_list = []
    for product_info in parse_table(rows):
        product_list.append(product_info)
    return product_list

# for prod in hyundai_home_shopping(arrow.get('2017-04-09')):
#     print(prod)