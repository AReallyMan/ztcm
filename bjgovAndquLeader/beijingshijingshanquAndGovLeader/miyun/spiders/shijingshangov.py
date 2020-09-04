# -*- coding: utf-8 -*-

# @Time : 2020-08-04 10:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re
import time

import scrapy
from scrapy.spiders import CrawlSpider, Rule

from ..items import MiyunItem
from ..settings import *
from scrapy.linkextractors import LinkExtractor


# 北京市门头沟区领导信息
class NewpaperSpider(scrapy.Spider):
    """
    1、通过Rule匹配机构设置部门所有的url
    2、找到领导简介url
    3、获取数据
    """
    name = 'sjsgov'
    start_urls = ['http://www.bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/zfbm_1951/',
                  'http://www.bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/jdbsc_1952/']

    def parse(self, response):

        '''
        领导信息url是通过js加载出来的，我们先获取到url
        :param response:
        :return:
        '''
        item = MiyunItem()
        urllist = re.compile(r"http://www.bjsjs.gov.cn/[a-z]+/[a-z]+/[a-z]+_\d+/ldjs_\d+/").findall(response.text)
        type = (re.compile(r'[\u4e00-\u9fa5]+').findall(re.compile(r'介绍(.*)').findall(response.xpath("//div[@class='crumbs btmLine']/text()").extract_first())[0])[0])
        item['type'] = type
        for url in urllist:
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.getMsg)

    def getMsg(self, response):
        item = response.meta['item']
        for path in response.xpath("//ul[@class='list_ldjs']/li"):
            item['ld_icon'] = response.url + str(path.xpath("./div/a/img/@src").extract_first()).replace(
                "./", '')
            if path.xpath("./div/h3/text()"):
                item['ld_name'] = path.xpath("./div/h3/text()").extract_first()
            elif path.xpath("./div/a/img/@alt"):
                item['ld_name'] = re.compile(r'[\u4e00-\u9fa5]+').findall(path.xpath("./div/a/img/@alt").extract_first())[0]
            else:
                item['ld_name'] = ''
            item['ld_office'] = str(response.xpath("//div[@class='uName']/text()").extract_first()).replace("政务公开", '')
            item['ld_resume'] = str(path.xpath("./div[@class='txtCon']").xpath("string(.)").extract_first()).strip()
            item['ld_position'] = path.xpath("./div/h3/span/text()").extract_first()
            item['ld_duty'] = re.compile(r'分工(.*)').findall(item['ld_resume'])[0]
            item['ld_url'] = response.url
            item['province'] = '北京市'
            item['city'] = '石景山区'
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if '街道' in item['type']:
                item['county'] = item['ld_office']
            else:
                item['county'] = ''
            yield item
