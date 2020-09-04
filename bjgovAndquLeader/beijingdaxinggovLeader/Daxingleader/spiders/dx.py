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


class Dx(BasePortiaSpider):
    name = "dx"
    allowed_domains = [u'www.bjdx.gov.cn']
    start_urls = [u'http://www.bjdx.gov.cn/bjsdxqrmzf/zwfw/jgzq/index.html']
    rules = [
        Rule(
            LinkExtractor(
                allow=(
                    u'/bjsdxqrmzf/zwfw/jgzq/[a-z]+/[a-z0-9]+/index\\.html',
                    u'/bjsdxqrmzf/zwfw/jgzq/[a-z]+/[a-z]+/ldjj\\d+/index\\.html',
                    u'/bjsdxqrmzf/zwfw/jgzq/[a-z]+/[a-z]+/ldjj/index\\.html',
                    u'/bjsdxqrmzf/zwfw/jgzq/[a-z]+/[a-z]+/ldjj\\d+/\\d+/index\\.html'),
                deny=()),
            callback='parse_item',
            follow=True)]
    items = [
        [
            Item(
                PortiaItem,
                None,
                u'body',
                [
                    Field(
                        u'city',
                        '.header > .gg_nav > .pubCon > li:nth-child(2) > .ejNav > .pubCon > .textLeft > a:nth-child(1)::attr(href)',
                        []),
                    Field(
                        u'county',
                        '.header > .gg_nav > .pubCon > li:nth-child(2) > .ejNav > .pubCon > .textLeft > a:nth-child(2)::attr(href)',
                        []),
                    Field(
                        u'ld_politics',
                        '.header > .gg_nav > .pubCon > li:nth-child(4) > .ejNav > .pubCon > .textCenter > a:nth-child(3)::attr(href)',
                        []),
                    Field(
                        u'ld_workDate',
                        '.header > .gg_nav > .pubCon > li:nth-child(6) > .ejNav > .pubCon > div > a:nth-child(1)::attr(href)',
                        []),
                    Field(
                        u'ld_partyDate',
                        '.header > .gg_nav > .pubCon > li:nth-child(7) > a::attr(href)',
                        []),
                    Field(
                        u'ld_createTime',
                        '.header > .gg_nav > .pubCon > li:nth-child(7) > .ejNav > .pubCon > div > a:nth-child(7)::attr(href)',
                        []),
                    Field(
                        u'type',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .rels > span > a:nth-child(4) *::text',
                        []),
                    Field(
                        u'ld_office',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .rels > span > a:nth-child(5) *::text',
                        []),
                    Field(
                        u'province',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article *::text',
                        []),
                    Field(
                        u'ld_icon',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(1) > img::attr(src)',
                        []),
                    Field(
                        u'ld_name',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(2) *::text',
                        []),
                    Field(
                        u'ld_position',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(3) *::text',
                        []),
                    Field(
                        u'ld_birth',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(4) *::text',
                        []),
                    Field(
                        u'ld_gender',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(5) *::text',
                        []),
                    Field(
                        u'ld_nation',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(6) *::text',
                        []),
                    Field(
                        u'ld_native',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(7) *::text',
                        []),
                    Field(
                        u'modifyTime',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(7) *::text',
                        []),
                    Field(
                        u'edu_background',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(8) *::text',
                        []),
                    Field(
                        u'ld_resume',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(10) *::text',
                        []),
                    Field(
                        u'ld_duty',
                        '.pubCon > .con > .detail_con > .portlet > div:nth-child(2) > .detailCon > .article > p:nth-child(11) *::text',
                        [])])]]
