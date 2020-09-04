# @Time : 2020-07-09 14:26:36
# @Author : ZhangYangyang
# @Software: PyCharm
import datetime
import re
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.utils.response import get_base_url
from .starturls import FeedGenerator, FragmentGenerator


class RequiredFieldMissing(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class PortiaItemLoader(ItemLoader):
    def get_value(self, value, *processors, **kw):
        required = kw.pop('required', False)
        val = super(PortiaItemLoader, self).get_value(value, *processors, **kw)
        if required and not val:
            raise RequiredFieldMissing(
                'Missing required field "{value}" for "{item}"'.format(
                    value=value, item=self.item.__class__.__name__))
        return val


class BasePortiaSpider(CrawlSpider):
    items = []

    def start_requests(self):
        for url in self.start_urls:
            if isinstance(url, dict):
                type_ = url['type']
                if type_ == 'generated':
                    for generated_url in FragmentGenerator()(url):
                        yield self.make_requests_from_url(generated_url)
                elif type_ == 'feed':
                    yield FeedGenerator(self.parse)(url)
            else:
                yield self.make_requests_from_url(url)

    def parse_item(self, response):
        for sample in self.items:
            items = []
            try:
                for definition in sample:
                    items.extend(
                        [i for i in self.load_item(definition, response)]
                    )
            except RequiredFieldMissing as exc:
                self.logger.warning(str(exc))
            """
            1、爬取北京市延庆区网站机构设置中的领导信息
            2、通过一定的规则对数据进行处理                    
            """
            if items:
                for item in items:

                    if item['type'] not in ['动态信息', '基本信息']:  # 正则无法区分的导航栏这里进行筛选去除
                        item['city'] = "延庆区"
                        item['county'] = ""
                        if len(re.compile(r'\d+.*\d+.*出生').findall(item['ld_resume'])) != 0:
                            item['ld_birth'] = str(re.compile(r'\d+.*\d+.*出生').findall(item['ld_resume'])[0]).replace(
                                "出生", "")
                        else:
                            item['ld_birth'] = ''
                        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        item['ld_native'] = ''
                        item['ld_partyDate'] = ''
                        item['ld_url'] = ''
                        if len(re.compile(r'\d+年\d+...工作').findall(item['ld_resume'])) == 0 and len(
                                re.compile(r'\d+ 年 \d+ ...工作').findall(item['ld_resume'])) == 0:
                            item['ld_workDate'] = ''
                        elif len(re.compile(r'\d+年\d+...工作').findall(item['ld_resume'])) != 0:
                            item['ld_workDate'] = str(re.compile(r'\d+年\d+...工作').findall(item['ld_resume'])[0])
                        elif len(re.compile(r'\d+ 年 \d+ ...工作').findall(item['ld_resume'])) != 0:
                            item['ld_workDate'] = str(re.compile(r'\d+ 年 \d+ ...工作').findall(item['ld_resume'])[0])
                        item['province'] = "北京市"
                        # item['ld_native'] = re.compile(r'[\u4e00-\u9fa5]+人').findall(item['ld_resume'])[0]
                        # if len(re.compile(r'现任.*曾任').findall(item['ld_resume'])) != 0:
                        #     item['ld_position'] = str(re.compile(r'现任.*曾任').findall(item['ld_resume'])[0]).replace("曾任",
                        #                                                                                            "")
                        if len(re.compile(r'现任.*?。').findall(item['ld_resume'])) != 0:
                            item['ld_position'] = re.compile(r'现任.*?。').findall(item['ld_resume'])[0]
                        if len(re.compile(r'职责.*').findall(item['ld_resume'])) != 0:
                            item['ld_duty'] = str(re.compile(r'职责.*').findall(item['ld_resume'])[0]).replace("职责分工", "")
                        if "籍贯" in item['ld_resume'] and len(
                                re.compile(r'籍贯[\u4e00-\u9fa5]+').findall(item['ld_resume'])) != 0:
                            item['ld_native'] = re.compile(r'籍贯[\u4e00-\u9fa5]+').findall(item['ld_resume'])[0]
                        elif "人" in item['ld_resume'] and re.compile(r'[\u4e00-\u9fa5]+人').findall(item['ld_resume']):
                            item['ld_native'] = re.compile(r'[\u4e00-\u9fa5]+人').findall(item['ld_resume'])[0]
                        else:
                            item['ld_native'] = ''
                        if "党员" in item['ld_resume']:
                            item['ld_politics'] = "党员"
                        elif "预备党" in item['ld_resume']:
                            item['ld_politics'] = "中共预备党员"
                        elif "团员" in item['ld_resume']:
                            item['ld_politics'] = "共青团员"
                        elif "民革" in item['ld_resume']:
                            item['ld_politics'] = " 民革党员"
                        elif "民盟" in item['ld_resume']:
                            item['ld_politics'] = "民盟盟员"
                        elif "民建" in item['ld_resume']:
                            item['ld_politics'] = "民建会员"
                        elif "民进" in item['ld_resume']:
                            item['ld_politics'] = "民进会员"
                        elif "农工" in item['ld_resume']:
                            item['ld_politics'] = "农工党党员"
                        elif "致公" in item['ld_resume']:
                            item['ld_politics'] = "致公党党员"
                        elif "九三学社" in item['ld_resume']:
                            item['ld_politics'] = "九三学社社员"
                        elif "台盟" in item['ld_resume']:
                            item['ld_politics'] = "台盟盟员"
                        elif "共产党" in item['ld_resume']:
                            item['ld_politics'] = "党员"
                        else:
                            item['ld_politics'] = ''
                        if "加入" in item['ld_resume'] and len(re.compile(r'\d+年\d+..入').findall(item['ld_resume'])) != 0:
                            item['ld_partyDate'] = str(re.compile(r'\d+年\d+..入').findall(item['ld_resume'])[0])
                        elif "入" in item['ld_resume'] and len(re.compile(r'\d+年\d+.入').findall(item['ld_resume'])) != 0:
                            item['ld_partyDate'] = str(re.compile(r'\d+年\d+.入').findall(item['ld_resume'])[0])
                        else:
                            item['ld_partyDate'] = ''
                        yield item
                break

    def load_item(self, definition, response):
        selectors = response.css(definition.selector)
        for selector in selectors:
            selector = selector if selector else None
            ld = PortiaItemLoader(
                item=definition.item(),
                selector=selector,
                response=response,
                baseurl=get_base_url(response)
            )
            for field in definition.fields:
                if hasattr(field, 'fields'):
                    if field.name is not None:
                        ld.add_value(field.name,
                                     self.load_item(field, selector))
                else:
                    ld.add_css(field.name, field.selector, *field.processors,
                               required=field.required)
            yield ld.load_item()
