# 将数据库中内容和内容的html不符合的进行删除，再次进行爬取
import re

import mysql.connector
from lxml import etree

# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)

cursor_test = conn_test.cursor()
cursor_test.execute(
    f"SELECT id, title, content, content_html FROM col_chief_public WHERE origin = '国家市场监督管理总局缺陷产品召回技术中心'")
rows = cursor_test.fetchall()
set_url = set()
for id, title, content, content_html in rows:
    if not content:
        html = etree.HTML(content_html)
        content = ''.join(html.xpath('//font//text()')).strip()
        print(content)
        insert_sql = "UPDATE col_chief_public SET content = %s WHERE id = %s"
        cursor_test.execute(insert_sql, (content, id))
        conn_test.commit()

        # if content:

    # if title_url not in set_url:
    #     set_url.add(title_url)
    # else:
    #     print(id, title, title_url, content)
    # print(id, title, content)
    # if not content:
    #     print(id, title, content)
    # cursor_test.execute("DELETE FROM col_chief_public WHERE id = %s", (id,))
    # conn_test.commit()
    # insert_sql = "UPDATE col_paper_notice SET content = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (content, id))
    # conn_test.commit()

    # cursor_test.execute("DELETE FROM col_paper_notice WHERE id = %s", (id,))
    # conn_test.commit()

# new_original_pdf = re.sub(r'\.\.\/\.\.', '', original_pdf)
# pdf_url = upload_file_by_url(new_original_pdf, '1111', 'pdf')
#
# insert_sql = "UPDATE col_paper_page SET original_pdf = %s WHERE id = %s"
# cursor_test.execute(insert_sql, (new_original_pdf, id))
# conn_test.commit()
# if status == 'doing':
#     insert_sql = "UPDATE col_web_queue SET status = %s WHERE id = %s"
#     cursor_test.execute(insert_sql, ())
#     conn_test.commit()


cursor_test.close()
conn_test.close()
