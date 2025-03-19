import mysql.connector.pooling
from dbutils.pooled_db import PooledDB

# 配置数据库连接信息
db_config = {
    "host": "rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    "user": "col2024",
    "password": "Bm_a12a06",
    "database": "col",
    "port": 3306,
}

# 创建连接池
pool = PooledDB(
    creator=mysql.connector,  # 使用 mysql.connector 作为数据库驱动
    maxconnections=10,  # 连接池中最大连接数
    mincached=2,  # 初始化时连接池中至少创建的空闲连接
    maxcached=5,  # 连接池中最多闲置的连接
    maxusage=None,  # 一个连接最多被重复使用的次数，None 表示无限制
    blocking=True,  # 当连接池达到最大连接数时，是否阻塞等待
    **db_config
)


# 从连接池中获取连接
def get_connection():
    return pool.connection()


# # 使用连接池中的连接执行查询
# def query_data():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM col_config")
#     result = cursor.fetchall()
#     cursor.close()
#     conn.close()  # 将连接返回到连接池
#     return result
#
#
# # 示例：查询数据
# data = query_data()
# print(data)
