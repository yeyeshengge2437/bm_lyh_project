import requests

cookies = {
    'acw_tc': '2760820417410906427174471ed88d7993f3ca6efcf66df4121f94765e5de9',
    'BIGipServerszee.com.cn_New': '187934912.36895.0000',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'acw_tc=2760820417410906427174471ed88d7993f3ca6efcf66df4121f94765e5de9; BIGipServerszee.com.cn_New=187934912.36895.0000',
}

response = requests.get('https://www.szee.com.cn/jrzc/', headers=headers)
print(response.content.decode())
