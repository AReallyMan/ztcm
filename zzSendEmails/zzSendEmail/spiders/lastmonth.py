# -*- coding: utf-8 -*-
import datetime

import scrapy
from dateutil.relativedelta import relativedelta


class LastmonthSpider(scrapy.Spider):
    name = 'lastmonth'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    start_time = str(datetime.date.today() - relativedelta(months=1))
    end_time = str(datetime.date.today())

    def parse(self, response):
        yield {}
