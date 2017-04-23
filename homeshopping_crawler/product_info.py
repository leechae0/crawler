# -*- coding: utf-8 -*-
import datetime


class ProductInfo(object):
    def __init__(self, name, category, start_time, end_time=None, price=None, image=None, product_id=None, detail_product_url=None):

        self.name = name
        self.category = category
        self.start_time = start_time
        self.end_time = end_time
        self.detail_product_url = detail_product_url
        self.price = price
        self.product_id = product_id
        self.image = image
        self.market_id = None
        self.market_name = None
