import time
from datetime import datetime

import requests
import json
from queue import Queue
from threading import Thread
import mysql.connector
import hashlib
import redis

# 连接到redis数据库
redis_conn = redis.Redis()

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
    "ktrqBegin": "20240724",
    "ktrqEnd": "20250731",
    "pageSize": 80,
    "slfy": "21"
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data)
print(response.json())

total_page = response.json()["data"]["pages"]
print(f"总页数{total_page}")


def run():
    while not task_queue.empty():
        page = task_queue.get()
        url = "https://lnsfw.lnsfy.gov.cn//lawsuit/api/case-center/v1/third/court/external/getCourtAnnouncementInfo"
        data = {
            "ah": "",
            "curPage": page,
            "ktrqBegin": "20240724",
            "ktrqEnd": "20250731",
            "pageSize": 80,
            "slfy": "21"
        }
        print(f"当前爬取{page}页")
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=headers, data=data)
        time.sleep(1)
        for item in response.json()["data"]["records"]:
            # 案号
            case_no = item["ah"]
            # 案由
            cause = item["ay"]
            # 法院
            court = item["fymc"]
            # 当事人
            members = item["dsr"]
            # 内容
            # content = item["zxnr"]

            # 开庭时间
            open_time = item["ktrq"] + " " + item["kssj"]
            # 开庭地点
            court_room = item["ktft"]
            # 审判长
            room_leader = item["cbrDesc"]
            # 部门
            department = item["cbbmDesc"]
            # url = "https://lnsfw.lnsfy.gov.cn/lnssfw/pages/gsgg/gglist.html?lx=ktgg"
            # 发布时间
            # release_date = item["ktrq"]
            # update_time = item["gxsj"]
            # 设置创建时间
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 设置创建日期
            create_date = datetime.now().strftime('%Y-%m-%d')
            # 来源
            origin = "https://lnsfw.lnsfy.gov.cn/lnssfw/pages/gsgg/gglist.html?lx=ktgg"
            # 来源域名
            origin_domain = "lnsfw.lnsfy.gov.cn"
            data = f"案号：{case_no}, Cause: {cause}, 法院: {court}, 当事人: {members}, 开庭时间: {open_time}, 开庭地点: {court_room}, 审判长: {room_leader}, 部门: {department},来源: {origin}, 来源域名: {origin_domain}"
            # 数据去重
            hash_value = hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()
            # 判断唯一的哈希值是否在集合中
            if not redis_conn.sismember("liaoning_set", hash_value):
                # 不重复哈希值添加到集合中
                redis_conn.sadd("liaoning_set", hash_value)
                print("新数据：", data)
                # 连接到测试库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col_test"
                )
                cursor_test = conn_test.cursor()
                # 将数据插入到case_open_copy1表中
                insert_sql = "INSERT INTO case_open_copy1 (case_no, cause, court, members, open_time, court_room, room_leader, department,  origin, origin_domain, create_time, create_date) VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql, (
                    case_no, cause, court, members, open_time, court_room, room_leader, department,
                    origin,
                    origin_domain, create_time, create_date))
                print("插入成功")
                conn_test.commit()
                cursor_test.close()
                conn_test.close()
            else:
                print("重复数据：", data)


if __name__ == '__main__':
    task_queue = Queue()

    for page in range(1, total_page):
        task_queue.put(page)

    t_list = []
    for i in range(3):
        t = Thread(target=run)
        t_list.append(t)
        t.start()

    for t in t_list:
        t.join()
