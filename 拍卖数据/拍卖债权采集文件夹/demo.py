import requests

cookies = {
    'Hm_lvt_263a15f1b2e57ebc22960d3fa7c5537e': '1742349542,1742785191',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'HWWAFSESTIME': '1742785201457',
    'HWWAFSESID': 'a69c173ba6d111fb8a',
    'pids': '3715887-5058583-5078057-5193907-5411677-5382935-5513977-5513982-5513989-5750904',
    'Hm_lpvt_263a15f1b2e57ebc22960d3fa7c5537e': '1742866238',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://zc.gpai.net/zc/detail?id=3715887',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'ut': 'null',
    # 'Cookie': 'Hm_lvt_263a15f1b2e57ebc22960d3fa7c5537e=1742349542,1742785191; HMACCOUNT=FDD970C8B3C27398; HWWAFSESTIME=1742785201457; HWWAFSESID=a69c173ba6d111fb8a; pids=3715887-5058583-5078057-5193907-5411677-5382935-5513977-5513982-5513989-5750904; Hm_lpvt_263a15f1b2e57ebc22960d3fa7c5537e=1742866238',
}

response = requests.get(
    'https://zc.gpai.net/zc/api/item/item?info=%7B%22id%22:%223715887%22%7D',
    cookies=cookies,
    headers=headers,
)
print(response.json())
