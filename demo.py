import requests
import time
url = "https://www.gwamcc.com/Ajax/GetTjieInfo.ashx"

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Referer": "https://www.gwamcc.com/MCInfo.aspx?liName=101",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

cookies = {
    "ASP.NET_SessionId": "qicyv4ne2etv4ncaqcowgmos"
}


timestamp = int(time.time() * 1000)
params = {
    "t": str(timestamp),
    "pSize": "100",
    "pIndex": "1",
    "_": str(timestamp - 100)  # 示例差值
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    cookies=cookies
)

# 输出响应内容
print(response.status_code)
print(response.json())  # 如果是 JSON 响应