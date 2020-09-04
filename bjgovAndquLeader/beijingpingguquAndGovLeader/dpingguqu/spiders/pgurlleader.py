# -*- coding: utf-8 -*-

# @Time : 2020-07-27 11:25:55
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
import time
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import DpingguquItem
from ..settings import *


class NewpaperSpider(CrawlSpider):

    name = 'd2'

    start_urls = ['http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/fdzdgknr/jgzn432/index.html']
    rules = {
        Rule(LinkExtractor(allow='/pgqrmzf/bm/[a-z0-9]+/[a-z0-9]+/index\.html'),
             callback='parse_item'),
        Rule(LinkExtractor(allow='/pgqrmzf/zfxxgk68/xzjd20/[a-z]+/[a-z0-9]+/index\.html'),
             callback='parse_item')
    }

    def parse_item(self, response):
            """
            通过xpath设置过滤条件，筛选符合的数据爬取
            """
            item = DpingguquItem()
            next_url = response.xpath("//div[@class='xxgk-FenYe clearfix']/p/a[3]/@tagname").extract_first()
            if next_url == '[NEXTPAGE]':
                item['ld_url'] = ''
            else:
                item['ld_url'] = next_url
                yield item

            last_url = response.xpath("//div[@class='xxgk-FenYe clearfix']/p/a[4]/@tagname").extract_first()
            if last_url == '[LASTPAGE]':
                item['ld_url'] = ''
            else:
                item['ld_url'] = last_url
                yield item
            #item['ld_url'] = response.url

