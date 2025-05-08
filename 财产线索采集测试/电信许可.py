import requests

cookies = {
    'jsessionid': 'rBQtExroaBsYrmW3nEFL6U6Gu4iiUz9YASgA',
    'ariauseGraymode': 'false',
    'wzws_sessionid': 'gTMzZDBmMqBoGgTwgjBhZjRiMoAxMTcuODkuMi43OQ==',
    'route': '1746535729.943.105318.438572',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://dxzhgl.miit.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://dxzhgl.miit.gov.cn/dxxzsp/xkz/xkzgl/resource/qiyesearch.jsp?num=%25E5%25B0%258F%25E7%25B1%25B3%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E8%25B4%25A3%25E4%25BB%25BB%25E5%2585%25AC%25E5%258F%25B8&type=xuke',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'jsessionid=rBQtExroaBsYrmW3nEFL6U6Gu4iiUz9YASgA; ariauseGraymode=false; wzws_sessionid=gTMzZDBmMqBoGgTwgjBhZjRiMoAxMTcuODkuMi43OQ==; route=1746535729.943.105318.438572',
}

params = {
    'pageNum': '1',
    'pageSize': '10',
}

data = {
    'num': '小米科技有限责任公司',
    'type': 'xuke',
}

response = requests.post(
    'https://dxzhgl.miit.gov.cn/dxxzsp/corpinfo/getcorpinfo.wf',
    params=params,
    # cookies=cookies,
    headers=headers,
    data=data,
)
print(response.content.decode('utf-8'))