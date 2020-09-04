# -*- coding: utf-8 -*-

# @Time : 2020-07-31 10:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re
import scrapy
from ..items import MiyunItem
from ..settings import *


# 北京市房山区领导信息
class NewpaperSpider(scrapy.Spider):
    """
    1、通过正则匹配机构设置底下所有的url
    2、找到领导简介url
    3、进行数据处理，获取领导信息
    """
    name = 'fs'
    start_urls = ['http://www.bjfsh.gov.cn/zwgk/ldjs/']

    def parse(self, response):
        '''
        获取领导信息
        :param response:
        :return:
        '''
        item = MiyunItem()
        i = 0  # 用于判断区领导的单外
        for list in response.xpath("//div[@class='bd']/ul[@class='ldjsList']"):
            i += 1
            for person in list.xpath("./li"):
                item['ld_icon'] = 'http://www.bjfsh.gov.cn/zwgk/ldjs/' + re.compile(r'./(.*)').findall(person.xpath("./div/img/@src").extract_first())[0]
                item['ld_name'] = ''.join(re.compile(r'[\u4e00-\u9fa5]+').findall(person.xpath("./div[2]/h2/text()").extract_first()))
                item['ld_position'] = re.compile(r'现任(.*?。)').findall(person.xpath("./div[2]/p[1]/text()").extract_first())[0]
                item['ld_resume'] = ''.join(re.findall(u"[\u4e00-\u9fa5]+|：|。|，", person.xpath("./div[2]").xpath('string(.)').extract_first()))
                if i == 1:
                    item['ld_office'] = '中共房山区委'
                elif i == 2:
                    item['ld_office'] = '房山区人大'
                elif i == 3:
                    item['ld_office'] = '房山区政府'
                elif i == 4:
                    item['ld_office'] = '房山区政协'
                else:
                    item['ld_office'] = ''
                duty = person.xpath("./div[2]/p[1]/text()").extract_first()
                if "负责" in duty:
                    item['ld_duty'] = re.compile(r'负责(.*)').findall(duty)[0]
                elif '组织' in duty:
                    item['ld_duty'] = re.compile(r'组织(.*?。)').findall(duty)[0]
                elif '领导' in duty:
                    item['ld_duty'] = re.compile(r'领导(.*?。)').findall(duty)[0]
                elif '协助' in duty:
                    item['ld_duty'] = re.compile(r'协助(.*?。)').findall(duty)[0]
                elif '主持' in duty:
                    item['ld_duty'] = re.compile(r'主持(.*?。)').findall(duty)[0]
                else:
                    item['ld_duty'] = ''
                item['ld_url'] = response.url
                item['province'] = '北京市'
                item['city'] = '房山区'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if '区委' in item['ld_office']:
                    item['type'] = '区委'
                elif '区人大' in item['ld_office']:
                    item['type'] = '区人大'
                elif '区政府' in item['ld_office']:
                    item['type'] = '区政府'
                elif '区政协' in item['ld_office']:
                    item['type'] = '区政协'
                else:
                    item['type'] = ''
                yield item




