import hashlib
import json

import mysql.connector

conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col"
                )
cursor_test = conn_test.cursor()

# 查询origin = "辽宁省法院诉讼服务网开庭公告"的数据
cursor_test.execute("SELECT id, case_no, cause, court, members, open_time FROM col_case_open WHERE origin = '辽宁省法院诉讼服务网开庭公告'")
rows = cursor_test.fetchall()
for id, case_no, cause, court, members, open_time in rows:
    unique_value = f"{str(case_no)}"
    hash_value = hashlib.md5(json.dumps(unique_value).encode('utf-8')).hexdigest()
    # 将hash_value加入表中
    insert_sql = "UPDATE col_case_open SET md5 = %s WHERE id = %s"
    # 执行SQL语句
    cursor_test.execute(insert_sql, (hash_value, id))
    conn_test.commit()

cursor_test.close()
conn_test.close()