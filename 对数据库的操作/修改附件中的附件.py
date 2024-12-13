import mysql.connector

conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
cursor_test = conn_test.cursor()
# 获取版面来源的版面链接
# cursor_test.execute(f"SELECT id, url, state FROM col_judicial_auctions")
cursor_test.execute(f"SELECT id, subject_annex, subject_annex_up FROM col_judicial_auctions")
rows = cursor_test.fetchall()
for row in rows:
    id = row[0]
    subject_annex = row[1]
    subject_annex_up = row[2]
    print(id, subject_annex, subject_annex_up)
    # annex_list = subject_annex.split(',')
    # annex_str = ''
    # for annex in annex_list:
    #     value = annex[0:9]
    #     if value == 'https:htt':
    #         annex_new = annex[6:]
    #         annex_str += annex_new + ','
    #     else:
    #         annex_str += annex + ','
    # annex_up = str(annex_str[:-2])
    # print(annex_up)
    # cursor_test.execute("UPDATE col_judicial_auctions SET subject_annex_up = %s, subject_annex = %s  WHERE id = %s", (annex_up, annex_up, id))
    # conn_test.commit()
cursor_test.close()
conn_test.close()


