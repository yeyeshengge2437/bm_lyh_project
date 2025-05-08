import re

import execjs
import requests

# 这里补充一下cookies
count_num = 0


def build_api_headers(url, key_no, pid, tid, json_data=None):
    """
    构造请求头
    Args:
        url: 链接，包含参数
        key_no: 企业编号
        pid: 页面的加密参数pid
        tid: 页面的加密参数tid
        json_data: post请求的json数据
    Returns:
        response对象
    """
    headers = {'authority': 'www.qcc.com', 'accept': 'application/json, text/plain, */*',
               'accept-language': 'zh-CN,zh;q=0.9', 'cache-control': 'no-cache', 'content-type': 'application/json',
               'origin': 'https://www.qcc.com', 'pragma': 'no-cache',
               'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
               'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
               'x-requested-with': 'XMLHttpRequest', "referer": f'https://www.qcc.com/firm/{key_no}.html', 'x-pid': pid}

    # 正则取出'/api'及其后面的所有内容
    path = re.findall(r'(/api.*)', url)[0]

    # print(f"path: {path}")
    # 执行qichacha.js中的run方法
    with open('./qcc_headers.js', 'r', encoding='utf-8') as f:
        js = f.read()
    if json_data:
        ctx = execjs.compile(js).call('run', path, tid, json_data)
    else:
        ctx = execjs.compile(js).call('run', path, tid)
    # ctx是个字典，便利出所有的key和value，添加到headers中，不要覆盖原来的headers
    for k, v in ctx.items():
        headers[k] = v
    return headers


def post_api(url, key_no, pid, tid, cookies, json_data=None):
    """
    请求企查查api接口，post请求
    Args:
        url: 链接，包含参数
        key_no: 企业编号
        pid: 页面的加密参数pid
        tid: 页面的加密参数tid
        json_data: post请求的json数据
    Returns:
        response对象
    """
    headers = build_api_headers(url, key_no, pid, tid, json_data)

    response = requests.post(url, cookies=cookies, headers=headers, json=json_data)
    return response


def get_api(url, key_no, pid, tid, cookies, json_data=None):
    """
    get请求企查查api接口
    Args:
        url: 链接，包含参数
        key_no: 企业编号
        pid: 页面的加密参数pid
        tid: 页面的加密参数tid

    Returns:
        response对象
    """
    headers = build_api_headers(url, key_no, pid, tid, json_data)

    response = requests.get(url, cookies=cookies, headers=headers)
    return response


def get_response(url, key_no, pid, tid, cookies, params=None):
    main_member = get_api(url, key_no, pid, tid, cookies).json()
    print(main_member)
    global count_num
    count_num += 1
    print(f'现有请求次数{count_num}')
    return main_member


# url = 'https://www.qcc.com/api/datalist/mainmember?isNewAgg=true&keyNo=e01ade065389b3428b6ede6dc941cd3a&nodeName=Employees&pageIndex=2'
# key_no = 'e01ade065389b3428b6ede6dc941cd3a'
# pid = 'd286822c69c92897df86b6eb1767a5fa'
# tid = '202c66ff69f1b03090b9e46d5ee4cb98'
# cookies = {
#     'QCCSESSID': 'c8fd4cec040da168dbf740bd7c',
#     'qcc_did': 'c92dff49-b4b9-430f-b2d3-55f2f7114522',
#     'UM_distinctid': '196140bf3052b11-0e7e33fa5ab18f-26011d51-13c680-196140bf3061661',
#     'tfstk': 'gcXnKhZa_6RQ4uQxJNJQiBAdvPVTAD9WoaHJyLLz_F8sJ2Hd4L8lzFBpJMpEzYbk5XHLAQQMqNSXwLpLO3mCIZD-pyNC4YvJUrUYH-IBvL9zkcad56iB23hrU4drbFJJqNlC4djCALi6xZSfPMgomUD18L7yQC-JVL-rUYribnYZL3ke4VrMVFJrzeJr_F-D4HJyUaSaj3TwzA3EbeQPROz6U9AuBHDhGHAHuM8FvMBZlChC4FqabOfpKEykSYkPIHjtax1qn7LVGedvlNytKLjwqNAAtrDhrgSfaCXo8kQV4w6MdKV8AIfN6sdhsykkW9KkgLRi4YSMIF_cBKyqSh1Nv_WC-0DyA9BvZEOg4YOJQtdVgwm7cGJe4aOferMB8gSfhsp0Kqth_ivG4LGZghjsFhrRQbGWThtMknhlAvrp6eD4jlcVGB-6Y-EgjbGWThtMklqigrOefHyA.',
#     'acw_tc': '0a47308617441890120471609e01619f37142320e0de3cb5108326bafc624d',
#     'CNZZDATA1254842228': '51069784-1744093050-%7C1744190044',
# }
# get_response(url, key_no, pid, tid, cookies)


def post_response(url, key_no, pid, tid, cookies, json_data=None):
    financial = post_api(url, key_no, pid, tid, cookies, json_data=json_data).json()
    print(financial)
    global count_num
    count_num += 1
    print(f'现有请求次数{count_num}')
    return financial


# url = f'https://www.qcc.com/api/datalist/changelist'
# key_no = '9cce0780ab7644008b73bc2120479d31'
# pid = '708896223eaab213e0b8126b57e77375'
# tid = '202c66ff69f1b03090b9e46d5ee4cb98'
# cookies = {
#     'QCCSESSID': 'c8fd4cec040da168dbf740bd7c',
#     'qcc_did': 'c92dff49-b4b9-430f-b2d3-55f2f7114522',
#     'UM_distinctid': '196140bf3052b11-0e7e33fa5ab18f-26011d51-13c680-196140bf3061661',
#     'tfstk': 'gcXnKhZa_6RQ4uQxJNJQiBAdvPVTAD9WoaHJyLLz_F8sJ2Hd4L8lzFBpJMpEzYbk5XHLAQQMqNSXwLpLO3mCIZD-pyNC4YvJUrUYH-IBvL9zkcad56iB23hrU4drbFJJqNlC4djCALi6xZSfPMgomUD18L7yQC-JVL-rUYribnYZL3ke4VrMVFJrzeJr_F-D4HJyUaSaj3TwzA3EbeQPROz6U9AuBHDhGHAHuM8FvMBZlChC4FqabOfpKEykSYkPIHjtax1qn7LVGedvlNytKLjwqNAAtrDhrgSfaCXo8kQV4w6MdKV8AIfN6sdhsykkW9KkgLRi4YSMIF_cBKyqSh1Nv_WC-0DyA9BvZEOg4YOJQtdVgwm7cGJe4aOferMB8gSfhsp0Kqth_ivG4LGZghjsFhrRQbGWThtMknhlAvrp6eD4jlcVGB-6Y-EgjbGWThtMklqigrOefHyA.',
#     'acw_tc': '0a47308817441951581953909e003f9ca72aa9e11dee85309b304ce6d8c6e1',
#     'CNZZDATA1254842228': '51069784-1744093050-%7C1744195242',
# }
# json_data = {
#     'keyNo': '9cce0780ab7644008b73bc2120479d31',
#     'pageIndex': 2,
#     'isNewAgg': True,
#     'isAggs': True,
# }
# post_response(url, key_no, pid, tid, cookies, json_data)


