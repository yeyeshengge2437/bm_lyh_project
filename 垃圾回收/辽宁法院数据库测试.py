import mysql.connector

# 连接到测试库
conn_test = mysql.connector.connect(
  host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
  user="col2024",
  password="Bm_a12a06",
  database="col_test"
)

# 创建游标对象
cursor = conn_test.cursor()

# 执行查询
query = "UPDATE case_open_copy1 SET origin = '辽宁省法院诉讼服务网开庭公告' WHERE origin = 'https://lnsfw.lnsfy.gov.cn/lnssfw/pages/gsgg/gglist.html?lx=ktgg';"
cursor.execute(query)
# query = "SELECT create_date FROM case_open_copy1"
# cursor.execute(query)
# # 获取所有结果
# create_dates = cursor.fetchall()

# # 遍历结果
# for create_date_tuple in create_dates:
#     create_date = create_date_tuple[0]  # 假设create_date是第一个字段
#     print(create_date)
#
# print(len(create_dates))
# 提交更改
conn_test.commit()

# 关闭游标和数据库连接
cursor.close()
conn_test.close()

