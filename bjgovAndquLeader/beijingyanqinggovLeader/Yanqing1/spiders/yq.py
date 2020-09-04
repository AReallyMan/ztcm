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
# @Time : 2020-07-09 14:26:36
# @Author : ZhangYangyang
# @Software: PyCharm


# 北京市延庆区领导信息
class Yq(BasePortiaSpider):
    name = "yq"
    allowed_domains = [u'www.bjyq.gov.cn']
    '''
    1、正则无法区分领导和机构以及其他导航栏
    2、通过爬虫爬取网站所有领导导航栏地址，添加到start_urls
    '''
    start_urls = [
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972711/1972713/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972870/1972872/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972937/1972939/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972928/1972930/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972918/1972920/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972831/1972833/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972809/1972811/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972819/1972821/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972908/1972910/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972786/1972788/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972850/1972852/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972841/1972843/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbmy/2576204/2576206/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbmy/2668717/2668719/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbmy/2668717/2668719/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbmy/2537155/2537157/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972860/1972862/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/cgzfjcj/ldbz3585/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/dzj/ldbz43/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbmy/2705806/2705808/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/gdzx/ldbz9/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/xwdx/ldbz75/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/zzzx/ldbz25/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/mlscyy/ldbz7899/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/daj/ldbz54/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/bdltqbsc/ldbz826592/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972881/1972883/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/sczx/ldbz57/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/cl/ldbz8265/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/txw/ldbz14/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/jgswglfw/ldbz59/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/gsl/ldbz55/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/kx/ldbz68/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/lgbj/ldbz2/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/zgh/ldbz91/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/qxj/ldbz8148/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/2530359/2530361/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/1983143/1983145/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/xfb/ldbz84/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/jw53/ldbz49/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/xzbmfwdt/ldbz8243/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/mfj87/ldbz8467/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/szsrw66/ldbz5825/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/2524663/2524665/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/fl88/ldbz8870/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/zfhcxjsw/ldbz71/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/jjhxxhw/ldbz26/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/jtj/ldbz86/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/hbj78/ldbz88/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/swj65/ldbz90/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/nw90/ldbz64/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/lyw/ldbz8/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/1718459/1718463/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/sww/ldbz27/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/czj91/ldbz78/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/sfj/ldbz79/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/fgw/ldbz7221/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/kw/ldbz58/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/ajj13/ldbz16/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/2007669/2007671/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/2003188/2003190/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/yllhj/ldbz10/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/sjj/ldbz56/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/mzj90/ldbz96/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972726/1972728/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/zfb80/ldbz95/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972743/1972745/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/xzjd62/1972773/1972775/index.shtml',
        u'http://www.bjyq.gov.cn/yanqing/zbm/tyj/ldbz72/index.shtml',

    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=(u'/yanqing/[a-z0-9]+/[a-z0-9]+/[a-z0-9]+/\\d+/index\\.shtml'),
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
                             '.ulA:nth-child(1) > .levelTwo > .ulB > li:nth-child(3) > a::attr(href)',
                             []),
                       Field(u'city',
                             '.ulA:nth-child(1) > .levelTwo > .ulB > li:nth-child(5) > a::attr(href)',
                             []),
                       Field(u'county',
                             '.ulA:nth-child(1) > .levelTwo > .ulB > li:nth-child(7) > a::attr(href)',
                             []),
                       Field(u'ld_birth',
                             '.ulA:nth-child(2) > .levelTwo > .ulB > .none::attr(href)',
                             []),
                       Field(u'ld_createTime',
                             '.ulA:nth-child(2) > .levelTwo > .ulB > li:nth-child(5) > a::attr(href)',
                             []),
                       Field(u'ld_workDate',
                             '.ulA:nth-child(3) > .levelTwo > .ulB > li:nth-child(10) > a::attr(href)',
                             []),
                       Field(u'ld_partyDate',
                             '.ulA:nth-child(4) > .levelTwo > .ulB > li:nth-child(5) > a::attr(href)',
                             []),
                       Field(u'ld_native',
                             '.ulA:nth-child(5) > .levelTwo > .ulB > li:nth-child(4) > a::attr(href)',
                             []),
                       Field(u'ld_nation',
                             '#\\35 d4f01d3baca4ffeae0a69e858fbd334 > div:nth-child(2) *::text',
                             [Regex(u'.\u65cf')]),
                       Field(u'ld_office',
                             '.SkinObject:nth-child(3) *::text',
                             []),
                       Field(u'type',
                             '.SkinObject:nth-child(4) *::text',
                             []),
                       Field(u'ld_resume',
                             '#mainText > div *::text',
                             []),
                       Field(u'ld_gender',
                             '#mainText > div *::text',
                             [Regex(u'[\u7537,\u5973]')]),
                       Field(u'ld_icon',
                             '#mainText > div > p:nth-child(1) > img::attr(src)',
                             []),
                       Field(u'ld_position',
                             'p:nth-child(2) *::text',
                             [Regex(u'\u73b0\u4efb.*')]),
                       Field(u'ld_duty',
                             'p:nth-child(4) > span > span > span > span > span > span *::text',
                             []),
                       Field(u'ld_politics',
                             '.newFootCon:nth-child(2) > li:nth-child(1) > a::attr(href)',
                             []),
                       Field(u'ld_url',
                             '.newFootConTwo > li:nth-child(2) *::text',
                             [])])]]
