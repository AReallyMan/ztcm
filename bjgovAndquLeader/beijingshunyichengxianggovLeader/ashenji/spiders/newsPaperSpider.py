# -*- coding: utf-8 -*-

# @Time : 2020-07-20 10:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
from ..items import AshenjiItem

# 顺义区住房和城乡建设委员会
class NewpaperSpider(scrapy.Spider):

        name = 'sj'

        start_urls = [
            'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qzfcxjsw/440968/index.html',
            'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html'
        ]

        def parse(self, response):
            item = AshenjiItem()
            # 获取页面结构
            ps = response.xpath("//div[@id='easysiteText']/div/p").extract()
            # 获取页面导航栏上的单位名称
            if response.xpath('//*[@id="xxly"]/text()'):
                ld_office = response.xpath('//*[@id="xxly"]/text()').extract()
            else:
                ld_office = "单位"
            # 获取页面导航栏上的单位类型
            if response.xpath("//a[@class='SkinObject'][4]/text()"):
                type = response.xpath("//a[@class='SkinObject'][4]/text()").extract()
            else:
                type = '类型'
            # 用头像建立索引下标
            psd = [i for i, p in enumerate(ps) if "img" in p]
            psNew = response.xpath("//div[@id='easysiteText']/div/p")
            lis = []
            '''
            根据img建立索引下标，把两个索引下标的p标签的内容和img封装为第一个人的信息
            把姓名各种字段根据正则进行数据处理
            '''
            for j in range(0, len(psd)):
                if psNew[psd[j]].xpath('./img/@src').extract():
                    ld_icon = psNew[psd[j]].xpath('./img/@src').extract()
                    ld_icon = "http://www.bjshy.gov.cn" + ld_icon[0]
                if j < len(psd) - 1:
                    for k in range(psd[j], psd[j + 1]):
                        lis.append(psNew[k].xpath('./span/text()').extract())
                    ld_resume = ''
                    for i in range(0, len(lis)):
                        ld_resume += str(lis[i])
                    if len(re.compile(r'职务.*出生').findall(ld_resume)) != 0:
                        ld_position = str(re.compile(r'职务.*出生').findall(ld_resume)).replace('出生', '').replace("职务：",'')
                    else:
                        ld_position = ''
                    if len(re.compile(r'分工.*?。').findall(ld_resume)) != 0:
                        ld_duty = re.compile(r'分工.*?。').findall(ld_resume)
                    else:
                        ld_duty = ''
                    if len(re.compile(r'姓名：[\u4e00-\u9fa5]{2,3}').findall(ld_resume)) != 0:
                        ld_name = str(re.compile(r'姓名：[\u4e00-\u9fa5]{2,3}').findall(ld_resume)).replace("姓名：", '')
                    else:
                        ld_name = '未取到'
                    if "王继红" in ld_name:
                        ld_position = "党组成员、四级调研员"
                    if "郑国栋" in ld_name:
                        ld_position = "党组成员、副主任"
                    if "http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qzfcxjsw/440968/2020050816591669327.jpg" in ld_icon:
                        ld_name = "张巍"
                        ld_duty = '负责棚户区改造、拆迁征收管理、轨道交通建设、城市建设重点工程管理。分管征收拆迁管理科、城建项目管理服务中心。'
                        ld_resume = '  曾任顺义区发展改革委固定资产投资科副科长、科长，顺义区浅山建设办副调研员、顺义区发展改革委副调研员，中关村科技园区顺义园管委会产业发展处处长（副处级）、中关村科技园区顺义园管委会正处职。'
                        ld_position = "党组成员、副主任（正处级）"
                    province = '北京市'
                    city = '顺义区'
                    ld_name = str(ld_name).replace("['", '').replace("']", '')
                    item['ld_name'] = re.compile(r'[\u4e00-\u9fa5]+').findall(ld_name)[0]  # 姓名
                    item['ld_office'] = ld_office[0]
                    ld_resume = str(ld_resume).replace("['", '').replace("']", '')
                    content = re.findall(u"[\u4e00-\u9fa5]+|\d{4}年|\d{2}月|\d{1}月", ld_resume)
                    item['ld_resume'] = ''.join(content)
                    item['ld_duty'] = str(ld_duty).replace("[", '').replace("]", '')
                    item['ld_position'] = str(ld_position).replace("[", '').replace("]", '')
                    item['ld_url'] = response.url
                    item['province'] = province
                    item['city'] = city
                    item['ld_icon'] = ld_icon
                    item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    item['type'] = type[0]
                    lis = []  # 初始化列表，不然会把第二次循环的内容也加上
                    yield item
