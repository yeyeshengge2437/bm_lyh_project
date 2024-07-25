import time
from datetime import datetime

import requests
import json
from queue import Queue
from threading import Thread
import mysql.connector
import hashlib
import redis

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://lnsfw.lnsfy.gov.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
url = "https://lnsfw.lnsfy.gov.cn//lawsuit/api/case-center/v1/third/court/external/getCourtAnnouncementInfo"
data = {
    "ah": "",
    "curPage": 1,
    "ktrqBegin": "20240725",
    "ktrqEnd": "20241231",    "pageSize": 40,
    "slfy": "21"
}
# print(f"当前爬取1页")
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data)
data = response.json()
total = data["data"]["total"]
time.sleep(1)
print(f"打印数据总数{total}")
# for item in response.json()["data"]["records"]:
#     case_no = item["ah"]
#     cause = item["ay"]
#     court = item["fymc"]
#     members = item["dsr"]
#     # content = item["zxnr"]
#     # create_time = item["cjsj"]
#     # 开庭时间由item["ktrq"] 与 item["kssj"]拼接
#     open_time = item["ktrq"] + " " + item["kssj"]
#
#     court_room = item["ktft"]
#     room_leader = item["cbrDesc"]
#     department = item["cbbmDesc"]
#     url = "https://lnsfw.lnsfy.gov.cn/lnssfw/pages/gsgg/gglist.html?lx=ktgg"
#     release_date = item["ktrq"]
#     # update_time = item["gxsj"]
#     # 设置创建时间
#     create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     # 设置创建日期
#     create_date = datetime.now().strftime('%Y-%m-%d')
#     origin = item['fymc']
#     origin_domain = "https://lnsfw.lnsfy.gov.cn"
#     data = f"案号：{case_no}, Cause: {cause}, 法院: {court}, 当事人: {members}, 开庭时间: {open_time}, 开庭地点: {court_room}, 审判长: {room_leader}, 部门: {department}, 发布时间: {release_date}, 来源: {origin}, 来源域名: {origin_domain}, url: {url}"
