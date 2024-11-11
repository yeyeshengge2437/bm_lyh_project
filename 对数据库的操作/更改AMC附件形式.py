import os
import re

import mysql.connector
import requests
from DrissionPage import ChromiumOptions, ChromiumPage
from lxml import etree

from AMC.api_paper import upload_file_by_url, get_image, get_now_image, upload_file

# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)


cursor_test = conn_test.cursor()
cursor_test.execute(
    "SELECT id, paper, page_url, original_files, files FROM col_paper_notice WHERE paper LIKE '%公司%'")
# cursor_test.execute(
#     "SELECT id, paper, page_url, original_img, img_url FROM col_paper_page WHERE id = 1293610")

rows = cursor_test.fetchall()
for id, paper, page_url, original_files, files in rows:
    if files and "'" in files:
        print(id, paper, page_url, original_files, files)
        # original_files = original_files.replace("'", '"')
        # files = files.replace("'", '"')
        #
        # insert_sql = "UPDATE col_paper_notice SET original_files = %s, files = %s WHERE id = %s"
        # cursor_test.execute(insert_sql, (original_files, files, id))
        # conn_test.commit()


cursor_test.close()
conn_test.close()
