import json
import os

import requests
from PIL import Image

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False

produce_url = "http://118.31.45.18:29810"


def get_img_url():
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'tell_tool_list': [
            'quark_img_table_tell'
        ]
    }
    data_str = json.dumps(data, ensure_ascii=False)
    url = produce_url + "/inner-api/paper-deal/tell-queue/next"
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
    url = produce_url + "/inner-api/paper-deal/tell-queue/success"
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


def compress_img(file_name):
    # 打开彩色图片文件
    color_image = Image.open(file_name)
    # 转换为黑白模式
    black_and_white_image = color_image.convert('L')
    # 将图像转换为调色板模式（8位）
    palette_image = black_and_white_image.convert('P', palette=Image.ADAPTIVE)
    # 保存黑白图片
    black_and_white_image.save(file_name, optimize=True)


def compress_image(input_path, output_path, max_size_mb=9):
    # 打开图片
    img = Image.open(input_path)

    # 初始化质量参数
    quality = 95  # 从较高的质量开始
    i = 0

    # 循环直到文件大小小于最大大小
    while True:
        # 保存图片
        img.save(f'{output_path}_{i}.jpg', 'JPEG', quality=quality, optimize=True)

        # 检查文件大小
        if os.path.getsize(f'{output_path}_{i}.jpg') <= max_size_mb * 1024 * 1024:
            return f'{output_path}_{i}.jpg'
        else:
            os.remove(f'{output_path}_{i}.jpg')

        # 如果文件仍然太大，降低质量并重试
        quality -= 5
        i += 1
        if quality < 10:  # 防止质量降到过低
            return None


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

        compress_name = compress_image(filename, 'yasuo', max_size_mb=9)

        return compress_name
    else:
        raise Exception('下载图像失败')
