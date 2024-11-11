import os
import re

import mysql.connector
import requests
from lxml import etree

from AMC.api_paper import upload_file_by_url

# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)

cursor_test = conn_test.cursor()
cursor_test.execute(
    "select id, page_url, content_html, day from col_paper_notice where paper = '浙江省浙商资产管理有限公司'")
rows = cursor_test.fetchall()
for id, page_url, content_html, day in rows:
    print(day)
    # 使用re匹配日期
    # if day[0] == '0':
    #     print(day)
    #     new_date = '0000-00-00'
    #
    #     insert_sql = "UPDATE col_paper_notice SET day= %s WHERE id = %s"
    #     cursor_test.execute(insert_sql, (new_date, id))
    #     conn_test.commit()



    # html = etree.HTML(content_html)
    # annex = html.xpath("//@href | //@src")
    # if annex:
    #     files = []
    #     original_url = []
    #     for ann in annex:
    #         if "http" not in ann:
    #             ann = "https://www.amcim.com" + ann
    #         file_type = ann.split('.')[-1]
    #         if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
    #                          'png', 'jpeg'] and "uploads" in ann:
    #             file_url = upload_file_by_url(ann, "neimenggu", file_type)
    #             files.append(file_url)
    #             original_url.append(ann)
    # else:
    #     files = ''
    #     original_url = ''
    # if not files:
    #     files = ''
    #     original_url = ''
    # files = str(files)
    # original_url = str(original_url)
    # if original_url:
    #     print(original_url)
    #
    # insert_sql = "UPDATE col_paper_notice SET original_files = %s,files = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (original_url, files, id))
    # conn_test.commit()

cursor_test.close()
conn_test.close()