# -*- coding: utf-8 -*-

# @Time : 2020-07-31 16:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re
import scrapy
from ..items import MiyunItem
from ..settings import *
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


# 北京市门头沟区领导信息
class NewpaperSpider(CrawlSpider):
    """
    1、通过Rule正则匹配区领导所有的url
    2、找到领导简介url
    3、进行数据处理，获取领导信息
    """
    name = 'mtg'
    start_urls = ['http://www.bjmtg.gov.cn/bjmtg/zwxx/qld/qld/index.shtml']
    rules = {
        Rule(LinkExtractor(allow='/bjmtg/zwxx/qld/\d+/\d+\.shtml'), callback='getMsg'),
    }

    def getMsg(self, response):
        item = MiyunItem()
        item['ld_url'] = response.url
        if response.xpath("//div[@class='main-right fr']/div/img/@src"):
            item['ld_icon'] = item['ld_url'][:46] + response.xpath("//div[@class='main-right fr']/div/img/@src").extract_first()
        elif response.xpath("//div[@class='main-right fr']/p/img"):
            item['ld_icon'] = item['ld_url'][:46] + response.xpath("//div[@class='main-right fr']/p/img").extract_first()
        elif response.xpath("//div[@class='main-right fr']/div/div/img/@src"):
            item['ld_icon'] = item['ld_url'][:46] + response.xpath("//div[@class='main-right fr']/div/div/img/@src").extract_first()
        else:
            item['ld_icon'] = ''
        item['ld_name'] = response.xpath("//meta[@name='ArticleTitle']/@content").extract_first()
        ld_resume = ''.join(re.compile(r'[\u4e00-\u9fa5]+|\d{4}年|\d月|\d{2}月|：|。|，').findall(response.xpath("//div[@class='main-right fr']").extract_first()))
        if '我的简历' in ld_resume and "宋体" in ld_resume:
            item['ld_resume'] = ld_resume.replace("我的简历", '').replace('宋体', '')
        elif '我的简历' in ld_resume:
            item['ld_resume'] = ld_resume.replace("我的简历", '')
        elif '微软雅黑' in ld_resume:
            item['ld_resume'] = ld_resume.replace("微软雅黑", '')
        else:
            item['ld_resume'] = ld_resume
        if re.compile(u'现任(.*?。)').findall(item['ld_resume']):
            item['ld_position'] = re.compile(u'现任(.*?。)').findall(item['ld_resume'])[0]
        elif re.compile(u'职务(.*?。)').findall(item['ld_resume']):
            item['ld_position'] = re.compile(u'职务(.*?。)').findall(item['ld_resume'])[0]
        else:
            item['ld_position'] = ''
        item['city'] = '门头沟区'
        item['ld_office'] = item['city'] + str(response.xpath("//div[@class='BreadcrumbNav']/p/a[4]/span/text()").extract_first()).replace("领导", '')
        if re.compile(u'分工(.*)').findall(item['ld_resume']):
            if "：" in re.compile(u'分工(.*)').findall(item['ld_resume'])[0]:
                item['ld_duty'] = re.compile(u'分工：(.*)').findall(item['ld_resume'])[0]
            else:
                item['ld_duty'] = re.compile(u'分工(.*)').findall(item['ld_resume'])[0]
        else:
            item['ld_duty'] = ''
        item['province'] = '北京市'
        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['type'] = str(response.xpath("//div[@class='BreadcrumbNav']/p/a[4]/span/text()").extract_first()).replace("领导", '')
        yield item




