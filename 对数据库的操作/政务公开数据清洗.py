# 将数据库中内容和内容的html不符合的进行删除，再次进行爬取
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
    f"SELECT id,name, punish_organ, punish_content, wf_fact, punish_date, content_detail FROM col_punish WHERE origin = '中国市场监管行政处罚文书网'")
rows = cursor_test.fetchall()
count = 0
for id,name, punish_organ, punish_content, wf_fact, punish_date, content_detail in rows:
    content_detail = f'当事人名称:{name},处罚机关:{punish_organ}, 处罚日期:{punish_date}, 处罚内容:{punish_content}, 处罚依据:{wf_fact}' + content_detail
    print(content_detail)
    insert_sql = "UPDATE col_punish SET content_detail = %s WHERE id = %s"
    cursor_test.execute(insert_sql, (content_detail, id))
    conn_test.commit()
    # if not content:
    #     html = etree.HTML(content_html)
    #     content = ''.join(html.xpath('//font//text()')).strip()
    #     print(content)
    #     insert_sql = "UPDATE col_chief_public SET content = %s WHERE id = %s"
    #     cursor_test.execute(insert_sql, (content, id))
    #     conn_test.commit()

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
