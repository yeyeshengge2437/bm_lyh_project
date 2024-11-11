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

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9136)
page = ChromiumPage(co)
cursor_test = conn_test.cursor()
cursor_test.execute(
    "SELECT id, paper, page_url, original_img, img_url FROM col_paper_page WHERE paper = '吉林省盛融资产管理有限责任公司'")

rows = cursor_test.fetchall()
for id, paper, page_url, original_img, img_url in rows:
    if not img_url:
        print(id, paper, page_url, original_img, img_url)
        try:
            image = get_image(page, page_url, "xpath=//div[@class='nry_right']",
                                          left_offset=10, right_offset=20)
        except:
            image = get_now_image(page, page_url)
        # 将报纸url上传
        up_img = upload_file(image, "png", "paper")
        insert_sql = "UPDATE col_paper_page SET original_img = %s, img_url = %s WHERE id = %s"
        cursor_test.execute(insert_sql, (up_img, up_img, id))
        conn_test.commit()

        if os.path.exists(f'{image}.png'):
            os.remove(f'{image}.png')

cursor_test.close()
conn_test.close()
page.close()
