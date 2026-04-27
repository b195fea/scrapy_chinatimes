import multiprocessing as mp
import sys
import os
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import logging

# 確保 Scrapy 能找到專案模組
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'chinatimes.settings')


def run_spider(search_keyword):
    try:
        print(f'呼叫爬蟲指令：傳遞參數:SEARCH_KEYWORD:{search_keyword}')
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl('chinatimes', search_keyword=search_keyword)
        process.start()
    except Exception as e:
        logging.error("發生錯誤訊息")
        logging.error(e.args)


if __name__ == '__main__':

    list_args = [('白珮茹',), ('張錦豪',), ('周雅玲',), ('彭立信',), ('廖先翔',), ('黃瑞傳',)]
    # 將參數傳入程式
    mp.set_start_method("spawn")
    for args in list_args:
        mp.Process(target=run_spider,
                   args=args).start()
