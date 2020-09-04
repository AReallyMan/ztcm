# -*- coding: utf-8 -*-

# @Time : 2020-08-07 14:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re

from scrapy.spiders import CrawlSpider, Rule

from ..items import ShunyiqulItem
from scrapy.linkextractors import LinkExtractor


# 顺义区委员会
class ShunyiSpider(CrawlSpider):
    name = 'wyh'

    start_urls = [
        'http://zhengxie.bjshy.gov.cn/news/95.aspx',
        'http://zhengxie.bjshy.gov.cn/news/96.aspx',
        'http://zhengxie.bjshy.gov.cn/news/167.aspx'
    ]
    rules = {
        Rule(LinkExtractor(allow='/news/show-\d+\.aspx'), callback='getMsg'),
    }

    def getMsg(self, response):
        '''
        获取页面领导信息
        :param response:
        :return:
        '''
        item = ShunyiqulItem()
        item['ld_name'] = response.xpath("//td[@id='textcontent']/p/span[2]/text()").extract_first()
        item['ld_icon'] = response.urljoin(response.xpath("//td[@id='textcontent']/p/img/@src").extract_first())
        item['ld_office'] = '顺义区委员会'
        item['ld_position'] = response.xpath("//td[@id='textcontent']/p/span[1]/text()").extract_first()
        item['ld_url'] = response.url
        item['province'] = '北京市'
        item['city'] = '顺义区'
        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['type'] = '区政协'
        yield item
