# -*- coding: utf-8 -*-

# @Time : 2020-08-03 16:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re
import scrapy
from ..items import MiyunItem
from ..settings import *
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# 北京市门头沟区领导信息
class NewpaperSpider(scrapy.Spider):
    """
    1、通过Rule正则匹配区领导所有的url
    2、找到领导简介url
    3、进行数据处理，获取领导信息
    """
    name = 'sjs'
    start_urls = ['http://www.bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/',
                  'http://www.bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qrd_1948/',
                  'http://www.bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzf_1949/',
                  'http://www.bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzx_1950/']

    def parse(self, response):
        item = MiyunItem()
        for path in response.xpath("//ul[@class='ldList']/li"):
            item['ld_url'] = response.url
            item['ld_name'] = path.xpath("./div/div[@class='con'][1]/p/text()").extract_first()
            item['ld_resume'] = path.xpath("./div/div[@class='con'][3]/p/text()").extract_first()
            item['ld_position'] = path.xpath("./div/div[@class='con'][2]/p/text()").extract_first()
            item['city'] = '石景山区'
            item['ld_duty'] = ''
            item['province'] = '北京市'
            item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['type'] = re.compile(r'[\u4e00-\u9fa5]+').findall(re.compile(r'介绍(.*)').findall(response.xpath("//div[@class='crumbs btmLine']/text()").extract_first())[0])[0]
            item['ld_office'] = item['city'] + item['type']
            item['ld_icon'] = response.url + str(
                    path.xpath("./div/img/@src").extract_first()).replace('./', '')
            yield item




