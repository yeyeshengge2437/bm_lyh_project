import os
import re

import mysql.connector
import requests


# 连接到测试库
conn_test = mysql.connector.connect(
  host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
  user="col2024",
  password="Bm_a12a06",
  database="col"
)

cursor_test = conn_test.cursor()

cursor_test.execute("SELECT id, status, remark FROM col_web_queue WHERE webpage_name = '河南商报'")
rows = cursor_test.fetchall()
for id, status, remark in rows:
    if '程序异常' in remark and '数据获取成功' not in remark and status == 'fail':
        print(id, status, remark)
        insert_sql = "UPDATE col_web_queue SET status = %s, try_num = %s WHERE id = %s"
        cursor_test.execute(insert_sql, ('todo', 0, id))
        conn_test.commit()
    # # 删除不符合的内容
    # cursor_test.execute("DELETE FROM col_paper_notice WHERE id = %s", (id,))
    # conn_test.commit()


    # new_original_pdf = re.sub(r'\.\.\/\.\.', '', original_pdf)
    # pdf_url = upload_file_by_url(new_original_pdf, '1111', 'pdf')
    #

    # conn_test.commit()
    # if status == 'doing':
    #     insert_sql = "UPDATE col_web_queue SET status = %s WHERE id = %s"
    #     cursor_test.execute(insert_sql, ('todo', id))
    #     conn_test.commit()


cursor_test.close()
conn_test.close()