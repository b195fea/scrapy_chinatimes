import logging

import scrapy
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chinatimes.items import ChinatimesItem
from time import sleep
import math
from pymongo import MongoClient
from chinatimes import settings

from selenium import webdriver
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9",
    "Host": "www.chinatimes.com",  #目標網站
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36" #使用者代理
}

# def checkIsExist(search_key, href):


# Chrome 瀏覽器設定
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless=new")  # 新版 Chrome 建議使用 --headless=new
# chrome_options.add_argument("--disable-gpu")   # 禁用 GPU 加速（可選）
# chrome_options.add_argument("--no-sandbox")    # 解決 Linux 權限問題（可選）


class ChinatimesSpider(scrapy.Spider):
    search_key = '張碩芳'
    name = 'chinatimes'
    allowed_domains = ['www.chinatimes.com']
    search_page = 1
    url_format = '''https://www.chinatimes.com/search/{}?page={}&chdtv'''


    def start_requests(self):
        try:
            start_url = self.url_format.format(self.search_key, self.search_page)
            print('開始爬蟲：{}'.format(start_url))
            # driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome()
            driver.get(start_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            max_count = soup.select_one('.search-result-count').text.replace(',', '')
            print('取得最大頁數：{}'.format(max_count))
            max_page = math.ceil(int(max_count) / 20)
            # start_url = url_format.format(search_key, 1)
            # yield scrapy.Request(url=start_url, callback=self.parse_list, headers=headers)
            for page_index in range(self.search_page, max_page + 1):
                start_url = self.url_format.format(self.search_key, page_index)
                yield scrapy.Request(url=start_url, callback=self.parse_list,headers=headers)
        except Exception as e:
            logging.error(f"parse_content Unexpected {err=}, {type(err)=}")
            tb = e.__traceback__
            while tb is not None:
                print(f"[parse_content]錯誤發生在文件 {tb.tb_frame.f_code.co_filename}，第 {tb.tb_lineno} 行")
                tb = tb.tb_next  # 追溯上一層調用
            print(driver.page_source)
        finally:
            driver.quit()

    def parse_list(self, response):
        print('進入parse_list:{}'.format(response.url))
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(response.url)
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".articlebox-compact")))

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            el_article_list = soup.select('.articlebox-compact')
            # 取得網址列表
            for el_article in el_article_list:
                item = ChinatimesItem()
                el_title_a = el_article.select_one('h3 a')
                item['url'] = el_title_a.get('href')  # 取得屬性
                item['title'] = el_title_a.get_text()  # 取得內文
                item['hour'] = el_article.select_one('.hour').get_text()
                item['date'] = el_article.select_one('.date').get_text()
                el_category_a = el_article.select_one('.category a')
                item['category'] = el_category_a.get_text()
                item['category_url'] = el_category_a.get('href')
                item['intro'] = el_article.select_one('.intro').get_text().strip()
                print('parse_list:{}'.format(item))

                yield scrapy.Request(item['url'], callback=self.parse_content, headers=headers, cb_kwargs={
                    'item': item
                })
        except Exception as err:
            print(f"parse_list Unexpected {err=}, {type(err)=}")
            tb = e.__traceback__
            while tb is not None:
                print(f"[parse_list]錯誤發生在文件 {tb.tb_frame.f_code.co_filename}，第 {tb.tb_lineno} 行")
                tb = tb.tb_next  # 追溯上一層調用
            print(driver.page_source)
        finally:
            driver.quit()


    def parse_content(self, response, item):
        print('進入parse_content，網址：{}'.format(response.url))
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(response.url)
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".meta-info")))

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            el_meta_info_div = soup.select_one('.meta-info')
            el_author_a = el_meta_info_div.select_one('.author a')
            if el_author_a is not None:
                item['author_url'] = el_author_a.get('href')  # 記者鏈接
                item['author'] = el_author_a.get_text().strip()  # 記者名字
            else:
                item['author_url'] = ''  # 記者鏈接
                item['author'] = el_meta_info_div.select_one('.author').get_text().strip()  # 記者名字
            item['source'] = el_meta_info_div.select_one('.source').get_text()  # 資料來源
            # 提取所有 <p> 的文本，合併成一個字串
            item['content'] = ' '.join([p.get_text(strip=True) for p in soup.select_one('.article-body').select('p')])
            item['tags'] = [tag.get_text() for tag in soup.select('.article-hash-tag .hash-tag a')]
            item['keywords'] = [self.search_key]
            print('parse_content:{}'.format(item))
            yield item
        except Exception as e:
            logging.error(f"parse_content Unexpected {err=}, {type(err)=}")
            tb = e.__traceback__
            while tb is not None:
                print(f"[parse_content]錯誤發生在文件 {tb.tb_frame.f_code.co_filename}，第 {tb.tb_lineno} 行")
                tb = tb.tb_next  # 追溯上一層調用
            print(driver.page_source)
        finally:
            driver.quit()