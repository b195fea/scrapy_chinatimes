from scrapy import cmdline
import logging
import math

if __name__ == '__main__':
    cmdline.execute("scrapy crawl chinatimes".split())