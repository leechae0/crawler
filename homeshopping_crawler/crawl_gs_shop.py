# -*- coding: utf-8 -*-
import arrow

from product_info import ProductInfo
from utils import build_soup, get_text, get_text_from_child, extract_value_from_url_key


def parsing_td_time(items):
    the_time = ''
    for td_item in items:
        for div_item in td_item.find_all('div', {'class': 'airSchedule-time'}):
            time_tag = div_item.find('strong')
            if time_tag:
                for child in time_tag.contents:
                    the_time = get_text(child)
    return the_time


def parsing_td_desc(items):
    category = ''
    product_name = ''
    for td_item in items:
        span_item = td_item.find('span', {'class': 'category'})
        if span_item:
            category_item = span_item.find('a', {'class': 'prod_link'})
            if category_item:
                category = get_text_from_child(category_item)
        div_item = td_item.find('div', {'class': 'tdWrap'})
        if div_item:
            product_item = div_item.find('a', {'class': 'prod_link'}, recursive=False)
            if product_item:
                product_name = get_text_from_child(product_item)
    return category, product_name


def parsing_td_price(items):
    the_price = ''
    for td_item in items:
        div_item = td_item.find('div', {'class': 'tdWrap'})
        if div_item:
            price_item = div_item.find('ins')
            price_item = price_item.find('b') if price_item else price_item
            if price_item:
                the_price = get_text_from_child(price_item)
    return the_price


def parsing_td_pic(items):
    the_id = ''
    for td_item in items:
        div_item = td_item.find('div', {'class': 'tdWrap'})
        if div_item:
            link = div_item.find('a')
            if link:
                the_id = extract_value_from_url_key(link['href'], 'prdid')
                break

    return the_id


def get_image_url_by_prod_id(prod_id):
    image_url = 'http://image.gsshop.com/image/{0}/{1}/{2}_L1.jpg'.format(
        prod_id[0:2],
        prod_id[2:4],
        prod_id
    )
    return image_url


def get_product_detail_url_by_prod_id(prod_id):
    prod_detail_url = 'http://with.gsshop.com/prd/prd.gs?prdid={0}'.format(
        prod_id
    )
    return prod_detail_url


def gs_shop(window_arrow):
    print('GS MALL')
    url = 'http://with.gsshop.com/tv/tvScheduleMain.gs?lseq=397357&selectDate={0}'.format(
        window_arrow.format('YYYYMMDD'))
    soup = build_soup(url)
    tables = soup.findAll('table')
    product_list = []
    for table in tables:
        rows = table.findAll('tr')
        the_time = ''
        for row in rows:
            column_times = row.find_all('td', {'class': 'time'})
            column_descs = row.find_all('td', {'class': 'desc'})
            column_prices = row.find_all('td', {'class': 'price'})
            column_pics = row.find_all('td', {'class': 'pic'})
            the_time = parsing_td_time(column_times) or the_time
            category, product = parsing_td_desc(column_descs)
            price = parsing_td_price(column_prices)
            the_id = parsing_td_pic(column_pics)
            if not category or not product:
                continue
            image_url = get_image_url_by_prod_id(the_id) if the_id else ''
            prod_detail_url = get_product_detail_url_by_prod_id(the_id) if the_id else ''
            product_list.append(
                ProductInfo(
                    name=product,
                    start_time=the_time.split('-')[0],
                    end_time=the_time.split('-')[1],
                    category=category,
                    price=price,
                    image=image_url,
                    product_id=the_id,
                    detail_product_url=prod_detail_url,
                )
            )
    return product_list


# for product in gs_shop(arrow.get('2017-04-09')):
#     print(product)
