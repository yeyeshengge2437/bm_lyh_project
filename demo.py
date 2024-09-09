import requests

cookies = {
    'PHPSESSID': 'ep8hogskiaqug0s5ffmkbdr4ou',
    'Hm_lvt_67efac7eaac6d157b1e34ceb0dfc729b': '1725609865,1725848690',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'Hm_lpvt_67efac7eaac6d157b1e34ceb0dfc729b': '1725850065',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=ep8hogskiaqug0s5ffmkbdr4ou; Hm_lvt_67efac7eaac6d157b1e34ceb0dfc729b=1725609865,1725848690; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_67efac7eaac6d157b1e34ceb0dfc729b=1725850065',
    'Pragma': 'no-cache',
    'Referer': 'https://flbook.com.cn/c/UgPGexTKLq',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'v': '20240818211858',
}

response = requests.get(
    'https://flbook.com.cn/upload/pages/2024/08/2459076.html',
    headers=headers,
)
print(response.text)