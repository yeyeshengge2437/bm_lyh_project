import json
import os
import random
import re
import requests

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False

# produce_url = "http://118.31.45.18:29810"
produce_url = "http://10.20.151.6:29707"


def qcc_parse_next(data=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    data_str = json.dumps(data, ensure_ascii=False)
    url = produce_url + "/inner-api/crp-deal/qcc-queue/next"
    response = s.post(url, headers=headers, data=data_str)
    # response = s.post(url, headers=headers)
    result = response.json()
    print(result)
    return result




def qcc_parse_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/corp/queue/success"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result


# 实例
"""
data = {
    'id' : '1',
    'remark' : '哪个AI',
    'input_token_num' : '输入token数',
    'output_token_num' : '输出token数',
    'output_text' : '输出',
    }
"""


def qcc_parse_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/corp/queue/fail"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result


def qcc_upload_detail_info(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/inner-api/crp-deal/qcc-queue/tell-crp-info"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    return result


def qcc_upload_info_list(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/inner-api/crp-deal/qcc-queue/tell-crp-list"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result
