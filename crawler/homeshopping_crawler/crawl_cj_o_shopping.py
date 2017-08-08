import arrow

from product_info import ProductInfo
from utils import build_soup, get_text


def parsing_item(tag):
    category = ''
    the_time = ''
    for h4_tag in tag.findAll('h4'):
        for children_of_h4_tag in h4_tag.contents:
            the_time = get_text(children_of_h4_tag) or the_time

        for strong_tag in h4_tag.findAll('strong'):
            for strong_tag_content in strong_tag.contents:
                category = get_text(strong_tag_content) or category

    for image_tag in tag.findAll('img'):
        for children_of_image_tag in image_tag.contents:
            if not children_of_image_tag.name and children_of_image_tag.strip():
                yield category, the_time, children_of_image_tag.strip()


def crawling_page(window_arrow, is_yesterday=False):
    start_date = window_arrow.format('YYYYMMDD')
    url = "http://www.cjmall.com/etv/broad/schedule_list_week_iframe.jsp?start_date=" + start_date
    page_source = build_soup(url)
    table_source = page_source.findAll('tr')
    table_date = window_arrow.format('YYYY/MM/DD')
    week_days = table_source[0].findAll('td')
    index_for_the_day = 0
    for week_day in week_days:
        if table_date in str(week_day):
            break
        index_for_the_day += 1

    product_list = []
    for column in table_source[1:]:
        hour = int(column.findAll('th')[0].text)
        if not is_yesterday and 0 <= hour <= 5:
            continue
        if is_yesterday and hour > 5:
            continue

        item_for_week_days = column.findAll('td')
        item = item_for_week_days[index_for_the_day]
        for category, the_time, parsed_name in parsing_item(item):
            product_list.append(ProductInfo(name=parsed_name, start_time=the_time, category=category,))
    return product_list


def cj_o_shopping(window_arrow):
    print('CJ MALL')
    product_list = crawling_page(window_arrow)
    product_list.extend(crawling_page(window_arrow.replace(days=-1), True))

    return product_list

# for prod in cj_o_shopping(arrow.get('2017-04-09')):
#     print (prod)
