import datetime

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
                        item['province'] = "北京市"
                        item['city'] = "延庆区"
                        item['ld_office'] = "北京市延庆区" + str(item['type']).replace("领导", "")
                        # item['ld_partyDate'] = str(item['ld_partyDate']).replace("人，", "")
                        item['type'] = str(item['type']).replace("领导", "")
                        item['ld_createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        item['ld_duty'] = ''
                        item['ld_politics'] = '党员'
                        if item['ld_name'] == "杨雪平":
                            item['ld_politics'] = '民进党'
                        if item['ld_name'] == "程大庆":
                            item['ld_politics'] = '农工党'
                        if item['ld_name'] == "谷艳兰":
                            item['ld_politics'] = '无党派'
                        if item['ld_name'] == "吴辰英":
                            item['ld_politics'] = '九三学社'
                        if item['ld_name'] == "罗瀛":
                            item['ld_politics'] = '民革党'
                        item['ld_url'] = ''
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
