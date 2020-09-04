# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CaigoushunyiItem(scrapy.Item):
    title = scrapy.Field()
    publish_time = scrapy.Field()
    budget = scrapy.Field()
    project = scrapy.Field()
    type = scrapy.Field()
    company = scrapy.Field()
    noticeTime = scrapy.Field()
    priceTime = scrapy.Field()
    openTime = scrapy.Field()
    address = scrapy.Field()
    url = scrapy.Field()
    day = scrapy.Field()
    zh_name = scrapy.Field()

    bidDocument = scrapy.Field()
    bidDeadline = scrapy.Field()
    detail = scrapy.Field()

    publish = scrapy.Field()
    type = scrapy.Field()
    biddingarea = scrapy.Field()
    purchase_person = scrapy.Field()
    purchase_telephone = scrapy.Field()
    agency = scrapy.Field()
    agency_person = scrapy.Field()
    agency_telephone = scrapy.Field()
    purchase_demand = scrapy.Field()
    inserttime = scrapy.Field()