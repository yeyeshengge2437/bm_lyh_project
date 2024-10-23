import json
import requests

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False

produce_url = "http://121.43.164.84:29807/inner-api"


def get_img_url():
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "description": ''
    }
    data_str = json.dumps(data, ensure_ascii=False)
    url = produce_url + "/paper-deal/quark/table-start"
    response = s.post(url, headers=headers, data=data_str)
    result = response.json()
    print(result)
    return result.get("value")


def img_url_identify_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/paper-deal/quark/table-success"
    data_str = json.dumps(data, ensure_ascii=False)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result


# 实例
"""
data = {
    'id' : '1',
    'quark_tables' : '夸克表格识别',
    'remark' : '识别成功'
    }
"""


def img_url_identify_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = produce_url + "/paper-deal/quark/table-fail"
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


def img_url_to_fail(image_url):
    # 图片的URL
    image_url = image_url

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
