import json
import os
import random
import re
import time
from datetime import datetime

import mysql.connector
import pdfplumber
import requests

produce_url = "http://121.43.164.84:29875"  # 生产环境
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
        raise Exception(f'pdf或图片下载失败')
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
    return result.get("value")["file_url"]


def upload_file(file_name, file_type, type="paper"):
    file_path = f"{file_name}.{file_type}"
    # 上传接口
    fr = open(file_path, 'rb')
    file_data = {"file": fr}
    url = produce_url + f"/file/upload/file?type={type}"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(file_path)
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
    conn_test = mysql.connector.connect(
        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
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


def judge_title_repeat(origin):
    """
    判断是否重复
    :param origin: 原始数据
    :return:
    """
    # 创建版面链接集合
    title_url_set = set()
    # 连接数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    cursor_test.execute(f"SELECT id, content_url FROM col_paper_notice WHERE paper = '{origin}'")
    rows = cursor_test.fetchall()
    for id, content_url in rows:
        title_url_set.add(content_url)
    cursor_test.close()
    conn_test.close()
    return title_url_set


def get_image(page, url, element, is_to_bottom=False, left_offset=0, right_offset=0, up_offset=0, down_offset=0):
    tab = page.new_tab()
    tab.get(url)
    tab.wait.ele_displayed(element)
    if is_to_bottom:
        tab.scroll.to_bottom()
    time.sleep(2)
    value = tab.ele(element).rect.corners
    top_left = value[0]
    bottom_right = value[2]
    # 将top_left元组中的浮点数转换为整数
    top_left1 = (int(top_left[0] - left_offset), int(top_left[1] + up_offset))
    # 将bottom_right元组中的浮点数转换为整数
    bottom_right1 = (int(bottom_right[0] + right_offset), int(bottom_right[1] - down_offset))
    length = bottom_right1[1] - top_left1[1]
    if length < 16000:
        bytes_str = tab.get_screenshot(as_bytes='png', left_top=top_left1, right_bottom=bottom_right1)
    else:
        bottom_right1 = (int(bottom_right[0] + right_offset), 8000)
        bytes_str = tab.get_screenshot(as_bytes='png', left_top=top_left1, right_bottom=bottom_right1)
    # 随机的整数
    random_int = random.randint(0, 1000000)
    with open(f'{random_int}.png', 'wb') as f:
        f.write(bytes_str)
    tab.close()
    return random_int


def get_now_image(page, url):
    tab = page.new_tab()
    tab.get(url)
    time.sleep(2)
    bytes_str = tab.get_screenshot(as_bytes='png')
    # 随机的整数
    random_int = random.randint(0, 1000000)
    with open(f'{random_int}.png', 'wb') as f:
        f.write(bytes_str)
    tab.close()
    return random_int
