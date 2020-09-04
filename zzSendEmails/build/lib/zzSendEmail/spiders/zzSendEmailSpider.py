# -*- coding: utf-8 -*-
import datetime

import scrapy
from ..items import ZzsendemailItem


class ZzsendemailspiderSpider(scrapy.Spider):
    name = 'zzSendEmailSpider'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']
    # 设置事件参数

    start_time = end_time = str(datetime.date.today())

    def parse(self, response):
        yield ZzsendemailItem()
