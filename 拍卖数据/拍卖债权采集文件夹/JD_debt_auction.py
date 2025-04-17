import random
import re
import time
from datetime import datetime, timedelta
import json
import os
from typing import Dict
from api_paimai import upload_file_by_url
import requests

from a_mysql_connection_pool import get_connection
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from DrissionPage.common import Settings
import tempfile
from api_paimai import judge_repeat, judge_repeat_attracting, judge_repeat_link


# 处理时间
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


# 保存json数据，测试使用
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


# 删除额外样式
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


# 更新京东拍卖链接
def update_jd_auction_link():
    """
    更新京东拍卖链接，并更新数据库
    :return:
    """
    co = ChromiumOptions()
    co = co.set_user_data_path(r"D:\chome_data\jingdong")
    # co = co.set_argument('--no-sandbox')
    # co = co.headless()
    co.set_paths(local_port=9211)
    page = ChromiumPage(co)
    page.set.auto_handle_alert()
    page.get("https://pmsearch.jd.com/?childrenCateId=12767")
    for _ in range(3):
        page.scroll.to_bottom()
        time.sleep(2)
    time.sleep(4)
    for page_num in range(80):
        print(page_num)
        if page_num != 0:
            page.ele("xpath=//a[@class='ui-pager-next']").click(by_js=True)
            for _ in range(3):
                page.scroll.to_bottom()
                time.sleep(2)
            time.sleep(4)

        html_etree = etree.HTML(page.html)
        try:
            target_html = html_etree.xpath("//div[@class='App']//div[@class='goods-list-container']")[0]
        except Exception as e:
            print('获取html出错', e)
            continue
        new_html = ''
        for con in target_html:
            new_html += etree.tostring(con, encoding='utf-8').decode()
        new_html_ = etree.HTML(new_html)
        target_html_ = new_html_.xpath("//ul/li")
        for target in target_html_:
            try:
                url = 'https:' + target.xpath(".//a/@href")[0]
                url_name = target.xpath(".//a//text()")[0]
                state = ''.join(target.xpath(".//div[@class='item-status']//text()"))
            except Exception as e:
                print('解析url和url名字时出错', e)
                continue
            state_sql, id_sql = judge_repeat_link(url)
            if state_sql == state:
                continue
            elif state_sql != state and state_sql:
                # 状态存在，状态和数据库中的不一致，更新数据库
                conn_test = get_connection()
                cursor_test = conn_test.cursor()
                # 上传文件
                insert_sql = "UPDATE col_judicial_auctions SET url=%s, title=%s,  state=%s WHERE id = %s"
                cursor_test.execute(insert_sql, (
                    url, url_name, state, id_sql))
                conn_test.commit()
                cursor_test.close()
                conn_test.close()
                print('更新数据库', url, url_name, state)
            elif not state_sql:
                # 状态不存在，插入数据库
                conn_test = get_connection()
                cursor_test = conn_test.cursor()
                insert_sql = "INSERT INTO col_judicial_auctions (url, title, state) VALUES (%s, %s, %s)"
                cursor_test.execute(insert_sql, (url, url_name, state))
                conn_test.commit()
                cursor_test.close()
                conn_test.close()
                print('插入数据库', url, url_name, state)
    page.quit()


def get_data(page_num, pro_id):
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        # 'referer': 'https://pmsearch.jd.com/',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        # 'cookie': '__jdu=17219744346561554622123; mba_muid=17219744346561554622123; shshshfpa=90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570; shshshfpx=90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570; light_key=AASBKE7rOxgWQziEhC_QY6yaB3PQ6pVpcy9uYd_PD0N1ReA0e-l3oBNJnSJd3xypi9G1dQ3H; pin=qwertyuiop2437; unick=nty47n2qtsb0ac; TrackID=1XApSoDl49V6MFvfHdLb-v1mjxgdjA_vFF7jJh1jU97Jm8vz4rjO9x1nHnGMMR0C9i6PK-n2uG17cNBI7ZbQ0WcBipZDtqz2esLSm7LfTGK0|||GoDjOYOhdgEboMHtDlun2Q; pinId=GoDjOYOhdgEboMHtDlun2Q; __jdv=96383255|baidu|-|organic|notset|1741655240850; joyya=1741673531.1741673815.21.1is84qr; RT="z=1&dm=jd.com&si=4iqr2zcnp5q&ss=m85bm3ra&sl=0&tt=0&r=8a72d04d1c1858ccd327b87ff7dfb81d&ul=12f68&hd=12f74"; shshshfpb=BApXS_4JgjvBAOjIe0u_EfeI01o8m0OKABnJ0cl9o9xJ1Mv8SPoG2; __jd_ref_cls=LoginDisposition_Go; jcap_dvzw_fp=tRyvbuoZufpryigwQ6_IIislWWGZ6Y6aRtwEC7eqiByFJ97hrGyE5mra9RTnFMk4DxeQfrv-FASUctjl946k_Q==; x-rp-evtoken=mGW9U4qbzsaBdCMe70m9pDuTjiz3piFqsCwDvZ27ENXDYBL4AxLLg32ouMB5v6uArvatCzpZFMXnU2aIaYLhSw%3D%3D; _gia_d=1; 3AB9D23F7A4B3CSS=jdd03V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPIAAAAMVRX7G7GQAAAAADIHXAMLKRBH6RUX; __jda=128418189.17219744346561554622123.1721974435.1741832547.1741844017.26; __jdb=128418189.2.17219744346561554622123|26.1741844017; __jdc=128418189; flash=3_X_8iXbzkemy3jEDqj8VDsOA2ESN9INL_TpgBgYUm1D032nqALAZUexXxtJEEkhjJHZ2uFYHvUoiXOGNetD5QDa_Pevj-DD385LSLUf4UfWi8HNZvnIqa7aqhrNa78w0nnNarCQeTS6_dULAwUsCsyurag8wI1f7Lw3qqreLwokW420M*; 3AB9D23F7A4B3C9B=V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPI; sdtoken=AAbEsBpEIOVjqTAKCQtvQu17dM1jxVG_QCwPRz30NnS3EYIsVigxdObqm2b1pEeeSmss7kRi0gvyvmFvx7BxH4hCGPYbctSas_Ve-XOD-qgYXdpYZtZ33CZeiaHK9pGWKMb7XzbYFqLM',
    }
    url = "https://api.m.jd.com/api"
    page_num = int(page_num)
    body = {"investmentType": "", "apiType": 12, "page": page_num, "pageSize": 200, "keyword": "", "provinceId": pro_id,
            "cityId": "", "countyId": "", "multiPaimaiStatus": "1", "multiDisplayStatus": "", "multiPaimaiTimes": "",
            "childrenCateId": "109", "currentPriceRangeStart": "", "currentPriceRangeEnd": "",
            "timeRangeTime": "endTime", "timeRangeStart": "", "timeRangeEnd": "", "loan": "", "purchaseRestriction": "",
            "orgId": "", "orgType": "", "sortField": 9, "projectType": 2, "reqSource": 0, "labelSet": "",
            "publishSource": "", "publishSourceStr": [], "defaultLabelSet": ""}
    params = {
        "appid": "paimai",
        "functionId": "paimai_searchMerchantsProduct",
        "body": f"{body}",
        # "jsonp": "jsonp_1741844105627_11005"
    }
    response = requests.get(
        url,
        params=params,
        # cookies=cookies,
        headers=headers,
    )
    # print(f'当前第{page_num}页')
    data_list = response.json()
    # time.sleep(3)
    # print(data_list)
    datas = data_list["datas"]
    for data in datas:
        id_ = data["id"]
        url = f"https://auction.jd.com/zichan/tuijie/item/{id_}"
        url_name = data["name"]
        data_dict = {"url": url, "url_name": url_name}
        id, from_queue = judge_repeat_attracting(url)
        if not id:
            # 状态不存在，插入数据库
            conn_test = get_connection()
            cursor_test = conn_test.cursor()
            insert_sql = "INSERT INTO col_judicial_auctions_investing (url, title) VALUES (%s, %s)"
            cursor_test.execute(insert_sql, (url, url_name))
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
            print('插入数据库', url, url_name)


# 更新京东招商链接
def update_jd_investment_link():
    for pro in range(1, 32 + 1):
        for page_num in range(1, 10):
            try:
                get_data(page_num, pro)
            except Exception as e:
                print(e)
                continue


# 获取一个京东拍卖的空链接
def get_jd_auction_null_url():
    conn = get_connection()
    cursor = conn.cursor()

    # 参数化查询（防止 SQL 注入）
    query = "SELECT * FROM col_judicial_auctions WHERE url LIKE %s AND (from_queue IS NULL OR from_queue = '') and state != '预告中' LIMIT 1"
    search_pattern = "%jd%"  # 匹配任意位置包含 "jd" 的 URL
    cursor.execute(query, (search_pattern,))
    # 获取结果
    row = cursor.fetchone()
    if row:
        print(row)
        id = row[0]
        url_sql = row[1]
        title_sql = row[2]
        state_sql = row[3]
        print(id, url_sql, title_sql, state_sql)
        return id, url_sql, title_sql, state_sql
    else:
        return None, None, None, None


# 获取一个京东招商的空链接
def get_jd_attracting_null_url():
    conn = get_connection()
    cursor = conn.cursor()

    # 参数化查询（防止 SQL 注入）
    query = "SELECT * FROM col_judicial_auctions_investing WHERE url LIKE %s AND (from_queue IS NULL OR from_queue = '') LIMIT 1"
    search_pattern = "%auction.jd%"  # 匹配任意位置包含 "jd" 的 URL
    cursor.execute(query, (search_pattern,))
    # 获取结果
    row = cursor.fetchone()
    if row:
        print(row)
        id = row[0]
        url_sql = row[1]
        title_sql = row[2]
        print(id, url_sql, title_sql)
        return id, url_sql, title_sql
    else:
        return None, None, None


# 获取京东债权招商详细数据
def get_jd_attracting_data(id_, url, url_name, from_queue):
    """
    获取京东债权拍卖数据
    :param id_: 数据库id
    :param url: 链接
    :param url_name: 链接名称
    :param from_queue: 来源队列
    :return:
    """
    # 禁用全局自动化特征
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True

    # 配置浏览器参数
    options = ChromiumOptions()
    # options.set_argument('--disable-blink-features=AutomationControlled')
    options.set_argument('--incognito')
    options.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')

    # # 随机化UA
    # ua = UserAgent()
    # options.set_argument(f'--user-agent={ua.random}')
    url = url
    title = url_name
    id_value, from_queue_value = judge_repeat_attracting(url)
    if from_queue_value:
        # page.quit()
        # print(1234567)
        return
    # 启动浏览器
    page = ChromiumPage(options)

    # 设置随机窗口尺寸
    page.set.window.size(1366 + random.randint(-100, 100), 768 + random.randint(-50, 50))
    # 访问目标网站
    page.get(url)
    page.scroll.to_bottom()
    time.sleep(4)

    tree = etree.HTML(page.html)
    page.quit()
    # 执行清理并输出, 测试阶段展示html
    tree = remove_styles(tree)
    cleaned_html = etree.tostring(tree, encoding='unicode', pretty_print=True)
    # print(cleaned_html)
    # return
    disposition_subject = ''.join(
        tree.xpath("//dl[@class='sc-fBuWsC GdrRc']/dd[@class='sc-jhAzac bHuVwS']//text()"))  # 资产处置主体
    reference_value = ''  # 参考价值
    recruitment_time = ''.join(tree.xpath(
        "//div[@class='sc-Rmtcm jTBHht'][1]/dl[@class='sc-fBuWsC GdrRc'][4]/dd[@class='sc-hzDkRC kHJBpV']/text()"))  # 招募时间
    recruitment_time = ''.join(re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', recruitment_time))  # 招募时间
    type = ''.join(tree.xpath("//dl[@class='sc-fBuWsC GdrRc'][1]/dd[@class='sc-hzDkRC kHJBpV']/text()"))  # 类型
    guarantee_method = ''.join(tree.xpath(
        "//div[@class='sc-Rmtcm jTBHht'][1]/dl[@class='sc-fBuWsC GdrRc'][3]/dd[@class='sc-hzDkRC kHJBpV']/text()"))  # 担保方式
    total = ''.join(tree.xpath("//dl[@class='sc-fBuWsC kHwFGn']//text()")) + ',其中：' + ''.join(
        tree.xpath("//dl[@class='sc-fBuWsC GdrRc'][2]/dd[@class='sc-hzDkRC kHJBpV']//text()"))  # 债权总金额
    situation = ''.join(tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][2]/p//text()"))  # 债务人情况
    guarantor = ''.join(tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][3]/p//text()"))  # 担保人情况
    collateral_list = tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][4]")  # 抵押物情况
    collateral = ''
    for con in collateral_list:
        collateral += etree.tostring(con, encoding='utf-8').decode()
    detail_list = tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][1]")  # 公告详情
    detail_html = ''
    for con in detail_list:
        detail_html += etree.tostring(con, encoding='utf-8').decode()
    detail = ''.join(tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][1]//text()"))  # 公告详情
    supple_mater = ''.join(
        tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][5]/a[@class='sc-kvZOFW gOWYUa']//text()"))  # 附件
    # original_annexs = tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][5]/a[@class='sc-kvZOFW gOWYUa']")   # 附件链接
    # print(len(original_annexs))
    annex_urls = ''
    # if len(original_annexs) > 0:
    #     for original_annex in original_annexs:
    #         page.ele("xpath=//div[@class='sc-frDJqD cDnLeJ'][5]/a[@class='sc-kvZOFW gOWYUa']").click(by_js=True)
    #         time.sleep(4)
    #         annex_urls += page.url + ','
    #         page.back()
    data_dict = {
        "disposition_subject": disposition_subject,
        "reference_value": reference_value,
        "recruitment_time": recruitment_time,
        "type": type,
        "guarantee_method": guarantee_method,
        "total": total,
        "situation": situation,
        "guarantor": guarantor,
        "collateral": collateral,
        "detail": detail,
        "more_info": detail_html,
        "supple_mater": supple_mater,
        "annex_urls": annex_urls,
    }

    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    create_date = datetime.now().strftime('%Y-%m-%d')

    try:
        conn_test = get_connection()
        cursor_test = conn_test.cursor()
        # 上传文件
        insert_sql = "UPDATE col_judicial_auctions_investing SET url = %s, title = %s, disposition_subject = %s, reference_value = %s, recruitment_time = %s, type = %s, guarantee_method = %s, total = %s, situation = %s, guarantor = %s, collateral = %s, detail = %s, more_info = %s, supple_mater = %s, create_time = %s, create_date = %s, from_queue = %s WHERE id = %s;"

        cursor_test.execute(insert_sql, (
            url, title, disposition_subject, reference_value, recruitment_time, type, guarantee_method, total,
            situation, guarantor, collateral, detail, detail_html, supple_mater, create_time,
            create_date, from_queue, id_))
        conn_test.commit()
        print(data_dict)
        cursor_test.close()
        conn_test.close()
    except Exception as e:
        print(f"Error: {e}")
        pass


# 获取京东债权拍卖详细数据
def get_jd_auction_detail(id_, url, url_name, state, from_queue, state_now=''):
    # 禁用全局自动化特征
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True

    # 配置浏览器参数
    options = ChromiumOptions()
    # options.set_argument('--disable-blink-features=AutomationControlled')
    options.set_argument('--incognito')
    options.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')

    # # 随机化UA
    # ua = UserAgent()
    # options.set_argument(f'--user-agent={ua.random}')
    url = url
    title = url_name
    state_sql, id = judge_repeat(url)
    if state_sql:
        # page.quit()
        return
    # 启动浏览器
    page = ChromiumPage(options)

    # 设置随机窗口尺寸
    page.set.window.size(1366 + random.randint(-100, 100), 768 + random.randint(-50, 50))
    # 访问目标网站
    page.get(url)
    page.scroll.to_bottom()
    time.sleep(4)

    tree = etree.HTML(page.html)
    page.close()

    # 执行清理并输出, 测试阶段展示html
    cleaned_tree = remove_styles(tree)
    # cleaned_html = etree.tostring(cleaned_tree, encoding='unicode', pretty_print=True)
    # print(cleaned_html)
    # return

    state = state
    stage = ''
    address = ''.join(tree.xpath("//div[contains(@class, 'pm-location')]/em/text()"))
    start_bid = ''.join(tree.xpath(
        "//li[2]/div[@class='index_label__Nie1n ']/div[@id='right-content']//span[contains(@class, 'index_value__YfM3M ')]/text()"))
    sold_price = ''.join(tree.xpath("//div[@class='priceInfoItemPriceWrap']//text()"))
    sold_price = ''.join(re.findall(r'¥(.*)', sold_price))
    sold_price = re.sub(r'保证金.*', '', sold_price)
    sold_price = re.sub(r'变卖.*', '', sold_price)
    outcome = ''.join(tree.xpath("//div[@class='index_auctionstatusbanner__statustext__RxEYN']/span//text()"))
    end_time = ''
    start_time = ''
    if state_now == '已结束' or state_now == '进行中':
        end_time_str = ''.join(tree.xpath(
            "//div[@class='index_auctionstatusbanner__endtime__7-dda']/text() | //div[@class='main-block-content']/div[1]//text()"))
        end_time = ''.join(re.findall(r'(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2})', end_time_str))  # 结束时间
        end_time = end_time.replace('年', '-').replace('月', '-').replace('日', '')
        if not end_time:
            end_time = ''.join(re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', end_time_str))  # 结束时间
    elif state_now == '预告中':
        distance_end = ''.join(tree.xpath("//div[@class='index_countdown__remainTime__O7MNa']/div//text()"))
        if not distance_end:
            distance_end = ''.join(tree.xpath("//div[@class='index_countdown__time__ArsTv']//text()"))
        start_time = parse_opentime(distance_end)
        print(distance_end)
        print(start_time)
    procedure_str = ''  # 拍卖程序
    disposal_unit = ''.join(tree.xpath("//a[@id='disposalUnitTag']/text()"))  # 处置单位
    bidding_status = ''.join(tree.xpath("//table[@class='index_bidList__i8yA2']/tbody/tr[1]/td[1]/div/text()"))  # 竞买状态
    bidding_code = ''.join(tree.xpath("//table[@class='index_bidList__i8yA2']/tbody/tr[1]/td[2]/div/text()"))  # 竞买代码
    bidding_price = ''.join(tree.xpath("//table[@class='index_bidList__i8yA2']/tbody/tr[1]/td[3]/div/text()"))  # 竞买价格
    bidding_time = ''.join(tree.xpath("//table[@class='index_bidList__i8yA2']/tbody/tr[1]/td[4]/div/text()"))  # 竞买时间
    auction_history = f'竞买状态:{bidding_status} 竞买代码:{bidding_code} 竞买价格:{bidding_price} 竞买时间:{bidding_time}'
    people_num = ''.join(tree.xpath("//div[@class='index_auctionstatusbanner__statistics__-mtfv']//text()"))  # 竞买人数
    people_num = ''.join(re.findall(r'(\d+)人报名', people_num))
    # subject_info_etree = tree.xpath("//div[@class='paimaiDetailContainer']/div[@class='pm-content']/ul[@class='floors']/li[3]")  # 标的物信息_html
    subject_info_etree = tree.xpath(
        "//div[@class='paimaiDetailContainer']/div[@class='pm-content']/ul[@class='floors']/li | //div[@id='pmMainFloor']/ul[@class='floors']/li")  # 标的物信息_html
    subject_info = ''
    for subject_con in subject_info_etree:
        subject_con_str = subject_con.xpath(".//text()")
        if '标的物详情描述' in subject_con_str:
            subject_info += etree.tostring(subject_con, encoding='utf-8').decode()

    subject_annex_up_list = tree.xpath("//ul[@class='floors']//@href")  # 标的物信息附件上传
    subject_annex = ''
    subject_annex_up = ''
    for annex in subject_annex_up_list:
        if annex == 'http://zichan.jd.com/':
            continue
        else:
            file_name = random.randint(100000, 999999)
            url_type = annex.split('.')[-1]
            if url_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                            'png', 'jpg', 'jpeg', "PDF"]:
                file_url = upload_file_by_url(annex, f"{file_name}", url_type)
                subject_annex += annex + ','
                subject_annex_up += file_url + ','
    subject_annex = str(subject_annex[:-1])
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
        'auction_html': auction_html
    }
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    create_date = datetime.now().strftime('%Y-%m-%d')
    # 上传到数据库
    conn_test = get_connection()
    cursor_test = conn_test.cursor()
    # 上传文件
    insert_sql = "UPDATE col_judicial_auctions SET url = %s, title = %s, state = %s, stage = %s, address = %s, start_bid = %s, sold_price = %s, outcome = %s, end_time = %s, procedure_str = %s, auction_html = %s, subject_annex_up = %s, subject_info = %s, disposal_unit = %s, auction_history = %s, people_num = %s, subject_annex = %s, create_time = %s, create_date = %s, from_queue = %s WHERE id = %s;"

    cursor_test.execute(insert_sql,
                        (url, title, state, stage, address, start_bid, sold_price,
                         outcome,
                         end_time, procedure_str, auction_html, subject_annex_up,
                         subject_info,
                         disposal_unit, auction_history, people_num, subject_annex,
                         create_time,
                         create_date, from_queue, id_))
    conn_test.commit()

    cursor_test.close()
    conn_test.close()
    print(value)


# 获取京东拍卖数据
def auction(from_queue):
    update_jd_auction_link()
    while True:
        id_, url_sql, title_sql, state_sql = get_jd_auction_null_url()
        if url_sql:
            get_jd_auction_detail(id_, url_sql, title_sql, state_sql, from_queue, state_now=state_sql)
        else:
            break


# 获取京东招商数据
def investment(from_queue):
    update_jd_investment_link()
    while True:
        id_, url_sql, title_sql = get_jd_attracting_null_url()
        if url_sql:
            get_jd_attracting_data(id_, url_sql, title_sql, from_queue)
        else:
            break


while True:
    time.sleep(1)
    auction("5678")
    investment('5678')
# get_jd_auction_null_url()
