import json
import random
import re
from 验证码识别 import get_captcha
import requests
import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\data_one")
co.set_paths(local_port=9136)
random_float = random.uniform(1, 5)
# 连接浏览器
page = ChromiumPage(co)
tab = page.get_tab()
# 访问网页
tab.get('https://www.qcc.com/')
# time.sleep(3)
search_name = tab.ele("xpath=//input[@id='searchKey']")
search_name.click()
time.sleep(1)
search_name.input('金川集团股份有限公司')
# search_name.input('华为通数字科技（北京）有限公司')
# 搜索按键点击
tab.ele("xpath=//span[@class='input-group-btn']/button[@class='btn btn-primary']").click(by_js=True)
time.sleep(2)
# 获取公司列表
company_list = tab.eles("xpath=//div[@class='search-cell']//tr")
# 点击第一个公司
# tab.ele("xpath=//div[@class='search-cell']//tr[1]//a[@class='title copy-value']").click(by_js=True)
# 获取第一个公司链接
company_url = tab.ele("xpath=//div[@class='search-cell']//tr[1]//a[@class='title copy-value']").attr('href')
new_tab = page.new_tab()
tab.close()
new_tab.get(company_url)
# 获取公司基础信息
company_info = new_tab.ele("xpath=//section[@id='cominfo']/div[@class='cominfo-normal']/table[@class='ntable']")
company_info_html = company_info.html
# print(company_info_html)  # 目前基础信息为html的表格信息，需要时进行解析调用


# 获取公司股东信息

try:
    shareholder_info_list = new_tab.eles(
        "xpath=//section[@id='partner']/div[@class='tablist tablist-cpartner']//span[@class='tab-item']")
    new_tab.scroll.to_see(shareholder_info_list[0])
except:
    shareholder_info_list = new_tab.eles(
        "xpath=//section[@id='partner']/div[@class='tablist tablist-ipopartner']//span[@class='tab-item']")
    new_tab.scroll.to_see(shareholder_info_list[0])
for shareholder_info in shareholder_info_list:
    print(str(shareholder_info.text))
    if "最新公示" in shareholder_info.text:
        shareholder_info.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        latest_ann = new_tab.ele(
            "xpath=//section[@id='partner']/div[@class='tablist tablist-ipopartner']//table[@class='ntable']")
        latest_ann_html = latest_ann.html
        print("-------------------最新公示----------------")
        print(latest_ann_html)
        pass  # 有的第一个表是最新公示，有的是股东信息。
    elif "股东信息" in shareholder_info.text and "历史股东信息" not in shareholder_info.text:
        shareholder_info.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        shareholder = new_tab.ele(
            "xpath=//section[@id='partner']/div[@class='tablist tablist-cpartner']//table[@class='ntable']")
        shareholder_html = shareholder.html
        print("-------------------股东信息----------------")
        print(shareholder_html)
        pass  # 最新公示和股东信息都可能在第一个表首页。
    elif "工商登记" in shareholder_info.text:
        shareholder_info.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        business_info = new_tab.ele(
            "xpath=//section[@id='partner']/div[@class='tablist tablist-cpartner']//table[@class='ntable']")
        business_info_html = business_info.html
        print("-------------------工商登记----------------")
        print(business_info_html)
        pass
    elif "历史股东信息" in shareholder_info.text:
        shareholder_info.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        his_shareholder_info = new_tab.ele(
            "xpath=//section[@id='partner']//div[@class='app-ntable']/table[@class='ntable']")  # 获取历史股东的信息表
        his_shareholder_info_html = his_shareholder_info.html
        print(his_shareholder_info_html)
    elif "历史股东镜像" in shareholder_info.text:
        shareholder_info.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        try:

            his_shareholder_mirror = new_tab.eles(
                "xpath=//section[@id='partner']//table[@class='ntable ntable-table-fixed']")
            value = his_shareholder_mirror[0]
        except:
            his_shareholder_mirror = new_tab.eles(
                "xpath=//section[@id='partner']//div[@class='ntable-scroll dragable fixed-over']")
            value = his_shareholder_mirror[0]
        his_shareholder_mirror_html = ''
        for mirror in his_shareholder_mirror:
            his_shareholder_mirror_html += mirror.html
        print("-------------------历史股东镜像----------------")
        print(his_shareholder_mirror_html)
        pass
    else:
        print(f"未知股东信息:{shareholder_info.text}")

# 获取主要人员

key_personnel_list = new_tab.eles("xpath=//div[@class='tablist']//span[@class='tab-item']")
new_tab.scroll.to_see(key_personnel_list[0])
for key_personnel in key_personnel_list:
    if "主要人员" in key_personnel.text and "历史主要人员" not in key_personnel.text:
        key_personnel_info_html = ''
        # 正则匹配文本中的数字
        num = re.findall(r'\d+', key_personnel.text)[0]
        num = int(num)
        print(num)
        key_personnel.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        key_personnel_info = new_tab.ele("xpath=//section[@id='mainmember']//table[@class='ntable']")
        key_personnel_info_html += key_personnel_info.html
        if num > 10:
            frequency = int(num / 10)
            print(frequency)
            for _ in range(frequency):
                target_list = new_tab.eles("xpath=//section[@id='mainmember']//ul[@class='pagination']//a")
                if target_list[-1].text == '>':
                    target_list[-1].click(by_js=True)
                    new_tab.wait(random_float)
                    key_personnel_info = new_tab.ele("xpath=//section[@id='mainmember']//table[@class='ntable']")
                    key_personnel_info_html += key_personnel_info.html
        print("-------------------主要人员----------------")
        print(key_personnel_info_html)
    elif "历史主要人员" in key_personnel.text:
        his_key_personnel_info_html = ''
        num = re.findall(r'\d+', key_personnel.text)[0]
        num = int(num)
        print(num)
        key_personnel.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        his_key_personnel_info = new_tab.eles("xpath=//section[@id='mainmember']//table[@class='ntable']")[-1]
        his_key_personnel_info_html += his_key_personnel_info.html
        if num > 10:
            frequency = int(num / 10)
            print(frequency)
            for _ in range(frequency):
                target_list = new_tab.eles("xpath=//section[@id='mainmember']//ul[@class='pagination']//a")
                if target_list[-1].text == '>':
                    target_list[-1].click(by_js=True)
                    new_tab.wait(random_float)
                    his_key_personnel_info = new_tab.eles("xpath=//section[@id='mainmember']//table[@class='ntable']")[
                        -1]
                    his_key_personnel_info_html += his_key_personnel_info.html
        print("-------------------历史主要人员----------------")
        print(his_key_personnel_info_html)

# 获取对外投资信息
try:
    outbound_investment_list = new_tab.eles("xpath=//section[@id='touzilist']//span[@class='tab-item']")
    new_tab.scroll.to_see(outbound_investment_list[0])
except:
    print("没有对外投资信息")
    outbound_investment_list = []
for outbound_investment in outbound_investment_list:
    if "对外投资" in outbound_investment.text and "历史对外投资" not in outbound_investment.text and "对外投资(间接)" not in outbound_investment.text:
        outbound_investment_html = ''
        num = re.findall(r'\d+', outbound_investment.text)[0]
        num = int(num)
        print(num)
        outbound_investment.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        outbound_investment_info = new_tab.ele(
            "xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")
        outbound_investment_html += outbound_investment_info.html
        if num > 10:
            frequency = int(num / 10)
            print(frequency)
            for _ in range(frequency):
                target_list = new_tab.eles("xpath=//section[@id='touzilist']//ul[@class='pagination']//a")
                if target_list[-1].text == '>':
                    target_list[-1].click(by_js=True)
                    new_tab.wait(random_float)
                    outbound_investment_info = new_tab.ele(
                        "xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")
                    outbound_investment_html += outbound_investment_info.html
        print("-------------------对外投资----------------")
        print(outbound_investment_html)
    elif "历史对外投资" in outbound_investment.text:
        his_outbound_investment_html = ''
        num = re.findall(r'\d+', outbound_investment.text)[0]
        num = int(num)
        print(num)
        try:
            outbound_investment.ele("xpath=//a").click(by_js=True)
        except:
            print("存在验证码")
            get_captcha(page, tab)
            break
        new_tab.wait(random_float)
        his_outbound_investment_info = \
        new_tab.eles("xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")[-1]
        his_outbound_investment_html += his_outbound_investment_info.html
        if num > 10:
            frequency = int(num / 10)
            print(frequency)
            for _ in range(frequency):
                target_list = new_tab.eles("xpath=//section[@id='touzilist']//ul[@class='pagination']//a")
                if target_list[-1].text == '>':
                    target_list[-1].click(by_js=True)
                    new_tab.wait(random_float)
                    his_outbound_investment_info = \
                    new_tab.eles("xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")[
                        -1]
                    his_outbound_investment_html += his_outbound_investment_info.html
        print("-------------------历史对外投资----------------")
        print(his_outbound_investment_html)
    elif "对外投资(间接)" in outbound_investment.text:
        indirect_outbound_investment_html = ''
        num = re.findall(r'\d+', outbound_investment.text)[0]
        num = int(num)
        print(num)
        outbound_investment.ele("xpath=//a").click(by_js=True)
        new_tab.wait(random_float)
        indirect_outbound_investment_info = \
        new_tab.eles("xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")[1]
        indirect_outbound_investment_html += indirect_outbound_investment_info.html
        if num > 10:
            frequency = int(num / 10)
            print(frequency)
            for _ in range(frequency):
                try:
                    target_list = new_tab.eles("xpath=//section[@id='touzilist']//ul[@class='pagination']//a")
                    for target in target_list:
                        if target.text == '>':
                            target.click(by_js=True)
                            new_tab.wait(random_float)
                            indirect_outbound_investment_info = new_tab.eles(
                                "xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")[1]
                            indirect_outbound_investment_html += indirect_outbound_investment_info.html
                except:
                    print("存在验证码")
                    get_captcha(page, tab)
                    tab.refresh()
                    input()
                    break
        print("-------------------对外投资(间接)----------------")
        print(indirect_outbound_investment_html)

input("1111")
page.quit()
