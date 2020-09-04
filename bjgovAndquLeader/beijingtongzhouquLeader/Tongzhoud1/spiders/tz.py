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


class Tz(BasePortiaSpider):
    name = "tz"
    allowed_domains = [u'www.bjtzh.gov.cn']
    start_urls = [u'http://www.bjtzh.gov.cn/bjtz/xxfb/zhaolei/index.shtml']
    rules = [
        Rule(
            LinkExtractor(
                allow=(u'/bjtz/xxfb/[a-z]+/index\\.shtml'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [[Item(PortiaItem,
                   None,
                   u'html',
                   [Field(u'ld_name',
                          'title *::text',
                          []),
                       Field(u'ld_url',
                             '#cniil_wza::attr(href)',
                             []),
                       Field(u'ld_createTime',
                             '.u_beijing_guide:nth-child(5) > span > a::attr(href)',
                             []),
                       Field(u'province',
                             '.m_nav > li:nth-child(1) > a::attr(href)',
                             []),
                       Field(u'city',
                             '.m_nav > li:nth-child(3) > a::attr(href)',
                             []),
                       Field(u'county',
                             '.m_nav > li:nth-child(4) > a::attr(href)',
                             []),
                       Field(u'modifyTime',
                             '.m_nav > li:nth-child(5) > a::attr(href)',
                             []),
                       Field(u'ld_office',
                             '.BreadcrumbNav > p > a:nth-child(2)::attr(href)',
                             []),
                       Field(u'ld_icon',
                             '.zp > img::attr(src)',
                             []),
                       Field(u'ld_resume',
                             '.jl *::text',
                             []),
                       Field(u'ld_position',
                             '.p6 *::text',
                             [Regex(u'\uff1a.*')]),
                       Field(u'ld_duty',
                             '.jl > p:nth-child(3) *::text',
                             [])])]]
