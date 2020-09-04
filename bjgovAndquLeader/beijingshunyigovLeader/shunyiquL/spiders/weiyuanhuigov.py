# -*- coding: utf-8 -*-

# @Time : 2020-08-07 17:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
from ..items import ShunyiqulItem

# 还未存库
# 顺义区委员会机构设置信息（单位部门）
class ShunyiSpider(scrapy.Spider):
    name = 'wyhgov'

    start_urls = [
        'http://zhengxie.bjshy.gov.cn/content/zhengxiejigou.aspx'
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
        # 格式化页面数据
        content = ''.join(re.findall(r'[\u4e00-\u9fa5]+|一|二|三|四|五|六|七|八|、|\d|.|；', response.xpath("//div[@class='col-news-content']").xpath("string(.)").extract_first()))
        # 获取到所有科室名称，放在List集合中
        for name in response.xpath("//strong"):
            if name.xpath("./text()"):
                gov_name = name.xpath("./text()").extract_first()
                list.append(gov_name)
        # 获取到网页中最后几个字，通过正则匹配出最后一个科室的描述
        list.append(content[-12:-7])
        for k in range(0, len(list)):
            if k < len(list) - 1:
                t1 = list[k]
                t2 = list[k+1]
                item['gov_desc'] = re.findall(r''+t1+'(.*)'+t2+'', content)[0]
                item['gov_name'] = list[k]
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['type'] = '区委'
                item['gov_super'] = '顺义区委员会'
                item['gov_head'] = '主任'
                item['gov_url'] = response.url
                item['gov_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item
