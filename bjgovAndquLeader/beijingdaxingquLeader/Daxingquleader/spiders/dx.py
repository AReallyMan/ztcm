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


class Dx(BasePortiaSpider):
    name = "dx"
    allowed_domains = ['www.bjdx.gov.cn']
    start_urls = ['http://www.bjdx.gov.cn/bjsdxqrmzf/zwfw/ldzc/index.html']
    rules = [
        Rule(
            LinkExtractor(
                allow=(
                    '/bjsdxqrmzf/zwfw/ldzc/[a-z]+/index\\.html',
                    '/bjsdxqrmzf/zwfw/ldzc/[a-z]+/\\d+/index\\.html'),
                deny=()),
            callback='parse_item',
            follow=True)]
    items = [
        [
            Item(
                ItemItem,
                None,
                '#con',
                [
                    Field(
                        'modifyTime',
                        '.position > span > a:nth-child(1)::attr(href)',
                        []),
                    Field(
                        'type',
                        '.detail_con > .portlet > div:nth-child(2) > .rels > span > a:nth-child(4) *::text',
                        []),
                    Field(
                        'ld_name',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .subArticleTitle > h2 *::text',
                        []),
                    Field(
                        'ld_url',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .subArticleTitle > .detail > span:nth-child(1) *::text',
                        []),
                    Field(
                        'province',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .subArticleTitle > .detail > span:nth-child(2) *::text',
                        []),
                    Field(
                        'city',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .subArticleTitle > .detail > .fontDx > span:nth-child(1) *::text',
                        []),
                    Field(
                        'county',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .subArticleTitle > .detail > .fontDx > span:nth-child(2) *::text',
                        []),
                    Field(
                        'ld_createTime',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .subArticleTitle > .detail > .fontDx > span:nth-child(3) *::text',
                        []),
                    Field(
                        'ld_resume',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .article *::text',
                        []),
                    Field(
                        'ld_icon',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(1) > img::attr(src)',
                        []),
                    Field(
                        'ld_position',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .article > .right *::text',
                        [
                            Regex('现任.*?。')]),
                    Field(
                        'ld_duty',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .article > .right > p:nth-child(4) *::text',
                        []),
                    Field(
                        'ld_office',
                        '.detail_con > .portlet > div:nth-child(2) > .detailCon > .closeAn > a::attr(href)',
                        [])])]]
