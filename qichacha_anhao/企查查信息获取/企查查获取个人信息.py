import json
import random
import re
from 验证码识别 import get_captcha
import requests
import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
discovered_subject_dict = {}
pl_dict = {'https://www.qcc.com/pl/p67ef1577cd9222739c209094dfe70b6.html', 'https://www.qcc.com/pl/p7d4434c1293f33cf75bb8ccaa6e3a36.html', 'https://www.qcc.com/pl/p9f4d60a65222f170ed78765d302adca.html', 'https://www.qcc.com/pl/pbf19463b4cbf3d5b5ce750768405e2a.html', 'https://www.qcc.com/pl/pfe2c84b2c2d9f12ee59d8ea50e0451d.html', 'https://www.qcc.com/pl/p3a7b1edc76894d1fe1869f7b1b5585d.html', 'https://www.qcc.com/pl/p40ee7bf6d8961ce644f35e590bbeece.html', 'https://www.qcc.com/pl/p17aa3a46341d0acd0d8069fbce5bfc2.html', 'https://www.qcc.com/pl/p164021215e1567bdd7768cc9aac0090.html', 'https://www.qcc.com/pl/pa10c8cf419f13cb71a9d15d095e6602.html', 'https://www.qcc.com/pl/p2d681eb500fef458e7e9d6f5b658d76.html', 'https://www.qcc.com/pl/pr67c6ea2e1fec216c0ed3fdb5e04a45.html', 'https://www.qcc.com/pl/p6327e0d4c73aab4d529f91fb5a5a15d.html', 'https://www.qcc.com/pl/p6951d4f4805e11172464993dc99974d.html', 'https://www.qcc.com/pl/pr03667bf2438bd84b651b35d4ccc8e5.html', 'https://www.qcc.com/pl/pf17f321d1199af3c20fc46d016758de.html', 'https://www.qcc.com/pl/pr7681b697a0fda904e07e6920f7be28.html', 'https://www.qcc.com/pl/p9a1b9798f801a3d5dfd33bf6f498c71.html', 'https://www.qcc.com/pl/p553a056c60ae16a55af87c57ae0cc01.html', 'https://www.qcc.com/pl/pb0491727af65da5d7578fee8547c57a.html', 'https://www.qcc.com/pl/pr3faacc8ff3278436b66d061738cce3.html', 'https://www.qcc.com/pl/pr9c39c05593c2f981ab0552d53f9ece.html', 'https://www.qcc.com/pl/pr519cb05fce39edc2657431078722ea.html', 'https://www.qcc.com/pl/p93c9d4cde630e10a883f268488dacd4.html', 'https://www.qcc.com/pl/pr4626e4722d2496aef5bd3cee67da71.html', 'https://www.qcc.com/pl/p8040df93d2e1b3d28ffc39176a1ab42.html', 'https://www.qcc.com/pl/p76e3bc3c68ea5af6e61f18de66ff6a5.html', 'https://www.qcc.com/pl/pc2ebfdea808c30057fa4a1f67a07880.html', 'https://www.qcc.com/pl/pfb3abc94a334f6e1a11e5faa550e889.html', 'https://www.qcc.com/pl/prf48615c6d1d22366651ce7483dcc1e.html', 'https://www.qcc.com/pl/pr9fb5fb6c3474a05adbaaff0eceefe2.html', 'https://www.qcc.com/pl/p7f928c964a6dcff655f68d485403e1c.html', 'https://www.qcc.com/pl/pefbcdbe5fd5b7bf64800c5d38b9d5d7.html', 'https://www.qcc.com/pl/p331e73852d603c2f9c67cf9bf8947d4.html', 'https://www.qcc.com/pl/p722092b27acc69b91a5a547697dea44.html', 'https://www.qcc.com/pl/pr212d365c09638ba0e33b668d809401.html', 'https://www.qcc.com/pl/pb6255c07cd89ef2aa2f3c41e9d96ef7.html', 'https://www.qcc.com/pl/p0b5b6833b7a55e70e5807929aecbe7b.html', 'https://www.qcc.com/pl/pdfe0140580001a71b1f350164c9b5f9.html', 'https://www.qcc.com/pl/p82f2e9e0808a50c26c1cc57fcadb97c.html', 'https://www.qcc.com/pl/prdb60823135be780c99089f68472f27.html'}
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
def get_outbound_investment_info(tab):
    try:
        outbound_investment_info_list = tab.eles(
            "xpath=//section[@id='investlist']/div[@class='tablist']//span[@class='tab-item']")
        tab.scroll.to_see(outbound_investment_info_list[0])
    except:
        outbound_investment_info_list = tab.eles(
            "xpath=//section[@id='investlist']/div[@class='tablist']//span[@class='tab-item']")
        tab.scroll.to_see(outbound_investment_info_list[0])
    for outbound_investment in outbound_investment_info_list:  # 对外投资列表
        print(str(outbound_investment.text))
        if "对外投资" in outbound_investment.text and "历史对外投资" not in outbound_investment.text and "对外投资(间接)" not in outbound_investment.text:
            num = int("".join(re.findall(r'\d+', outbound_investment.text)))
            if num > 10:
                input("对外投资大于10条，请查看是否有翻页按钮")
            outbound_ = outbound_investment.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            latest_ann = tab.ele(
                "xpath=//section[@id='investlist']//table[@class='ntable']")
            latest_ann_html = latest_ann.html
            print("-------------------对外投资----------------")
            # print(latest_ann_html)
            info_list = get_table_subject(latest_ann_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["对外投资"] = info_list

        elif "历史对外投资" not in outbound_investment.text and "对外投资(间接)" in outbound_investment.text:
            num = int("".join(re.findall(r'\d+', outbound_investment.text)))
            if num > 10:
                input("对外投资(间接)大于10条，请查看是否有翻页按钮")
            outbound_ = outbound_investment.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            input("这里的xpath还未更改")
            tab.wait(random_float)
            shareholder = tab.ele(
                "xpath=//section[@id='partner']/div[@class='tablist tablist-cpartner']//table[@class='ntable']")
            shareholder_html = shareholder.html
            print("-------------------对外投资(间接)----------------")
            shareholder_info_ = get_table_subject(shareholder_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["对外投资(间接)"] = shareholder_info_
            pass  # 最新公示和股东信息都可能在第一个表首页。
        elif "历史对外投资" in outbound_investment.text and "对外投资(间接)" not in outbound_investment.text:
            num = int("".join(re.findall(r'\d+', outbound_investment.text)))
            if num > 10:
                input("历史对外投资大于10条，请查看是否有翻页按钮")
            outbound_ = outbound_investment.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            business_info = tab.ele(
                "xpath=//section[@id='investlist']/div[@class='tablist'][2]//table[@class='ntable']")
            business_info_html = business_info.html
            print("-------------------历史对外投资----------------")
            bus_info = get_table_subject(business_info_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["历史对外投资"] = bus_info
            pass
        else:
            print(f"未知对外投资信息:{outbound_investment.text}")

def get_outbound_appointment_info(tab):
    try:
        outbound_appointment_list = tab.eles(
            "xpath=//section[@id='postofficelist']/div[@class='tablist']//span[@class='tab-item']")
        tab.scroll.to_see(outbound_appointment_list[0])
    except:
        outbound_appointment_list = tab.eles(
            "xpath=//section[@id='postofficelist']/div[@class='tablist']//span[@class='tab-item']")
        tab.scroll.to_see(outbound_appointment_list[0])
    for outbound_appointment in outbound_appointment_list:  # 对外投资列表
        print(str(outbound_appointment.text))
        if "在外任职" in outbound_appointment.text and "历史在外任职" not in outbound_appointment.text:
            num = int("".join(re.findall(r'\d+', outbound_appointment.text)))
            if num > 10:
                input("在外任职大于10条，请查看是否有翻页按钮")
            outbound_ = outbound_appointment.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            latest_ann = tab.ele(
                "xpath=//section[@id='postofficelist']//table[@class='ntable']")
            latest_ann_html = latest_ann.html
            print("-------------------在外任职----------------")
            # print(latest_ann_html)
            info_list = get_table_subject(latest_ann_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["在外任职"] = info_list

        elif "历史在外任职" in outbound_appointment.text:
            num = int("".join(re.findall(r'\d+', outbound_appointment.text)))
            if num > 10:
                input("历史在外任职大于10条，请查看是否有翻页按钮")
            outbound_ = outbound_appointment.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            shareholder = tab.ele(
                "xpath=//section[@id='postofficelist']/div[@class='tablist'][2]//table[@class='ntable']")
            shareholder_html = shareholder.html
            print("-------------------历史在外任职----------------")
            shareholder_info_ = get_table_subject(shareholder_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["历史在外任职"] = shareholder_info_
            pass  # 最新公示和股东信息都可能在第一个表首页。
        else:
            print(f"未知任职信息:{outbound_appointment.text}")

def get_partners_info(tab):
    try:
        partners_list = tab.eles(
            "xpath=//section[@id='partnerlist']/div[@class='tcaption'][2]//span[@class='tab-item']")
        tab.scroll.to_see(partners_list[0])
    except:
        partners_list = tab.eles(
            "xpath=//section[@id='partnerlist']/div[@class='tablist']//span[@class='tab-item']")
        tab.scroll.to_see(partners_list[0])
    for partners in partners_list:
        print(str(partners.text))
        if "合作伙伴" in partners.text and "历史合作伙伴" not in partners.text:
            num = int("".join(re.findall(r'\d+', partners.text)))
            if num > 10:
                input("合作伙伴大于10条，请查看是否有翻页按钮")
            outbound_ = partners.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            latest_ann = tab.ele(
                "xpath=//section[@id='partnerlist']//table[@class='ntable']")
            latest_ann_html = latest_ann.html
            print("-------------------合作伙伴----------------")
            # print(latest_ann_html)
            info_list = get_table_subject(latest_ann_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["合作伙伴"] = info_list

        elif "历史合作伙伴" in partners.text:
            num = int("".join(re.findall(r'\d+', partners.text)))
            if num > 10:
                input("历史合作伙伴大于10条，请查看是否有翻页按钮")
            outbound_ = partners.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            shareholder = tab.ele(
                "xpath=//section[@id='partnerlist']/div[@class='his-partner-list']//table[@class='ntable']")
            shareholder_html = shareholder.html
            print("-------------------历史合作伙伴----------------")
            shareholder_info_ = get_table_subject(shareholder_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["历史合作伙伴"] = shareholder_info_
            pass  # 最新公示和股东信息都可能在第一个表首页。
        else:
            print(f"未知合作伙伴信息:{partners.text}")

def get_affiliates_info(tab):
    try:
        affiliates_list = tab.eles(
            "xpath=//section[@id='allcompanylist']/div[@class='tablist']//span[@class='tab-item']")
        tab.scroll.to_see(affiliates_list[0])
    except:
        affiliates_list = tab.eles(
            "xpath=//section[@id='allcompanylist']/div[@class='tablist']//span[@class='tab-item']")
        tab.scroll.to_see(affiliates_list[0])
    for affiliates in affiliates_list:
        print(str(affiliates.text))
        if "全部关联企业" in affiliates.text and "历史全部关联企业" not in affiliates.text:
            num = int("".join(re.findall(r'\d+', affiliates.text)))
            if num > 10:
                input("全部关联企业大于10条，请查看是否有翻页按钮")
            outbound_ = affiliates.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            latest_ann = tab.ele(
                "xpath=//section[@id='allcompanylist']//table[@class='ntable']")
            latest_ann_html = latest_ann.html
            print("-------------------全部关联企业----------------")
            # print(latest_ann_html)
            info_list = get_table_subject(latest_ann_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["全部关联企业"] = info_list

        elif "历史全部关联企业" in affiliates.text:
            num = int("".join(re.findall(r'\d+', affiliates.text)))
            if num > 10:
                input("历史全部关联企业大于10条，请查看是否有翻页按钮")
            outbound_ = affiliates.ele("xpath=//a")
            if not outbound_:
                continue
            outbound_.click(by_js=True)
            tab.wait(random_float)
            all_html = ''
            shareholder = tab.ele(
                "xpath=//section[@id='allcompanylist']/div[@class='tablist'][2]//table[@class='ntable']")
            all_html += shareholder.html
            if num > 10:
                frequency = int(num / 10)
                print(frequency)
                for _ in range(frequency):
                    target_list = tab.eles("xpath=//section[@id='partnerlist']/div[@class='his-partner-list']//ul[@class='pagination']//a")
                    if target_list[-1].text == '>':
                        target_list[-1].click(by_js=True)
                        tab.wait(random_float)
                        outbound_investment_info = tab.ele(
                            "xpath=//section[@id='allcompanylist']/div[@class='tablist'][2]//table[@class='ntable']")
                        all_html += outbound_investment_info.html
            print("-------------------历史全部关联企业----------------")
            shareholder_info_ = get_table_subject(all_html, xpath_loc="//span[@class='upside-line']//a", xpath_href="./@href", xpath_text=".//text()")
            discovered_subject_dict["历史全部关联企业"] = shareholder_info_
            pass  # 最新公示和股东信息都可能在第一个表首页。
        else:
            print(f"未知关联企业信息:{affiliates.text}")
co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\data_one")
co.set_paths(local_port=9136)
random_float = random.uniform(1, 5)
# 连接浏览器
page = ChromiumPage(co)
new_tab = page.get_tab()
# 访问网页
new_tab.get('https://www.qcc.com/pl/p67ef1577cd9222739c209094dfe70b6.html')
get_outbound_investment_info(new_tab)   # 对外投资
get_outbound_appointment_info(new_tab)  # 对外任职
get_affiliates_info(new_tab)          # 全部关联企业
get_partners_info(new_tab)         # 合作伙伴
print(discovered_subject_dict)
input()
page.quit()
