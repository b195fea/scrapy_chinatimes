# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pymongo
from chinatimes import settings
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
from urllib.parse import urlparse, urlunparse


class MongoDBPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def __init__(self, settings):
        self.client = None
        self.db = None
        self.collection = None
        self.settings = settings
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        """连接到MongoDB数据库"""
        self.logger.info(f'開始連接MongoDB數據庫')
        print('開始連接MongoDB數據庫')
        try:
            # 从settings获取MongoDB配置
            # 获取MongoDB配置
            mongo_uri = self.settings.get('MONGO_URI', 'mongodb://localhost:27017/')
            mongo_user = self.settings.get('MONGO_USER', '')
            self.logger.info(f'使用者賬號：{mongo_user}')
            mongo_password = self.settings.get('MONGO_PASSWORD', '')
            self.logger.info(f'使用者密碼：{mongo_password}')
            mongo_db = self.settings.get('MONGO_DATABASE', 'chinatimes_news')
            mongo_collection = self.settings.get('MONGO_COLLECTION', 'articles')

            # 如果提供了用户名和密码，则构建带认证的连接URI
            if mongo_user and mongo_password:
                # 使用urlparse解析原始MongoDB连接URI，便于后续修改认证信息
                parsed_uri = urlparse(mongo_uri)
                # 重构包含认证信息的URI
                auth_netloc = f"{mongo_user}:{mongo_password}@{parsed_uri.netloc}"
                self.logger.info(f"auth_netloc URI: {auth_netloc}")
                mongo_uri = urlunparse(parsed_uri._replace(netloc=auth_netloc))
                mongo_uri = '''mongodb://insight:insight20250701@127.0.0.1:27017/admin'''
                self.logger.info(f"连接URI: {mongo_uri}")

            # 建立数据库连接
            self.client = pymongo.MongoClient(mongo_uri)
            self.db = self.client[mongo_db]
            self.collection = self.db[mongo_collection]

            # 创建唯一索引，避免重复存储
            self.collection.create_index('url', unique=True)
            self.logger.info(f"成功连接到MongoDB: {mongo_uri}, 数据库: {mongo_db}, 集合: {mongo_collection}")
        except Exception as e:
            self.logger.error(f"MongoDB连接失败: {str(e)}")
            raise

    def close_spider(self, spider):
        """关闭MongoDB连接"""
        if self.client:
            self.client.close()
            self.logger.info("MongoDB连接已关闭")

    def process_item(self, item, spider):
        """存储item到MongoDB"""
        try:
            adapter = ItemAdapter(item)
            item_dict = adapter.asdict()

            # 分离普通字段和数组字段，避免MongoDB更新冲突
            non_keyword_fields = {k: v for k, v in item_dict.items() if k != 'keywords'}
            
            # 使用$set设置普通字段，$addToSet处理keywords数组
            self.collection.update_one(
                {'url': item_dict['url']},  # 查询条件
                {
                    '$set': non_keyword_fields,  # 设置/更新普通字段
                    '$addToSet': {'keywords': {'$each': item_dict['keywords']}}  # 添加关键词（新增/更新都适用）
                },
                upsert=True  # 如果不存在则插入新文档
            )
            self.logger.debug(f"成功存储/更新数据: {item_dict['title']}")
            return item
        except pymongo.errors.DuplicateKeyError:
            self.logger.warning(f"数据已存在，跳过存储: {item['url']}")
            raise DropItem(f"重复数据: {item['url']}")
        except Exception as e:
            self.logger.error(f"存储数据失败: {str(e)}", exc_info=True)
            raise DropItem(f"存储失败: {str(e)}")




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
            # self.db[settings.MONGO_COLLECTION].insert_one(item)
        except Exception as e:
            print(e)

    def close_spider(self, spider):
        try:
            self.db_client.close()
        except Exception as e:
            print(e)