# -*- coding: utf-8 -*-

# @Time : 2020-07-31 16:26:36
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
class NewpaperSpider(CrawlSpider):
    """
    1、通过Rule匹配机构设置部门所有的url
    2、找到领导简介url
    3、获取数据
    """
    name = 'mtggov'
    start_urls = ['http://www.bjmtg.gov.cn/bjmtg/zwxx/jgsz/index.shtml']
    rules = {
        Rule(LinkExtractor(allow='/bjmtg/[a-z]+/[a-z]+/[a-z]+/index\.shtml'), callback='getLeaderUrl'),
    }

    def getLeaderUrl(self, response):
        if response.xpath("//ul[@class='mt5']/li[2]/a/@href"):
            leaderUrl = 'http://www.bjmtg.gov.cn' + response.xpath("//ul[@class='mt5']/li[2]/a/@href").extract_first()
            yield scrapy.Request(url=leaderUrl, callback=self.getPage)

    def getPage(self, response):
        pages = re.compile(r"page_div',(\d)").findall(response.text)[0]
        for page in range(1, int(pages) + 1):
            if page == 1:
                yield scrapy.Request(url=response.url, callback=self.getMsg, dont_filter=True)
            else:
                lurl = str(response.url).split("index")[0] + 'index_' + str(page) + '' + \
                       str(response.url).split("index")[1]
                yield scrapy.Request(url=lurl, callback=self.getMsg)

    def getMsg(self, response):
        item = MiyunItem()
        for path in response.xpath("//ul[@class='mt20 list']/li"):
            item['ld_icon'] = 'http://www.bjmtg.gov.cn' + str(path.xpath("./div/img/@src").extract_first()).replace(
                "\n", '')
            item['ld_name'] = str(path.xpath("./div/p[1]/text()").extract_first()).strip()
            item['ld_office'] = response.xpath("//div[@class='BreadcrumbNav']/p/a[5]/text()").extract_first()
            item['ld_resume'] = ''.join(re.compile(r'[\u4e00-\u9fa5]+|\d{4}年|\d月|\d{2}月|：|。|，').findall(
                path.xpath("./div[2]").xpath("string(.)").extract_first()))
            if re.compile(r'现任(.*?。)').findall(item['ld_resume']):
                item['ld_position'] = re.compile(r'现任(.*?。)').findall(item['ld_resume'])[0]
            elif re.compile(r'现任(.*?)基本').findall(item['ld_resume']):
                if '个人' in re.compile(r'现任(.*?)基本').findall(item['ld_resume']):
                    item['ld_position'] = re.compile(r'现任(.*?)个人基本').findall(item['ld_resume'])[0]
                else:
                    item['ld_position'] = re.compile(r'现任(.*?)基本').findall(item['ld_resume'])[0]
            elif re.compile(r'现任(.*?，)').findall(item['ld_resume']):
                item['ld_position'] = re.compile(r'现任(.*?，)').findall(item['ld_resume'])[0]
            elif re.compile(r'党(.*?)工作').findall(item['ld_resume']):
                item['ld_position'] = re.compile(r'党(.*?)工作').findall(item['ld_resume'])[0]
            elif '园林绿化局' in item['ld_office'] and re.compile(r'。(.*)负责').findall(item['ld_resume']):
                item['ld_position'] = re.compile(r'。(.*)负责').findall(item['ld_resume'])[0]
            elif re.compile(r'务：(.*?)性').findall(item['ld_resume']):
                item['ld_position'] = re.compile(r'务：(.*?)性').findall(item['ld_resume'])[0]
            else:
                item['ld_position'] = ''

            if re.compile(r'分工.*?。').findall(item['ld_resume']):
                item['ld_duty'] = re.compile(r'分工.*?。').findall(item['ld_resume'])[0]
            elif re.compile(r'分管.*?。').findall(item['ld_resume']):
                item['ld_duty'] = re.compile(r'分管.*?。').findall(item['ld_resume'])[0]
            elif re.compile(r'分工.*').findall(item['ld_resume']):
                item['ld_duty'] = re.compile(r'分工.*').findall(item['ld_resume'])[0]
            elif re.compile(r'主持.*?。').findall(item['ld_resume']):
                item['ld_duty'] = re.compile(r'主持.*?。').findall(item['ld_resume'])[0]
            elif '区体育局' in item['ld_office'] and re.compile(r'党组工作.*').findall(item['ld_resume']):
                item['ld_duty'] = re.compile(r'党组工作.*').findall(item['ld_resume'])[0]
            elif re.compile(r'负责.*?。').findall(item['ld_resume']):
                item['ld_duty'] = re.compile(r'负责.*?。').findall(item['ld_resume'])[0]
            else:
                item['ld_duty'] = ''
            item['ld_url'] = response.url
            item['province'] = '北京市'
            item['city'] = '门头沟区'
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['type'] = response.xpath("//div[@class='BreadcrumbNav']/p/a[4]/text()").extract_first()
            if '乡镇' in item['type'] or '办事处' in item['type']:
                item['county'] = item['ld_office']
            else:
                item['county'] = ''
            yield item
