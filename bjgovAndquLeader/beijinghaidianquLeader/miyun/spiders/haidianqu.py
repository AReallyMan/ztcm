# -*- coding: utf-8 -*-

# @Time : 2020-08-04 13:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re

import scrapy as scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import MiyunItem
from ..settings import *


# 北京市海淀区领导信息
class NewpaperSpider(scrapy.Spider):
    """
    1.遍历页面领导信息
    2.数据处理
    """
    name = 'hd'
    start_urls = ['http://www.bjhd.gov.cn/zwdt/xxgk/zfxxgk/ldjs/qzf/']

    def parse(self, response):
        for url in re.compile(r'http://zyk.bjhd.gov.cn/zwdt/xxgk/zfxxgk/ldjs/qzf/\d+/t\d+_\d+\.shtml').findall(response.text):
            yield scrapy.Request(url=url, callback=self.getMsg)

    def getMsg(self, response):
        '''
        获取领导信息
        :param response:
        :return:
        '''
        item = MiyunItem()
        if response.xpath("//div[@id='mainText']/p/img/@src"):
            item['ld_icon'] = str(response.url).split("/t")[0] + '/' + str(response.xpath("//div[@id='mainText']/p/img/@src").extract_first()).replace("./", '')
        elif response.xpath("//div[@id='mainText']/div/p/img/@src"):
            item['ld_icon'] = str(response.url).split("/t")[0] + '/' + str(response.xpath("//div[@id='mainText']/div/p/img/@src").extract_first()).replace("./", '')
        elif response.xpath("//div[@class='mainTextBox']/div/img/@src"):
            item['ld_icon'] = str(response.url).split("/t")[0] + '/' + str(response.xpath("//div[@class='mainTextBox']/div/img/@src").extract_first()).replace("./", '')
        else:
            item['ld_icon'] = str(response.url).split("/t")[0] + '/' + str(
                response.xpath("//div[@class='mainTextBox']/div/span/img/@src").extract_first()).replace("./", '')
        item['ld_name'] = response.xpath("//div[@class='header']/h1/text()").extract_first()
        item['ld_resume'] = ''.join(re.compile(u"[\u4e00-\u9fa5]+|\d{4}年|\d月|\d{2}月|：|。|，|；|、").findall(response.xpath("//div[@id='mainText']").xpath('string(.)').extract_first()))
        item['ld_position'] = re.compile(u'现任(.*?。)').findall(item['ld_resume'])[0]
        item['ld_office'] = '区政府'
        item['ld_duty'] = re.compile(u'分管.*').findall(item['ld_resume'])[0]
        item['ld_url'] = response.url
        item['province'] = '北京市'
        item['city'] = '海淀区'
        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['type'] = '区政府'
        yield item




