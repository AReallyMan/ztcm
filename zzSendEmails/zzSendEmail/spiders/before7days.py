# -*- coding: utf-8 -*-
import scrapy
import datetime
from dateutil.relativedelta import relativedelta

class Before7daysSpider(scrapy.Spider):
    name = 'before7days'
    #allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']
    start_time = str(datetime.date.today() - relativedelta(days=7))
    end_time = str(datetime.date.today())
    def parse(self, response):
        yield {}
