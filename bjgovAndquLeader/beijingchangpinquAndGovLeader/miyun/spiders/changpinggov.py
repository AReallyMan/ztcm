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
class NewpaperSpider(CrawlSpider):
    """
    1.遍历页面领导信息
    2.数据处理
    """
    name = 'cpgov'
    start_urls = ['http://www.bjchp.gov.cn/cpqzf/315734/1012559/1012560/2218276/index.html',
                  'http://www.bjchp.gov.cn/cpqzf/zj/cbjd/xxgk/1513568/index.html']
    rules = {
        Rule(LinkExtractor(allow='/cpqzf/zj/[a-z]+/[a-z0-9]+/\d+/index\.html'), callback='getUrl'),
        Rule(LinkExtractor(allow='/cpqzf/\d+/[0-9a-z]+/[0-9a-z]+/\d+/index\.html'), callback='getUrl')
    }

    def getUrl(self, response):
        url = 'http://www.bjchp.gov.cn' + response.xpath("//ul[@class='left_munu_c']/li[3]/h3/a/@href").extract_first()
        yield scrapy.Request(url=url, callback=self.getMsg)

    def getMsg(self, response):
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
            item['ld_office'] = response.xpath("//a[@class='SkinObject'][3]/text()").extract_first()
            item['ld_duty'] = re.compile(r'分工.*').findall(item['ld_resume'])[0]
            item['ld_url'] = response.url
            item['province'] = '北京市'
            item['city'] = '昌平区'
            item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['type'] = str(response.xpath("//div[@class='zhenjie_menu']/p/text()").extract_first()).replace("信息", '').replace("昌平区", '')
            if '镇街' in item['type']:
                item['county'] = item['ld_office']
            else:
                item['county'] = ''
            yield item




