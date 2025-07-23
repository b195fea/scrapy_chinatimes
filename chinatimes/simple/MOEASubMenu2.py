from pymongo import MongoClient
from chinatimes import settings

def checkIsExist(search_key, href):
    connection = MongoClient('mongodb://192.168.3.6:27017')
    spider_name = 'chinatimes'  # 爬虫名称：中时新闻网
    db_chinatimes = connection[spider_name]
    search_key = 'carbonTax'  # 搜寻条件：碳费
    col_carbonTax = db_chinatimes[search_key]

    count = col_carbonTax.count_documents({'search_key':search_key,'href':href})
    if count == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    search_key = '碳費'
    href = 'https://www.chinatimes.com/newspapers/20250306000208-260210'
    print(checkIsExist(search_key,href))