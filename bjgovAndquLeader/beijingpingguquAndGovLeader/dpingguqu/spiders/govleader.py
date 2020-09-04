# -*- coding: utf-8 -*-

# @Time : 2020-07-27 11:25:55
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
import time
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import DpingguquItem
from ..settings import *


# 北京市平谷区机构设置领导信息
class NewpaperSpider(CrawlSpider):
    name = 'd3'
    start_urls = ['http://www.bjpg.gov.cn/pgqrmzf/bm/tjj60/tjxx46/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/scjdglj/jgzn83/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/512291/512299/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/qybj/jgzn2021/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/512258/512266/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/pgz/jgzn1298/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/qxfb/jgzn9990/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/qtyjrj/jgzn84/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/qzfb/jgzn87/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/sjj/jgzn26/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/tyj/jgzn1277/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/nyj24/jgzn75/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/436381/jgzn4/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/csgw/jgzn29/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/sww/jgzn1220/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/swj0/jgzn3627/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/pgqxgjdbsc/jgzn224/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/pgqbhjdbsc/jgzn61/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dhsz/jgzn9710/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/hsyx/jgzn92/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ykz/jgzn1223/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/zlyz/jgzn37/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/xezx/jgzn10/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/jhhz/jgzn85/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ljdz/jgzn46/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dxzz/jgzn20/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dgcz/jgzn13/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/sdzz/jgzn76/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ndlhz/jgzn73/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/mcyz/jgzn22/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/mfz/jgzn99/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/xgzz/jgzn91/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/wxzz/jgzn97/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/gzw/jgzn8/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/429753/jgzn2837/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/zjw/jgzn25/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/mfgyy/jgzn28/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/jxw/jgzn60/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/xggw/jgzn5086/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/yllhj/jgzn93/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/whg/jgzn82/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/wjw/jgzn89/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/sfj/jgzn50/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/tjj60/jgzn33/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/rlsbj/jgzn5/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/rfb/jgzn74/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/jw6/jgzn7/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/hbj98/jgzn43/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/mfwljd/jgzn3/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/jtj/jgzn3650/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/cg/jgzn12/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/fgw20/jgzn47/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/zhfwzx/jgzn58/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/czj/jgzn64/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/ajj48/jgzn95/index.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/pgz/jgzn1298/66c8f726-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/pgz/jgzn1298/66c8f726-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/scjdglj/jgzn83/9b5b3667-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/scjdglj/jgzn83/9b5b3667-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/qzfb/jgzn87/e429af6d-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/qzfb/jgzn87/e429af6d-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/nyj24/jgzn75/d11cedc9-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/nyj24/jgzn75/d11cedc9-3.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/pgqxgjdbsc/jgzn224/e2114ce0-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/pgqxgjdbsc/jgzn224/e2114ce0-3.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/pgqxgjdbsc/jgzn224/e2114ce0-4.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/hsyx/jgzn92/92ca1c5d-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/xezx/jgzn10/266c91b4-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/xezx/jgzn10/266c91b4-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/hsyx/jgzn92/92ca1c5d-3.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/jhhz/jgzn85/c016a74a-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dhsz/jgzn9710/a4f01676-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ykz/jgzn1223/29c1e69d-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/zlyz/jgzn37/10c24d58-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/jhhz/jgzn85/c016a74a-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dhsz/jgzn9710/a4f01676-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ykz/jgzn1223/29c1e69d-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/zlyz/jgzn37/10c24d58-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ndlhz/jgzn73/ae5e2d01-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dxzz/jgzn20/e6c34340-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dxzz/jgzn20/e6c34340-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ljdz/jgzn46/4a89a74a-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/mcyz/jgzn22/064b4904-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/mfz/jgzn99/e12d0bbe-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dgcz/jgzn13/22051eab-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ndlhz/jgzn73/ae5e2d01-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/ljdz/jgzn46/4a89a74a-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/mcyz/jgzn22/064b4904-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/mfz/jgzn99/e12d0bbe-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/dgcz/jgzn13/22051eab-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/xgzz/jgzn91/b13916a0-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/xgzz/jgzn91/b13916a0-3.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/436381/jgzn4/6a438f00-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/wxzz/jgzn97/4541c2a6-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/436381/jgzn4/6a438f00-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/zfxxgk68/xzjd20/wxzz/jgzn97/4541c2a6-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/sfj/jgzn50/ca9af9ec-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/sfj/jgzn50/ca9af9ec-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/xggw/jgzn5086/ebdecf06-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/xggw/jgzn5086/ebdecf06-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/tjj60/jgzn33/592d0d62-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/rlsbj/jgzn5/0fa4ba07-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/tjj60/jgzn33/592d0d62-2.html',
                  'http://www.bjpg.gov.cn/pgqrmzf/bm/rlsbj/jgzn5/0fa4ba07-3.html',

                  ]
    rules = {
        Rule(LinkExtractor(allow='ldxx\d+/\d+/index\.html'),
             callback='parse_item'),
    }

    def parse_item(self, response):
        '''
        通过xpathList列表存储页面所有情况img的xpath
        :param response:
        :return: 领导信息
        '''
        item = DpingguquItem()
        xpathList = ["//div[@class='detailContent']/p/img/@src", "//div[@class='detailContent']/div/div/p/img/@src",
                     "//span/img/@src", "//div[@class='detailContent']/div/p/img/@src", "//div[@class='detailContent']/div/img/@src",
                     "//div[@class='detailContent']/div/div/div/p/img/@src"]
        for xpath in xpathList:
            if response.xpath(xpath):
                # 调用getMsg（）方法返回三个值，ld_name领导姓名, ld_position职位, ld_icon头像
                item['ld_name'] = self.getMsg(xpath, response)[0]
                item['ld_position'] = self.getMsg(xpath, response)[1]
                item['ld_icon'] = self.getMsg(xpath, response)[2]
                item['ld_office'] = str(response.xpath("//p[@class='detaiSource']/span[3]/text()").extract_first()).replace("作者：", '')
                item['ld_resume'] = ''.join(re.findall(u"[\u4e00-\u9fa5]+|\d{4}年|\d月|\d{2}月|：|。|，|；|、", response.xpath("//div[@class='detailContent']").xpath('string(.)').extract_first()))
                if re.compile(r'分工.*').findall(item['ld_resume']):
                    item['ld_duty'] = str(re.compile(r'分工.*').findall(item['ld_resume'])).replace('分工：', '').replace("['", '').replace("']", '')
                else:
                    item['ld_duty'] = ''
                if '区' not in item['ld_office'] and ('镇' in item['ld_office'] or '乡' in item['ld_office'] or '街道' in item['ld_office']):
                    item['type'] = '乡镇街道'
                else:
                    item['type'] = '区委'
                item['ld_url'] = response.url
                item['province'] = '北京市'
                item['city'] = '平谷区'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "乡镇" in item['type']:
                    item['county'] = item['ld_office']
                else:
                    item['county'] = ''
                yield item

    def getMsg(self, xpath, response):
        '''
        把处理信息的模块封装为一个方法
        :param xpath: 针对不同页面需要处理的xpath
        :param response:
        :return: ld_name领导姓名, ld_position职位, ld_icon头像
        '''
        title = "//div[@class='detailBoxWrap']/h3/text()"
        ld_icon = 'http://www.bjpg.gov.cn' + response.xpath(xpath).extract_first()
        if re.compile(r'[\u4e00-\u9fa5]+').findall(ld_icon) and '图' not in \
                re.compile(r'[\u4e00-\u9fa5]+').findall(ld_icon)[0]:
            ld_name = re.compile(r'[\u4e00-\u9fa5]+').findall(ld_icon)[0]
            ld_position = str(response.xpath(title).extract_first()).replace(ld_name, '')
        else:
            '''
                有些领导可以通过icon获取到领导姓名，其他获取不到的只能通过拆分职位和姓名
                下面列出了平谷区出现的职位和姓名，进行拆分
            '''
            if '：' in response.xpath(title).extract_first():
                ld_name = str(
                    re.compile(r'：[\u4e00-\u9fa5]+').findall(response.xpath(title).extract_first())[0]).replace("：", '')
                ld_position = str(re.compile(r'.*：').findall(response.xpath(title).extract_first())[0]).replace("：", '')
            elif '主任' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'主任.*').findall(response.xpath(title).extract_first())[0]).replace("主任", '')
                ld_position = re.compile(r'.*主任').findall(response.xpath(title).extract_first())[0]
            elif '调研员' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'调研员.*').findall(response.xpath(title).extract_first())[0]).replace("调研员", '')
                ld_position = re.compile(r'.*调研员').findall(response.xpath(title).extract_first())[0]
            elif '局长' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'局长.*').findall(response.xpath(title).extract_first())[0]).replace("局长", '')
                ld_position = re.compile(r'.*局长').findall(response.xpath(title).extract_first())[0]
            elif '镇长' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'镇长.*').findall(response.xpath(title).extract_first())[0]).replace("镇长", '')
                ld_position = re.compile(r'.*镇长').findall(response.xpath(title).extract_first())[0]
            elif '书记' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'书记.*').findall(response.xpath(title).extract_first())[0]).replace("书记", '')
                ld_position = re.compile(r'.*书记').findall(response.xpath(title).extract_first())[0]
            elif '部长' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'部长.*').findall(response.xpath(title).extract_first())[0]).replace("部长", '')
                ld_position = re.compile(r'.*部长').findall(response.xpath(title).extract_first())[0]
            elif '党组成员' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'党组成员.*').findall(response.xpath(title).extract_first())[0]).replace("党组成员", '')
                ld_position = re.compile(r'.*党组成员').findall(response.xpath(title).extract_first())[0]
            elif '织委员' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'织委员.*').findall(response.xpath(title).extract_first())[0]).replace("织委员", '')
                ld_position = re.compile(r'.*织委员').findall(response.xpath(title).extract_first())[0]
            elif '主席' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'主席.*').findall(response.xpath(title).extract_first())[0]).replace("主席", '')
                ld_position = re.compile(r'.*主席').findall(response.xpath(title).extract_first())[0]
            elif '队长' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'队长.*').findall(response.xpath(title).extract_first())[0]).replace("队长", '')
                ld_position = re.compile(r'.*队长').findall(response.xpath(title).extract_first())[0]
            elif '处级待遇' in response.xpath(title).extract_first():
                ld_name = str(re.compile(r'处级待遇.*').findall(response.xpath(title).extract_first())[0]).replace("处级待遇", '')
                ld_position = re.compile(r'.*处级待遇').findall(response.xpath(title).extract_first())[0]
            else:
                ld_name = response.xpath(title).extract_first()
                ld_position = response.xpath(title).extract_first()
        return ld_name, ld_position, ld_icon

