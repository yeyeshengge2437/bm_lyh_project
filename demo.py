import requests

cookies = {
    'recordurl': '%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject26427.html%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Findex.php%253Fclass3%253D52%2526page%253D100%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.prechina.net/project/project.php?class3=52',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'recordurl=%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject26427.html%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Findex.php%253Fclass3%253D52%2526page%253D100%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52',
}

params = {
    'class3': '52',
    'page': '2',
}

response = requests.get('https://www.prechina.net/project/index.php', params=params, cookies=cookies, headers=headers)
print(response.text)