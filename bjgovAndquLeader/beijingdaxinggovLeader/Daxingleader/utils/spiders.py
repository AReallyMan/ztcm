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
            if items:
                for item in items:
                    if len(item) != 6:
                        item['city'] = "大兴区"
                        item['county'] = ''
                        if len(re.compile(r'出生年月.\d+.\d+').findall(item['province'])) != 0:
                            item['ld_birth'] = str(re.compile(r'出生年月.\d+.\d+').findall(item['province'])[0]).replace("出生年月：", "")
                        if len(re.compile(r'工作分工.*').findall(item['province'])) != 0:
                            item['ld_duty'] = re.compile(r'工作分工.*').findall(item['province'])[0]
                        item['ld_gender'] = re.compile(r'[男,女]').findall(item['province'])[0]
                        if len(re.compile(r'学历背景：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['edu_background'] = str(re.compile(r'学历背景：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("学历背景：", "")
                        else:
                            item['edu_background'] = ''
                        if len(re.compile(r'姓名：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_name'] = str(re.compile(r'姓名：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("姓名：", "")
                        elif len(re.compile(r'^ [\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_name'] = re.compile(r'^ [\u4e00-\u9fa5]+').findall(item['province'])[0]
                        elif len(re.compile(r'^[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_name'] = re.compile(r'^[\u4e00-\u9fa5]+').findall(item['province'])[0]
                        if len(re.compile(r'民族：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_nation'] = str(re.compile(r'民族：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("民族：", "")
                        elif len(re.compile(r'民 族：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_nation'] = str(
                                re.compile(r'民 族：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("民 族：", "")
                        elif len(re.compile(r'民\u3000\u3000族：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_nation'] = str(
                                re.compile(r'民\u3000\u3000族：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("民\u3000\u3000族：", "")
                        if len(re.compile(r'籍贯：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_native'] = str(re.compile(r'籍贯：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("籍贯：", '')
                        elif len(re.compile(r'籍 贯：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_native'] = str(
                                re.compile(r'籍 贯：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("籍 贯：", '')
                        elif len(re.compile(r'籍\u3000\u3000贯：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_native'] = str(
                                re.compile(r'籍\u3000\u3000贯：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("籍\u3000\u3000贯：", '')
                        item['ld_partyDate'] = ''
                        item['ld_politics'] = ''
                        if len(re.compile(r'职务：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_position'] = str(re.compile(r'职务：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("职务：",'')
                        elif len(re.compile(r'职 务：[\u4e00-\u9fa5]+').findall(item['province'])) != 0:
                            item['ld_position'] = str(
                                re.compile(r'职 务：[\u4e00-\u9fa5]+').findall(item['province'])[0]).replace("职 务：", '')
                        item['ld_resume'] = item['province']
                        item['ld_workDate'] = ''
                        item['province'] = "北京市"
                        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # 机关后勤的不同统一，这边特殊处理一下
                        if item['ld_icon'] == "http://www.bjdx.gov.cn/images/content/2018-09/20180906162457532399.jpg":
                            item['ld_name'] = "郝望"
                            item['ld_position'] = "党组书记、主任"
                        if item['ld_icon'] == "http://www.bjdx.gov.cn/images/content/2018-09/20180906162719803447.jpg":
                            item['ld_name'] = "李洪来"
                            item['ld_position'] = "党组副书记"
                        if item['ld_icon'] == "http://www.bjdx.gov.cn/images/content/2018-09/20180906163023610550.jpg":
                            item['ld_name'] = "张晓军"
                            item['ld_position'] = "党组成员、副主任"
                        if item['ld_icon'] == "http://www.bjdx.gov.cn/images/content/2018-10/20181015142622700479.jpg":
                            item['ld_name'] = "卫问童"
                            item['ld_position'] = "副主任"
                        if item['ld_icon'] == "http://www.bjdx.gov.cn/images/content/2018-09/20180906173534505841.jpg":
                            item['ld_name'] = "马宁"
                            item['ld_position'] = "党组成员、副主任"
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
