import json
import re

import requests
import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\data_one")
co.set_paths(local_port=9136)


def get_people(people_set, html):
    tree = etree.HTML(html)
    info_list = tree.xpath("//span[@class='name']/a")
    for info in info_list:
        info_name = ''.join(info.xpath(".//text()"))
        info_href = ''.join(info.xpath(".//@href"))
        if len(info_name) > 4:
            break
        people_set.add(info_name)
        print(info_name)
        print(info_href)
    # print(people_set)


def get_people_info(page, table_xpath, next_xpath, people_set):
    partner_html = page.ele(table_xpath).html
    # print(lian_list_html)

    get_people(people_set, partner_html)
    # 判断是否有下一页元素
    target_list = page.eles(next_xpath)
    while True:
        if target_list[-1].text == '>':
            target_list[-1].click(by_js=True)
            time.sleep(2)
            partner_html = page.ele(
                table_xpath).html
            if "无数据" in partner_html:
                break
            # print(partner_html)
            get_people(people_set, partner_html)
        else:
            break


page = ChromiumPage(co)
page.get('https://www.qcc.com/firm/6a6a2bdfcfec0102221e27582488b71f.html')
page.wait.doc_loaded()
people_set = set()
# input()
# -------------------股东信息-------------------------
print("-------------------股东信息-------------------------")
get_people_info(page, table_xpath="xpath=//section[@id='partner']//table[@class='ntable']", next_xpath="xpath=//section[@id='partner']//ul[@class='pagination']//a", people_set=people_set)
# -------------------历史股东人员信息-------------------------
print("-------------------历史股东人员信息-------------------------")
page.ele("xpath=//section[@id='partner']//span[@class='tab-item'][2]/a[@class='item']/span[@class='item-title']").click(by_js=True)
get_people_info(page, table_xpath="xpath=//section[@id='partner']//div[@class='app-ntable']/table[@class='ntable']", next_xpath="xpath=//section[@id='partner']//ul[@class='pagination']//a", people_set=people_set)
# -------------------主要人员信息-------------------------
print("-------------------主要人员信息-------------------------")
get_people_info(page, "xpath=//section[@id='mainmember']//table[@class='ntable']", next_xpath="xpath=//section[@id='mainmember']//ul[@class='pagination']//a", people_set=people_set)
# -------------------历史主要人员信息-------------------------
print("-------------------历史主要人员信息-------------------------")
page.ele("xpath=//section[@id='mainmember']//span[@class='tab-item'][2]/a[@class='item']/span[@class='item-title']").click(by_js=True)
get_people_info(page, "xpath=//section[@id='mainmember']/div[@class='tablist'][2]//table[@class='ntable']", next_xpath="xpath=//section[@id='mainmember']//ul[@class='pagination']//a", people_set=people_set)

input()

page.quit()
