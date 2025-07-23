# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from chinatimes import settings
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ChinatimesPipeline:
    db_client = ''
    db = ''

    def open_spider(self, spider):
        # db_uri = spider.settings.get('MONGODB_URI', 'mongodb://192.168.3.27:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'chinatimes')
        # self.db_client = MongoClient('mongodb://192.168.3.6:27017')
        self.db_client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = self.db_client[settings.DB_CLIENT]

    def process_item(self, item, spider):
        self.insert(item)
        return item

    def insert(self, item):
        try:
            item = dict(item)
            self.db[settings.BOARD_NAME].insert_one(item)
        except Exception as e:
            print(e)

    def close_spider(self, spider):
        try:
            self.db_client.close()
        except Exception as e:
            print(e)