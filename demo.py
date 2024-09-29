import requests

cookies = {
    'HMF_CI': 'b51b612efcab0fb27c3cf129d01b6f574f5c35286ebd064f20911ab85ac8b3639e702123686829fff908b7e875e092409b1eedcc0018acdbfec8209331613918b3',
    'HMY_JC': 'd7fa43c36a22fe7c4525116585ac9562f6f1cf631006ba0ca8684370c44b3e48ce,',
    '_trs_uv': 'm1n0z125_4878_bybu',
    '_trs_ua_s_1': 'm1n0z124_4878_au31',
    'HBB_HC': '28ad45e10ced27acabad00019230299b571d6a16f4fa5e35f3ad63db9cabfb333afe529f9d8dd530042bfebc7adac70097',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'HMF_CI=b51b612efcab0fb27c3cf129d01b6f574f5c35286ebd064f20911ab85ac8b3639e702123686829fff908b7e875e092409b1eedcc0018acdbfec8209331613918b3; HMY_JC=d7fa43c36a22fe7c4525116585ac9562f6f1cf631006ba0ca8684370c44b3e48ce,; _trs_uv=m1n0z125_4878_bybu; _trs_ua_s_1=m1n0z124_4878_au31; HBB_HC=28ad45e10ced27acabad00019230299b571d6a16f4fa5e35f3ad63db9cabfb333afe529f9d8dd530042bfebc7adac70097',
    'Origin': 'https://jjjcb.ccdi.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://jjjcb.ccdi.gov.cn/epaper/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'docPubTime': '20240929',
}

response = requests.post('https://jjjcb.ccdi.gov.cn/reader/layout/findBmMenu.do',  cookies=cookies, headers=headers, data=data)
print(response.text)