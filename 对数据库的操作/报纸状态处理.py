import os
import re

import mysql.connector
import requests
from DrissionPage import ChromiumOptions, ChromiumPage
from lxml import etree

from AMC.api_paper import upload_file_by_url, get_image, get_now_image, upload_file

# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)


cursor_test = conn_test.cursor()
cursor_test.execute(
    "SELECT id, webpage_name, status FROM col_web_queue WHERE webpage_name = '潇湘晨报'")
# cursor_test.execute(
#     "SELECT id, paper, page_url, original_img, img_url FROM col_paper_page WHERE id = 1293610")

rows = cursor_test.fetchall()
for id, paper, status in rows:
    if status == 'doing':
        insert_sql = "UPDATE col_web_queue SET status = %s WHERE id = %s"
        cursor_test.execute(insert_sql, ('todo', id))
        conn_test.commit()
    if status == 'todo':
        print(id, paper, status)

cursor_test.close()
conn_test.close()
