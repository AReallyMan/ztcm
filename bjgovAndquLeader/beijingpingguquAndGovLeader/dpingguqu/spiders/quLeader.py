# -*- coding: utf-8 -*-

# @Time : 2020-07-27 11:25:55
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
import time
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import DpingguquItem
from ..settings import *


# 区领导
class NewpaperSpider(CrawlSpider):

    name = 'd'

    start_urls = ['http://www.bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qrd/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzf/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzx/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzx/cba5c47e-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qzf/cba5c47e-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zwxx0/ldzc13/qw/cba5c47e-2.html']
    rules = {
        Rule(LinkExtractor(allow='/pgqrmzf/zwxx0/ldzc13/[a-z]+/\d+/index\.html'),
             callback='parse_item')
    }

    def parse_item(self, response):
            """
            通过xpath设置过滤条件，筛选符合的数据爬取
            """
            item = DpingguquItem()
            item['ld_name'] = str(re.compile(r'：.*').findall(response.xpath("//div[@class='easysite-news-title']/h2/text()").extract_first())).replace("：", '').replace("['", '').replace("']", '')
            item['ld_office'] = '平谷区' + response.xpath("//div[@class='easysite-bread-nav']/p/span/a[4]/text()").extract_first()
            item['ld_url'] = response.url
            item['ld_resume'] = ''.join(re.findall(u"[\u4e00-\u9fa5]+|\d{4}年|\d月|\d{2}月|：|。|，|；|、", response.xpath("//div[@id='easysiteText']").xpath('string(.)').extract_first()))
            if re.compile(r'负责.*').findall(item['ld_resume']):
                item['ld_duty'] = re.compile(r'负责.*').findall(item['ld_resume'])[0]
            else:
                item['ld_duty'] = ''
            if re.compile(r'现任.*').findall(response.xpath("//div[@id='easysiteText']/p[1]").extract_first()):
                item['ld_position'] = ''.join(re.compile(r'[\u4e00-\u9fa5]+').findall(re.compile(r'现任.*').findall(response.xpath("//div[@id='easysiteText']/p[1]").extract_first())[0]))
            else:
                item['ld_position'] = str(re.compile(r'[\u4e00-\u9fa5]+：').findall(response.xpath("//div[@class='easysite-news-title']/h2/text()").extract_first())).replace("：", '').replace("['", '').replace("']", '')
            item['province'] = '北京市'
            item['city'] = '平谷区'
            item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['type'] = response.xpath("//div[@class='easysite-bread-nav']/p/span/a[4]/text()").extract_first()
            item['ld_icon'] = response.xpath("//meta[@name='Image']/@content").extract_first()
            yield item
