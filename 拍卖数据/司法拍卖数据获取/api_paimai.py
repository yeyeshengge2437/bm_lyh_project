import json
import os
import random
import re
from datetime import datetime
from a_mysql_connection_pool import get_connection
import mysql.connector
import pdfplumber
import requests

produce_url = "http://118.31.45.18:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False


def paper_queue_next(webpage_url_list=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if webpage_url_list is None:
        webpage_url_list = []

    url = test_url + "/website/queue/next"
    data = {
        "webpage_url_list": webpage_url_list
    }

    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    print(result)
    return result.get("value")


def paper_queue_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = test_url + "/website/queue/success"
    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result.get("value")


def paper_queue_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    try:
        if data is None:
            data = {}
        url = test_url + "/website/queue/fail"
        data_str = json.dumps(data)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def paper_queue_delay(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    try:
        if data is None:
            data = {}
        url = test_url + "/website/queue/delay"
        data_str = json.dumps(data)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def upload_file_by_url(file_url, file_name, file_type, type="paper", verify=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    file_name = file_name + str(random.randint(1, 999999999))
    r = requests.get(file_url, headers=headers, verify=verify)
    if r.status_code != 200:
        return None
    pdf_path = f"{file_name}.{file_type}"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}
    url = produce_url + f"/file/upload/file?type={type}"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    return result.get("value")["file_url"]


def date_conversion(date, origin_date, data_type):
    """
    日期格式转换
    :param date: 传入的日期数据
    :param origin_date: 原始日期数据的格式
    :param data_type: 想要的日期格式
    :return: 处理好日期格式的日期
    """
    # 日期格式正则表达式
    date = str(date)
    date_obj = datetime.strptime(date, origin_date)
    date = date_obj.strftime(data_type)
    return date


def parse_pdf(pdf_url, pdf_name):
    """
    目前未使用
    :param pdf_url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    try:
        r = requests.get(pdf_url, headers=headers)
        if r.status_code != 200:
            return False
        pdf_path = f"{pdf_name}.pdf"
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        if not os.path.exists(pdf_path):
            fw = open(pdf_path, 'wb')
            fw.write(r.content)
            fw.close()
        pdf_content = ''
        flag = 0
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                if '公告 ' in page.extract_text():
                    flag = 1
                    break
        if flag:
            os.remove(pdf_path)
            return True
        else:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            return False
    except:
        return False


def judging_criteria(title, article_content):
    """
    判断是否为债权公告
    :param title: 报纸的标题
    :param article_content: 报纸的内容
    :return:
    """
    explicit_claims = re.compile(
        r'(债权|转让|受让|处置|招商|营销|联合|催收|催讨)(信息)?的?(通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)')

    explicit_not_claims = re.compile(
        r'(法院公告|减资公告|注销公告|清算公告|合并公告|出让公告|重组公告|调查公告|分立公告|重整公告|悬赏公告|注销登记公告|施工公告|公益广告|采购信息公告)')

    possible_claims = re.compile(r'^(?=.*(公告|公 告|无标题|广告)).{1,10}$')

    possible_content = re.compile(r'(债权|债务|借款|催收)的?(公告|通知)')
    # 判断是否为债权公告
    # 明确为债权公告
    if explicit_claims.search(title) and not explicit_not_claims.search(title):
        return True
    # 可能为债权公告
    elif possible_claims.search(title) and possible_content.search(article_content) and not explicit_not_claims.search(
            title):
        return True
    else:
        return False


def judging_bm_criteria(title):
    """
    判断是否为需要的版面
    :param title: 文章标题
    :return:
    """
    explicit_claims = re.compile(
        r'(债权|转让|受让|处置|招商|营销|联合|催收|催讨)(信息)?的?(通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)')

    explicit_not_claims = re.compile(
        r'(法院公告|减资公告|注销公告|清算公告|合并公告|出让公告|重组公告|调查公告|分立公告|重整公告|悬赏公告|注销登记公告|施工公告|公益广告)')

    possible_claims = re.compile(r'(公告|公 告|无标题|广告)')
    # 匹配汉字数
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', title)
    chinese_count = len(chinese_chars)
    # 若标题为空
    if not title:
        return True
    # 若明确为债权标题
    if explicit_claims.search(title) and not explicit_not_claims.search(title):
        return True
    # 若疑似为债权标题
    elif possible_claims.search(title) and chinese_count < 10 and not explicit_not_claims.search(title):
        return True
    else:
        return False


def zhengquan_criteria(title):
    """
    判断证券类报纸是否有债权公告
    :param title: 文章标题
    :return:
    """
    explicit_claims = re.compile(
        r'(债权|转让|受让|处置|招商|营销|联合|催收|催讨)(信息)?的?(通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)')
    if explicit_claims.search(title):
        return True
    else:
        return False


def judge_bm_repeat(origin, bm_url):
    """
    判断版面是否重复
    :param origin: 原始数据
    :return:
    """
    # 创建版面链接集合
    bm_url_set = set()
    # 连接数据库
    conn_test = get_connection()
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    cursor_test.execute(f"SELECT id, page_url FROM col_paper_page WHERE paper = '{origin}'")
    rows = cursor_test.fetchall()
    for id, page_url in rows:
        bm_url_set.add(page_url)
    cursor_test.close()
    conn_test.close()
    if bm_url in bm_url_set:
        return False
    else:
        return True


def judge_repeat(url_href):
    """
    判断链接是否重复
    :return:
    """
    # 创建版面链接集合
    bm_url_set = set()
    # 连接数据库
    conn_test = get_connection()
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    # cursor_test.execute(f"SELECT id, url, state FROM col_judicial_auctions")
    cursor_test.execute(f"SELECT id, state FROM col_judicial_auctions WHERE url = '{url_href}' LIMIT 1;")
    rows = cursor_test.fetchall()
    cursor_test.close()
    conn_test.close()
    if rows:
        id = rows[0][0]
        state = rows[0][1]
        return state, id
    else:
        return False, 0


def judge_repeat_attracting(url_href):
    """
    判断链接是否在拍卖招商表中存在
    :return:
    """
    # 创建版面链接集合
    bm_url_set = set()
    # 连接数据库
    conn_test = get_connection()
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    # cursor_test.execute(f"SELECT id, url, state FROM col_judicial_auctions")
    cursor_test.execute(f"SELECT id FROM col_judicial_auctions_investing WHERE url = '{url_href}' LIMIT 1;")
    rows = cursor_test.fetchall()
    cursor_test.close()
    conn_test.close()
    if rows:
        id = rows[0][0]
        return id
    else:
        return 0


def sub_queues_add(data=None):
    """
    添加子队列
    data = {
        "name": "详细链接"
        "web_queue_id": 1, # 采集队列id
        "webpage_id": 2, # 数据项id
        "webpage_url": "http://www.baidu.com", # 数据项链接
        "sub_type": "类型", # 类型
    }
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    url = test_url + "/website/sub-queue/add"
    if data is None:
        data = {}

    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result


def sub_queues_next(webpage_url_list=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if webpage_url_list is None:
        webpage_url_list = []

    url = test_url + "/website/sub-queue/next"
    data = {
        "webpage_url_list": webpage_url_list
    }

    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    print(result)
    return result.get("value")


def sub_queues_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = test_url + "/website/sub-queue/success"
    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result.get("value")

def sub_queues_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    try:
        if data is None:
            data = {}
        url = test_url + "/website/sub-queue/fail"
        data_str = json.dumps(data)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        return result.get("value")
    except Exception as err:
        print(err)
        return None