import time

import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import requests
import datetime

co = ChromiumOptions().headless()

page = ChromiumPage(co)

page.get('https://ols.gzinternetcourt.gov.cn/#lassen/guangzhou/announcement')
cookie = {}
cookie_data = page.cookies()
for cookies in cookie_data:
    # 向字典中插入键值对
    cookie[cookies['name']] = cookies["value"]

# 使用datetime获取当前年月日
# 获取当前日期
today = datetime.date.today()

# 获取七天后的日期
seven_days_later = today + datetime.timedelta(days=30)
print(today, seven_days_later)

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://ols.gzinternetcourt.gov.cn",
    "Pragma": "no-cache",
    "Referer": "https://ols.gzinternetcourt.gov.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://ols.gzinternetcourt.gov.cn/portal/indexRpc/queryCourtTrialVos.json"

data = {
    "filterMap": f'{{"key":"","beginTime":"{today}","endTime":"{seven_days_later}","page":{{"begin":0,"length":10}}}}'
}
# 优化data

response = requests.post(url, headers=headers, cookies=cookie, data=data)

overall_data = response.text
print(overall_data)
count = response.json()['content']['count']
count_page = count // 10 + 1
print(count_page)

for i in range(1, count_page + 1):
    time.sleep(2)
    data = {
        "filterMap": f'{{"key":"","beginTime":"{today}","endTime":"{seven_days_later}","page":{{"begin":10,"length":10}}}}'
    }
    response = requests.post(url, headers=headers, cookies=cookie, data=data)
    print(response.text)

