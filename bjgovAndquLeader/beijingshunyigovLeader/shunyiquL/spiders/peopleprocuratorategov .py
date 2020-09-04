# -*- coding: utf-8 -*-

# @Time : 2020-08-07 15:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
from ..items import ShunyiqulItem


# 顺义区人民检察院机构设置信息（单位部门）
class ShunyiSpider(scrapy.Spider):
    name = 'peoplegov'

    start_urls = [
        'http://www.bjjc.gov.cn/bjoweb/minfo/view.jsp?ADMINVIEW=1&DMKID=46&ZLMBH=1&XXBH=56595'
    ]

    def parse(self, response):
        '''
        页面机构信息都是在一个p标签下，单位名称和简介的xpath不同，通过单位名称建立索引
        这里建立索引无法取到最后一个单位的信息，所有分了两种情况进行爬取
        :param response:
        :return:
        '''
        item = ShunyiqulItem()
        list = []
        # titleIndex单位名称的索引集合
        titleIndex = [i for i in range(0, len(response.xpath("//p[@class='a0']"))) if response.xpath('//p[@class="a0"][' + str(i) + ']/span/strong/font/text()')]
        # 在集合中加入最后一个p标签的索引，防止因为数组越界而丢失最后一条信息
        titleIndex.append(len(response.xpath("//p[@class='a0']")))
        for i in range(0, len(titleIndex)):
            # 单位的所有信息，并且防止数组越界
            if i < len(titleIndex) - 1:
                for k in range(titleIndex[i], titleIndex[i+1]):
                    if response.xpath('//p[@class="a0"]['+str(k)+']/span/text()'):
                        list.append(response.xpath('//p[@class="a0"]['+str(k)+']/span/text()').extract_first())
                item['gov_desc'] = '\n'.join(list)
                item['gov_name'] = response.xpath('//p[@class="a0"][' + str(titleIndex[i]) + ']/span/strong/font/text()').extract_first()
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['type'] = '行政单位'
                item['gov_super'] = '顺义区人民检察院'
                item['gov_head'] = '主任'
                item['gov_url'] = response.url
                item['gov_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                list = []
                yield item


