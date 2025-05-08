import requests

cookies = {
    'isClick': 'true',
    '_gscu_1690858230': '465874802plhug63',
    '_gscbrs_1690858230': '1',
    '_gscs_1690858230': '465874808n5blo63|pv:1',
    'JSESSIONID': '0000yWb8jvqsDFzHpQSvFoHlLkD:-1',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://xkz.nfra.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://xkz.nfra.gov.cn/jr/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'isClick=true; _gscu_1690858230=465874802plhug63; _gscbrs_1690858230=1; _gscs_1690858230=465874808n5blo63|pv:1; JSESSIONID=0000yWb8jvqsDFzHpQSvFoHlLkD:-1',
}

params = {
    'useState': '3',
    'organNo': '',
    'fatherOrganNo': '',
    'province': '',
    'orgAddress': '',
    'organType': '',
    'branchType': '',
    'fullName': '中国建设银行股份有限公司北京密云支行',
    'address': '',
    'flowNo': '',
    'jrOrganPreproty': '',
}

data = {
    'start': '0',
    'limit': '10',
}

response = requests.post(
    'https://xkz.nfra.gov.cn/jr/kCEXOP/getLicence.do',
    params=params,
    # cookies=cookies,
    headers=headers,
    data=data,
)
print(response.content.decode('utf-8'))
