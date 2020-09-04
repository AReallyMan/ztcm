# -*- coding: utf-8 -*-

# @Time : 2020-08-04 16:21:34
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re

import scrapy as scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import MiyunItem
from ..settings import *


# 北京市昌平区机构设置领导信息
class NewpaperSpider(scrapy.Spider):
    """
    1.遍历页面领导信息
    2.数据处理
    """
    name = 'cp'
    start_urls = ['http://www.bjchp.gov.cn/cpqzf/xxgk2671/ldjs90/qwld81/index.html',
                  'http://www.bjchp.gov.cn/cpqzf/xxgk2671/ldjs90/qrdld91/index.html',
                  'http://www.bjchp.gov.cn/cpqzf/xxgk2671/ldjs90/qzfld60/index.html',
                  'http://www.bjchp.gov.cn/cpqzf/xxgk2671/ldjs90/qzxld37/index.html']

    def parse(self, response):
        '''
        获取领导信息
        :param response:
        :return:
        '''
        item = MiyunItem()
        for path in response.xpath("//div[@class='ldbox']/ul"):
            item['ld_icon'] = 'http://www.bjchp.gov.cn' + path.xpath("./li/img/@src").extract_first()
            item['ld_name'] = re.compile(r'(.*)：').findall(path.xpath("./li/p[1]/text()").extract_first())[0]
            item['ld_resume'] = ''.join(re.compile(u"[\u4e00-\u9fa5]+|\d{4}年|\d月|\d{2}月|：|。|，|；|、").findall(path.xpath("./li[@class='ld_cont fr']").xpath('string(.)').extract_first()))
            item['ld_position'] = re.compile(r'：(.*)').findall(path.xpath("./li/p[1]/text()").extract_first())[0]
            item['ld_office'] = '昌平' + str(response.xpath("//div[@class='location']/span/a[4]/text()").extract_first()).replace("领导", '')
            item['ld_duty'] = ''
            item['ld_url'] = response.url
            item['province'] = '北京市'
            item['city'] = '昌平区'
            item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['type'] = item['ld_office']
            yield item




