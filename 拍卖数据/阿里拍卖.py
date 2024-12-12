import random
import re
from datetime import datetime, timedelta
import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from urllib.parse import urlencode, urljoin

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\ali_one")
# co = co.set_argument('--no-sandbox')
# co = co.headless()
co.set_paths(local_port=9153)


def encounter_verify(tab):
    # 随机0.15到1之间的数
    num = random.uniform(0.15, 1)
    if "亲，请拖动下方滑块完成验证" in tab.html:
        tab.wait(2)
        slider_loc = tab.ele("xpath=//span[@id='nc_1_n1z']")
        print(slider_loc.rect.location)
        tab.actions.hold(slider_loc).move_to((1000, 504), duration=num).release()
        tab.wait(2)
        if "验证失败" in tab.html:
            tab.ele("验证失败").click(by_js=None)
            if "验证失败" in tab.html:
                tab.ele("验证失败").click(by_js=None)
            if "请按住滑块" in tab.html:
                tab.refresh()
                encounter_verify(tab)
    return tab


def time_str_to_date(time_str, add=True):
    # 分割字符串并提取天数、小时、分钟和秒
    days = int(time_str.split('天')[0])
    hours = int(time_str.split('天')[1].split('时')[0])
    minutes = int(time_str.split('时')[1].split('分')[0])
    seconds = float(time_str.split('分')[1].split('秒')[0])

    # 将天数转换为小时，并与小时数相加
    total_hours = days * 24 + hours
    base_time = datetime.now()
    # 将总小时数、分钟数和秒数转换为timedelta对象并加到基础时间点上
    time_delta = timedelta(hours=total_hours, minutes=minutes, seconds=seconds)
    if add:
        result_time = base_time + time_delta
    else:
        result_time = base_time - time_delta

    return str(result_time)


data_dict = {}
data_list = []
page = ChromiumPage(co)
tab_1 = page.new_tab()
page_num = 0
while True:
# for i in range(3):
    page_num += 1
    print(f"第{page_num}页")
    status_orders = 2
    url = "https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch"
    params = {
        "disableNav": "YES",
        "page": f"{page_num}",
        "pmid": "2175852518_1653962822378",
        "pmtk": "20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879",
        "path": "27181431,27076131,25287064,27064540",
        "spm": "a2129.27064540.puimod-zc-focus-2021_2860107850.category-4-5",
        "fcatV4Ids": "[\"206067301\"]",
        "statusOrders": f"[\"{status_orders}\"]"  # 0:正在进行中, 1:即将拍卖, 2:已结束, 6:招商中
    }
    # 将参数字典转换为URL编码的字符串
    query_string = urlencode(params)
    # 将查询字符串附加到基础URL后面
    full_url = urljoin(url, '?' + query_string)
    tab_1.get(full_url)
    tab_1.wait(2)
    info_list = tab_1.eles("xpath=//div[@id='guid-2004318340']//div/a")
    if not info_list:
        break
    count = 0
    for info in info_list:
        href_text = info.text
        if "同类商品" not in href_text:
            href_url = info.attr("href")
            tab_2 = page.new_tab()
            tab_2.get(href_url)
            data_dict["链接"] = href_url
            # tab_2.get("https://zc-item.taobao.com/auction/858628010713.htm?spm=a2129.27076131.puimod-pc-search-list_2004318340.11&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431%2C27076131&track_id=7c0d2dea-2697-4448-bca9-474a89c6a04f")
            tab_2.wait(2)
            tab_2 = encounter_verify(tab_2)
            tab_2.wait(2)
            title = tab_2.ele("xpath=//div[@id='page']//h1")  # 标题
            if title:
                title = title.text  # 标题
                data_dict["标题"] = title
            state = tab_2.ele("xpath=//div[@id='page']//h1/span[@class='item-status']")  # 状态
            if state:
                state = state.text  # 状态
                data_dict["状态"] = state
            location = tab_2.ele("xpath=//div[@id='itemAddress']")  # 所在地
            if location:
                location = location.text  # 所在地
                data_dict["所在地"] = location
            sf_price = tab_2.ele("xpath=//span[@class='family-tahoma']", index=2)  # 起拍价
            if sf_price:
                sf_price = sf_price.text  # 起拍价
                data_dict["起拍价"] = sf_price + "元"
            if status_orders == 2:
                auction_results = tab_2.ele("xpath=//h1[@class='bid-fail'] | //h1[@class='bid-fail']/following-sibling::p")  # 拍卖结果
                if auction_results:
                    auction_results = auction_results.text  # 拍卖结果
                    data_dict["拍卖结果"] = auction_results
                    print("拍卖结果:", auction_results)
            about_time = tab_2.ele("xpath=//li[@id='sf-countdown']")  # 关于时间
            if about_time:
                about_time = about_time.text  # 关于时间
                if "距结束" in about_time:
                    about_time = about_time.replace("距结束", "")
                    time_data = ''.join(re.findall(r'(.*?)\d+次延时', about_time))
                    data_dict["结束时间"] = time_str_to_date(time_data, add=True)
                if "距开始" in about_time:
                    about_time = about_time.replace("距开始", "")
                    data_dict["开始时间"] = time_str_to_date(about_time, add=False)
            end_time = tab_2.ele("xpath=//ul[@class='pm-bid-eyebrow']/li[1]")  # 结束时间
            if end_time:
                end_time = end_time.text  # 结束时间
                if "结束时间" in end_time:
                    data_dict["结束时间"] = re.findall(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', end_time)[0]
            procedure = tab_2.ele("xpath=//div[@id='J_COMPONENT_MAIN_BOTTOM']")  # 获取程序
            if procedure:
                procedure = procedure.text  # 获取程序
                procedure = re.sub(r'\n', '', procedure)
                procedure = re.sub(r'\t', '', procedure)
                # print(procedure)
                procedure = ''.join(re.findall(r"程序(.*?)延时", procedure))  # 获取程序
                procedure = procedure.replace(":", "")
                data_dict["程序"] = procedure
            about_price = tab_2.ele("xpath=//li[@id='sf-price']")  # 关于价格
            if about_price:
                about_price = about_price.text  # 关于价格
                if "当前价" in about_price:
                    about_price = about_price.replace("当前价", "")
                    now_price = "".join(re.findall(r"\d+", about_price))
                    now_price = str(now_price) + about_price[-1]
                    data_dict["当前价"] = now_price
                if "拍下价" in about_price:
                    about_price = about_price.replace("拍下价", "")
                    now_price = "".join(re.findall(r"\d+", about_price))
                    now_price = str(now_price) + about_price[-1]
                    data_dict["成交价"] = now_price
                # data_dict["关于价格"] = about_price
            disposal_unit = tab_2.ele("xpath=//p[@class='org-name']")  # 处置单位
            if disposal_unit:
                disposal_unit = disposal_unit.text  # 处置单位
                data_dict["处置单位"] = disposal_unit
            bidding_num = tab_2.ele("xpath=//ul[@id='J_DetailTabMenu']/li[4]")  # 竞买次数
            if "竞买记录" not in bidding_num.text:
                bidding_num = tab_2.ele("xpath=//ul[@id='J_DetailTabMenu']/li[5]")  # 竞买次数
            if bidding_num:
                bidding_num = bidding_num.text  # 竞买次数
                bidding_num = re.sub(r'\n', '', bidding_num)
                bidd_num = ''.join(re.findall(r'\d+', bidding_num))
                bidd_click_num = int(bidd_num) / 20
                bidding_html = ""
                if bidd_num:
                    bidding_records = tab_2.ele("xpath=//div[@id='J_RecordContent']")  # 获取竞价记录
                    if bidding_records:
                        bidding_records = bidding_records.html  # 竞价记录,html信息
                        bidding_html += bidding_records
                    for _ in range(int(bidd_click_num)):
                        next_page = tab_2.ele("xpath=//ul[@id='J_PageContent']/li[2]/a[@class='pagebutton']")
                        next_page.click(by_js=True)
                        tab_2.wait(2)
                        tab_2 = encounter_verify(tab_2)
                        tab_2.wait(2)
                        bidding_records = tab_2.ele("xpath=//div[@id='J_RecordContent']")  # 获取竞价记录
                        if bidding_records:
                            bidding_records = bidding_records.html  # 竞价记录,html信息
                            bidding_html += bidding_records
                etree_html = etree.HTML(bidding_html)
                bidding_records = etree_html.xpath("//table[@id='J_RecordList']//div[@class='nickname']")
                bidd_set = set()
                for value in bidding_records:
                    bidd_set.add(value.text)
                bidding_stat = ''.join(etree_html.xpath("//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[1]//text()"))
                bidding_number = ''.join(etree_html.xpath("//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[2]//text()"))
                bidding_price = ''.join(etree_html.xpath("//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[3]//text()")) + "元"
                bidding_time = ''.join(etree_html.xpath("//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[4]//text()"))
                str_bidding = "竞买状态:" + bidding_stat + " 竞买号:" + bidding_number + " 竞买价:" + bidding_price + " 竞买时间:" + bidding_time + " 竞买人数:" + str(len(bidd_set))
                data_dict["竞价记录"] = str_bidding
            else:
                str_bidding = "竞买次数:0"
                data_dict["竞价记录"] = str_bidding
            number_applicants = tab_2.ele("xpath=//div[@id='J_COMPONENT_MAIN_BOTTOM']/div[2]")
            if number_applicants:
                number_applicants = number_applicants.text  # 竞买人数
                number_applicants = re.sub(r'\n', '', number_applicants)
                number_applicants = ''.join(re.findall(r'(\d+)人报名', number_applicants))
                data_dict["报名人数"] = number_applicants
                # print("报名人数:" + number_applicants)

            target_info = tab_2.ele("xpath=//div[@id='J_ItemDetailContent']")  # 标的信息
            if target_info:
                target_annex = ''
                target_html = target_info.html  # 标的信息,html信息
                data_dict["标的信息"] = target_html
                # print(target_html)
                target_ann = etree.HTML(target_html)
                target_info = target_ann.xpath("//@src | //@href")
                for value in target_info:
                    target_annex += "https:" + value + ","
                data_dict["标的信息附件"] = target_annex
            target_ann = tab_2.ele("xpath=//div[@id='page']//a[@class='unit-txt view-ano']").attr("href")  # 拍卖公告
            tab_3 = page.new_tab()
            tab_3.get(target_ann)
            tab_3.wait(2)
            tab_3 = encounter_verify(tab_3)
            tab_3.wait(2)
            target_ann = tab_3.ele("xpath=//div[@class='notice-detail']/table")  # 拍卖公告
            if target_ann:
                target_ann = target_ann.html  # 拍卖公告,html信息
                data_dict["拍卖公告"] = target_ann
            tab_3.close()
            data_list.append(data_dict.copy())
            print(data_dict)
            data_dict.clear()
            tab_2.close()
        # count += 1
        # if count == 10:
        #     break
        # break

tab_1.close()


# 将数据转换为DataFrame
df = pd.DataFrame(data_list)
# 将DataFrame写入Excel文件
excel_path = '结果.xlsx'  # 你想要保存的Excel文件路径
df.to_excel(excel_path, index=False)  # index=False表示不将行索引写入Excel文件

print(f'数据已写入{excel_path}')
page.quit()
