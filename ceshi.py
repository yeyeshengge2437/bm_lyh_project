import time
from datetime import datetime, timedelta

import requests
from lxml import etree
import re

headers_date = {
    "accept": "application/xml, text/xml, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

for year in range(2023, 2025):
    # 获取当前年月
    for month in range(1, 13):
        if month < 10:
            month = f"0{month}"
        year_month = f"{year}-{month}"
        url = f"https://kjb.zjol.com.cn/html/{year_month}/paper_existed.xml"
        params = {
            "time": "Wed Aug 07 2024 17:48:42 GMT 0800 (中国标准时间)"
        }
        response = requests.get(url, headers=headers_date, params=params)
        time.sleep(1)
        html_content = response.content.decode()
        datas = re.findall(r'<period_date>(.*?)</period_date>.*?<front_page>(.*?)</front_page>', html_content, re.S)
        for data in datas:
            year_month_day = data[0].split('-')
            url = f'https://kjb.zjol.com.cn/html/{year_month_day[0]}-{year_month_day[1]}/{year_month_day[2]}/{data[1]}'
            print(url)

try:
    pass
except Exception as e:
    pass