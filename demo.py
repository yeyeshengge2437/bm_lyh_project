import requests

cookies = {
    'wdcid': '1a251cb3e8a14457',
    'Hm_lvt_49c45e27427f57a7e60091b5ade64058': '1726708745,1728539877',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'Hm_lvt_08261419fd973f118d693f2d1ce6e02b': '1726708745,1728539877',
    'wdses': '4e2ffd2145c3dcbe',
    'Hm_lpvt_08261419fd973f118d693f2d1ce6e02b': '1728540647',
    'wdlast': '1728540647',
    'Hm_lpvt_49c45e27427f57a7e60091b5ade64058': '1728540665',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'wdcid=1a251cb3e8a14457; Hm_lvt_49c45e27427f57a7e60091b5ade64058=1726708745,1728539877; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_08261419fd973f118d693f2d1ce6e02b=1726708745,1728539877; wdses=4e2ffd2145c3dcbe; Hm_lpvt_08261419fd973f118d693f2d1ce6e02b=1728540647; wdlast=1728540647; Hm_lpvt_49c45e27427f57a7e60091b5ade64058=1728540665',
    'Pragma': 'no-cache',
    'Referer': 'https://hzdaily.hangzhou.com.cn/mrsb/2024/10/01/page_detail_3_20241001A02.html',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(
    'https://hzdaily.hangzhou.com.cn/mrsb/2024/10/01/article_list_3_20241001A02.html',
    cookies=cookies,
    headers=headers,
)
print(response.content.decode())