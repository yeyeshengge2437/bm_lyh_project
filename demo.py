import requests

cookies = {
    'RK': 'nBU4TPDzwS',
    'ptcz': 'faead0bb4c470764ffd3e2db5cc6d80201eab8a69fa8b7777adea4dd0b0fcfc2',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'RK=nBU4TPDzwS; ptcz=faead0bb4c470764ffd3e2db5cc6d80201eab8a69fa8b7777adea4dd0b0fcfc2',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI5ODk2MTY1Mg==&action=getalbum&album_id=3421134606546747396',
    cookies=cookies,
    headers=headers,
)
print(response.text)