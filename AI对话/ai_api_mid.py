import json
import os
import random
import re
import requests

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False

produce_url = "http://118.31.45.18:29810"



def ai_parse_next(data=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    data_str = json.dumps(data, ensure_ascii=False)
    url = produce_url + "/inner-api/ai-queue/tell-queue/next"
    response = s.post(url, headers=headers, data=data_str)
    result = response.json()
    print(result)
    return result.get("value")


# 实例
"""
data = {
    'tell_tool_list': [
                       "kimi_8k-kimi文本理解",
                       "kimi_32k-kimi图片理解",
                       "glm_4_air-智谱文本理解",
                       "glm_4v_plus-智谱图片理解"
                       ]
}
"""


def ai_parse_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/inner-api/paper-deal/tell-queue/success"
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


def ai_parse_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/inner-api/paper-deal/tell-queue/fail"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result


# 实例
"""
data = {
    'id' : '1',
    'remark' : '识别失败'
    }
"""

