# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from openpyxl import Workbook
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import redis
from kafka import KafkaProducer
import json
import os
import sys
import datetime
path = [
  "/usr/local/workspace-gerapy/gerapy/projects", "C:/Users/asus/Desktop/spiders", "/app/spiders"
]
[sys.path.append(p)for p in path if os.path.isdir(p)]


class MongoPipeline(object):
  def __init__(self):
    myclient = pymongo.MongoClient("mongodb://192.168.1.51:27017/")
    mydb = myclient["portia"]
    self.mycol = mydb["Beijing_leader"]

  def process_item(self, item, spider):
    if self.mycol.count_documents({'ld_name': item['ld_name']}) != 0 and self.mycol.count_documents(
            {'ld_position': item['ld_position']}) != 0:
      self.mycol.update({'ld_name': item['ld_name']},
                        {"$set": {'modifyTime': datetime.datetime.now().strftime("%Y-%m-%miyun %H:%M:%S")}}, False,
                        True)
    else:
      self.mycol.insert_one(dict(item))
