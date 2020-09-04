# -*- coding: utf-8 -*-

# @Time : 2020-08-06 13:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re

import scrapy as scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import MiyunItem
from ..settings import *


# 北京市海淀区机构设置领导信息
class NewpaperSpider(CrawlSpider):
    """
    1.遍历页面领导信息
    2.数据处理
    """
    name = 'hdgov'
    start_urls = ['http://www.bjhd.gov.cn/zfxxgk/qzfxxgk/']

    rules = {
        Rule(LinkExtractor(allow='/auto\d+\_\d+/'), callback='getList'),
        Rule(LinkExtractor(allow='/auto\d+/'), callback='getList'),
        Rule(LinkExtractor(allow='/jrb_51811/'), callback='getList'),
    }

    def getList(self, response):
        '''
        获取机构列表页链接
        :param response:
        :return:
        '''
        if re.findall(r'<a href=".(.*)" target="DataList"><i></i>领导介绍', response.text):
            listurl = re.findall(r'<a href=".(.*)" target="DataList"><i></i>领导介绍', response.text)[0]
            yield scrapy.Request(url=response.url + listurl, callback=self.getLeaderUrl)

    def getLeaderUrl(self, response):
        '''
        获取页面领导链接
        :param response:
        :return:
        '''
        for leaderUrl in re.findall(r'<a href=".(.*)" target="_blank">.*</a>', response.text):
            if "+" not in leaderUrl:
                yield scrapy.Request(url=str(response.url).split("index")[0] + leaderUrl, callback=self.getMsg)

    def getMsg(self, response):
        '''
        获取领导信息
        获取到的ld_resume格式比较多，正则有些ld_position、ld_duty没有匹配出来，
        后期可以直接在下边代码中，加入匹配的正则即可优化数据
        :param response:
        :return:
        '''
        item = MiyunItem()
        item['ld_icon'] = str(response.url).split("/t")[0] + '/' + response.xpath("//img/@oldsrc").extract_first()
        content = ''.join(re.findall(r'[\u4e00-\u9fa5]+|。|：|、|，|\d{4}年|\d{2}月', response.text))
        # 处理页面数据，可直接在相应的位置增加正则
        for tx in ['宋体', '仿宋', '微软雅黑']:
            if tx in content:
                content = content.replace(tx, '')
        item['ld_resume'] = re.findall(r'信息有效性：(.*)附件下载', content)[0]
        if re.findall(r'年版(.*)个人基本信息|个人简介：(.*)，[男,女]|个人简历(.*)[男,女]|个人简介(.*)[男,女]|基本情况：(.*)，[男,女]|基本信息：(.*)，[男,女]|姓名.([\u4e00-\u9fa5]{2,3})职务|姓名.([\u4e00-\u9fa5]{2,3})|([\u4e00-\u9fa5]{2,3})，[男,女]', item['ld_resume']):
            for name in re.findall(r'年版(.*)个人基本信息|个人简介：(.*)，[男,女]|个人简历(.*)[男,女]|个人简介(.*)[男,女]|基本情况：(.*)，[男,女]|基本信息：(.*)，[男,女]|姓名：([\u4e00-\u9fa5]{2,3})职务|姓名.([\u4e00-\u9fa5]{2,3})|([\u4e00-\u9fa5]{2,3})，[男,女]', item['ld_resume'])[0]:
                if len(name) != 0:
                    item['ld_name'] = name
                    break
        else:
            item['ld_name'] = ''
        if re.findall(r'现任(.*?。)|职务.(.*)个人基本信息|职务(.*)工作分工|现为(.*?。)|职务：(.*?。)', item['ld_resume']):
            for ld_position in re.findall(r'现任(.*?。)|职务.(.*)个人基本信息|职务(.*)工作分工|现为(.*?。)|职务：(.*?。)', item['ld_resume'])[0]:
                if len(ld_position) != 0:
                    item['ld_position'] = ld_position
                    break
        else:
            item['ld_position'] = ''
        if re.findall(r'负责.*|分工.(.*?。)', item['ld_resume']):
            for ld_duty in re.findall(r'负责.*|分工.(.*?。)', item['ld_resume']):
                if len(ld_duty) != 0:
                    item['ld_duty'] = ld_duty
                    break
        else:
            item['ld_duty'] = ''
        item['ld_office'] = response.xpath("//div[@class='location']/text()[3]").extract_first()
        item['ld_url'] = response.url
        item['province'] = '北京市'
        item['city'] = '海淀区'
        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['type'] = ''
        yield item
