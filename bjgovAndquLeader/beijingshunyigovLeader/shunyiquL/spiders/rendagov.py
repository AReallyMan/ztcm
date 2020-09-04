# -*- coding: utf-8 -*-

# @Time : 2020-08-10 09:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re

from scrapy.spiders import CrawlSpider, Rule

from ..items import ShunyiqulItem
from scrapy.linkextractors import LinkExtractor


# 顺义区人民代表大会常务委员会（机构设置）
class ShunyiSpider(CrawlSpider):
    name = 'rendagov'

    start_urls = [
        'http://renda.bjshy.gov.cn/rdweb/page/list.jsp?catalog=/rdgk/jgsz'
    ]
    rules = {
        Rule(LinkExtractor(allow='../\d{6}/\d{4}\.html'), callback='getMsg')
    }

    def getMsg(self, response):
        # 通过正则无法区分机构和其他新闻的链接，通过获取导航栏标签机构设置进行区分
        if "机构设置" in response.xpath("//div[@class='dqwz']/span/a/text()").extract():
            item = ShunyiqulItem()
            item['gov_desc'] = ''.join(response.xpath("//div[@class='abody']").xpath("string(.)").extract_first())
            item['gov_name'] = response.xpath("//div[@class='article']/h2/text()").extract_first()
            item['province'] = '北京市'
            item['city'] = '顺义区'
            item['type'] = '人大'
            item['gov_super'] = '北京市人大常委会'
            item['gov_head'] = '主任'
            item['gov_url'] = response.url
            item['gov_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield item
