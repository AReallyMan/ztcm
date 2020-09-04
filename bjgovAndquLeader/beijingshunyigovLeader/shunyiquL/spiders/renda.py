# -*- coding: utf-8 -*-

# @Time : 2020-08-07 12:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re

from scrapy.spiders import CrawlSpider, Rule

from ..items import ShunyiqulItem
from scrapy.linkextractors import LinkExtractor


# 顺义区人民代表大会常务委员会（主任之窗）在前边获取顺义区领导信息时，已经包含了主任之窗里的领导信息
class ShunyiSpider(CrawlSpider):
    name = 'renda'

    start_urls = [
        'http://renda.bjshy.gov.cn/rdweb/201811/916.html'
    ]
    rules = {
        Rule(LinkExtractor(allow='../\d+/\d+\.html'), callback='getMsg')
    }

    def getMsg(self, response):
        item = ShunyiqulItem()
        item['ld_resume'] = ''.join(response.xpath("//div[@class='zr-xxxx']").xpath("string(.)").extract_first())
        item['ld_name'] = response.xpath("//div[@class='zr-name']/a/text()").extract_first()
        item['ld_icon'] = response.urljoin(response.xpath("//div[@class='zrzc-photo']/img/@src").extract_first())
        item['ld_office'] = '顺义区人民代表大会常务委员会'
        item['ld_position'] = re.findall(r'现任(.*)', item['ld_resume'])[0]
        item['ld_duty'] = response.xpath("//div[@class='zrjy-xxxx zrjy-xxxx3']/p/text()").extract_first()
        item['ld_url'] = response.url
        item['province'] = '北京市'
        item['city'] = '顺义区'
        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['type'] = '区人大'
        yield item
