import time
from datetime import datetime

import requests
import json
from queue import Queue
from threading import Thread
import mysql.connector
import hashlib
import redis
from apscheduler.schedulers.blocking import BlockingScheduler

# 连接到redis数据库
redis_conn = redis.Redis()

# 隧道域名:端口号
tunnel = "x170.kdltps.com:15818"

# 用户名密码方式
username = "t12231186154417"
password = "kp1840rx"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}

import os
import json
import requests

produce_url = "http://121.43.164.84:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False


def paper_queue_next(webpage_url_list=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if webpage_url_list is None:
        webpage_url_list = []

    url = test_url + "/website/queue/next"
    data = {
        "webpage_url_list": webpage_url_list
    }

    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    print(result)
    return result.get("value")


def paper_queue_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = test_url + "/website/queue/success"
    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result.get("value")


def paper_queue_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    try:
        if data is None:
            data = {}
        url = test_url + "/website/queue/fail"
        data_str = json.dumps(data)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def upload_file_by_url(file_url, file_name, file_type, type="paper"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(file_url, headers=headers)
    if r.status_code != 200:
        return "获取失败"
    pdf_path = f"{file_name}.{file_type}"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}
    url = 'http://121.43.164.84:29775' + f"/file/upload/file?type={type}"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    return result.get("value")["file_url"]


value = paper_queue_next(webpage_url_list=['https://lnsfw.lnsfy.gov.cn/lnssfw/index.html'])
from_queue = value['id']
webpage_id = value["webpage_id"]


def execute(proxies_value=None):
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
    response = requests.post(url, headers=headers, data=data, proxies=proxies_value)
    # 获取状态码
    status_message = response.json()["message"]
    if status_message == '操作成功！':
        total_page = response.json()["data"]["pages"]
    else:
        return '网页问题'

    new_data_num = 0
    data_num = 0

    for page in range(1, total_page):
        url = "https://lnsfw.lnsfy.gov.cn//lawsuit/api/case-center/v1/third/court/external/getCourtAnnouncementInfo"
        data = {
            "ah": "",
            "curPage": page,
            "ktrqBegin": "20240724",
            "ktrqEnd": "20250731",
            "pageSize": 80,
            "slfy": "21"
        }

        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=headers, data=data, proxies=proxies_value)
        time.sleep(1)
        for item in response.json()["data"]["records"]:
            data_num += 1
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
            origin = "辽宁省法院诉讼服务网开庭公告"
            # 来源域名
            origin_domain = "lnsfw.lnsfy.gov.cn"
            data = f"案号：{case_no}"
            # 数据去重
            hash_value = hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()
            # 判断唯一的哈希值是否在集合中
            if not redis_conn.sismember("liaoning_set", hash_value):
                # 不重复哈希值添加到集合中
                redis_conn.sadd("liaoning_set", hash_value)
                # 连接到测试库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col"
                )
                cursor_test = conn_test.cursor()
                # 将数据插入到case_open_copy1表中
                insert_sql = "INSERT INTO col_case_open (case_no, cause, court, members, open_time, court_room, room_leader, department,  origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,  %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql, (
                    case_no, cause, court, members, open_time, court_room, room_leader, department,
                    origin,
                    origin_domain, create_time, create_date, from_queue, webpage_id))
                conn_test.commit()
                cursor_test.close()
                conn_test.close()
                new_data_num += 1
    now = datetime.now()
    print(f"时间:{now},本次爬取数据量：{data_num},本次爬取新增数据量：{new_data_num}")


max_attempts = 5  # 设置最大尝试次数
attempts = 0

while attempts < max_attempts:
    try:
        value = execute(proxies_value=None)
        if value == '网页问题':
            success_data = {
                "id": from_queue,
                'description': '网页自身问题',
            }
            paper_queue_success(success_data)
        else:
            success_data = {
                'id': from_queue,
                'description': '数据获取成功',
            }
            paper_queue_success(success_data)
        break
    except Exception as e:
        print(f"发生错误：{e}")
        attempts += 1  # 增加尝试次数
        time.sleep(3600)  # 等待一小时后再次尝试
        print(f"尝试再次爬取，尝试{attempts}/{max_attempts}")

    if attempts == max_attempts:
        fail_data = {
            "id": from_queue,
            'description': '程序问题',
        }
        paper_queue_fail(fail_data)
