# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import datetime


class MongoPipeline(object):
  def __init__(self):
    myclient = pymongo.MongoClient("mongodb://192.168.1.51:27017/")
    mydb = myclient["portia"]
    self.mycol = mydb["Beijing_leader"]

  def process_item(self, item, spider):
    if self.mycol.count_documents({'ld_name': item['ld_name']}) != 0 and self.mycol.count_documents(
            {'ld_position': item['ld_position']}) != 0:
      self.mycol.update({'ld_name': item['ld_name']},
                        {"$set": dict(item)}, False,
                        True)
    else:
      self.mycol.insert_one(dict(item))
