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
cursor_test.execute("SELECT id, case_no, cause, court, members, open_time, md5 FROM col_case_open WHERE case_no = '（2024）辽0202民初3246号'")
rows = cursor_test.fetchall()
for id, case_no, cause, court, members, open_time, md5 in rows:
    unique_value = f"{str(case_no)}"
    # 数据去重
    hash_value = hashlib.md5(json.dumps(unique_value).encode('utf-8')).hexdigest()
    print(hash_value)
    print(f"{id, case_no, cause, court, members, open_time, md5}")


cursor_test.close()
conn_test.close()