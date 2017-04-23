# -*- coding: utf-8 -*-
import urllib.parse

import arrow

from product_info import ProductInfo
from utils import build_soup, get_text_from_child, extract_value_from_url_key


def get_image_url_by_prod_id(prod_id):
    image_url = 'http://image.hnsmall.com/images/goods/{0}/{1}_g.png'.format(
        prod_id[-3:],
        prod_id
    )
    return image_url


def parse_table(rows, window_arrow):
    the_time = ''
    category = ''
    for row in rows:
        price = ''
        price_item = row.find('span', {'class': 'sell'})
        if price_item:
            price = get_text_from_child(price_item)

        td_time_item = row.find('td', {'class': 'dateTime'})
        if td_time_item:
            span_time_item = td_time_item.find('span', {'class': 'time'})
            the_time = get_text_from_child(span_time_item) or the_time

        td_goods_item = row.find('td', {'class': 'goods'})
        if td_goods_item:
            product_item = td_goods_item.find('div', {'class': 'text'}).find('a')
            product_url = product_item['href']
            prod_id = extract_value_from_url_key(product_url, 'goods_code')
            product_name = get_text_from_child(product_item)
            image = get_image_url_by_prod_id(prod_id)
            yield ProductInfo(
                name=product_name,
                start_time=the_time.split(' ~ ')[0],
                end_time=the_time.split(' ~ ')[1],
                category=category,
                price=price,
                image=image,
                product_id=prod_id,
                detail_product_url=product_url,
            )


def home_and_shopping(window_arrow):
    print('HNSMALL')
    url = "http://www.hnsmall.com/display/tvtable.do?from_date={0}".format(
        urllib.parse.quote(window_arrow.format('YYYY/MM/DD'), safe='')
    )

    soup = build_soup(url)
    rows = soup.find('table').find('tbody').find_all('tr')
    product_list = []
    for prod_info in parse_table(rows, window_arrow):
        product_list.append(prod_info)

    return product_list


# for prod in home_and_shopping(arrow.get('2017-04-09')):
#     print(prod)
