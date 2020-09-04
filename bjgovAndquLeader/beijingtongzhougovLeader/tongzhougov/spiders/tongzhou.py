# -*- coding: utf-8 -*-

# @Time : 2020-07-30 13:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
import time
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import TongzhougovItem
from ..settings import *


# 北京市通州区机构设置领导信息
class NewpaperSpider(CrawlSpider):
    """
    1、通过正则匹配机构设置底下所有的url
    2、找到领导简介url
    3、进行数据处理，获取领导信息
    """
    name = 'tz'
    start_urls = ['http://www.bjtzh.gov.cn/bjtz/xxfb/jgzn/index.shtml']
    rules = {
        Rule(LinkExtractor(allow='/bjtz/xxfb/[a-z]+/[a-z]+\.shtml'), callback='parse_item'),
    }

    def parse_item(self, response):
        '''
        获取到领导简介的连接
        :param response:
        :return:
        '''
        url =response.url
        leader_url = url.replace(url[-10:], 'ldjs.shtml')
        yield scrapy.Request(url=leader_url, callback=self.getMsg)

    def getMsg(self, response):
        '''
        获取领导信息
        :param response:
        :return:
        '''
        item = TongzhougovItem()
        for list in response.xpath("//div[@class='tab-content zzzz']"):
            item['ld_icon'] = 'http://www.bjtzh.gov.cn' + list.xpath("./div[1]/img/@src").extract_first()
            item['ld_name'] = re.compile(r"^[\u4e00-\u9fa5]+").findall(list.xpath("./div[2]/p[@class='zz']/text()").extract_first())[0]
            item['ld_position'] = str(list.xpath("./div[2]/p[@class='zz']/text()").extract_first()).replace(item['ld_name'], '')
            item['ld_resume'] = ''.join(re.findall(u"[\u4e00-\u9fa5]+|\d{4}年|\d月|\d{2}月|：|。|，", list.xpath("./div[2]").xpath('string(.)').extract_first()))
            if ''.join(re.findall(u"机构职能>.*>", response.xpath("//div[@class='BreadcrumbNav']/p").xpath('string(.)').extract_first())):
                item['ld_office'] = str(''.join(re.findall(u"机构职能>.*>",response.xpath("//div[@class='BreadcrumbNav']/p").xpath('string(.)').extract_first()))).replace("机构职能",'').replace(">",'')
            elif response.xpath("//div[@class='BreadcrumbNav']/p/a[4]/text()"):
                item['ld_office'] = response.xpath("//div[@class='BreadcrumbNav']/p/a[4]/text()").extract_first()
            else:
                item['ld_office'] = '未查到'
            if re.compile(r'分工.*?。').findall(item['ld_resume']):
                item['ld_duty'] = re.compile(r'分工.*?。').findall(item['ld_resume'])[0]
            else:
                item['ld_duty'] = ''
            item['ld_url'] = response.url
            item['province'] = '北京市'
            item['city'] = '通州区'
            item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if '镇' in item['ld_office'] or '道' in item['ld_office']:
                item['type'] = '乡镇街道'
            else:
                item['type'] = '区政府'
            yield item




