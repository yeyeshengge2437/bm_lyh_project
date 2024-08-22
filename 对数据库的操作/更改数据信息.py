import re

import mysql.connector

# 连接到测试库
conn_test = mysql.connector.connect(
  host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
  user="col2024",
  password="Bm_a12a06",
  database="col"
)

cursor_test = conn_test.cursor()

cursor_test.execute("SELECT id, annex FROM col_chief_public WHERE origin = '贵州药品监督管理局'")
rows = cursor_test.fetchall()
for id, annex in rows:
    if annex:
        new_annex = re.sub(r'test', 'live', annex)
        insert_sql = "UPDATE col_chief_public SET annex = %s WHERE id = %s"
        cursor_test.execute(insert_sql, (new_annex, id))
        conn_test.commit()
    # if status == 'doing':
    #     insert_sql = "UPDATE col_web_queue SET status = %s WHERE id = %s"
    #     cursor_test.execute(insert_sql, ('todo', id))
    #     conn_test.commit()


cursor_test.close()
conn_test.close()