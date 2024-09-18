import json

import requests


headers = {
    'ADMIN_ALLOW': '',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'BROWER_LANGUAGE': 'zh-CN',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'Hm_lvt_9b2a01de93671e1d3edfbffeda9b89f9=1724146656; VISIT_TAG=1726623174026; JSESSIONID=AF604898867BC95AFD5439EFDD2C7057',
    'Origin': 'http://ipaper.pagx.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://ipaper.pagx.cn/bz/html/index.html?date=2024-04-08&pageIndex=4&cid=1',
    'SCREEN': '900x1440',
    'SITE': 'gxfzb',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'myIdentity': '9195459e-c0be-47fd-8c0f-552e11cba122',
}
paper_time = "2024-04-08"
data_json = {"from":0,"size":999,"query":{"bool":{"must":[{"term":{"columns.id":1}},{"term":{"bz.date_date_sore":paper_time}}]}},"sort":[{"index_int_sore":{"order":"asc"}}]}
data_json = json.dumps(data_json)
data = {
    'index': 'bz_page',
    'query': data_json,
}

response = requests.post('http://ipaper.pagx.cn/data/query', headers=headers, data=data, verify=False)
print(response.json())