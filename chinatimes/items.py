# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinatimesItem(scrapy.Item):
    title = scrapy.Field() # 標題
    content = scrapy.Field() # 內容
    author = scrapy.Field() # 作者
    author_url = scrapy.Field() #作者鏈接
    source = scrapy.Field() #資料來源
    date = scrapy.Field() # 日期
    hour = scrapy.Field() # 時間
    tags = scrapy.Field() # 標籤
    url = scrapy.Field()  # 網址
    intro = scrapy.Field()  # 簡介
    category = scrapy.Field()  # 分類
    category_url = scrapy.Field()  # 分類鏈接
    keywords = scrapy.Field()  # 關鍵字
    scrapy_time = scrapy.Field() # 抓取時間
    pass
