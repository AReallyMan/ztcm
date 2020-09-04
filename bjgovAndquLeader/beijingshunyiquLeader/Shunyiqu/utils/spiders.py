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
                    item['city'] = "顺义区"
                    item['province'] = '北京市'
                    item['county'] = ''
                    item['ld_createTime'] = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")
                    item['ld_duty'] = ''
                    #if len(re.compile(r"现任.*").findall(item['ld_resume'])) != 0:
                    item['ld_position'] = str(re.compile(r"现任.*").findall(item['ld_resume'])[0]).replace("现任", "")
                    if len(re.compile(r"^[\u4e00-\u9fa5]+").findall(item['ld_resume'])) != 0:
                        item['ld_name'] = re.compile(r"^[\u4e00-\u9fa5]+").findall(item['ld_resume'])[0]
                    item['ld_url'] = ''
                    item['modifyTime'] = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")
                    if "区委" in item['ld_office']:
                        item['type'] = "区委"
                    if "代表大会" in item['ld_office']:
                        item['type'] = "区人大"
                    if "人民政府" in item['ld_office']:
                        item['type'] = "区政府"
                    if "政治协商" in item['ld_office']:
                        item['type'] = "区政协"
                    item['ld_icon'] = "http://www.bjshy.gov.cn" + item['ld_icon']

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
