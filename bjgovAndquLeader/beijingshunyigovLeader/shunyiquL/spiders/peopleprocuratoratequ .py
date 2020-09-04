# -*- coding: utf-8 -*-

# @Time : 2020-08-07 10:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
from ..items import ShunyiqulItem


# 顺义区人民检察院领导信息
class ShunyiSpider(scrapy.Spider):
    name = 'people'

    start_urls = [
        'http://www.bjjc.gov.cn/bjoweb/minfo/view.jsp?ADMINVIEW=1&DMKID=278&ZLMBH=0&XXBH=62201'
    ]

    def parse(self, response):
        item = ShunyiqulItem()
        for tx in response.xpath("//p[@class='MsoNormal']"):
            if '族' in ''.join(tx.xpath("string(.)").extract_first()):
                item['ld_resume'] = ''.join(tx.xpath("string(.)").extract_first())
                item['ld_name'] = re.findall(r'(.*)，[男,女]', item['ld_resume'])[0]
                item['ld_office'] = '顺义区人民检察院'
                item['ld_position'] = re.findall(r'北京市顺义区.*', item['ld_resume'])[0]
                item['ld_url'] = response.url
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = '区政府'
                yield item
