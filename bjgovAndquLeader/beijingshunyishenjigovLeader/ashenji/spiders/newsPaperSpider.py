# -*- coding: utf-8 -*-

# @Time : 2020-07-20 10:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
from ..items import AshenjiItem

# 顺义区审计局
class NewpaperSpider(scrapy.Spider):

        name = 'sj'

        start_urls = [
            'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html'
        ]

        def parse(self, response):
            item = AshenjiItem()
            ld_name = ['曾中坚', '绳桂华', '侯健', '王惠芳', '田学光', '肖建民']
            if "曾中坚" in ld_name:
                item['ld_office'] = "区审计局"
                item['ld_resume'] = '曾中坚，男，汉族，中共党员，江西宁都人，1967年3月出生，大学毕业（南京航空学院机械制造专业），高级工程师，1990年12月入党，1988年08月参加工作，现任党组书记、二级巡视员，主持党组全面工作。曾在军队工作，转业后任顺义区商务委党组书记、副区级，顺义区纪委区监委第十四联合派驻纪检监察组组长、副区级、二级巡视员。'
                item['ld_duty'] = '主持党组全面工作'
                item['ld_position'] = '党组书记、二级巡视员'
                item['ld_url'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html'
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['ld_icon'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/2020021817471859392.jpg'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = ' 区政府委办局'
                item['ld_name'] = '曾中坚'
                yield item
            if "绳桂华" in ld_name:
                item['ld_office'] = "区审计局"
                item['ld_resume'] = '绳桂华，女，汉族，群众，北京顺义人，1964年8月出生，研究生学历，审计师。现任副局长。分管综合法规审理科、农业与资源环境审计科。曾任顺义区审计局工交科科员、综合业务科副科长、综合业务科科长。'
                item['ld_duty'] = '分管综合法规审理科、农业与资源环境审计科'
                item['ld_position'] = '副局长'
                item['ld_url'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html'
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['ld_icon'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/2018112113305181544.jpg'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = ' 区政府委办局'
                item['ld_name'] = '绳桂华'
                yield item

            if "侯健" in ld_name:
                item['ld_office'] = "区审计局"
                item['ld_resume'] = "侯健，男，汉族，中共党员，山东淄博人，1975年10月出生，大学学历，会计师。现任党组成员、副局长、机关党支部书记。分管财政审计科、经济责任审计科、企业审计科。曾任北京市公路局顺义分局科员，顺义区审计局科员、行政事业审计科副科长、社会保障审计科副科长、社会保障审计科科长、财政金融审计科科长。"
                item['ld_duty'] = '分管财政审计科、经济责任审计科、企业审计科'
                item['ld_position'] = '党组成员、副局长、机关党支部书记'
                item['ld_url'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html'
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['ld_icon'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/2018112112535385478.jpg'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = ' 区政府委办局'
                item['ld_name'] = '侯健'
                yield item
            if "王惠芳" in ld_name:
                item['ld_office'] = "区审计局"
                item['ld_resume'] = "王惠芳，男，汉族，中共党员，河北栾城人，1960年12月出生，大学学历。现任二级调研员。分管内部审计指导所、工会工作。曾在军队工作，转业后任顺义区审计局副调研员。"
                item['ld_duty'] = '分管内部审计指导所、工会工作'
                item['ld_position'] = '二级调研员'
                item['ld_url'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html'
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['ld_icon'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/2018112112544048048.jpg'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = ' 区政府委办局'
                item['ld_name'] = '王惠芳'
                yield item
            if "田学光" in ld_name:
                item['ld_office'] = "区审计局"
                item[
                    'ld_resume'] = "田学光，男，汉族，中共党员，山东日照人，1969年4月出生，大学学历。现任四级调研员。协助曾中坚同志管理全局党建；分管机关党风廉政建设、人事、财务、安全、妇委会、计生及办公室其他工作。曾在军队工作，转业后任顺义区审计局副调研员。"
                item['ld_duty'] = '协助曾中坚同志管理全局党建；分管机关党风廉政建设、人事、财务、安全、妇委会、计生及办公室其他工作'
                item['ld_position'] = '四级调研员'
                item['ld_url'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html'
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['ld_icon'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/2018112112543587552.jpg'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = ' 区政府委办局'
                item['ld_name'] = '田学光'
                yield item
            if "肖建民" in ld_name:
                item['ld_office'] = "区审计局"
                item['ld_resume'] = '肖建民，男，汉族，中共党员，北京人，1970年9月出生，大学学历。现任四级调研员、机关党支部副书记。分管固定资产投资审计科、教科文卫审计科、机关团支部工作。顺义区杨镇企业公司科员、顺义区杨镇财政统计科副主任科员、财政统计科主任科员、顺义区杨镇人民政府财政科主任科员、财政科科长、经济发展办公室主任、纪委委员。'
                item['ld_duty'] = '分管固定资产投资审计科、教科文卫审计科、机关团支部工作'
                item['ld_position'] = '四级调研员、机关党支部副书记'
                item['ld_url'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html'
                item['province'] = '北京市'
                item['city'] = '顺义区'
                item['ld_icon'] = 'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/2018112113333456396.jpg'
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = ' 区政府委办局'
                item['ld_name'] = '肖建民'
                yield item
