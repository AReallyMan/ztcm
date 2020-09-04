# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

import pymongo
from openpyxl import Workbook
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))


class CaigoushunyiPipeline(object):
    def process_item(self, item, spider):
        return item


class ParsePipeline(object):
    # 处理文本中的空字符串
    def process_content(content):
        if content:
            content = [re.sub(r"\xa0|\s", "", i) for i in content]
            # 去除列表中的空字符串
            content = [i for i in content if len(i) > 0]
            return "".join(content)
        else:
            return ""


class MongoPipeline(object):
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://192.168.1.51:27017/")
        mydb = myclient["bid_item"]
        self.mycol = mydb["beijingShunyiSpider"]

    def process_item(self, item, spider):
        if self.mycol.count_documents({'url': item['url']}) != 0:
            self.mycol.update({'url': item['url']},
                              {"$set": dict(item)}, False,
                              True)
        else:
            self.mycol.insert_one(dict(item))
