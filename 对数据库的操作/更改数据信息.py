import mysql.connector

# 连接到测试库
conn_test = mysql.connector.connect(
  host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
  user="col2024",
  password="Bm_a12a06",
  database="col"
)

cursor_test = conn_test.cursor()

# 查询origin = "辽宁省法院诉讼服务网开庭公告"的数据
cursor_test.execute("SELECT id, status FROM col_web_queue WHERE webpage_name = '河南商报'")
rows = cursor_test.fetchall()
for id, status in rows:
    if status == 'doing':
        insert_sql = "UPDATE col_web_queue SET status = %s WHERE id = %s"
        cursor_test.execute(insert_sql, ('todo', id))
        conn_test.commit()


cursor_test.close()
conn_test.close()