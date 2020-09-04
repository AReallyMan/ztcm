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
    loader = PortiaItemLoader
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


                    item['ld_position'] = str(re.compile(r'职 务.*基本信息').findall(item['ld_resume'])[0]).replace("基本信息", "").replace("职 务：", "")
                    item['ld_name'] = str(item['ld_name']).replace("姓 名：", "").replace(" ","")
                    item['ld_icon'] = ''
                    if len(re.compile(r'分工.*').findall(item['ld_resume'])) != 0:
                        item['ld_duty'] = str(re.compile(r'分工.*').findall(item['ld_resume'])[0]).replace("分工：", "").replace("职 务：", "")
                    else:
                        item['ld_duty'] = ''
                    item['ld_url'] = ''
                    item['province'] = '北京市'
                    item['city'] = '密云区'
                    item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if '区委' in item['ld_position']:
                        item['type'] = '区委'
                    elif "区政府" in item['ld_position']:
                        item['type'] = '区政府'
                    elif "区人大" in item['ld_position']:
                        item['type'] = '区人大'
                    elif "区政协" in item['ld_position']:
                        item['type'] = '区政协'
                    if '区委' in item['ld_position'] and '区政府' in item['ld_position']:
                        item['type'] = '区委和区政府'
                    item['modifyTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if item['ld_name'] in ['潘临珠', '龚宗元', '朱柏成', '杨　珊', '蒋学甫', '王永浩', '刘永强', '王维民', '朱锡才']:
                        item['ld_office'] = '中共北京市密云区委员会'
                    if item['ld_name'] in ['王玉江', '孔令昌', '李光辉', '赵秦岭', '李洪山', '何继玲（不驻会）']:
                        item['ld_office'] = '北京市密云区人民代表大会常务委员会'
                    if item['ld_name'] in ['龚宗元', '杨 珊', '朱锡才', '刘　滨', '张明智']:
                        item['ld_office'] = '北京市密云区人民政府'
                    if item['ld_name'] in ['李长春', '孙　奇', '何丽娟', '相远方', '王森林（不驻会）', '杨伟兰（不驻会）']:
                        item['ld_office'] = '中国人民政治协商会议北京市密云区委员会'
                    yield item
                break

    def load_item(self, definition, response=None, selector=None):
        selector = response if selector is None else selector
        query = selector.xpath if definition.type == 'xpath' else selector.css
        selectors = query(definition.selector)
        for selector in selectors:
            selector = selector if selector else None
            ld = self.loader(
                item=definition.item(),
                selector=selector,
                response=response,
                baseurl=get_base_url(response)
            )
            for field in definition.fields:
                if hasattr(field, 'fields'):
                    if field.name is not None:
                        ld.add_value(field.name,
                                     self.load_item(field, response, selector))
                elif field.type == 'xpath':
                    ld.add_xpath(field.name, field.selector, *field.processors,
                                 required=field.required)
                else:
                    ld.add_css(field.name, field.selector, *field.processors,
                               required=field.required)
            yield ld.load_item()
