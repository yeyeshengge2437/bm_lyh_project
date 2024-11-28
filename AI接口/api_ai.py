import json
import re
import requests

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False

produce_url = "http://118.31.45.18:29810"


def img_url_to_file(image_url):
    # 图片的URL
    image_url = image_url
    image_url = re.sub(r'\?.*', '', image_url)
    # 请求头部，有些网站可能需要User-Agent来模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 发送GET请求
    response = requests.get(image_url, headers=headers)

    # 确保请求成功
    if response.status_code == 200:
        # 图片的文件名
        filename = image_url.split('/')[-1]

        # 打开一个文件来写入图片数据
        with open(filename, 'wb') as f:
            # 写入请求回来的图片数据
            f.write(response.content)

        return filename
    else:
        raise Exception('下载图像失败')


def ai_parse_next(data=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    data_str = json.dumps(data, ensure_ascii=False)
    url = produce_url + "/inner-api/paper-deal/tell-queue/next"
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

def pdf_content_except_table_update(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/inner-api/paper-deal/pdf-content-except-table-update"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result
