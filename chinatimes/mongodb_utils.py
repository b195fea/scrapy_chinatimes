# mongodb_utils.py
import pymongo
from urllib.parse import quote_plus
from scrapy.utils.project import get_project_settings
from itemadapter import ItemAdapter

class MongoDBUtils:

    def __init__(self):
        self.settings = get_project_settings()

        # 从settings获取MongoDB配置
        mongo_host = self.settings.get('MONGODB_HOST', 'localhost')
        mongo_port = self.settings.get('MONGODB_PORT', 27017)
        mongo_user = self.settings.get('MONGODB_USER')
        mongo_password = self.settings.get('MONGODB_PASSWORD')
        mongo_auth_db = self.settings.get('MONGODB_AUTH_DB', 'admin')

        self.mongo_db = self.settings.get('MONGODB_DATABASE', 'scrapy_temp')
        self.mongo_collection = self.settings.get('MONGODB_COLLECTION', 'collection_temp')

        # 动态构建MongoDB URI
        if mongo_user and mongo_password:
            # 对用户名和密码进行URL编码（处理特殊字符）
            encoded_user = quote_plus(mongo_user)
            encoded_password = quote_plus(mongo_password)
            self.mongo_uri = f"mongodb://{encoded_user}:{encoded_password}@{mongo_host}:{mongo_port}/{mongo_auth_db}"
        else:
            # 无用户名密码的情况
            self.mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"

        # 连接选项（可选）
        self.connect_timeout = self.settings.get('MONGODB_CONNECT_TIMEOUT', 5000)
        self.socket_timeout = self.settings.get('MONGODB_SOCKET_TIMEOUT', 30000)

        # 连接MongoDB
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        """连接MongoDB数据库"""
        try:
            # 添加连接选项
            connection_options = {
                'connectTimeoutMS': self.connect_timeout,
                'socketTimeoutMS': self.socket_timeout,
                'serverSelectionTimeoutMS': 5000
            }

            self.client = pymongo.MongoClient(self.mongo_uri, **connection_options)

            # 测试连接
            self.client.admin.command('ismaster')

            # 选择操作数据库
            self.db = self.client[self.mongo_db]
            self.collection = self.db[self.mongo_collection]

            print(f"成功连接到MongoDB: {self.mongo_uri}")
            print(f"操作数据库: {self.mongo_db}")
            print(f"集合: {self.mongo_collection}")

        except pymongo.errors.ServerSelectionTimeoutError as e:
            print(f"MongoDB连接超时: {e}")
            raise
        except pymongo.errors.OperationFailure as e:
            print(f"MongoDB认证失败: {e}")
            raise
        except Exception as e:
            print(f"MongoDB连接错误: {e}")
            raise

    def url_exists(self, url):
        """检查URL是否已存在"""
        try:
            return self.collection.find_one({'url': url}) is not None
        except Exception as e:
            print(f"检查URL存在性时出错: {e}")
            return False

    def insert_item(self, item):
        """插入新项目到MongoDB"""
        try:
            return self.collection.insert_one(dict(item))
        except Exception as e:
            print(f"插入数据时出错: {e}")
            return None

    def update_item(self, item, keywords_name):
        """更行項目到MongoDB
            keywords_name 增加
        """
        try:
            adapter = ItemAdapter(item)
            item_dict = adapter.asdict()

            # 分离普通字段和数组字段，避免MongoDB更新冲突
            non_keyword_fields = {k: v for k, v in item_dict.items() if k != 'keywords'}

            # 使用$set设置普通字段，$addToSet处理keywords数组
            return self.collection.update_one(
                {'url': item_dict['url']},  # 查询条件
                {
                    '$set': non_keyword_fields,  # 设置/更新普通字段
                    '$addToSet': {keywords_name: {'$each': item_dict[keywords_name]}}  # 添加关键词（新增/更新都适用）
                },
                upsert=True  # 如果不存在则插入新文档
            )
            print(f"成功存储/更新数据: {item_dict['title']}")
            return item
        except Exception as e:
            print(f"插入数据时出错: {e}")
            return None

    def close_connection(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()