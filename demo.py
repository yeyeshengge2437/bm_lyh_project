import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://dkjgfw.mnr.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://dkjgfw.mnr.gov.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'dwGuid': None,
}

response = requests.post(
    'https://dkjgfw.mnr.gov.cn/dks-webapi/site/DzkcAbnormalList/listNoLand',
    headers=headers,
    json=json_data,
)
print(response.json())
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"dwGuid":null}'
#response = requests.post('https://dkjgfw.mnr.gov.cn/dks-webapi/site/DzkcAbnormalList/listNoLand', headers=headers, data=data)