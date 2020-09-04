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


class Bjyq(BasePortiaSpider):
    name = "bjyq"
    allowed_domains = [u'www.bjyq.gov.cn']
    start_urls = [u'http://www.bjyq.gov.cn/yanqing/zwgk/ldzc/qwld/index.shtml']
    rules = [
        Rule(
            LinkExtractor(
                allow=(
                    u'/yanqing/zwgk/ldzc/[a-z]+/index\\.shtml',
                    u'/yanqing/zwgk/ldzc/[a-z]+/\\d+/index\\.shtml'),
                deny=()),
            callback='parse_item',
            follow=True)]
    items = [[Item(PortiaItem,
                   None,
                   u'html',
                   [Field(u'ld_name',
                          'title *::text',
                          []),
                       Field(u'province',
                             '.topFunction > li:nth-child(1) > a::attr(href)',
                             []),
                       Field(u'city',
                             '.topFunction > li:nth-child(2) > a::attr(href)',
                             []),
                       Field(u'ld_nation',
                             '.main *::text',
                             [Regex(u'.\u65cf')]),
                       Field(u'ld_gender',
                             '#\\35 d4f01d3baca4ffeae0a69e858fbd334 > div:nth-child(2) *::text',
                             [Regex(u'[\u7537,\u5973]')]),
                       Field(u'type',
                             '.SkinObject:nth-child(4) *::text',
                             []),
                       Field(u'ld_resume',
                             '#mainText > div *::text',
                             []),
                       Field(u'ld_partyDate',
                             '#mainText > div *::text',
                             [Regex(u'\\d+\u5e74\\d\u6708.\u515a')]),
                       Field(u'ld_icon',
                             '#mainText > div > p:nth-child(1) > img::attr(src)',
                             []),
                       Field(u'ld_workDate',
                             'p:nth-child(2) *::text',
                             [Regex(u'\\d+\u5e74\\d\u6708.\u52a0')]),
                       Field(u'ld_position',
                             'p:nth-child(2) *::text',
                             [Regex(u'\u73b0\u4efb.*')]),
                       Field(u'ld_birth',
                             'p:nth-child(2) > span > span:nth-child(3) *::text',
                             []),
                       Field(u'ld_native',
                             'p:nth-child(2) > span > span:nth-child(4) *::text',
                             [Regex(u'.*\u4eba')]),
                       Field(u'ld_politics',
                             '.newFootCon:nth-child(2) > li:nth-child(1) > a::attr(href)',
                             []),
                       Field(u'ld_createTime',
                             '.newFootCon:nth-child(2) > li:nth-child(2) > a::attr(href)',
                             []),
                       Field(u'ld_url',
                             '.newFootCon:nth-child(2) > li:nth-child(4) > a::attr(href)',
                             []),
                       Field(u'ld_office',
                             '.newFootConTwo > li:nth-child(1) *::text',
                             []),
                       Field(u'ld_duty',
                             '.newFootConTwo > li:nth-child(2) *::text',
                             [])])]]
