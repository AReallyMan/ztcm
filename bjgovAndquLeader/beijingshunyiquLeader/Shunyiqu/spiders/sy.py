from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem


class Sy(BasePortiaSpider):
    name = "sy"
    allowed_domains = [u'www.bjshy.gov.cn']
    start_urls = [u'http://www.bjshy.gov.cn/web/zwgk/ldjs/index.html']
    rules = [
        Rule(
            LinkExtractor(
                allow=(u'/web/zwgk/ldjs/[a-z]+/\\d+/index\\.html'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [
        [
            Item(
                PortiaItem,
                None,
                u'body',
                [
                    Field(
                        u'ld_duty',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(5) > .levelTwo > .ulB > .none::attr(href)',
                        []),
                    Field(
                        u'ld_position',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(5) > .levelTwo > .ulB > li:nth-child(2) > a::attr(href)',
                        []),
                    Field(
                        u'ld_url',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(5) > .levelTwo > .ulB > li:nth-child(4) > a::attr(href)',
                        []),
                    Field(
                        u'province',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(5) > .levelTwo > .ulB > li:nth-child(5) > a::attr(href)',
                        []),
                    Field(
                        u'city',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(5) > .levelTwo > .ulB > li:nth-child(6) > a::attr(href)',
                        []),
                    Field(
                        u'county',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(6) > .levelTwo > .ulB > .none::attr(href)',
                        []),
                    Field(
                        u'ld_createTime',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(6) > .levelTwo > .ulB > li:nth-child(3) > a::attr(href)',
                        []),
                    Field(
                        u'type',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(6) > .levelTwo > .ulB > li:nth-child(5) > a::attr(href)',
                        []),
                    Field(
                        u'modifyTime',
                        '.newHeadNav > .comwidth > .newtopNav > .clearfix > li:nth-child(6) > .levelTwo > .ulB > li:nth-child(6) > a::attr(href)',
                        []),
                    Field(
                        u'ld_office',
                        '.main > .cont > .content > .portlet > div:nth-child(2) > p > span > a:nth-child(4) *::text',
                        []),
                    Field(
                        u'ld_icon',
                        '.main > .cont > .content > .portlet > div:nth-child(2) > .ldxx_detail > .ldxx_detail_con > .ldxx_photo > img::attr(src)',
                        []),
                    Field(
                        u'ld_name',
                        '.main > .cont > .content > .portlet > div:nth-child(2) > .ldxx_detail > .ldxx_detail_con > .ldxx_introduce > h3 *::text',
                        []),
                    Field(
                        u'ld_resume',
                        '.main > .cont > .content > .portlet > div:nth-child(2) > .ldxx_detail > .ldxx_detail_con > .ldxx_introduce > .ldxx_txt > p:nth-child(1) *::text',
                        [])])]]
