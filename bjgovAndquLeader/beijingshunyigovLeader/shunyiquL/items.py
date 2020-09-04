# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShunyiqulItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # url链接
    ld_name = scrapy.Field()
    ld_icon = scrapy.Field()
    ld_office = scrapy.Field()
    ld_resume= scrapy.Field()
    ld_duty= scrapy.Field()
    ld_position= scrapy.Field()
    ld_url= scrapy.Field()
    province= scrapy.Field()
    city= scrapy.Field()
    county= scrapy.Field()
    ld_createTime= scrapy.Field()
    type= scrapy.Field()
    modifyTime = scrapy.Field()





    gov_name = scrapy.Field()
    gov_super = scrapy.Field()
    gov_head = scrapy.Field()
    gov_desc = scrapy.Field()
    gov_url = scrapy.Field()
    gov_type = scrapy.Field()
    gov_createTime = scrapy.Field()
    modifyTime = scrapy.Field()


