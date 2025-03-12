import random
import re
import time
from datetime import datetime, timedelta
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from urllib.parse import urlencode, urljoin
import redis

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\jingdong")
# co = co.set_argument('--no-sandbox')
# co = co.headless()
co.set_paths(local_port=9211)


class JingDongPaiMai:
    def __init__(self):
        self.page = ChromiumPage(co)

    def main_func_jingdong_data(self):
        self.page.set.auto_handle_alert()
        self.page.get("https://pmsearch.jd.com/?publishSource=9&childrenCateId=12767")
        for _ in range(3):
            self.page.scroll.to_bottom()
            time.sleep(2)
        time.sleep(4)
        for page_num in range(775):
            print(page_num)
            if page_num != 0:
                self.page.ele("xpath=//a[@class='ui-pager-next']").click(by_js=True)
                for _ in range(3):
                    self.page.scroll.to_bottom()
                    time.sleep(2)
                time.sleep(4)

            html_etree = etree.HTML(self.page.html)
            target_html = html_etree.xpath("//div[@class='App']//div[@class='goods-list-container']")[0]
            new_html = ''
            for con in target_html:
                new_html += etree.tostring(con, encoding='utf-8').decode()
            # print(new_html)
            new_html_ = etree.HTML(new_html)
            target_html_ = new_html_.xpath("//ul/li")
            for target in target_html_:
                try:
                    url = 'https:' + target.xpath(".//a/@href")[0]
                    url_name = target.xpath(".//a//text()")[0]
                    state = ''.join(target.xpath(".//div[@class='item-status']//text()"))
                    self.page.get(url)
                    self.page.scroll.to_bottom()
                    time.sleep(4)
                    html_detail = self.page.html
                except Exception as e:
                    print('解析url和url名字时出错', e)
                    continue
                print(url, url_name, state, html_detail)
        self.page.quit()


jd = JingDongPaiMai()
jd.main_func_jingdong_data()
