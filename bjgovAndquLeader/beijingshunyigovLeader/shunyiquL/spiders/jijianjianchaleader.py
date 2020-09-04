# -*- coding: utf-8 -*-

# @Time : 2020-08-10 13:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re

from scrapy.spiders import CrawlSpider, Rule

from ..items import ShunyiqulItem
from scrapy.linkextractors import LinkExtractor


# 顺义区纪检监察
class ShunyiSpider(scrapy.Spider):
    name = 'jjjc'

    start_urls = [
        'http://jwjcw.bjshy.gov.cn/web/static/articles/catalog_ff808081518ee0d201519f4e06850015/article_ff8080816ab335cd016ab5dd1c5b0047/ff8080816ab335cd016ab5dd1c5b0047.html'
    ]

    def parse(self, response):
        for people in response.xpath("//div[@class='contxt']/p"):
            item = ShunyiqulItem()
            for name in re.findall(r'[\u4e00-\u9fa5]{3}|[\u4e00-\u9fa5] [\u4e00-\u9fa5]', people.xpath("./text()").extract_first()):
                item['ld_name'] = name
                item['ld_position'] = people.xpath("./strong/text()").extract_first()
                if '记' in item['ld_position'] or '常' in item['ld_position']:
                  item['ld_office'] = '中共北京市顺义区纪律检查委员会'
                else:
                    item['ld_office'] = '北京市顺义区监察委员会'
                item['ld_url'] = response.url
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item


