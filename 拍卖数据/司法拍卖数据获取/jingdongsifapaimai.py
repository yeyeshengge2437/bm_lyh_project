# 京东拍卖
import json
import re
import time
from datetime import datetime
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Settings
from fake_useragent import UserAgent
import tempfile
import random
from lxml import etree
# import datetime
import re

"""
第一步，通过关键字查询，返回多项数据
"""


def by_keyword_search(keyword):
    co = ChromiumOptions()
    co = co.set_user_data_path(r"D:\chome_data\jingdong")
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True
    # options.set_argument('--disable-blink-features=AutomationControlled')
    # co.set_argument('--incognito')
    # co.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')
    # co = co.set_argument('--no-sandbox')
    # co = co.headless()
    co.set_paths(local_port=9212)

    page = ChromiumPage(co)
    page.get('https://auction.jd.com/sifa.html')
    page.wait.doc_loaded()
    time.sleep(4)
    page.ele("xpath=//input[@id='searchText']").input(keyword)
    time.sleep(random.randint(1, 7))
    page.ele("xpath=//button[@id='searchButton']").click(by_js=True)
    search_tab = page.latest_tab
    search_tab.wait.doc_loaded()
    time.sleep(4)
    search_tab.ele("xpath=//div[@class='s-line assets-type ']//li[1]//i").click(by_js=True)
    time.sleep(4)
    info_list = search_tab.eles("xpath=//div[@id='root']//div[@class='goods-list-container']/ul/li")
    for info in info_list:
        title = info.ele("xpath=//div[@class='item-name']").text
        url = info.ele("xpath=/a").attr('href')
        status = info.ele("xpath=//div[@class='item-status']").text
        item_time = info.ele("xpath=//div[@class='item-countdown']").text
        print(title, url, status, item_time)
    page.quit()


by_keyword_search('（2024）粤1303执2716号')

