# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.exceptions import IgnoreRequest
from scrapy.signals import spider_closed

from .mongodb_utils import MongoDBUtils

class ChinatimesSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ChinatimesDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        self.mongo_utils = MongoDBUtils()
        self.consecutive_duplicates = 0
        self.max_consecutive_duplicates = 1  # 默认值，可在settings中覆盖

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        # 从settings获取最大重复次数
        middleware.max_consecutive_duplicates = crawler.settings.getint(
            'MAX_CONSECUTIVE_DUPLICATES', 30
        )
        crawler.signals.connect(middleware.spider_closed, signal=spider_closed)
        return middleware

    def process_request(self, request, spider):
        """
        处理每个请求，检查URL是否已在MongoDB中存在
        """
        # 从 spider 实例中获取启动时传递的 coluid 参数
        # 检查URL是否已存在
        if self.mongo_utils.url_exists(request.url):
            spider.logger.info(
                f'检测到重复URL: {request.url},最大次數：{self.max_consecutive_duplicates},重複次數:{self.consecutive_duplicates}')
            # 更新连续重复计数
            self.consecutive_duplicates += 1
            spider.consecutive_duplicates = self.consecutive_duplicates

            # 检查是否达到停止条件
            if self.consecutive_duplicates >= self.max_consecutive_duplicates:
                spider.logger.info(f'达到最大重复次数 {self.max_consecutive_duplicates}，停止爬虫')
                spider.crawler.engine.close_spider(spider, '达到最大重复URL数量')

            # 忽略这个重复的请求
            raise IgnoreRequest(f"重复URL: {request.url}")

        return None

    def spider_closed(self, spider, reason):
        """爬虫关闭时清理资源"""
        spider.logger.info(f'爬虫关闭，原因: {reason}')
        spider.logger.info(f'最终连续重复计数: {self.consecutive_duplicates}')
        self.mongo_utils.close_connection()