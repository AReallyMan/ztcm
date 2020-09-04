from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import ItemItem, PortiaItem


class Bjmy(BasePortiaSpider):
    name = "bjmy"
    allowed_domains = ['www.bjmy.gov.cn']
    start_urls = ['http://www.bjmy.gov.cn/col/col30/index.html']
    rules = [
        Rule(
            LinkExtractor(
                allow=('/art/2020/\\d/|d+/art_\\d+\\_\\d+\\.html'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [
        [
            Item(
                ItemItem,
                None,
                '.wapper',
                [
                    Field(
                        'ld_icon',
                        'div:nth-child(1) > .lm_mbx > span *::text',
                        []),
                    Field(
                        'ld_office',
                        'div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(1) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(1) > .bt_link::attr(href)',
                        []),
                    Field(
                        'ld_position',
                        'div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(2) > table > tr > td:nth-child(1) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(2) > table > tr > td:nth-child(1) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > .bt_link::attr(href)',
                        []),
                    Field(
                        'type',
                        'div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(2) > table > tr > td:nth-child(2) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(2) > table > tr > td:nth-child(2) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > .bt_link::attr(href)',
                        []),
                    Field(
                        'ld_url',
                        'div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(2) > table > tr > td:nth-child(3) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(2) > table > tr > td:nth-child(3) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(3) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(3) > .bt_link::attr(href)',
                        []),
                    Field(
                        'province',
                        'div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(2) > table > tr > td:nth-child(4) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(2) > table > tr > td:nth-child(4) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(4) > .bt_link::attr(href), div:nth-child(1) > .lm_mbx > .lm_w5r > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(4) > .bt_link::attr(href)',
                        []),

                    Field(
                        'ld_createTime',
                        '.wz_sakb > .wz_sakl > li:nth-child(2) *::text',
                        []),
                    Field(
                        'ld_resume',
                        '.wz_sakb > .wz_article *::text',
                        []),
                    Field(
                        'modifyTime',
                        '.wz_sakb > .wz_article *::text',
                        []),
                    Field(
                        'ld_name',
                        '.wz_sakb > .wz_article > p:nth-child(2) *::text',
                        []),
                    Field(
                        'city',
                        '.wz_sakb > .wz_article > p:nth-child(4) *::text',
                        [
                            Regex('[男,女]')])])]]
