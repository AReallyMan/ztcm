# -*- coding: utf-8 -*-

# @Time : 2020-07-31 10:26:36
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


# 北京市房山区领导信息
class NewpaperSpider(CrawlSpider):
    """
    1、通过正则匹配机构设置底下所有的url
    2、找到领导简介url
    3、进行数据处理，获取领导信息
    """
    name = 'fsgov'
    start_urls = ['http://www.bjfsh.gov.cn/zfxxgk/2020jgzn/']
    rules = {
        Rule(LinkExtractor(allow='./zfbm/[a-z]+\_\d+/'), callback='getMsg'),
         Rule(LinkExtractor(allow='./xzjd/[a-z]+\_\d+/'), callback='getMsg')
    }

    def getMsg(self, response):
        '''
        获取领导信息
        :param response:
        :return:
        '''
        item = MiyunItem()
        for person in response.xpath("//div[@class='leadinfo']"):
            item['ld_icon'] = re.compile(r'./(.*)').findall(person.xpath("./div/img/@src").extract_first())[0]
            item['ld_name'] = ''.join(re.compile(r'[\u4e00-\u9fa5]+').findall(person.xpath("./div/ul/li/text()").extract_first())).replace('姓名', '')
            item['ld_position'] = ''.join(re.compile(r'[\u4e00-\u9fa5]+').findall(person.xpath("./div/ul/li[2]/text()").extract_first())).replace('职务', '')
            item['ld_resume'] = ''.join(re.compile(r'[\u4e00-\u9fa5]+').findall(person.xpath("./div/ul/li[3]/text()").extract_first() + person.xpath("./div/ul/li[4]/text()").extract_first()))
            item['ld_duty'] = ''.join(re.compile(r'[\u4e00-\u9fa5]+').findall(person.xpath("./div/ul/li[5]/text()").extract_first())).replace("工作分工", '')
            item['ld_office'] = ''.join(re.compile(r'[\u4e00-\u9fa5]+').findall(response.xpath("//div[@class='slideTitle']/text()").extract_first()))
            item['ld_url'] = response.url
            item['province'] = '北京市'
            item['city'] = '房山区'
            item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if '区' not in item['ld_office'] and ('镇' in item['ld_office'] or '乡' in item['ld_office'] or '道' in item['ld_office']):
                item['type'] = '乡镇（街道）'
            elif '燕山办事处' in item['ld_office']:
                item['type'] = '政府派出机构'
            else:
                item['type'] = '政府部门'
            if '乡镇' in item['type']:
                item['county'] = item['ld_office']
            else:
                item['county'] = ''
            yield item




