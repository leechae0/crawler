# -*- coding: utf-8 -*-
import datetime


class ProductInfo(object):
    def __init__(self, name, category, start_time, end_time=None, price=None, image=None, shop_prod_id=None, product_id=None, detail_product_url=None, shop_code=None,
                 ch_no=None):

        self.name = name
        self.category = category
        self.start_time = start_time
        self.end_time = end_time
        self.ch_no=ch_no
        self.detail_product_url = detail_product_url
        self.price = price
        self.shop_prod_id=shop_prod_id
        self.product_id = product_id
        self.image = image
        self.market_id = None
        self.market_name = None
        self.shop_code=shop_code

