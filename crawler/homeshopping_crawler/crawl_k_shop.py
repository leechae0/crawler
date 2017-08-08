# -*- coding: utf-8 -*-
from datetime import datetime

import arrow


import requests
import json
from product_info import ProductInfo


def k_shop(window_arrow):
    print(' K SHOP')

    url = 'http://apitest.skymall.co.kr/apiv4/tv/today-goods-list?'
    params = {
        'mediaCode': 'TV07',
        'uk': 'TT131127012',
        'ck':'20170417145200',
        'nolog':'EPG'
    }
    response = requests.get(
        url,
        params=params,
        timeout=7.0,
    )

    response_json = response.json()

    #print(response_json)

    goodList = response_json['data']['goodsList']
    product_list = []

    for goods in goodList:
        startTime = goods['startTime']
        endTime = goods['endTime']

        # startTime = window_arrow
        # endTime = window_arrow
        product_list =[]
        product_list = goods['subGoodsList']
        for item in product_list:
            goodUrl = item['goodsUrl']
            goodsCode = item['goodsCode']
            goodsName = item['goodsName']
            saleDcAmt = item['saleDcAmt']

            imageUrl = get_imageUrl(goodUrl)


            print("startTime    : " + startTime)
            print("endTime      : " + endTime)
            print("goodName     : " + goodsName)
            print("goodCode     : " + goodsCode)
            print("imageUrl     : " + imageUrl)
            print("saleDcAmt    : " + str(saleDcAmt))
            print("detailURl    : " + "http://www.kshop.co.kr/goods/"+goodsCode)
            yield ProductInfo(
                name=goodsName,
                start_time=startTime,
                end_time=endTime,
                category='',
                shop_code='7',
                ch_no='20',
                shop_prod_id=goodsCode,
                product_id='003711'+goodsCode,
                detail_product_url="http://www.kshop.co.kr/goods/"+goodsCode,
                image=imageUrl,
                price=str(saleDcAmt),
            )
#
# def make_up_time(time):
#     # input : 2450 --> output : YYYY/MM/DD HH/mm/ss
#     time = datetime.strptime(time, '%H:%M')
#     arrow.get('2017-04-20')
#
#     year = time.struct_time.tm_year
#     month = time.struct_time.tm_mon
#
#
#     return time
#
#
#  if product.start_time:
#         hour_minute = datetime.datetime.strptime(product.start_time, '%H:%M').time()
#         product.start_time = window_arrow.replace(
#             hour=hour_minute.hour,
#             minute=hour_minute.minute
#         ).format('YYYY/MM/DD HH:mm:ss')



def get_imageUrl(goodUrl):
    url=goodUrl.replace('/w240','')
    r_url = url.replace('_i_','_g_')
    imageUrl=r_url.strip()

    return imageUrl

k_shop(arrow.get('2017-04-09'))