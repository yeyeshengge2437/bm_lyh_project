# 将数据库中内容和内容的html不符合的进行删除，再次进行爬取
import hashlib
import json
import re

import mysql.connector
from lxml import etree

# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)
cursor_test = conn_test.cursor()
cursor_test.execute(
    f"SELECT id, title, title_url, content,pub_date,origin_domain, md5_key FROM col_chief_public WHERE id = '112756'")
rows = cursor_test.fetchall()
set_url = set()
for id, title, title_url, content,pub_date,origin_domain, md5_key in rows:
    # if id == 14597:
    #     print(title, content, pub_date, origin_domain)
    #     uni_data = f'{str(title), str(content), str(pub_date), str(origin_domain)}'
    #     md5_key1 = hashlib.md5(json.dumps(uni_data).encode('utf-8')).hexdigest()
    #     print(md5_key1)
    #     print(id, title_url, md5_key)
    # if id == 21411:
    #     uni_data = f'{str(title), str(content), str(pub_date), str(origin_domain)}'
    #     md5_key1 = hashlib.md5(json.dumps(uni_data).encode('utf-8')).hexdigest()
    #     print(md5_key1)
        print(id, title_url, title)
    # if title_url not in set_url:
    #     set_url.add(title_url)
    # else:
    #     print(id, title_url)
    # if not content:
    #     html = etree.HTML(content_html)
    #     content = ''.join(html.xpath('//font//text()')).strip()
    #     print(content)
    #     insert_sql = "UPDATE col_chief_public SET content = %s WHERE id = %s"
    #     cursor_test.execute(insert_sql, (content, id))
    #     conn_test.commit()

cursor_test.close()
conn_test.close()
