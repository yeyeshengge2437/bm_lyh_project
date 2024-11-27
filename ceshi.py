import requests

cookies = {
    'JSESSIONID': 'DB2A56972D6A8AEF1C99FDB201088922',
    'wzws_sessionid': 'gDExNy44OS4yLjExNKBnRbmigmQxMGJjZYFmNTFiYjQ=',
    'pcxxw': '5529501c709dbfb32f534d3d4a825990',
    'JSESSIONID': '187000E09F5215C3DA9ECD1DF9B55FEA',
    'wzws_cid': '7ed366089abb683952e80bcdc9c1bf307498536e549c0b24105005883dc209d075a7c297c369160b1accfd10fd7637ffc0df504d30fad2218b2f19fb2a7bc1718fe414df8c9be772fe9ca0accbaa4989',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=DB2A56972D6A8AEF1C99FDB201088922; wzws_sessionid=gDExNy44OS4yLjExNKBnRbmigmQxMGJjZYFmNTFiYjQ=; pcxxw=5529501c709dbfb32f534d3d4a825990; JSESSIONID=187000E09F5215C3DA9ECD1DF9B55FEA; wzws_cid=7ed366089abb683952e80bcdc9c1bf307498536e549c0b24105005883dc209d075a7c297c369160b1accfd10fd7637ffc0df504d30fad2218b2f19fb2a7bc1718fe414df8c9be772fe9ca0accbaa4989',
    'Pragma': 'no-cache',
    'Referer': 'https://pccz.court.gov.cn/pcajxxw/pcws/wsxq?id=CB4A756E6FFF011C66BA9C76BA4B4EF5',
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

params = {
    'id': 'CB4A756E6FFF011C66BA9C76BA4B4EF5',
}

response = requests.get('https://pccz.court.gov.cn/pcajxxw/pcws/wsxq', params=params, cookies=cookies, headers=headers)
print(response.text)
