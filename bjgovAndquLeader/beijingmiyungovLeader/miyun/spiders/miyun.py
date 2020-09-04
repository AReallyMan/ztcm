# -*- coding: utf-8 -*-

# @Time : 2020-07-30 13:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import MiyunItem
from ..settings import *


# 北京市密云区机构设置领导信息
class NewpaperSpider(CrawlSpider):
    """
    1、通过正则匹配机构设置底下所有的url
    2、找到领导简介url
    3、进行数据处理，获取领导信息
    """
    name = 'my'
    start_urls = ['http://www.bjmy.gov.cn/col/col31/index.html']
    rules = {
        Rule(LinkExtractor(allow='http://www.bjmy.gov.cn/col/col\d+/index\.html'), callback='getMsg')
    }

    def getMsg(self, response):
        '''
        获取领导信息
        :param response:
        :return:
        '''
        item = MiyunItem()
        if len(response.xpath("//div[@class='bd']/div/table")) != 0:
            for list in response.xpath("//div[@class='bd']/div/table"):
                item['ld_icon'] = 'http://www.bjmy.gov.cn' + list.xpath("./tr/td/p/img/@src").extract_first()
                item['ld_name'] = list.xpath("./tr/th/p/text()").extract_first()
                item['ld_position'] = list.xpath("./tr[2]/td/p/text()").extract_first()
                item['ld_resume'] = list.xpath("./tr[4]/td/p[3]/text()").extract_first() + ''.join(re.findall(u"[\u4e00-\u9fa5]+|：|。|，", list.xpath("./tr[5]/td").xpath('string(.)').extract_first()))
                item['ld_office'] = response.xpath("//tr/td[4]/a/text()").extract_first()
                item['ld_duty'] = list.xpath("./tr[3]/td/div/p/text()").extract_first()
                item['ld_url'] = response.url
                item['province'] = '北京市'
                item['city'] = '密云区'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = response.xpath("//tr/td[3]/a/text()").extract_first()
                if "乡镇" in item['type'] or "街道" in item['type']:
                    item['county'] = item['ld_office']
                else:
                    item['county'] = ''
                yield item




