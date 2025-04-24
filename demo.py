import requests

cookies = {
    'JSESSIONID': '6A598DE43B2900E10AF0DF9EE48FB248',
    'Hm_lvt_f2b90fd96a52d3f32c2685f6e3f3e93b': '1745389440',
    'Hm_lpvt_f2b90fd96a52d3f32c2685f6e3f3e93b': '1745389440',
    'HMACCOUNT': 'FDD970C8B3C27398',
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': 'JSESSIONID=6A598DE43B2900E10AF0DF9EE48FB248; Hm_lvt_f2b90fd96a52d3f32c2685f6e3f3e93b=1745389440; Hm_lpvt_f2b90fd96a52d3f32c2685f6e3f3e93b=1745389440; HMACCOUNT=FDD970C8B3C27398',
}

response = requests.get(
    'https://cqjy.jxggzyjy.cn/uc/upload//atta//20240628/1719562099953.xlsx',
    # cookies=cookies,
    headers=headers,
)
print(response.content)
print(response.status_code)
# https://cqjy.jxggzyjy.cn/uc/upload//atta//20250314/1741938691695.xlsx
# http://cqjy.jxggzyjy.cn/uc/upload//atta//20240628/1719562099953.xlsx