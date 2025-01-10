import datetime
import time

import mysql.connector
import requests
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_gdcourt_info(from_queue, webpage_id):
    origin = "广东法院网"
    origin_domain = "gdcourts.gov.cn"
    for page in range(1, 500 + 1):
        if page == 1:
            url = 'https://www.gdcourts.gov.cn/ktgg/index.html'
        else:
            url = f'https://www.gdcourts.gov.cn/ktgg/index_{page}.html'
        response = requests.get(url, headers=headers)
        time.sleep(2)
        res = response.text
        res_html = etree.HTML(res)
        kt_list = res_html.xpath('//tr')
        for kt in kt_list[1:]:
            open_time = ''.join(kt.xpath('./td[1]//text()'))
            court_str = ''.join(kt.xpath('./td[2]//text()'))
            court_str_list = court_str.split('\n')
            court_name = court_str_list[0]
            court_room = court_str_list[1]
            case_no = ''.join(kt.xpath('./td[3]/a//text()'))
            url = ''.join(kt.xpath('./td[3]/a//@href'))

            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 设置创建日期
            create_date = datetime.datetime.now().strftime('%Y-%m-%d')
            # 连接到测试库
            conn_test = mysql.connector.connect(
                host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col"
            )
            cursor_test = conn_test.cursor()
            # 将数据插入到表中
            insert_sql = "INSERT INTO col_case_open (case_no, court,  open_time, court_room, origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,%s,%s,%s, %s,%s, %s, %s, %s, %s,)"

            cursor_test.execute(insert_sql, (
                case_no, court_name, open_time, court_room,
                origin,
                origin_domain, create_time, create_date, from_queue, webpage_id))
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 设置创建日期
            create_date = datetime.datetime.now().strftime('%Y-%m-%d')
            department = ''
            # 连接到测试库
            conn_test = mysql.connector.connect(
                host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col"
            )
            cursor_test = conn_test.cursor()
            # 将数据插入到表中
            insert_sql = "INSERT INTO col_case_open (case_no,  court,  open_time, court_room, department, origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor_test.execute(insert_sql, (
                case_no, court_name, open_time, court_room,
                department,
                origin,
                origin_domain, create_time, create_date, from_queue, webpage_id))
            # print("插入成功")
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
            print(f"开庭时间：{open_time}, 法院：{court_name}, 地点：{court_room}, 案号：{case_no}, 链接：{url}")

