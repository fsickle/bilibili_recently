# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class TextPipeLine():
    '''
    对 Item 进行处理
    '''
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['describe']:
            if len(item['describe']) > self.limit:
                item['describe'] = item['describe'][0:self.limit].rstrip()+'...'
        return item



class MongoPipeLine(object):
    '''
    存储 Item 进入 mongodb
    '''
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()