import mysql.connector
conn_test = mysql.connector.connect(
                                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                                    user="col2024",
                                    password="Bm_a12a06",
                                    database="col",
                                )

url = "https://zc-item.taobao.com/auction/722253087969.htm"
title = "测试"
cursor_test = conn_test.cursor()
# 上传文件
insert_sql = "INSERT INTO col_judicial_auctions (url, title) VALUES (%s, %s)"

cursor_test.execute(insert_sql,
                    (url, title))
conn_test.commit()

cursor_test.close()
conn_test.close()
