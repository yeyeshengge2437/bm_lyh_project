import re

import execjs
import requests

# 这里补充一下cookies
cookies = {
    'qcc_did': 'aa80c299-a44e-4b99-bd8f-846f1f237214',
    'UM_distinctid': '191db1e9c1327b0-0fff366dedf7e-26001151-13c680-191db1e9c14297d',
    'QCCSESSID': '256acdafd4bcb3138feb7a3896',
    'tfstk': 'g9PIsj1JyHxQ-ltg-MQZcRul7nG7Vu1qVUg8ozdeyXhp23Uxb2PFxzn7VlogVYbn40n74zeF7s54-ycowQsVgs8Jc-wzO0KrwXc9koPVzs54-yHPvxclgW8jbYiI2bHKefUtjqKpJud-XNg-zHpJ9uUO5c0ryBHp9P3tPquKwbE8WNgoX0hz7BgNRc4CRDssFdYQmyn6wQFdZvibqLRJw5gId7UKfyaQ12MIDAR6iYPLbzFUtAXMQb4ahuw8DGJEv-gbfxyCcBZbx4EsTSQlKAD8N7ggIg9Sc8UUn8H1J6UsODM8_lL2IXw8x7M3dUb0WXEgnmDdIG0_TSkSmAtOvPzsvxw7YGA-Y-aTfxPwbIlYnlNSHjIrSIofpppWl1dS5m715LvuY6WJZ2v8oXHKSVSP5N94rv3i5m715LvopV0azN_63zf..',
    'acw_tc': '1a0c384c17390863891202078e0081d4afc3a1a5facc43cd38bc6f7a5aa404',
    'CNZZDATA1254842228': '1515781789-1725958102-https%253A%252F%252Fwww.zsamc.com%252F%7C1739086397',
}


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

    print(f"path: {path}")
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


def post_api(url, key_no, pid, tid, json_data=None):
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


def get_api(url, key_no, pid, tid, json_data=None):
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


if __name__ == '__main__':
    # 以某企业为例
    key_no = 'aee58eada8653b42219d5a49a0579668'
    pid = 'cdf1ed52eb66ae9a3604ca5de50dd168'
    tid = '1337360c2151ab8820984ba1bc4e9645'

    # 请求可能需要会员，如果没有会员可以访问其他不需要会员的接口
    # get请求
    page_index = 1
    get_url = f'https://www.qcc.com/api/datalist/noticelist?isNewAgg=true&keyNo=aee58eada8653b42219d5a49a0579668&KeyNo=aee58eada8653b42219d5a49a0579668&pageIndex=1'
    main_member = get_api(get_url, key_no, pid, tid).json()
    print(main_member)

    # # post请求
    # post_url = 'https://www.qcc.com/api/datalist/noticelist'
    # json_data = {
    #     'isNewAgg': 'true',
    #     'keyNo': 'aee58eada8653b42219d5a49a0579668',
    #     'KeyNo': 'aee58eada8653b42219d5a49a0579668',
    #     'pageIndex': '1',
    # }
    # financial = post_api(post_url, key_no, pid, tid, json_data=json_data).json()
    # print(financial)
