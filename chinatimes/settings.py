# Scrapy settings for chinatimes project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# settings.py
LOG_LEVEL = 'INFO'  # 可选值：CRITICAL, ERROR, WARNING, INFO, DEBUG（默认）

BOT_NAME = "chinatimes"

SPIDER_MODULES = ["chinatimes.spiders"]
NEWSPIDER_MODULE = "chinatimes.spiders"
MAX_CONSECUTIVE_DUPLICATES = 10 # 文章最高重複次數

# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}
HTTPERROR_ALLOWED_CODES = [403]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "chinatimes (+http://www.yourdomain.com)"
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 5 # 5秒延迟
AUTOTHROTTLE_ENABLED = True # 启用自动限速
CONCURRENT_REQUESTS_PER_DOMAIN = 2  # 并发控制


# CONCURRENT_REQUESTS_PER_DOMAIN = 1
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
#     'myproject.middlewares.RandomProxyMiddleware': 300,
# }
# Obey robots.txt rules
# ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "chinatimes.middlewares.ChinatimesSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "chinatimes.middlewares.ChinatimesDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# MongoDB数据库配置
MONGODB_URI = 'mongodb://localhost:27017/'  # 你的MongoDB连接字符串
MONGODB_DATABASE = 'scrapy'  # 数据库名称
MONGODB_COLLECTION = 'chinatimesArticles'  # 集合名称
MONGODB_USER = ''
MONGODB_PASSWORD = ''


# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 禁用默认管道，启用MongoDB管道
    # 'chinatimes.pipelines.LtnPipeline': 300,
    'chinatimes.pipelines.MongoDBPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL = 'INFO'  # 从 DEBUG 调整为 INFO