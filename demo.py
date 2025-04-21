import requests

cookies = {
    'Hm_lvt_0ebc0266344b7e1dbda8f61a3a7ee5a1': '1744954682',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'Hm_lpvt_0ebc0266344b7e1dbda8f61a3a7ee5a1': '1744958141',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Client-Id': 'gxcq',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'http://ljs.gxcq.com.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'Cookie': 'Hm_lvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1744954682; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1744958141',
}

params = {
    'assetsId': '7d44b2065be64dc7ad2c859842dcd222',
    'n': '0.8934065628209489',
}

response = requests.get(
    'http://ljs.gxcq.com.cn/api/dscq-project/assets-detail/normal-detail',
    params=params,
    cookies=cookies,
    headers=headers,
    verify=False,
)
print(response.json())