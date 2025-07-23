# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChinatimesItem(scrapy.Item):
    title = scrapy.Field() # 標題
    content = scrapy.Field() # 內容
    author = scrapy.Field() # 作者
    author_href = scrapy.Field() #作者鏈接
    source = scrapy.Field() #資料來源
    date = scrapy.Field() # 日期
    hour = scrapy.Field() # 時間
    tags = scrapy.Field() # 標籤
    href = scrapy.Field()  # 網址
    intro = scrapy.Field()  # 簡介
    category = scrapy.Field()  # 分類
    category_href = scrapy.Field()  # 分類鏈接
    search_key2 = scrapy.Field()  # 搜索條件
    pass
