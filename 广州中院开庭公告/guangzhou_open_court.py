import json
from datetime import datetime
import mysql.connector
import hashlib
import redis
import requests
from lxml import etree

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

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://www.gzcourt.gov.cn/fygg/index.html",
    "Sec-Fetch-Dest": "iframe",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

url = "https://www.gzcourt.gov.cn/wwfx/webapp/ktgg/ktggdata.jsp"
response = requests.get(url, headers=headers)
print("状态码：", response.status_code)
if response.status_code == 200:
    html = etree.HTML(response.text)
    # 获取全部开庭公告
    all_notice = html.xpath("//table[@class='pageTable']/tbody/tr[position()>1]")
    # 新增数据
    new_num = 0

    for notice in all_notice[:-1]:
        notice_info = notice.xpath("./td/text()")
        case_no = notice_info[4]
        cause = notice_info[5]
        court = notice_info[1]
        members = notice_info[6]
        open_time = notice_info[2].rstrip()
        # 分割日期和时间
        date_part = open_time[:8]
        time_part = open_time[8:]
        # 将日期部分格式化为 "YYYY-MM-DD"
        formatted_date = datetime.strptime(date_part, "%Y%m%d").strftime("%Y-%m-%d")
        # 将时间部分格式化为 "HH:MM"
        # formatted_time = time_part.replace(':', '')
        formatted_time = time_part
        # 合并日期和时间部分
        open_time = f"{formatted_date} {formatted_time}"
        court_room = notice_info[3]
        # 设置创建时间
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 设置创建日期
        create_date = datetime.now().strftime('%Y-%m-%d')
        # 来源
        origin = "广东省广州市中级人民法院"
        # 来源域名
        origin_domain = "gzcourt.gov.cn"
        data_unique = case_no
        # 数据去重
        hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
        # 判断唯一的哈希值是否在集合中
        if not redis_conn.sismember("guangzhou_set", hash_value):
            # 不重复哈希值添加到集合中
            redis_conn.sadd("guangzhou_set", hash_value)
            new_num += 1
            # 连接到测试库
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col"
            )
            cursor_test = conn_test.cursor()
            # 将数据插入到case_open_copy1表中
            insert_sql = "INSERT INTO case_open (case_no, cause, court, members, open_time, court_room,  origin, origin_domain, create_time, create_date) VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor_test.execute(insert_sql, (
                case_no, cause, court, members, open_time, court_room,
                origin,
                origin_domain, create_time, create_date))
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
    print("新增数据数：", new_num)
