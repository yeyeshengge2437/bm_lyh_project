import json
from datetime import datetime
import hashlib
import mysql.connector.pooling
from dbutils.pooled_db import PooledDB

# 配置数据库连接信息
db_config = {
    "host": "rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    "user": "col2024",
    "password": "Bm_a12a06",
    "database": "col_test",
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
    sql = "SELECT id, url, data_key, res_type, json_data, key_no, from_queue, webpage_id FROM col_qcc_res_data WHERE webpage_id = %s"
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


def generate_md5(data):
    """
    生成输入数据的 MD5 哈希值

    参数:
        data: 可以是字符串、字典、列表等

    返回:
        返回数据的 MD5 哈希值（32位十六进制字符串）
    """
    # 如果是字典或列表，先转成 JSON 字符串
    if isinstance(data, (dict, list)):
        data = json.dumps(data, sort_keys=True, ensure_ascii=False)

    # 如果是字符串，编码成字节
    if isinstance(data, str):
        data = data.encode('utf-8')

    # 计算 MD5
    md5_hash = hashlib.md5(data)
    return md5_hash.hexdigest()


def up_part_qcc_data(data_value, data_key, key_no, from_queue, webpage_id):
    if data_key in ['business_info', 'credit_eval', "headquarter"]:
        data_md5 = generate_md5(str(data_value))
        data_status = "current"
        data_json = json.dumps(data_value, ensure_ascii=False)
        up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue, webpage_id)

    else:
        if 'his_' in data_key:
            # 历史信息，增加标识
            data_status = 'history'
            for up_data in data_value:
                if up_data:
                    data_key = data_key.replace('his_', '')
                    data_json = json.dumps(up_data, ensure_ascii=False)
                    data_md5 = generate_md5(str(up_data))
                    up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue,
                                webpage_id)
        else:
            for up_data in data_value:
                if up_data:
                    data_status = "current"
                    data_json = json.dumps(up_data, ensure_ascii=False)
                    data_md5 = generate_md5(str(up_data))
                    up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue,
                                webpage_id)


def in_qcc_cookies(cookies, cookies_is_effective, cookies_tag):
    """
    插入一条可以用的cookies
    :param cookies:
    :param cookies_is_effective:
    :param cookies_tag:
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()
    # 上传数据
    insert_sql = "INSERT INTO col_qcc_res_data (cookies, cookies_is_effective, cookies_tag) VALUES (%s, %s, %s)"
    cursor.execute(insert_sql, (cookies, cookies_is_effective, cookies_tag))
    cookies_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return True, cookies_id


def lapse_qcc_cookies(cookies_id):
    """
    将cookies数据信息失效掉
    :param cookies_id:
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()
    up_sql = "UPDATE col_qcc_res_data SET cookies_is_effective = %s WHERE id = %s"
    cursor.execute(up_sql, (0, cookies_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def available_qcc_cookies(cookies_id):
    """
    将cookies数据信息变为有效
    :param cookies_id:
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()
    up_sql = "UPDATE col_qcc_res_data SET cookies_is_effective = %s WHERE id = %s"
    cursor.execute(up_sql, (1, cookies_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def up_qcc_cookies(cookies, cookies_is_effective, cookies_id):
    """
    更新cookies的状态
    :param cookies:
    :param cookies_is_effective: 1：可用， 0:不可用， 2：正在处理中
    :param cookies_id:
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()
    up_sql = "UPDATE col_qcc_res_data SET cookies = %s, cookies_is_effective = %s WHERE id = %s"
    cursor.execute(up_sql, (cookies, cookies_is_effective, cookies_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def search_qcc_cookies_one():
    """
    随机获取一个可以用的cookies
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id, cookies, cookies_tag FROM col_qcc_res_data WHERE cookies_is_effective = %s"
    cursor.execute(sql, (1,))
    result = cursor.fetchone()
    if result:
        cookies_id = result[0]
        cookies = result[1]
        cookies_tag = result[2]
        up_sql = "UPDATE col_qcc_res_data SET cookies_is_effective = %s WHERE id = %s ORDER BY RAND() LIMIT 1"
        cursor.execute(up_sql, (2, cookies_id,))
        conn.commit()
        cursor.close()
        conn.close()
        cookies = json.loads(cookies)
        return cookies_id, cookies, cookies_tag
    else:
        cursor.close()
        conn.close()
        return False, False, False
def get_lapse_qcc_cookies():
    """
    获取一个已经失效的cookies信息
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id, cookies_tag FROM col_qcc_res_data WHERE cookies_is_effective = %s ORDER BY RAND() LIMIT 1"
    cursor.execute(sql, (0,))
    result = cursor.fetchone()
    if result:
        id_ = result[0]
        cookies_tag = result[1]
        cursor.close()
        conn.close()
        return id_, cookies_tag
    else:
        cursor.close()
        conn.close()
        return False, False


