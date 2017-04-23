# -*- coding: utf-8 -*-
import datetime

import arrow
import xlwt

from crawl_cj_o_shopping import cj_o_shopping
from crawl_gs_shop import gs_shop
from crawl_home_and_shopping import home_and_shopping
from crawl_hyundai_home_shopping import hyundai_home_shopping
from crawl_lotte_home_shopping import lotte_home_shopping
from crawl_k_shop import k_shop


def build_xlwt(product_list):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('test', cell_overwrite_ok=True)

    row = 0
    for product in product_list:
        worksheet.write(row, 0, product.start_time)
        worksheet.write(row, 1, product.end_time)
        worksheet.write(row, 2, product.market_name)
        worksheet.write(row, 3, product.category)
        worksheet.write(row, 4, product.name)
        worksheet.write(row, 5, product.product_id)
        worksheet.write(row, 6, product.image)
        worksheet.write(row, 7, product.price)
        worksheet.write(row, 8, product.detail_product_url)
        row += 1

    workbook.save("EPG.xls")




def make_up_product_info(product, window_arrow, market_id, market_name):
    product.market_name = market_name
    product.market_id = market_id
    if product.start_time:
        if market_name=="kshop":
            hour = str(product.start_time)[0:2]
            miniute = str(product.start_time)[2:4]
            time = hour + ":" + miniute
            HM_Time = datetime.datetime.strptime(time, '%H:%M').time()

            date = arrow.utcnow().date()
            cur_date_time = str(date) + str(HM_Time)

            product.start_time=cur_date_time.format('YYYY/MM/DD HH:mm:ss')

        else:
            hour_minute = datetime.datetime.strptime(product.start_time, '%H:%M').time()
            product.start_time = window_arrow.replace(
                hour=hour_minute.hour,
                minute=hour_minute.minute
            ).format('YYYY/MM/DD HH:mm:ss')
    if product.end_time:
        if product.market_name=="kshop":
            hour = str(product.end_time)[0:2]
            miniute = str(product.end_time)[2:4]
            if hour ==24:
                hour =00
                time = hour + ":" + miniute
                HM_Time = datetime.datetime.strptime(time, '%H:%M').time()

            date = arrow.utcnow().date()
            cur_date_time = str(date) + str(HM_Time)

            product.end_time=cur_date_time.format('YYYY/MM/DD HH:mm:ss')

        else:
            hour_minute = datetime.datetime.strptime(product.end_time, '%H:%M').time()
            product.end_time = window_arrow.replace(
                hour=hour_minute.hour,
                minute=hour_minute.minute
            ).format('YYYY/MM/DD HH:mm:ss')
    return product



def yield_product(window_arrow):
    # for product in cj_o_shopping(window_arrow):
    #     yield make_up_product_info(product, window_arrow, 1, 'cjmall')

    for product in gs_shop(window_arrow):
        yield make_up_product_info(product, window_arrow, 2, 'gsshop')

    for product in hyundai_home_shopping(window_arrow):
        if product.product_id.startswith('20'):
            product.product_id = product.product_id[2:]
        yield make_up_product_info(product, window_arrow, 3, 'hmall')

    for product in home_and_shopping(window_arrow):
        yield make_up_product_info(product, window_arrow, 4, 'hnsmall')

    for product in lotte_home_shopping(window_arrow):
        yield make_up_product_info(product, window_arrow, 5, 'lotte')

    for product in k_shop(window_arrow):
        yield make_up_product_info(product, '', 6, 'kshop')



def main():
    print("#################################################")
    print("####### Homeshopping EPG Crawling Program #######")
    print("#################################################")

    window_start_arrow = arrow.get('2017-04-20')
    window_end_arrow = arrow.get('2017-04-21')
    product_list = []
    for day_date in range((window_end_arrow - window_start_arrow).days + 1):
        print('[{0}] DATE: {1}'.format(
            day_date,
            window_start_arrow.replace(days=day_date).datetime)
        )
        product_list.extend(
            [p for p in yield_product(window_start_arrow.replace(days=day_date))]
        )
    build_xlwt(product_list)


if __name__ == '__main__':
    main()
