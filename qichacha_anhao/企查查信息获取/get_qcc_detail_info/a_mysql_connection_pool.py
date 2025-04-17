from datetime import datetime

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


def up_qcc_data(subject_id, data_type, data_status, data_key, data_json, from_queue, webpage_id):
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    create_date = datetime.now().strftime('%Y-%m-%d')
    conn = get_connection()
    cursor = conn.cursor()
    # 上传到报纸的图片或PDF
    insert_sql = "INSERT INTO col_corp_search_data (subject_id, data_type, data_status, data_key, data_json, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s, %s,%s, %s, %s, %s, %s, %s)"

    cursor.execute(insert_sql,
                   (subject_id, data_type, data_status, data_key, data_json, create_time, from_queue, create_date,
                    webpage_id))
    conn.commit()
    cursor.close()
    conn.close()  # 将连接返回到连接池
    return True


def up_qcc_res_data(url, data_key, res_type, json_data, key_no, webpage_id):
    conn = get_connection()
    cursor = conn.cursor()
    # 上传数据
    insert_sql = "INSERT INTO col_qcc_res_data (url, data_key, res_type, json_data, key_no, webpage_id) VALUES (%s,%s, %s,%s, %s, %s)"
    cursor.execute(insert_sql, (url, data_key, res_type, json_data, key_no, webpage_id))
    conn.commit()
    cursor.close()
    conn.close()  # 将连接返回到连接池
    return True


def get_ban_data(webpage_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM col_qcc_res_data WHERE webpage_id = %s"
    cursor.execute(sql, (webpage_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def del_ban_data(id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM col_qcc_res_data WHERE id = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True



