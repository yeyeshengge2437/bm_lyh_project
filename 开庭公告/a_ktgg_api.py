import base64
import json
import time
from datetime import datetime

from DrissionPage import ChromiumPage, ChromiumOptions
import os
import json
import requests
import pymongo
import ddddocr
import mysql.connector
import hashlib
import redis

produce_url = "http://118.31.45.18:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False


def queue_next(webpage_url_list=None):
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


def queue_success(data=None):
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


def queue_fail(data=None):
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

def judge_repeat_invest(url_href):
    """
    判断链接是否重复
    :return:
    """
    # 连接数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    # cursor_test.execute(f"SELECT id, url, state FROM col_judicial_auctions")
    cursor_test.execute(f"SELECT id FROM col_case_open WHERE url = '{url_href}' LIMIT 1;")
    rows = cursor_test.fetchall()
    if rows:
        return True
    else:
        return False

def judge_repeat_case(case):
    """
    判断案号是否重复
    :return:
    """
    # 连接数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    # cursor_test.execute(f"SELECT id, url, state FROM col_judicial_auctions")
    cursor_test.execute(f"SELECT id FROM col_case_open WHERE case_no = '{case}' LIMIT 1;")
    rows = cursor_test.fetchall()
    if rows:
        return True
    else:
        return False