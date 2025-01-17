import requests

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219222f3b4cd57d-00aecf78074de38-26001151-1296000-19222f3b4cea6c%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyMjJmM2I0Y2Q1N2QtMDBhZWNmNzgwNzRkZTM4LTI2MDAxMTUxLTEyOTYwMDAtMTkyMjJmM2I0Y2VhNmMifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219222f3b4cd57d-00aecf78074de38-26001151-1296000-19222f3b4cea6c%22%7D',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219222f3b4cd57d-00aecf78074de38-26001151-1296000-19222f3b4cea6c%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyMjJmM2I0Y2Q1N2QtMDBhZWNmNzgwNzRkZTM4LTI2MDAxMTUxLTEyOTYwMDAtMTkyMjJmM2I0Y2VhNmMifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219222f3b4cd57d-00aecf78074de38-26001151-1296000-19222f3b4cea6c%22%7D',
    'Pragma': 'no-cache',
    'Referer': 'https://e.xzxw.com/xzrb/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://e.xzxw.com/xzrb/202501/16/node_01.html', cookies=cookies, headers=headers)
print(response.text)
