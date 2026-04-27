import logging

import scrapy
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..items import ChinatimesItem
from time import sleep
import math
from datetime import datetime

from selenium import webdriver

# Chrome 瀏覽器設定（headless + anti-detection）
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")       # 新版無頭模式，不彈視窗
chrome_options.add_argument("--disable-gpu")        # 禁用 GPU 加速
chrome_options.add_argument("--no-sandbox")         # 解決權限問題
chrome_options.add_argument("--disable-dev-shm-usage")  # 避免 /dev/shm 空間不足
chrome_options.add_argument(
    "--disable-blink-features=AutomationControlled")  # 隱藏自動化標記
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


class ChinatimesSpider(scrapy.Spider):
    name = 'chinatimes'
    allowed_domains = ['www.chinatimes.com']
    search_page = 1
    url_format = '''https://www.chinatimes.com/search/{}?page={}&chdtv'''

    def __init__(self, search_keyword=None):
        self.search_keyword = search_keyword
        now = datetime.now()
        self.scrapy_time = now.strftime('%Y-%m-%d %H:%M')
        # 每個 spider 實例只建立一次 driver，所有頁面共用
        self.driver = webdriver.Chrome(options=chrome_options)
        # 隱藏 webdriver 屬性，降低被偵測機率
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })

    def closed(self, reason):
        """爬蟲關閉時釋放 driver"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def start_requests(self):
        print(f'start_requests')
        start_url = self.url_format.format(
            self.search_keyword, self.search_page)
        print('開始爬蟲：{}'.format(start_url))
        yield scrapy.Request(url=start_url, callback=self.parse_list)

    def parse_first(self, response):
        print(f'parse_first')
        soup = BeautifulSoup(response.text, 'html.parser')
        max_count = soup.select_one(
            '.search-result-count').text.replace(',', '')
        max_page = math.ceil(int(max_count) / 20)
        for page_index in range(self.search_page, max_page + 1):
            start_url = self.url_format.format(self.search_keyword, page_index)
            yield scrapy.Request(url=start_url, callback=self.parse_list)

    def parse_list(self, response):
        print('進入parse_list:{}'.format(response.url))
        try:
            self.driver.get(response.url)
            sleep(2)  # 等待 JS 渲染
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # soup = BeautifulSoup(response.body, 'html.parser')
            el_article_list = soup.select('.articlebox-compact')
            print(f'el_article_list{el_article_list}')
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
                item['intro'] = el_article.select_one(
                    '.intro').get_text().strip()
                item['scrapy_time'] = self.scrapy_time
                print('parse_list:{}'.format(item))

                yield scrapy.Request(item['url'], callback=self.parse_content, cb_kwargs={
                    'item': item
                })
        except Exception as e:
            print(f"parse_list Unexpected {e=}, {type(e)=}")
            tb = e.__traceback__
            while tb is not None:
                print(
                    f"[parse_list]錯誤發生在文件 {tb.tb_frame.f_code.co_filename}，第 {tb.tb_lineno} 行")
                tb = tb.tb_next  # 追溯上一層調用
            print(self.driver.page_source)

    def parse_content(self, response, item):
        print('進入parse_content，網址：{}'.format(response.url))
        try:
            self.driver.get(response.url)
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".meta-info")))

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            el_meta_info_div = soup.select_one('.meta-info')
            el_author_a = el_meta_info_div.select_one('.author a')
            if el_author_a is not None:
                item['author_url'] = el_author_a.get('href')  # 記者鏈接
                item['author'] = el_author_a.get_text().strip()  # 記者名字
            else:
                item['author_url'] = ''  # 記者鏈接
                item['author'] = el_meta_info_div.select_one(
                    '.author').get_text().strip()  # 記者名字
            item['source'] = el_meta_info_div.select_one(
                '.source').get_text()  # 資料來源
            # 提取所有 <p> 的文本，合併成一個字串
            item['content'] = ' '.join(
                [p.get_text(strip=True) for p in soup.select_one('.article-body').select('p')])
            item['tags'] = [tag.get_text()
                            for tag in soup.select('.article-hash-tag .hash-tag a')]
            item['keywords'] = [self.search_keyword]
            item['scrapy_time'] = self.scrapy_time
            print('parse_content:{}'.format(item))
            yield item
        except Exception as e:
            logging.error(f"parse_content Unexpected {e=}, {type(e)=}")
            tb = e.__traceback__
            while tb is not None:
                print(
                    f"[parse_content]錯誤發生在文件 {tb.tb_frame.f_code.co_filename}，第 {tb.tb_lineno} 行")
                tb = tb.tb_next  # 追溯上一層調用
            print(self.driver.page_source)
