# 获取京东招商中的链接
import json
import os
import time
from typing import Dict

import requests


def save_to_json(data: Dict, filename: str = "data.json") -> None:
    """
    将数据追加到 JSON 文件，每次保存完整数据
    :param data: 要保存的字典数据，需包含 url, url_name, state
    :param filename: JSON 文件名 (默认: data.json)
    """
    # 如果文件不存在则初始化空列表
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)

    # 读取现有数据
    with open(filename, 'r') as f:
        existing_data = json.load(f)

    # 检查重复（根据 url 去重）
    urls = {item['url'] for item in existing_data}
    if data['url'] not in urls:
        existing_data.append(data)
    else:
        # 如果已存在，可以选择更新状态（可选）
        for item in existing_data:
            if item['url'] == data['url']:
                item.update(data)
                break

    # 写入更新后的数据
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=True)


cookies = {
    '__jdu': '17219744346561554622123',
    'mba_muid': '17219744346561554622123',
    'shshshfpa': '90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570',
    'shshshfpx': '90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570',
    'light_key': 'AASBKE7rOxgWQziEhC_QY6yaB3PQ6pVpcy9uYd_PD0N1ReA0e-l3oBNJnSJd3xypi9G1dQ3H',
    'pin': 'qwertyuiop2437',
    'unick': 'nty47n2qtsb0ac',
    'TrackID': '1XApSoDl49V6MFvfHdLb-v1mjxgdjA_vFF7jJh1jU97Jm8vz4rjO9x1nHnGMMR0C9i6PK-n2uG17cNBI7ZbQ0WcBipZDtqz2esLSm7LfTGK0|||GoDjOYOhdgEboMHtDlun2Q',
    'pinId': 'GoDjOYOhdgEboMHtDlun2Q',
    '__jdv': '96383255|baidu|-|organic|notset|1741655240850',
    'joyya': '1741673531.1741673815.21.1is84qr',
    'RT': '"z=1&dm=jd.com&si=4iqr2zcnp5q&ss=m85bm3ra&sl=0&tt=0&r=8a72d04d1c1858ccd327b87ff7dfb81d&ul=12f68&hd=12f74"',
    'shshshfpb': 'BApXS_4JgjvBAOjIe0u_EfeI01o8m0OKABnJ0cl9o9xJ1Mv8SPoG2',
    '__jd_ref_cls': 'LoginDisposition_Go',
    'jcap_dvzw_fp': 'tRyvbuoZufpryigwQ6_IIislWWGZ6Y6aRtwEC7eqiByFJ97hrGyE5mra9RTnFMk4DxeQfrv-FASUctjl946k_Q==',
    'x-rp-evtoken': 'mGW9U4qbzsaBdCMe70m9pDuTjiz3piFqsCwDvZ27ENXDYBL4AxLLg32ouMB5v6uArvatCzpZFMXnU2aIaYLhSw%3D%3D',
    '_gia_d': '1',
    '3AB9D23F7A4B3CSS': 'jdd03V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPIAAAAMVRX7G7GQAAAAADIHXAMLKRBH6RUX',
    '__jda': '128418189.17219744346561554622123.1721974435.1741832547.1741844017.26',
    '__jdb': '128418189.2.17219744346561554622123|26.1741844017',
    '__jdc': '128418189',
    'flash': '3_X_8iXbzkemy3jEDqj8VDsOA2ESN9INL_TpgBgYUm1D032nqALAZUexXxtJEEkhjJHZ2uFYHvUoiXOGNetD5QDa_Pevj-DD385LSLUf4UfWi8HNZvnIqa7aqhrNa78w0nnNarCQeTS6_dULAwUsCsyurag8wI1f7Lw3qqreLwokW420M*',
    '3AB9D23F7A4B3C9B': 'V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPI',
    'sdtoken': 'AAbEsBpEIOVjqTAKCQtvQu17dM1jxVG_QCwPRz30NnS3EYIsVigxdObqm2b1pEeeSmss7kRi0gvyvmFvx7BxH4hCGPYbctSas_Ve-XOD-qgYXdpYZtZ33CZeiaHK9pGWKMb7XzbYFqLM',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    # 'referer': 'https://pmsearch.jd.com/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    # 'cookie': '__jdu=17219744346561554622123; mba_muid=17219744346561554622123; shshshfpa=90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570; shshshfpx=90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570; light_key=AASBKE7rOxgWQziEhC_QY6yaB3PQ6pVpcy9uYd_PD0N1ReA0e-l3oBNJnSJd3xypi9G1dQ3H; pin=qwertyuiop2437; unick=nty47n2qtsb0ac; TrackID=1XApSoDl49V6MFvfHdLb-v1mjxgdjA_vFF7jJh1jU97Jm8vz4rjO9x1nHnGMMR0C9i6PK-n2uG17cNBI7ZbQ0WcBipZDtqz2esLSm7LfTGK0|||GoDjOYOhdgEboMHtDlun2Q; pinId=GoDjOYOhdgEboMHtDlun2Q; __jdv=96383255|baidu|-|organic|notset|1741655240850; joyya=1741673531.1741673815.21.1is84qr; RT="z=1&dm=jd.com&si=4iqr2zcnp5q&ss=m85bm3ra&sl=0&tt=0&r=8a72d04d1c1858ccd327b87ff7dfb81d&ul=12f68&hd=12f74"; shshshfpb=BApXS_4JgjvBAOjIe0u_EfeI01o8m0OKABnJ0cl9o9xJ1Mv8SPoG2; __jd_ref_cls=LoginDisposition_Go; jcap_dvzw_fp=tRyvbuoZufpryigwQ6_IIislWWGZ6Y6aRtwEC7eqiByFJ97hrGyE5mra9RTnFMk4DxeQfrv-FASUctjl946k_Q==; x-rp-evtoken=mGW9U4qbzsaBdCMe70m9pDuTjiz3piFqsCwDvZ27ENXDYBL4AxLLg32ouMB5v6uArvatCzpZFMXnU2aIaYLhSw%3D%3D; _gia_d=1; 3AB9D23F7A4B3CSS=jdd03V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPIAAAAMVRX7G7GQAAAAADIHXAMLKRBH6RUX; __jda=128418189.17219744346561554622123.1721974435.1741832547.1741844017.26; __jdb=128418189.2.17219744346561554622123|26.1741844017; __jdc=128418189; flash=3_X_8iXbzkemy3jEDqj8VDsOA2ESN9INL_TpgBgYUm1D032nqALAZUexXxtJEEkhjJHZ2uFYHvUoiXOGNetD5QDa_Pevj-DD385LSLUf4UfWi8HNZvnIqa7aqhrNa78w0nnNarCQeTS6_dULAwUsCsyurag8wI1f7Lw3qqreLwokW420M*; 3AB9D23F7A4B3C9B=V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPI; sdtoken=AAbEsBpEIOVjqTAKCQtvQu17dM1jxVG_QCwPRz30NnS3EYIsVigxdObqm2b1pEeeSmss7kRi0gvyvmFvx7BxH4hCGPYbctSas_Ve-XOD-qgYXdpYZtZ33CZeiaHK9pGWKMb7XzbYFqLM',
}


def get_data(page_num, pro_id):
    url = "https://api.m.jd.com/api"
    page_num = int(page_num)
    body = {"investmentType": "", "apiType": 12, "page": page_num, "pageSize": 200, "keyword": "", "provinceId": pro_id,
            "cityId": "", "countyId": "", "multiPaimaiStatus": "1", "multiDisplayStatus": "", "multiPaimaiTimes": "",
            "childrenCateId": "109", "currentPriceRangeStart": "", "currentPriceRangeEnd": "",
            "timeRangeTime": "endTime", "timeRangeStart": "", "timeRangeEnd": "", "loan": "", "purchaseRestriction": "",
            "orgId": "", "orgType": "", "sortField": 9, "projectType": 2, "reqSource": 0, "labelSet": "",
            "publishSource": "", "publishSourceStr": [], "defaultLabelSet": ""}
    params = {
        "appid": "paimai",
        "functionId": "paimai_searchMerchantsProduct",
        "body": f"{body}",
        # "jsonp": "jsonp_1741844105627_11005"
    }
    response = requests.get(
        url,
        params=params,
        # cookies=cookies,
        headers=headers,
    )
    print(f'当前第{page_num}页')
    data_list = response.json()
    # time.sleep(3)
    print(data_list)
    datas = data_list["datas"]
    for data in datas:
        id_ = data["id"]
        url = f"https://auction.jd.com/zichan/tuijie/item/{id_}"
        url_name = data["name"]
        state = ''
        data_dict = {"url": url, "url_name": url_name, "state": state}
        save_to_json(data_dict, 'jd_attracting.json')
        print(data_dict)


for pro in range(1, 32 + 1):
    for page_num in range(1, 100):
        try:
            get_data(page_num, pro)
        except:
            break
