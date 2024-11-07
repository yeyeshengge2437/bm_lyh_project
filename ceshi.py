import requests

cookies = {
    '_trs_uv': 'm1n0z125_4878_bybu',
    'HMF_CI': 'b51b612efcab0fb27c3cf129d01b6f576d0c929838ef33795b2a3248fab5cf3237ef343d0a656219569221d9889767da80671c1052806a443aae5a45b359153801',
    'HMY_JC': 'f9c952a99e74b7b8db90062bba84e331e73760f235814dd7bc94a6b1224e047723,',
    '_trs_ua_s_1': 'm36zeb1j_4878_bqb7',
    'HBB_HC': 'b87b5c43a9290d26ce3b2333435d134b7a6f450e714f503071fdc1c253d222b3a8b0d5a9acd1cb377d3b634eab3a0b07d3',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_trs_uv=m1n0z125_4878_bybu; HMF_CI=b51b612efcab0fb27c3cf129d01b6f576d0c929838ef33795b2a3248fab5cf3237ef343d0a656219569221d9889767da80671c1052806a443aae5a45b359153801; HMY_JC=f9c952a99e74b7b8db90062bba84e331e73760f235814dd7bc94a6b1224e047723,; _trs_ua_s_1=m36zeb1j_4878_bqb7; HBB_HC=b87b5c43a9290d26ce3b2333435d134b7a6f450e714f503071fdc1c253d222b3a8b0d5a9acd1cb377d3b634eab3a0b07d3',
    'Origin': 'https://jjjcb.ccdi.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://jjjcb.ccdi.gov.cn/epaper/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'docPubTime': '20241103',
}

response = requests.post('https://jjjcb.ccdi.gov.cn/reader/layout/findBmMenu.do', cookies=cookies, headers=headers, data=data)
print(response.text)