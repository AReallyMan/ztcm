# -*- coding: utf-8 -*-

# @Time : 2020-08-05 14:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import MiyunItem
from ..settings import *


# 北京市怀柔区领导信息
class NewpaperSpider(CrawlSpider):
    """
    1、通过正则匹配机构设置底下所有的url
    2、找到领导简介url
    3、进行数据处理，获取领导信息
    """
    name = 'hr'
    start_urls = ['http://www.bjhr.gov.cn/zwgk/qldjs/qwld/201911/t20191107_484494.html']
    rules = {
        Rule(LinkExtractor(allow='/[a-z]+/\d+/t\d+\_\d+\.html', unique=False), callback='getMsg')
    }

    def getMsg(self, response):
        '''
        获取领导信息
        :param response:
        :return:
        '''
        item = MiyunItem()
        item['ld_icon'] = str(response.url).split("/t")[0] + "/" + str(response.xpath("//div[@class='ldjj']/p/img/@src").extract_first()).replace('./', '')
        item['ld_name'] = response.xpath("//div[@class='ldjj']/p[2]/text()").extract_first()
        item['ld_position'] = response.xpath("//div[@class='ldjj']/p[3]/text()").extract_first()
        if response.xpath("//div[@class='ldjj']/div"):
            item['ld_resume'] = ''.join(re.findall(u"[\u4e00-\u9fa5]+|：|。|，|、", response.xpath("//div[@class='ldjj']/div").xpath('string(.)').extract_first()))
        item['ld_duty'] = re.findall(r'分工(.*)', item['ld_resume'])[0]
        item['ld_url'] = response.url
        item['province'] = '北京市'
        item['city'] = '怀柔区'
        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['type'] = str(response.xpath("//div[@class='crumbs']/a[4]/text()").extract_first()).replace('领导', '')
        item['ld_office'] = item['city'] + item['type']
        yield item




