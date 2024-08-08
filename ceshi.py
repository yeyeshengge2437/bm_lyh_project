import requests


headers = {
    "accept": "application/xml, text/xml, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://kjb.zjol.com.cn/html/2024-08/06/node_2697.htm",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
# cookies = {
#     "SERVERID": "8f2d604e1b801b055f710f7f963e620a|1723024073|1723023414"
# }
url = "https://kjb.zjol.com.cn/html/2024-06/paper_existed.xml"
params = {
    "time": "Wed Aug 07 2024 17:48:42 GMT 0800 (中国标准时间)"
}
response = requests.get(url, headers=headers, params=params)

print(response.text)
print(response)