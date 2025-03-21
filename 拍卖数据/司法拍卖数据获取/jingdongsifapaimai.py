# 京东拍卖
import json
import re
import time
from datetime import datetime, timedelta
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Settings
from fake_useragent import UserAgent
import tempfile
from a_mysql_connection_pool import get_connection
import random
from lxml import etree
# import datetime
import re
from api_paimai import sub_queues_add, judge_repeat, sub_queues_success, paper_queue_success

"""
第一步，通过关键字查询，返回多项数据
"""


def parse_opentime(s):
    # 处理绝对时间格式
    if s.startswith("开拍时间："):
        try:
            dt = datetime.strptime(s, "开拍时间：%Y年%m月%d日 %H:%M:%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

    # 处理剩余时间格式
    elif "距离开拍仅剩：" in s:
        # 正则匹配时、分、秒
        match = re.match(
            r"距离开拍仅剩：(?:(\d+)时)?(\d+)分(\d+)秒",
            s
        )
        if not match:
            return None

        # 提取时间部分（缺失的部分默认为0）
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2))
        seconds = int(match.group(3))

        # 计算开拍时间（当前时间 + 时间差）
        delta = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )
        open_time = datetime.now() + delta

        return open_time.strftime("%Y-%m-%d %H:%M:%S")

    else:
        return None


def remove_styles(tree):
    # 删除 <style> 标签
    for tag in tree.xpath('//style | //link[@rel="stylesheet"]'):
        parent = tag.getparent()
        if parent is not None:
            parent.remove(tag)
    # 删除 <style> 标签
    for tag in tree.xpath('//script'):
        parent = tag.getparent()
        if parent is not None:
            parent.remove(tag)
    # 删除内联样式属性
    for element in tree.xpath('//@style'):
        parent = element.getparent()
        del parent.attrib['style']
    return tree


def by_keyword_search(web_queue_id, webpage_id, webpage_url, keyword):
    co = ChromiumOptions()
    co = co.set_user_data_path(r"D:\chome_data\jingdong")
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True
    # co.set_argument('--disable-blink-features=AutomationControlled')
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
    data_list = []
    for info in info_list:
        title = info.ele("xpath=//div[@class='item-name']").text
        url = info.ele("xpath=/a").attr('href')
        status = info.ele("xpath=//div[@class='item-status']").text
        item_time = info.ele("xpath=//div[@class='item-countdown']").text
        # 需判断这个链接是否在数据库中存在，并返回存在该队列的id
        state_db, id_db = judge_repeat(url)
        if not id_db:
            print(title, url, status, item_time)
            data_add = {
                "name": url,
                "web_queue_id": web_queue_id,
                "webpage_id": webpage_id,
                "webpage_url": webpage_url,
                "sub_type": "detail",
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


def get_detail_info(value_id, url, from_queue):
    co = ChromiumOptions()
    co = co.set_user_data_path(r"D:\chome_data\jingdong")
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True
    # co.set_argument('--disable-blink-features=AutomationControlled')
    co.set_argument('--incognito')
    # co.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')
    # co = co.set_argument('--no-sandbox')
    # co = co.headless()
    co.set_paths(local_port=9212)

    state_sql, id = judge_repeat(url)
    if state_sql:
        # page.quit()
        return
    # 启动浏览器
    page = ChromiumPage(co)
    page.get(url)
    page.wait.doc_loaded()
    for _ in range(4):
        page.scroll.to_bottom()
        time.sleep(2)
    time.sleep(4)
    tree = etree.HTML(page.html)
    page.close()
    # # 执行清理并输出, 测试阶段展示html
    # cleaned_tree = remove_styles(tree)
    # cleaned_html = etree.tostring(cleaned_tree, encoding='unicode', pretty_print=True)
    # print(cleaned_html)
    # return
    title = ''.join(tree.xpath("//div[@class='pm-name']//text()"))
    state = ''.join(tree.xpath("//div[@class='mt']/div[@class='state']//text()")).strip()
    if state == '拍卖结束':
        state = '已结束'
    elif state == '正在进行':
        state = '进行中'
    elif state == '即将开始':
        state = '预告中'
    stage = ''
    address = ''.join(tree.xpath("//div[contains(@class, 'pm-location')]/em/text()"))
    start_bid = ''.join(tree.xpath(
        "//div[@class='list description']//text()"))
    start_bid = ''.join(re.findall(r'起拍价\s*[:：]\s*￥\s*(\d{1,3}(?:,\d{3})*)', start_bid))
    sold_price = ''.join(tree.xpath("//div[@class='mc']/div[@class='price deal']//text()"))
    sold_price = ''.join(re.findall(r'¥(.*)', sold_price))
    outcome = ''.join(tree.xpath("//div[@class='mt']/div[@class='result']/span//text()"))
    end_time = ''
    start_time = ''
    if state == '已结束' or state == '进行中' or state == '已中止':
        end_time = ''.join(tree.xpath("//div[@class='mt']/div[@class='endtime']//text()"))
        end_time = ''.join(re.findall(r'(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2})', end_time))  # 结束时间
        end_time = end_time.replace('年', '-').replace('月', '-').replace('日', '')
    elif state == '预告中':
        distance_end = ''.join(tree.xpath("//div[@class='index_countdown__remainTime__O7MNa']/div//text()"))
        if not distance_end:
            distance_end = ''.join(tree.xpath("//div[@class='index_countdown__time__ArsTv']//text()"))
        start_time = parse_opentime(distance_end)
        # print(start_time)
        # print(distance_end)
        # print(start_time)
    if not start_time:
        start_time = None
    procedure_str = ''  # 拍卖程序
    disposal_unit = ''.join(tree.xpath("//a[@id='disposalUnitTag']/text()"))  # 处置单位
    bidding_status = ''.join(tree.xpath("//table[@class='bidList']/tbody/tr/td[1]//text()"))  # 竞买状态
    bidding_code = ''.join(tree.xpath("//table[@class='bidList']/tbody/tr/td[3]//text()"))  # 竞买人
    bidding_price = ''.join(tree.xpath("//table[@class='bidList']/tbody/tr/td[2]//text()"))  # 竞买价格
    bidding_time = ''.join(tree.xpath("//table[@class='bidList']/tbody/tr/td[4]/text()"))  # 竞买时间
    auction_history = f'竞买状态:{bidding_status} 竞买人:{bidding_code} 竞买价格:{bidding_price} 竞买时间:{bidding_time}'
    people_num = ''.join(tree.xpath("//div[@class='index_auctionstatusbanner__statistics__-mtfv']//text() | //div[@class='endtime']//text()"))  # 竞买人数
    people_num = ''.join(re.findall(r'(\d+)人报名', people_num))
    # subject_info_etree = tree.xpath("//div[@class='paimaiDetailContainer']/div[@class='pm-content']/ul[@class='floors']/li[3]")  # 标的物信息_html
    subject_info_etree = tree.xpath(
        "//div[@class='paimaiDetailContainer']/div[@class='pm-content']/ul[@class='floors']/li[3] | //ul[@class='floors']/li[@class='floor']")  # 标的物信息_html
    subject_info = ''
    for con in subject_info_etree:
        subject_info += etree.tostring(con, encoding='utf-8').decode()
    subject_annex_up_list = tree.xpath("//ul[@class='floors']//@href")  # 标的物信息附件上传
    subject_annex_up = ''
    for annex in subject_annex_up_list:
        if annex.split('.')[-1] not in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                        'png', 'jpg']:
            continue
        if annex == 'http://zichan.jd.com/':
            continue
        if 'http' not in annex:
            annex = 'http:' + annex
        subject_annex_up += annex + ','
    subject_annex_up = subject_annex_up[:-1]
    auction_html_etree = tree.xpath("//div[@class='pm-content']//li[@class='floor index_floor__1u9-C'][1]")  # 拍卖公告_html
    auction_html = ''
    for con in auction_html_etree:
        auction_html += etree.tostring(con, encoding='utf-8').decode()

    value = {
        'url': url,
        'title': title,
        'state': state,
        'stage': stage,
        'address': address,
        'start_bid': start_bid,
        'sold_price': sold_price,
        'outcome': outcome,
        'end_time': end_time,
        'procedure_str': procedure_str,
        'disposal_unit': disposal_unit,
        'auction_history': auction_history,
        'people_num': people_num,
        'subject_info': subject_info,
        'subject_annex_up': subject_annex_up,
        'auction_html': auction_html,
        'start_time': start_time,
    }
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    create_date = datetime.now().strftime('%Y-%m-%d')
    # 上传到数据库
    conn_test = get_connection()
    cursor_test = conn_test.cursor()
    # 上传文件
    insert_sql = "INSERT INTO col_judicial_auctions (url, title, state, stage, address, start_bid, sold_price, outcome, end_time, procedure_str, auction_html, subject_annex_up, subject_info, disposal_unit, auction_history, people_num, subject_annex, create_time, create_date, from_queue, start_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    cursor_test.execute(insert_sql,
                        (url, title, state, stage, address, start_bid, sold_price,
                         outcome,
                         end_time, procedure_str, auction_html, subject_annex_up,
                         subject_info,
                         disposal_unit, auction_history, people_num, subject_annex_up,
                         create_time,
                         create_date, from_queue, start_time))
    id_value = cursor_test.lastrowid
    # 这里放成功的方法
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
    print(value)

# get_detail_info('https://paimai.jd.com/308213221', 1234)
