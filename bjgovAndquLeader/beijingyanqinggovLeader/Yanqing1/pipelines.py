# -*- coding: utf-8 -*-

import pymongo
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class Yanqing1Pipeline(object):
    def process_item(self, item, spider):
        return item
class MongoPipeline(object):
	def __init__(self):
		myclient = pymongo.MongoClient("mongodb://192.168.1.51:27017/")
		mydb = myclient["portia"]
		self.mycol = mydb["gggg"]
	def process_item(self, item, spider):
		self.mycol.insert_one(dict(item))

