import requests

cookies = {
    'uid': '1728368802373_8718772985',
    'zycna': 'JwwyRIkbYF0BAXPBuY3dtKaX',
    'Hm_lvt_b4ae0087f7b17481d650cc0a8574f040': '1728368802',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'Hm_lpvt_b4ae0087f7b17481d650cc0a8574f040': '1728369188',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'uid=1728368802373_8718772985; zycna=JwwyRIkbYF0BAXPBuY3dtKaX; Hm_lvt_b4ae0087f7b17481d650cc0a8574f040=1728368802; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_b4ae0087f7b17481d650cc0a8574f040=1728369188',
    'Pragma': 'no-cache',
    'Referer': 'https://jxzx.jxnews.com.cn/system/count//0052038/000000000000/000/000/c0052038000000000000_000000042.shtml',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'periodsName': '2024-09-24',
}

response = requests.post('https://app.lhwww.com.cn/epaperPc/getEditionNumByPeriods', cookies=cookies, headers=headers, data=data)
print(response.text)