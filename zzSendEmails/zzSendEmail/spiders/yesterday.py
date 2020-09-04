# -*- coding: utf-8 -*-
import scrapy
import datetime


class YesterdaySpider(scrapy.Spider):
    name = 'yesterday'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    start_time = str(datetime.date.today() - datetime.timedelta(days=1))
    end_time = str(datetime.date.today())

    def parse(self, response):
        yield {}
