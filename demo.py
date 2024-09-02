import requests


headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '__jsluid_s=97ef77e01505c53919b77048e0d148c5; Hm_lvt_54db9897e5a65f7a7b00359d86015d8d=1722564716,1724919146; Hm_lpvt_54db9897e5a65f7a7b00359d86015d8d=1724919146; HMACCOUNT=FDD970C8B3C27398; SHAREJSESSIONID=7a857d55-1dcc-450c-b0e9-bd09157a6582',
    'Origin': 'https://cfws.samr.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://cfws.samr.gov.cn/list.html?21_s=110101',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

datas = {
    'pageSize': '200',
    'pageNum': '1',
    'queryCondition': '[{"key":"3_s", "id":"08", "name":"无证无照经营 "}]',
    'sortFields': '',
    'ciphertext': '1101101 1001110 111000 1101010 1100100 1100011 110101 1101000 1010001 1101110 1011000 1001001 1100010 1011001 1101100 1111001 1001000 1101010 110010 1001000 1001000 110011 110111 1101010 110010 110000 110010 110100 110000 111000 110011 110000 1010101 1101010 1100001 1101110 1100110 1010011 1001100 1010000 1010110 1101111 1101110 1001101 1101010 1101011 110010 1101000 1000100 1110010 1011000 1110101 1101101 1010001 111101 111101',
}
data = {
    'pageSize': '20',
    'pageNum': '1',
    'queryCondition': '',
    'sortFields': '',
    'ciphertext': '111000 1110010 1110110 1100001 110101 1010101 1101000 1101000 1000011 1000110 1110010 1101011 1110111 1001111 1000110 1011001 1101101 1110001 1111000 1001100 1100011 1100011 110111 110010 110010 110000 110010 110100 110000 111001 110000 110010 1110011 1010101 101111 1011001 110011 1100010 1100001 1110011 1001011 1110001 1101110 1010010 1001100 1101010 1110011 1010101 101111 1110010 1001111 111000 111000 1000001 111101 111101',
}
response = requests.post('https://cfws.samr.gov.cn/queryDoc', headers=headers, data=data)

print(response.json())
