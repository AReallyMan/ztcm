# -*- coding: utf-8 -*-

# @Time : 2020-08-05 13:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import MiyunItem
from ..settings import *
import scrapy


# 北京市怀柔区机构设置领导信息
class NewpaperSpider(scrapy.Spider):
    """
    1、通过正则匹配机构设置底下所有的url
    2、找到领导简介url
    3、进行数据处理，获取领导信息
    """
    name = 'hrgov'
    start_urls = ['http://www.bjhr.gov.cn/zwgk/jgzn/xzjd/',
                  'http://www.bjhr.gov.cn/zwgk/jgzn/wbj/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.getPage)

    def getPage(self, response):
        pages = re.findall(r'var countPage = (\d)', response.text)[0]
        for page in range(0, int(pages)):
            if page == 0:
                yield scrapy.Request(url=str(response.url) + "/index.html", callback=self.getList)
            else:
                yield scrapy.Request(url=str(response.url) + "/index_" + str(page) + ".html", callback=self.getList)

    def getList(self, response):
        for listurl in response.xpath("//div[@class='hr_ls_li']/ul/li/a/@href").extract():
            yield scrapy.Request(url=listurl, callback=self.getLeader)

    def getLeader(self, response):
        leaderurl = response.url + re.findall(r'/([a-z]+)jgzn/', response.url)[0] + "ldjs"
        yield scrapy.Request(url=leaderurl, callback=self.getMsg)

    def getMsg(self, response):
        item = MiyunItem()
        for path in response.xpath("//div[@class='leadinfo']"):
            if path.xpath("./div[@class='lead_content']/div/p[1]/text()"):
                item['ld_icon'] = response.url + str(path.xpath("./div/img/@src").extract_first()).replace('./', '')
                item['ld_name'] = re.findall(r'[\u4e00-\u9fa5]+', str(path.xpath("./div[@class='lead_content']/div/p[1]/text()").extract_first()).replace("姓名" ,''))[0]
                item['ld_position'] = path.xpath("./div[@class='lead_content']/div/p[2]/text()").extract_first()
                item['ld_duty'] = path.xpath("./div[@class='lead_content']/div/p[3]/text()").extract_first()
                item['ld_url'] = response.url
                item['ld_resume'] = path.xpath("./div[@class='lead_content']/div/p[5]/text()").extract_first()
                item['province'] = '北京市'
                item['city'] = '怀柔区'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = response.xpath("//div[@class='hr_ls_b']/span/a[4]/@title").extract_first()
                item['ld_office'] = response.xpath("//div[@class='hr_ls_b']/span/a[5]/@title").extract_first()
                if '镇乡' in item['type']:
                    item['county'] = item['ld_office']
                else:
                    item['county'] = ''
                yield item




