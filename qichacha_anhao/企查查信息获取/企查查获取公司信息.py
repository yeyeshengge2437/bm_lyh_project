import json
import random
import re
from 验证码识别 import get_captcha
import requests
import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

discovered_subject_dict = {}

def get_table_subject(html, xpath_loc, xpath_href=".//@href", xpath_text=".//text()"):
    """
    获取表格中的公司信息和个人信息链接
    :param html: 表的html
    :param xpath_loc: 获取公司或个人的位置
    :param xpath_href: href的路径
    :param xpath_text: 名称的路径
    :return:
    """
    all_info = []
    target_html = etree.HTML(html)
    # 获取股东名称和链接
    infos = target_html.xpath(xpath_loc)
    for info in infos:
        info_dict = {}
        info_name = ''.join(info.xpath(xpath_text))
        info_link = ''.join(info.xpath(xpath_href))
        if info_link:
            if "firm" in info_link:
                info_dict["是否为公司"] = "1"
                info_dict["名称"] = info_name
                info_dict["链接"] = info_link
            else:
                info_dict["是否为公司"] = "0"
                info_dict["名称"] = info_name
                info_dict["链接"] = info_link
        else:
            info_dict["是否为公司"] = "未知"
            info_dict["名称"] = info_name
        all_info.append(info_dict)
    return all_info

def get_company_info(tab):
    # 获取公司基础信息
    company_info = new_tab.ele("xpath=//section[@id='cominfo']/div[@class='cominfo-normal']/table[@class='ntable']")
    company_info_html = company_info.html
    print(company_info_html)  # 目前基础信息为html的表格信息，需要时进行解析调用


def get_company_shareholder_info(tab):
    try:
        shareholder_info_list = tab.eles(
            "xpath=//section[@id='partner']/div[@class='tablist tablist-cpartner']//span[@class='tab-item']")
        tab.scroll.to_see(shareholder_info_list[0])
    except:
        shareholder_info_list = tab.eles(
            "xpath=//section[@id='partner']/div[@class='tablist tablist-ipopartner']//span[@class='tab-item']")
        tab.scroll.to_see(shareholder_info_list[0])
    for shareholder_info in shareholder_info_list:  # 股东信息列表
        print(str(shareholder_info.text))
        if "最新公示" in shareholder_info.text:
            shareholder_info.ele("xpath=//a").click(by_js=True)
            tab.wait(random_float)
            latest_ann = tab.ele(
                "xpath=//section[@id='partner']/div[@class='tablist tablist-ipopartner']//table[@class='ntable']")
            latest_ann_html = latest_ann.html
            print("-------------------最新公示----------------")
            # print(latest_ann_html)
            info_list = get_table_subject(latest_ann_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["最新公示"] = info_list

        elif "股东信息" in shareholder_info.text and "历史股东信息" not in shareholder_info.text:
            shareholder_info.ele("xpath=//a").click(by_js=True)
            tab.wait(random_float)
            shareholder = tab.ele(
                "xpath=//section[@id='partner']/div[@class='tablist tablist-cpartner']//table[@class='ntable']")
            shareholder_html = shareholder.html
            print("-------------------股东信息----------------")
            shareholder_info_ = get_table_subject(shareholder_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["股东信息"] = shareholder_info_
            pass  # 最新公示和股东信息都可能在第一个表首页。
        elif "工商登记" in shareholder_info.text:
            shareholder_info.ele("xpath=//a").click(by_js=True)
            tab.wait(random_float)
            business_info = tab.ele(
                "xpath=//section[@id='partner']/div[@class='tablist tablist-cpartner']//table[@class='ntable']")
            business_info_html = business_info.html
            print("-------------------工商登记----------------")
            bus_info = get_table_subject(business_info_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["工商登记"] = bus_info
            pass
        elif "历史股东信息" in shareholder_info.text:
            shareholder_info.ele("xpath=//a").click(by_js=True)
            tab.wait(random_float)
            his_shareholder_info = tab.ele(
                "xpath=//section[@id='partner']//div[@class='app-ntable']/table[@class='ntable']")  # 获取历史股东的信息表
            his_shareholder_info_html = his_shareholder_info.html
            # print(his_shareholder_info_html)
            his_shareholder = get_table_subject(his_shareholder_info_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["历史股东信息"] = his_shareholder
        elif "历史股东镜像" in shareholder_info.text:
            shareholder_info.ele("xpath=//a").click(by_js=True)
            tab.wait(random_float)
            try:
                his_shareholder_mirror = tab.eles(
                    "xpath=//section[@id='partner']//table[@class='ntable ntable-table-fixed']")
                value = his_shareholder_mirror[0]
            except:
                his_shareholder_mirror = tab.eles(
                    "xpath=//section[@id='partner']//div[@class='ntable-scroll dragable fixed-over']")
                value = his_shareholder_mirror[0]
            his_shareholder_mirror_html = ''
            for mirror in his_shareholder_mirror:
                his_shareholder_mirror_html += mirror.html
            print("-------------------历史股东镜像----------------")
            # print(his_shareholder_mirror_html)
            his_shareholder_mirror = get_table_subject(his_shareholder_mirror_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["历史股东镜像"] = his_shareholder_mirror
            pass
        else:
            print(f"未知股东信息:{shareholder_info.text}")


def get_company_key_personnel(tab):
    key_personnel_list = tab.eles("xpath=//div[@class='tablist']//span[@class='tab-item']")
    tab.scroll.to_see(key_personnel_list[0])
    for key_personnel in key_personnel_list:
        if "主要人员" in key_personnel.text and "历史主要人员" not in key_personnel.text:
            key_personnel_info_html = ''
            # 正则匹配文本中的数字
            num = re.findall(r'\d+', key_personnel.text)[0]
            num = int(num)
            print(num)
            key_personnel.ele("xpath=//a").click(by_js=True)
            tab.wait(random_float)
            key_personnel_info = tab.ele("xpath=//section[@id='mainmember']//table[@class='ntable']")
            key_personnel_info_html += key_personnel_info.html
            if num > 10:
                frequency = int(num / 10)
                print(frequency)
                for _ in range(frequency):
                    target_list = tab.eles("xpath=//section[@id='mainmember']//ul[@class='pagination']//a")
                    if target_list[-1].text == '>':
                        target_list[-1].click(by_js=True)
                        tab.wait(random_float)
                        key_personnel_info = tab.ele("xpath=//section[@id='mainmember']//table[@class='ntable']")
                        key_personnel_info_html += key_personnel_info.html
            print("-------------------主要人员----------------")
            # print(key_personnel_info_html)
            key_personnel_info = get_table_subject(key_personnel_info_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["主要人员"] = key_personnel_info
        elif "历史主要人员" in key_personnel.text:
            his_key_personnel_info_html = ''
            num = re.findall(r'\d+', key_personnel.text)[0]
            num = int(num)
            print(num)
            key_personnel_ = key_personnel.ele("xpath=//a")
            if not key_personnel_:
                continue
            key_personnel_.click(by_js=True)
            tab.wait(random_float)
            his_key_personnel_info = tab.eles("xpath=//section[@id='mainmember']//table[@class='ntable']")[-1]
            his_key_personnel_info_html += his_key_personnel_info.html
            if num > 10:
                frequency = int(num / 10)
                print(frequency)
                for _ in range(frequency):
                    target_list = tab.eles("xpath=//section[@id='mainmember']//ul[@class='pagination']//a")
                    if target_list[-1].text == '>':
                        target_list[-1].click(by_js=True)
                        tab.wait(random_float)
                        his_key_personnel_info = tab.eles("xpath=//section[@id='mainmember']//table[@class='ntable']")[
                            -1]
                        his_key_personnel_info_html += his_key_personnel_info.html
            print("-------------------历史主要人员----------------")
            # print(his_key_personnel_info_html)
            his_key_personnel_info = get_table_subject(his_key_personnel_info_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["历史主要人员"] = his_key_personnel_info


def get_company_outbound_investment(tab):
    try:
        outbound_investment_list = tab.eles("xpath=//section[@id='touzilist']//span[@class='tab-item']")
        tab.scroll.to_see(outbound_investment_list[0])
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
            tab.wait(random_float)
            outbound_investment_info = tab.ele(
                "xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")
            outbound_investment_html += outbound_investment_info.html
            if num > 10:
                frequency = int(num / 10)
                print(frequency)
                for _ in range(frequency):
                    target_list = tab.eles("xpath=//section[@id='touzilist']//ul[@class='pagination']//a")
                    if target_list[-1].text == '>':
                        target_list[-1].click(by_js=True)
                        tab.wait(random_float)
                        outbound_investment_info = tab.ele(
                            "xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")
                        outbound_investment_html += outbound_investment_info.html
            print("-------------------对外投资----------------")
            outbound_info = get_table_subject(outbound_investment_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["对外投资"] = outbound_info
        elif "历史对外投资" in outbound_investment.text:
            his_outbound_investment_html = ''
            num = re.findall(r'\d+', outbound_investment.text)[0]
            num = int(num)
            print(num)
            outbound_in_ = outbound_investment.ele("xpath=//a")
            if not outbound_in_:
                continue
            outbound_in_.click(by_js=True)
            tab.wait(random_float)
            his_outbound_investment_info = \
            tab.eles("xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")[-1]
            his_outbound_investment_html += his_outbound_investment_info.html
            if num > 10:
                frequency = int(num / 10)
                print(frequency)
                for _ in range(frequency):
                    target_list = tab.eles("xpath=//section[@id='touzilist']//ul[@class='pagination']//a")
                    if target_list[-1].text == '>':
                        target_list[-1].click(by_js=True)
                        tab.wait(random_float)
                        his_outbound_investment_info = \
                        tab.eles("xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")[
                            -1]
                        his_outbound_investment_html += his_outbound_investment_info.html
            print("-------------------历史对外投资----------------")
            his_out_info = get_table_subject(his_outbound_investment_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["历史对外投资"] = his_out_info
        elif "对外投资(间接)" in outbound_investment.text:
            indirect_outbound_investment_html = ''
            num = re.findall(r'\d+', outbound_investment.text)[0]
            num = int(num)
            print(num)
            outbound_ = outbound_investment.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            indirect_outbound_investment_info = \
            tab.eles("xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")[1]
            indirect_outbound_investment_html += indirect_outbound_investment_info.html
            if num > 10:
                frequency = int(num / 10)
                print(frequency)
                for _ in range(frequency):
                    try:
                        target_list = tab.eles("xpath=//section[@id='touzilist']//ul[@class='pagination']//a")
                        for target in target_list:
                            if target.text == '>':
                                target.click(by_js=True)
                                tab.wait(random_float)
                                indirect_outbound_investment_info = tab.eles(
                                    "xpath=//section[@id='touzilist']//div[@class='app-ntable']/table[@class='ntable']")[1]
                                indirect_outbound_investment_html += indirect_outbound_investment_info.html
                    except:
                        print("存在验证码")
                        get_captcha(page)
                        tab.refresh()
                        input()
                        break
            print("-------------------对外投资(间接)----------------")
            indirect_out = get_table_subject(indirect_outbound_investment_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["对外投资(间接)"] = indirect_out

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\data_one")
co.set_paths(local_port=9136)
random_float = random.uniform(1, 5)
# 连接浏览器
page = ChromiumPage(co)
new_tab = page.get_tab()
# 访问网页
new_tab.get('https://www.qcc.com/firm/6a6a2bdfcfec0102221e27582488b71f.html')   # 金川集团股份有限公司
# get_captcha(page)
# new_tab.wait(2)
# new_tab.refresh()
# new_tab.get('https://www.qcc.com/firm/0572b3d8cbb4ab8e0bc120b1b03ce318.html')   # 安徽天一美达物流科技有限公司
# input(1)
# # 获取公司信息
# get_company_info(new_tab)
# 获取公司股东信息
get_company_shareholder_info(new_tab)
# 获取主要人员
get_company_key_personnel(new_tab)
# 获取对外投资信息
get_company_outbound_investment(new_tab)
print(discovered_subject_dict)

page.quit()
