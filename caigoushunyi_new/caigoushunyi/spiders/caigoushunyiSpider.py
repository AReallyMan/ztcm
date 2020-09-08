# -*- coding: utf-8 -*-
# update by zhangyangyang
# update at 2020-08-12
# desc 对招标信息添加正则进行处理
import datetime
import scrapy
from datetime import date
from ..items import CaigoushunyiItem
from ..parsefiles.re_parse import *
from ..parsefiles.content_parse import *
from ..pipelines import *


# 顺义区招标
class CaigoushunyispiderSpider(scrapy.Spider):
    """
    获取顺义区招标网站信息，并对信息进行处理
    """
    name = 'beijingShunyiSpider'
    zh_name = u'北京市顺义区政府采购网-招标公告'
    today = str(date.today())
    # today = '2020-09-02'  # 可能获取测试日期的数据
    allowed_domains = ['caigou.bjshy.gov.cn']
    # 招标公告
    start_urls = ['http://caigou.bjshy.gov.cn/level2.jsp?caid=011-002&topage=1']
    basic_url = 'http://caigou.bjshy.gov.cn/'

    def start_requests(self):
        """
        控制分页，默认从第一页发起请求
        """
        # 到一月份左右
        for i in range(1, 40):
            url = self.start_urls[0][:-1] + str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        判断页面数据的日期，和当前日期比较，相等则为今天数据，发起请求
        :param response: 页面响应的信息
        :return:
        """
        tr_list = response.css(".level2page_table tr:nth-child(1) tr")
        item = CaigoushunyiItem()
        # 遍历信息列表，找出今天的数据进行处理
        for tr in tr_list:
            publish_time = tr.xpath('./td[2]/span[@id="newss"]/text()').extract_first()
            # 发布时间
            item['day'] = publish_time
            #if publish_time == self.today:
            url = tr.xpath('./td[1]/span[@class="level2_word"]/a/@href').extract_first()
            # item['noticeTime'] = publish_time
            title = tr.xpath('./td[1]/span[@class="level2_word"]/a/text()').extract_first() + u"招标公告"
            item['title'] = title[2:]
            # 对符合的url发起请求
            yield scrapy.Request(url=self.basic_url + url, callback=self.detail_parse, meta={"item": item.copy()})

    def detail_parse(self, response):
        """
        获取页面数据信息，处理字段信息
        （说明：页面数据通过两种方式获取。一：先从页面截取到需要到的数据段，再添加正则处理。二：直接在页面通过p段落去正则匹配。）
        """
        item = response.meta['item']
        """
        方式一：整段截取数据后，再进行正则处理
        """
        # 获取到整个页面的数据信息
        all_content = ''.join(response.xpath("//tr[@valign='top']").xpath("string(.)").extract())
        # 开标时间
        parse_opentime = parse_name(parse_name(all_content, re_parse_address__openTime_bidDeadline), re_parse_openTime) if parse_name(all_content, re_parse_address__openTime_bidDeadline) else ''
        # 投标截止时间
        parse_biddeadline = parse_name(parse_name(all_content, re_parse_address__openTime_bidDeadline), re_parse_bidDeadline) if parse_name(all_content,re_parse_address__openTime_bidDeadline) else ''
        # 开标地点
        parse_address = parse_name(parse_name(all_content, re_parse_address__openTime_bidDeadline),re_parses_address) if parse_name(all_content, re_parse_address__openTime_bidDeadline) else ''
        # 公告期限
        parse_noticetime = parse_name(all_content, re_parse_noticeTime) if parse_name(all_content, re_parse_noticeTime) else ''
        # 采购人单位名称
        parse_company = parse_name(parse_name(all_content, re_parse_caigou), re_parse_company) if parse_name(all_content, re_parse_caigou) else ''
        # 采购单位联系人
        parse_purchase_person = parse_name(parse_name(all_content, re_parse_caigou), re_parse__purchase_person) if parse_name(all_content, re_parse_caigou) else ''
        # 采购单位联系方式
        parse__purchase_telephone = parse_name(parse_name(all_content, re_parse_caigou), re_parse__purchase_telephone) if parse_name(all_content, re_parse_caigou) else ''
        # 发售时间
        parse_priceTime = parse_name(parse_name(all_content, re_parse_priceTimeAndbidDocument), re_parse_priceTime) if parse_name(all_content, re_parse_priceTimeAndbidDocument) else ''
        # 发售地点
        parse_bidDocument = parse_name(parse_name(all_content, re_parse_priceTimeAndbidDocument),re_parse_bidDocument) if parse_name(all_content,re_parse_priceTimeAndbidDocument) else ''
        # 代理机构名称
        parse_agency = parse_name(parse_name(all_content, re_parse_daili), re_parse_agency) if parse_name(all_content, re_parse_daili) else ''
        # 代理机构联系人
        parse_agency_person = parse_name(parse_name(all_content, re_parse_daili), re_parse_agency_person) if parse_name(all_content, re_parse_daili) else ''
        # 代理机构联系方式
        parse_agency_telephone = parse_name(parse_name(all_content, re_parse_daili), re_parse_agency_telephone) if parse_name(all_content, re_parse_daili) else ''
        # 预算金额
        parse_budget = parse_name(all_content, re_parse_budget)
        """
        方式二：以p标签的形式直接在页面中通过正则获取字段数据
        """
        p_list = response.xpath('//tr[@valign="top"]//p')
        bid_content = "\n".join([ParsePipeline.process_content(p.xpath('.//text()').extract()) for p in p_list])
        budget = parse_name(bid_content, re_budget)
        project = parse_name(bid_content, re_project)
        company = parse_name(bid_content, re_company)
        noticeTime = parse_name(bid_content, re_noticeTime)
        pricetime = parse_name(bid_content, re_priceTime)
        bidDocument = parse_name(bid_content, re_bidDocument)
        bidDeadline = parse_name(bid_content, re_bidDeadline)
        openTime = parse_name(bid_content, re_openTime)
        address = parse_name(bid_content, re_address)
        agency = parse_name(bid_content, re_agency)
        purchase_demand = parse_name(all_content, re_purchase_demand)
        agency_person = parse_name(bid_content, re_agency_person)
        purchase_telephone = parse_name(bid_content, re_purchase_telephone)
        purchase_person = parse_name(bid_content, re_purchase_person)
        agency_telephone = parse_name(bid_content, re_agency_telephone)

        """
        获取字段数据
        """
        item['url'] = response.url
        item['company'] = company if company else parse_company
        item['purchase_person'] = purchase_person if purchase_person else parse_purchase_person
        item['purchase_telephone'] = purchase_telephone if purchase_telephone else parse__purchase_telephone
        item['agency'] = agency if agency else parse_agency
        item['agency_person'] = agency_person if agency_person else parse_agency_person
        item['agency_telephone'] = agency_telephone if agency_telephone else parse_agency_telephone
        item['inserttime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['project'] = project if project else re.findall(r'(.*)招标公告', item['title'])[0]
        item['bidDocument'] = parse_bidDocument if parse_bidDocument else bidDocument
        item['budget'] = budget if budget else parse_budget
        item['priceTime'] = parse_priceTime if parse_priceTime else pricetime

        item['noticeTime'] = noticeTime if noticeTime else parse_noticetime
        item['bidDeadline'] = bidDeadline if bidDeadline else parse_biddeadline
        item['openTime'] = openTime if openTime else parse_opentime
        item['address'] = address if address else parse_address

        item['type'] = '招标网站'
        item['biddingarea'] = ''  # 招标区域目前没有看到，先赋值为null
        item['purchase_demand'] = purchase_demand
        item['zh_name'] = "北京市顺义区政府采购网招标公告"
        yield item


