import mysql.connector
import requests
from lxml import etree

from AMC.api_paper import upload_file_by_url

# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)

cursor_test = conn_test.cursor()
# 查询数据
cursor_test.execute(
    "SELECT id, name, former_name, gender, id_num, address, role, company, office, relationship, asset, is_died, other FROM col_paper_people"
)
rows = cursor_test.fetchall()

# 处理每一行数据
for row in rows:
    data = {
        "id": row[0],
        "name": row[1],
        "former_name": row[2],
        "gender": row[3],
        "id_num": row[4],
        "address": row[5],
        "role": row[6],
        "company": row[7],
        "office": row[8],
        "relationship": row[9],
        "asset": row[10],
        "is_died": row[11],
        "other": row[12]
    }

    # 处理其他字段
    fields = ["former_name", "gender", "id_num", "address", "role", "company", "office", "relationship", "asset", "is_died", "other"]
    for field in fields:
        if data[field] in ['无', None, []]:
            data[field] = ''

    # 更新数据库中的记录
    update_query = """
    UPDATE col_paper_people
    SET former_name = %s, gender = %s, id_num = %s, address = %s, role = %s, company = %s, office = %s, relationship = %s, asset = %s, is_died = %s, other = %s
    WHERE id = %s
    """
    cursor_test.execute(update_query, (
        data["former_name"], data["gender"], data["id_num"], data["address"], data["role"], data["company"], data["office"],
        data["relationship"], data["asset"], data["is_died"], data["other"], data["id"]
    ))
    conn_test.commit()

cursor_test.close()
conn_test.close()