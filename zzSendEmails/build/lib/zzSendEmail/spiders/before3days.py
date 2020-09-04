# -*- coding: utf-8 -*-
import scrapy
import datetime
from dateutil.relativedelta import relativedelta

class Before3daysSpider(scrapy.Spider):
    name = 'before3days'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']
    start_time = str(datetime.date.today() - relativedelta(days=3))
    end_time = str(datetime.date.today())
    def parse(self, response):
        yield {}
