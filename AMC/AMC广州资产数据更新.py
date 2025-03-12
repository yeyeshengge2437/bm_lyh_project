# 131
import os
import re

import mysql.connector
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, paper_queue_next, \
    paper_queue_success, upload_file_by_url

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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def guangdong_gai(queue_id, webpage_id):
    conn_test_1 = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col"
    )

    cursor_test_1 = conn_test_1.cursor()
    cursor_test_1.execute(
        "select id, page_url, update_time, title from col_paper_notice where paper = '广州资产管理有限公司'")
    rows = cursor_test_1.fetchall()
    for id, page_url, update_time, title in rows:
        if update_time:
            continue
        if title == '肇庆夏威夷大酒店等132户不良债权资产处置公告':
            print(page_url, update_time, title)
            annex = str(["https://www.guangzhouamc.com/upload/37/cms/content/20250109/1736406296771.docx"])
            up_annex = str(["https://res.debtop.com/col/live/paper/202503/10/202503101729119da28e41816d4e88.docx"])

            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 上传到测试数据库
            conn_test = mysql.connector.connect(
                host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col",
            )
            cursor_test = conn_test.cursor()
            # file_url = upload_file_by_url(annex, "guangzhou", 'docx')
            # print(file_url)

            insert_sql = "UPDATE col_paper_notice SET from_queue=%s, update_time=%s, original_files=%s, files=%s WHERE id = %s"
            cursor_test.execute(insert_sql, (queue_id, update_time, annex, up_annex, id))
            conn_test.commit()

            cursor_test.close()
            conn_test.close()

    cursor_test_1.close()
    conn_test_1.close()


# guangdong_gai(111, 222)

paper_queue = paper_queue_next(webpage_url_list=['https://www.guangzhouamc.com/asset/chuzhigonggao.html'])
queue_id = paper_queue['id']
webpage_id = paper_queue["webpage_id"]
print(queue_id, webpage_id)
guangdong_gai(queue_id, webpage_id)
data = {
    "id": queue_id,
    'description': f'数据获取成功',
}
paper_queue_success(data=data)
# 1752755 16472
# https://www.utrustamc.com/czgg/info.aspx?itemid=18282
