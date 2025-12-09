# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
import logging
from urllib.parse import urlparse, urlunparse
from .mongodb_utils import MongoDBUtils


class MongoDBPipeline:

    def __init__(self):
        self.mongo_utils = MongoDBUtils()
        self.logger = logging.getLogger(__name__)

    def close_spider(self, spider):
        """关闭MongoDB连接"""
        self.mongo_utils.close_connection()
        pass

    def process_item(self, item, spider):
        """存储item到MongoDB"""
        try:
            return self.mongo_utils.update_item(item, 'keywords')
        except Exception as e:
            self.logger.error(f"存储数据失败: {str(e)}", exc_info=True)
            raise DropItem(f"存储失败: {str(e)}")
