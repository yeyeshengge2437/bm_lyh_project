# 获取京东拍卖已结束的所有链接
import random
import re
import time
from datetime import datetime, timedelta
import json
import os
from typing import Dict
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from urllib.parse import urlencode, urljoin
import redis




def save_to_json(data: Dict, filename: str = "data.json") -> None:
    """
    将数据追加到 JSON 文件，每次保存完整数据
    :param data: 要保存的字典数据，需包含 url, url_name, state
    :param filename: JSON 文件名 (默认: data.json)
    """
    # 如果文件不存在则初始化空列表
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)

    # 读取现有数据
    with open(filename, 'r') as f:
        existing_data = json.load(f)

    # 检查重复（根据 url 去重）
    urls = {item['url'] for item in existing_data}
    if data['url'] not in urls:
        existing_data.append(data)
    else:
        # 如果已存在，可以选择更新状态（可选）
        for item in existing_data:
            if item['url'] == data['url']:
                item.update(data)
                break

    # 写入更新后的数据
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=True)


class JingDongPaiMai:
    co = ChromiumOptions()
    co = co.set_user_data_path(r"D:\chome_data\jingdong")
    # co = co.set_argument('--no-sandbox')
    # co = co.headless()
    co.set_paths(local_port=9211)
    def __init__(self):
        self.page = ChromiumPage(self.co)

    def main_func_jingdong_data(self):
        """
        获取京东拍卖已结束的所有链接并保存到json中
        :return:
        """
        self.page.set.auto_handle_alert()
        self.page.get("https://pmsearch.jd.com/?publishSource=9&childrenCateId=12767")
        for _ in range(3):
            self.page.scroll.to_bottom()
            time.sleep(2)
        time.sleep(4)
        for page_num in range(50):
            print(page_num)
            if page_num != 0:
                self.page.ele("xpath=//a[@class='ui-pager-next']").click(by_js=True)
                for _ in range(3):
                    self.page.scroll.to_bottom()
                    time.sleep(2)
                time.sleep(4)

            html_etree = etree.HTML(self.page.html)
            try:
                target_html = html_etree.xpath("//div[@class='App']//div[@class='goods-list-container']")[0]
            except Exception as e:
                print('获取html出错', e)
                input()
                continue
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
                    # self.page.get(url)
                    # self.page.scroll.to_bottom()
                    # time.sleep(4)
                    # html_detail = self.page.html
                except Exception as e:
                    print('解析url和url名字时出错', e)
                    continue
                print(url, url_name, state)
                data_dict = {"url": url, "url_name": url_name, "state": state}
                save_to_json(data_dict, 'jingdongpaimai.json')
        self.page.quit()



# jd = JingDongPaiMai()
# jd.main_func_jingdong_data()
