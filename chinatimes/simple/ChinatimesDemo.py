from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import os
from bs4 import BeautifulSoup
from chinatimes.items import ChinatimesItem
from chinatimes import settings

# 設定下載路徑(請修改為你自己的目標路徑)
download_dir = r"D:\9.1_work\scrapy\StatisticQry"
# 起始索引 (從31開始)
current_index = 40
# 最大重試次數
MAX_RETRIES = 3

# Chrome 瀏覽器設定
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "profile.default_content_settings.popups": 0,
    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
}
chrome_options.add_experimental_option("prefs", prefs)

if __name__ == '__main__':
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
    try:
        search_key = '碳費'
        search_page = 3
        # start_url = '''https://www.chinatimes.com/search/{}?page={}&chdtv'''.format(search_key,search_page)
        # driver.get(start_url)
        #
        # print(driver.title)
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        #
        #
        # el_search_count = soup.select_one('.search-result-count')
        # print(el_search_count, el_search_count.text.replace(',',''))
        # # el_article_list = soup.find('.article-list ')
        # el_article_list = soup.select('.articlebox-compact')
        # # el_article_list = soup.find_all('div',class_= '.articlebox-compact')
        # print(len(el_article_list))
        # item = ChinatimesItem()
        #
        # data = { }
        # # 取得網址列表
        # for el_article in el_article_list:
        #     print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
        #     el_title_a = el_article.select_one('h3 a')
        #     item['href'] = el_title_a.get('href') # 取得屬性
        #     item['title'] = el_title_a.get_text() # 取得內文
        #     item['hour'] = el_article.select_one('.hour').get_text()
        #     item['date'] = el_article.select_one('.date').get_text()
        #     el_category_a = el_article.select_one('.category a')
        #     item['category'] = el_category_a.get_text()
        #     item['category_href'] = el_category_a.get('href')
        #     item['intro'] = el_article.select_one('.intro').get_text().strip()
        #     data[item['href']] = item
        #     # print(item)
        #     break

            # print(el_article)

        print('---------------------------------------------------')
        print('---------------------------------------------------')
        item = ChinatimesItem()
        # 取得網址內容
        # url = 'https://www.chinatimes.com/realtimenews/20250306001818-260410'
        # url = 'https://www.chinatimes.com/newspapers/20250331000149-260202?chdtv' # 沒有作者鏈接
        url = 'https://www.chinatimes.com/newspapers/20250331000334-260208?chdtv'  # 有作者鏈接
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(el_meta_info_div)
        el_meta_info_div = soup.select_one('.meta-info')
        el_author_a = el_meta_info_div.select_one('.author a')
        if el_author_a is not None:
            item['author_href'] = el_author_a.get('href')  # 記者鏈接
            item['author'] = el_author_a.get_text().strip()  # 記者名字
        else:
            item['author_href'] = '' # 記者鏈接
            item['author'] = el_meta_info_div.select_one('.author').get_text().strip()  # 記者名字

        item['source'] = el_meta_info_div.select_one('.source').get_text()  # 資料來源
        # item['source'] = el_meta_info_a.select_one('.source').get_text()  # 資料來源
        # el_article_body_div.select('.article-body')
        # 提取所有 <p> 的文本，合併成一個字串
        item['content'] = ' '.join([p.get_text(strip=True) for p in soup.select_one('.article-body').select('p')])
        item['tags'] = [tag.get_text() for tag in soup.select('.article-hash-tag .hash-tag a')]
        print(item)
        # combined_text = ' '.join(soup.select('.article-body p ::text').getall()).strip()
        # print()


        #
        # el_article_body_div = soup.select_one('.article-body')
        # data = [ el for el.get_text() in el_article_body_div.select('p')]



        # item =


    finally:
        driver.quit()
