import json
import os
from datetime import datetime

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


def upload_file_by_url(file_url, file_name, file_type, type="paper"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(file_url, headers=headers)
    if r.status_code != 200:
        return "获取失败"
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


def parse_pdf(pdf_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    r = requests.get(pdf_url, headers=headers)
    pdf_path = f"111.pdf"
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
        return False
