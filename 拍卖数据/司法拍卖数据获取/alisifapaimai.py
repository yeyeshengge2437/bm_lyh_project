import json
import random
import re
import time
from datetime import datetime, timedelta
import mysql.connector
from DrissionPage.common import Settings
import tempfile
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from api_paimai import sub_queues_add, judge_repeat, sub_queues_success, paper_queue_success
from a_mysql_connection_pool import get_connection

status_mapping = {
    "todo": "待开始",
    "doing": "进行中",
    "delay": "延时",
    "done": "已结束",
    "success": "成交",
    "failure": "流拍",
    "break": "中止",
    "revocation": "撤回"
}


def timestamp_to_datetime(timestamp):
    """
    将时间戳转换为 xxxx-xx-xx xx:xx 格式的日期时间字符串
    :param timestamp: 时间戳（秒级或毫秒级）
    :return: 格式化后的日期时间字符串
    """
    # 如果时间戳是毫秒级，转换为秒级
    if len(str(timestamp)) > 10:
        timestamp = timestamp / 1000
    # 使用 time.strftime 格式化时间
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))


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


def encounter_verify(tab):
    count = 0
    while True:
        count += 1
        if count > 1800:
            tab.refresh()
        if '验证码拦截' in tab.html:
            print("遇到验证码")
            tab.set.window.max()
            time.sleep(2)
        else:
            tab.set.window.mini()
            return tab


def by_keyword_search_ali(web_queue_id, webpage_id, webpage_url, keyword):
    co = ChromiumOptions()
    co.set_argument('--incognito')
    co.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')
    # co = co.set_user_data_path(r"D:\chome_data\jingdong")
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True
    # co.set_argument('--disable-blink-features=AutomationControlled')
    # co.set_argument('--incognito')
    # co.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')
    # co = co.set_argument('--no-sandbox')
    # co = co.headless()
    co.set_paths(local_port=9233)

    page = ChromiumPage(co)
    page.get(f'https://sf.taobao.com/item_list.htm?_input_charset=utf-8&q={keyword}')
    page.wait.doc_loaded()
    time.sleep(4)
    search_tab = page.latest_tab
    search_tab.wait.doc_loaded()
    time.sleep(4)
    # target = etree.HTML(search_tab.html)
    # print(search_tab.html)
    search_json_str = re.findall(r'<script id="sf-item-list-data" type="text/json">(.*?)</script>', search_tab.html,
                                 re.DOTALL)
    if search_json_str:
        search_json = search_json_str[0]
        search_json = json.loads(search_json)
        data_list = []
        for search_item in search_json['data']:
            url_str = 'https:' + ''.join(search_item['itemUrl'])
            url = re.sub(r'\?.*', '', url_str)
            title = ''.join(search_item['title'])
            state_en = ''.join(search_item['status'])
            state = status_mapping.get(state_en, '未知')  # 拍卖状态
            state_bid = search_item.get('initialPrice')  # 起拍价
            sold_price = search_item.get("currentPrice")  # 成交价
            start_time_unix = search_item.get('start')
            start_time = timestamp_to_datetime(start_time_unix)  # 开始时间
            end_time_unix = search_item.get('end')
            end_time = timestamp_to_datetime(end_time_unix)  # 结束时间
            people_num = search_item.get('applyCount')  # 报名人数
            value_dict = {
                'url': url,
                'title': title,
                'state': state,
                'state_bid': state_bid,
                'sold_price': sold_price,
                'start_time': start_time,
                'end_time': end_time,
                'people_num': people_num,
            }
            value_str = json.dumps(value_dict)
            state_db, id_db = judge_repeat(url)
            if not id_db:
                data_add = {
                    "name": url,
                    "web_queue_id": web_queue_id,
                    "webpage_id": webpage_id,
                    "webpage_url": webpage_url,
                    "sub_type": "detail",
                    "remark": value_str,
                }
                sub_queues_add(data_add)
            else:
                value_data = {
                    "data_id": id_db,
                    "data_table": "col_judicial_auctions"
                }
                data_list.append(value_data)
        page.quit()
        if data_list:
            return data_list
        return None


def get_detail_info_ali(value_id, url, from_queue, remark):
    co = ChromiumOptions()
    # co.set_argument('--incognito')
    co.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')
    co = co.set_user_data_path(r"D:\chome_data\ali_one")
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True
    co.set_paths(local_port=9233)
    state_sql, id_sql = judge_repeat(url)
    flag = True
    if state_sql:
        flag = False
    page = ChromiumPage(co)
    data_dict = {}
    tab_2 = page.new_tab()
    tab_2.get(url)
    remark_json = json.loads(remark)
    state = remark_json.get("state")
    state_bid = remark_json.get("state_bid")
    sold_price = remark_json.get("sold_price")
    start_time = remark_json.get("start_time")
    end_time = remark_json.get("end_time")
    people_num = remark_json.get("people_num")

    data_dict["链接"] = url
    # tab_2.get("https://zc-item.taobao.com/auction/858628010713.htm?spm=a2129.27076131.puimod-pc-search-list_2004318340.11&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431%2C27076131&track_id=7c0d2dea-2697-4448-bca9-474a89c6a04f")
    tab_2.wait(2)
    tab_2 = encounter_verify(tab_2)
    tab_2.wait(2)
    title = tab_2.ele("xpath=//div[@id='page']//h1")  # 标题
    if title:
        title = title.text  # 标题
        data_dict["标题"] = title
    else:
        tab_2.close()
        return  # 跳过没有标题的 ---------------------------------------------------------

    location = tab_2.ele("xpath=//div[@id='itemAddress']")  # 所在地
    if location:
        location = location.text  # 所在地
        data_dict["所在地"] = location
    if state_sql:
        auction_results = tab_2.ele(
            "xpath=//h1[@class='bid-fail'] | //h1[@class='bid-fail']/following-sibling::p")  # 拍卖结果
        if auction_results:
            auction_results = auction_results.text  # 拍卖结果
            data_dict["拍卖结果"] = auction_results
            print("拍卖结果:", auction_results)

    procedure = tab_2.ele("xpath=//div[@id='J_COMPONENT_MAIN_BOTTOM']")  # 获取程序
    if procedure:
        procedure = procedure.text  # 获取程序
        procedure = re.sub(r'\n', '', procedure)
        procedure = re.sub(r'\t', '', procedure)
        # print(procedure)
        procedure = ''.join(re.findall(r"程序(.*?)延时", procedure))  # 获取程序
        procedure = procedure.replace(":", "")
        if procedure:
            data_dict["程序"] = procedure

    disposal_unit = tab_2.ele("xpath=//p[@class='org-name']")  # 处置单位
    if disposal_unit:
        disposal_unit = disposal_unit.text  # 处置单位
        data_dict["处置单位"] = disposal_unit
    bidding_num = tab_2.ele("xpath=//ul[@id='J_DetailTabMenu']/li[4]")  # 竞买次数
    if bidding_num:
        if "竞买记录" not in bidding_num.text:
            if "应买记录" not in bidding_num.text:
                bidding_num = tab_2.ele("xpath=//ul[@id='J_DetailTabMenu']/li[5]")  # 竞买次数
    if bidding_num:
        bidding_num = bidding_num.text  # 竞买次数
        bidding_num = re.sub(r'\n', '', bidding_num)
        bidd_num = ''.join(re.findall(r'\d+', bidding_num))
        bidding_html = ""
        if bidd_num:
            bidd_click_num = int(bidd_num) / 20
            bidding_records = tab_2.ele("xpath=//div[@id='J_RecordContent']")  # 获取竞价记录
            if bidding_records:
                bidding_records = bidding_records.html  # 竞价记录,html信息
                bidding_html += bidding_records
            for _ in range(int(bidd_click_num)):
                next_page = tab_2.ele(
                    "xpath=//ul[@id='J_PageContent']/li[2]/a[@class='pagebutton']")
                next_page.click(by_js=True)
                tab_2.wait(2)
                tab_2 = encounter_verify(tab_2)
                tab_2.wait(2)
                bidding_records = tab_2.ele("xpath=//div[@id='J_RecordContent']")  # 获取竞价记录
                if bidding_records:
                    bidding_records = bidding_records.html  # 竞价记录,html信息
                    bidding_html += bidding_records
        etree_html = etree.HTML(bidding_html)
        if etree_html:
            bidding_records = etree_html.xpath(
                "//table[@id='J_RecordList']//div[@class='nickname']")
            bidd_set = set()
            for value in bidding_records:
                bidd_set.add(value.text)
            bidding_stat = ''.join(etree_html.xpath(
                "//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[1]//text()"))
            bidding_number = ''.join(etree_html.xpath(
                "//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[2]//text()"))
            bidding_price = ''.join(etree_html.xpath(
                "//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[3]//text()")) + "元"
            bidding_time = ''.join(etree_html.xpath(
                "//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[4]//text()"))
            str_bidding = "竞买状态:" + bidding_stat + " 竞买号:" + bidding_number + " 竞买价:" + bidding_price + " 竞买时间:" + bidding_time + " 竞买人数:" + str(
                len(bidd_set))
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
            if "https" not in value[0:5]:
                annex_url = "https:" + value + ","
            else:
                annex_url = value + ","
            target_annex += annex_url
        data_dict["标的信息附件"] = target_annex
    target_ann = tab_2.ele("xpath=//div[@id='page']//a[@class='unit-txt view-ano']")
    if target_ann:  # 拍卖公告
        target_ann_href = target_ann.attr("href")
        tab_3 = page.new_tab()
        tab_3.get(target_ann_href)
        tab_3.wait(2)
        tab_3 = encounter_verify(tab_3)
        tab_3.wait(2)
        target_ann = tab_3.ele("xpath=//div[@class='notice-detail']/table")  # 拍卖公告
        if target_ann:
            target_ann = target_ann.html  # 拍卖公告,html信息
            target_ann = str(target_ann)
            target_ann = re.sub(r"\n", '', target_ann)
            target_ann = re.sub(r" ", '', target_ann)
            data_dict["拍卖公告"] = target_ann
        tab_3.close()
    tab_2.close()
    if data_dict:
        url = data_dict.get("链接")
        start_time = start_time
        title = data_dict.get("标题")
        state = state
        stage = data_dict.get("阶段")
        address = data_dict.get("所在地")
        start_bid = state_bid
        sold_price = sold_price
        outcome = data_dict.get("拍卖结果")
        end_time = end_time
        procedure_str = data_dict.get("程序")
        disposal_unit = data_dict.get("处置单位")
        auction_history = data_dict.get("竞价记录")
        people_num = people_num
        subject_info = data_dict.get("标的信息")
        subject_annex = data_dict.get("标的信息附件")
        subject_annex_up = subject_annex
        auction_html = data_dict.get("拍卖公告")
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        create_date = datetime.now().strftime('%Y-%m-%d')
        print(procedure_str)
        # 上传到测试数据库
        conn_test = get_connection()

        cursor_test = conn_test.cursor()
        if flag:
            # 上传文件
            insert_sql = "INSERT INTO col_judicial_auctions (url, start_time, title, state, stage, address, start_bid, sold_price, outcome, end_time, procedure_str, auction_html, subject_annex_up, subject_info, disposal_unit, auction_history, people_num, subject_annex, update_time, from_queue, create_time, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # 22个占位符

            cursor_test.execute(insert_sql,
                                (url, start_time, title, state, stage, address, start_bid, sold_price,
                                 outcome,
                                 end_time,
                                 procedure_str, auction_html, subject_annex_up, subject_info,
                                 disposal_unit,
                                 auction_history, people_num, subject_annex, update_time,
                                 from_queue, create_time, create_date))  # 注意这里去掉了最后的id参数
            conn_test.commit()
            id_value = cursor_test.lastrowid
            # 成功的方法
            data_success = {
                'id': value_id,  # 子队列id
                'data_list': [{
                    'data_id': id_value,
                    'data_table': 'col_judicial_auctions',
                }]
            }
            sub_queues_success(data_success)
        else:
            # 更新操作
            # 上传文件
            update_sql = "UPDATE col_judicial_auctions SET url = %s, start_time = %s, title = %s, state = %s, stage = %s, address = %s, start_bid = %s, sold_price = %s, outcome = %s, end_time = %s, procedure_str = %s, auction_html = %s, subject_annex_up = %s, subject_info = %s, disposal_unit = %s, auction_history = %s, people_num = %s, subject_annex = %s, update_time = %s, from_queue = %s, create_time = %s, create_date = %s WHERE id = %s;"
            cursor_test.execute(update_sql,
                                (url, start_time, title, state, stage, address, start_bid, sold_price,
                                 outcome,
                                 end_time,
                                 procedure_str, auction_html, subject_annex_up, subject_info,
                                 disposal_unit,
                                 auction_history, people_num, subject_annex, update_time,
                                 from_queue, create_time, create_date,
                                 id_sql))
            id_value = id_sql
            # 成功的方法
            data_success = {
                'id': value_id,  # 子队列id
                'data_list': [{
                    'data_id': id_value,
                    'data_table': 'col_judicial_auctions',
                }]
            }
            sub_queues_success(data_success)
            conn_test.commit()
        cursor_test.close()
        conn_test.close()

        print(data_dict)
    page.quit()


# page.quit()

# get_detail_info_ali(123, '已成交', 'https://sf-item.taobao.com/sf_item/885727158030.htm', 345, '{}')
# by_keyword_search(1, 1, 'https://pmsearch.jd.com/', '（2024）苏1081执恢412号')
