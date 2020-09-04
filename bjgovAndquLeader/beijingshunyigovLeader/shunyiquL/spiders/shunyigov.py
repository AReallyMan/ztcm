# -*- coding: utf-8 -*-

# @Time : 2020-07-20 10:25:06
# @Author : ZhangYangyang
# @Software: PyCharm
import scrapy
import datetime
import re
from ..items import ShunyiqulItem


# 顺义区机构设置领导信息
class ShunyiSpider(scrapy.Spider):
    name = 'shunyi'

    start_urls = [
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/sjczgldw/sghgtwsyfj/442486/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/sjczgldw/syglfj/442462/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/bxyz44/442006/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/dsgzz46/442126/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/zz31/441982/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/ncz48/441934/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/mlz99/442030/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/lqz89/441910/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/lsz19/442078/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/bwz16/442102/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/lwtz59/442054/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/yz61/441958/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/tzz62/441886/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/hsyz23/441862/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/nfxz99/441838/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qzwfwglbgs/441550/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qzfwsqwbgs/441526/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qmfj/441381/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qyllhj/441356/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qcgzfjcj/441502/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qxfb/441478/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qtjj/441308/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qtyj/441284/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qjrb/441405/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qgzw/441234/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qlyfzw/441186/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsjj/441162/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qwsjsw/441137/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsww/744845/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qswj/441064/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qnwnyj/441040/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qaqjgj/441258/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qjtj/669215/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qcsglw/440992/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qzfcxjsw/440968/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qhbj/440944/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qrlsbj/440920/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qczj/440896/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qsfj/440872/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qmzj/440848/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qjjxxhw/440824/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qkw/440800/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qjw/440773/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qfzggw/440749/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qzfbgs/440725/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qjsydw/qzzyfwzx/442270/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qjsydw/qtzcjj/442342/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qjsydw/qscjyglzx/442294/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qjsydw/qzbqyrczx/442390/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qjsydw/qhwzx/442246/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qjsydw/qylfwzx/442222/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qjsydw/qjgz/442198/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qjsydw/qdzj/442174/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/bscz95/441814/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/glyz93/441790/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/zqyz77/441766/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/nlsz40/441742/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/mpz38/441718/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/rhz51/441694/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/kgjdbsc69/441670/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/sfjdbsc79/441646/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/wqjdbsc20/441622/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/syjdbsc26/745038/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/zzfhjdbsc/sljdbsc72/441574/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/sjczgldw/sygafj/444734/index.html',
        'http://www.bjshy.gov.cn/web/zwgk/jgxx/qzfwbj/qscjgj/662857/index.html'
    ]

    def parse(self, response):
        item = ShunyiqulItem()
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
            if j < len(psd) - 1:
                for k in range(psd[j], psd[j + 1]):
                    #if psNew[k].xpath('./text()').extract():
                    lis.append(psNew[k].xpath('./text()').extract())
                ld_resume = ''
                for i in range(0, len(lis)):
                    ld_resume += str(lis[i])
                item['ld_icon'] = "http://www.bjshy.gov.cn" + ld_icon[0]

                if len(re.compile(r'姓名：[\u4e00-\u9fa5]{2,3}').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'姓名：[\u4e00-\u9fa5]{2,3}').findall(ld_resume)).replace("姓名：",'')
                elif len(re.compile(r'姓名：[\u4e00-\u9fa5]..[\u4e00-\u9fa5]').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'姓名：[\u4e00-\u9fa5]..[\u4e00-\u9fa5]').findall(ld_resume)).replace("姓名：", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}：男，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}：男，').findall(ld_resume)).replace("：男，", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}：女，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}：女，').findall(ld_resume)).replace("：女，", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}男，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}男，').findall(ld_resume)).replace("男，", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}女，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}女，').findall(ld_resume)).replace("女，", '')

                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}.男，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}.男，').findall(ld_resume)).replace("男，", '')
                elif len(re.compile(r'　　[\u4e00-\u9fa5]{2,3}　　').findall(ld_resume)) != 0:
                    ld_name = re.compile(r'　　[\u4e00-\u9fa5]{2,3}　　').findall(ld_resume)
                elif len(re.compile(r'　　[\u4e00-\u9fa5]{2,3}　　').findall(ld_resume)) != 0:
                    ld_name = re.compile(r'　　[\u4e00-\u9fa5]{2,3}　　').findall(ld_resume)
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3} 男，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3} 男，').findall(ld_resume)).replace("男，", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3} 女，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3} 女，').findall(ld_resume)).replace("女，", '')

                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}  男，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}  男，').findall(ld_resume)).replace("男，", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}  女，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}  女，').findall(ld_resume)).replace("女，", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}，女').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}，女').findall(ld_resume)).replace("，女", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}  男').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}  男').findall(ld_resume)).replace("男", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}  女').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}  女').findall(ld_resume)).replace("女", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}　　男').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}　　男').findall(ld_resume)).replace("男", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}　　女').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}　　女').findall(ld_resume)).replace("女", '')

                elif len(re.compile(r'【基本信息】[\u4e00-\u9fa5]{2,3}，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'【基本信息】[\u4e00-\u9fa5]{2,3}，').findall(ld_resume)).replace("【基本信息】", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}　　职务').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}　　职务').findall(ld_resume)).replace("职务", '')
                elif len(re.compile(r'　　　　[\u4e00-\u9fa5]{2,3}，').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'　　　　[\u4e00-\u9fa5]{2,3}，').findall(ld_resume)).replace("，", '')
                elif len(re.compile(r'[\u4e00-\u9fa5]{2,3}，男').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'[\u4e00-\u9fa5]{2,3}，男').findall(ld_resume)).replace("，男", '')
                elif len(re.compile(r'　　[\u4e00-\u9fa5]{2,3}：').findall(ld_resume)) != 0:
                    ld_name = str(re.compile(r'　　[\u4e00-\u9fa5]{2,3}：').findall(ld_resume)).replace("：", '')
                elif len(re.compile(r'　　    [\u4e00-\u9fa5]+').findall(ld_resume)) != 0:
                    name = re.compile(r'　　    [\u4e00-\u9fa5]+').findall(ld_resume)
                    ld_name = re.compile(r'[\u4e00-\u9fa5]+').findall(name[0])  # 姓名
                elif len(re.compile(r'　　　　[\u4e00-\u9fa5]{2,3}').findall(ld_resume)) != 0:
                    ld_name = re.compile(r'　　　　[\u4e00-\u9fa5]{2,3}').findall(ld_resume)
                elif "杜井龙" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "杜井龙"
                elif "赵丽婷" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "赵丽婷"
                elif "张晓梅" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "张晓梅"
                elif "佟海剑" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "佟海剑"
                elif "赵建节" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "赵建节"
                elif "施洪新" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "施洪新"
                elif "闫沛枭" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "闫沛枭"
                elif "许国学" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "许国学"
                elif "贾国增" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "贾国增"
                elif "李书国" in ld_resume and "市规划自然委顺义分局" in ld_office:
                    ld_name = "李书国"


                elif "于长雷" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "于长雷"
                elif "乔龙" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "乔龙"
                elif "李云峰" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "李云峰"
                elif "郑海涛" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "郑海涛"
                elif "张红伟" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "张红伟"
                elif "王国刚" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "王国刚"
                elif "王宇" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "王宇"
                elif "胡彩霞" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "胡彩霞"

                elif "刘松涛" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "刘松涛"
                elif "魏琼" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "魏琼"
                elif "马大刚" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "马大刚"
                elif "杨玉杰" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "杨玉杰"
                elif "王京民" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "王京民"

                elif "赵宇航" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "赵宇航"
                elif "王春雨" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "王春雨"
                elif "左延臣" in ld_resume and "顺义区李桥镇" in ld_office:
                    ld_name = "左延臣"

                else:
                    ld_name = '未取到'
                if len(re.compile(r'现任.*?。').findall(ld_resume)) != 0:
                    ld_position = re.compile(r'现任.*?。').findall(ld_resume)
                elif len(re.compile(r'务：[\u4e00-\u9fa5]+').findall(ld_resume)) != 0:
                    ld_position = str(re.compile(r'务：[\u4e00-\u9fa5]+').findall(ld_resume)).replace("务：", '')
                elif len(re.compile(r'　.*【基本信息】').findall(ld_resume)) != 0:
                    ld_position = str(re.compile(r'　.*【基本信息】').findall(ld_resume)).replace("【基本信息】", '').replace(ld_name[0],
                                                                                               '')[0]
                else:
                    ld_position = ''
                if len(re.compile(r'负责.*').findall(ld_resume)) != 0:
                    ld_duty = re.compile(r'负责.*').findall(ld_resume)
                elif len(re.compile(r'分工.*').findall(ld_resume)) != 0:
                    ld_duty = str(re.compile(r'分工.*').findall(ld_resume)[0]).replace('分工】', '')
                elif len(re.compile(r'主要工作.*?。').findall(ld_resume)) != 0:
                    ld_duty = re.compile(r'主要工作.*?。').findall(ld_resume)
                else:
                    ld_duty = ''
                province = '北京市'
                city = '顺义区'
                ld_name = str(ld_name).replace("['", '').replace("']", '')
                item['ld_name'] = re.compile(r'[\u4e00-\u9fa5]+').findall(ld_name)[0]  # 姓名
                item['ld_office'] = ld_office[0]
                ld_resume = str(ld_resume).replace("['", '').replace("']", '')
                #  u"[\u4e00-\u9fa5]+|\miyun{4}年|\d月|\miyun{2}月|：|。|，
                content = re.findall(u"[\u4e00-\u9fa5]+|\d{4}年|\d月|\d{2}月|：|。|，|、|；", ld_resume)
                item['ld_resume'] = ''.join(content)
                item['ld_duty'] = str(ld_duty).replace("[", '').replace("]", '')
                item['ld_position'] = str(ld_position).replace("['", '').replace("']", '')
                item['ld_url'] = response.url
                item['province'] = province
                item['city'] = city
                item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['type'] = type[0]
                if '镇政府和街道' in item['type']:
                    item['county'] = str(item['ld_office']).replace("顺义区", '')
                else:
                    item['county'] = ''
                lis = []  # 初始化列表，不然会把第二次循环的内容也加上
                yield item
