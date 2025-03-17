import mysql.connector

# 数据库连接配置
db_config = {
    "host": "rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    "user": "col2024",
    "password": "Bm_a12a06",
    "database": "col",
}

# 连接数据库
try:
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    # 定义删除条件和SQL语句
    paper_value = ("江苏产权市场网",)
    delete_queries = [
        "DELETE FROM col_paper_page WHERE paper = %s",
        "DELETE FROM col_paper_notice WHERE paper = %s"
    ]

    # 执行删除操作
    total_deleted = 0
    for query in delete_queries:
        cursor.execute(query, paper_value)
        total_deleted += cursor.rowcount

    db.commit()  # 提交事务

    print(f"成功删除 {total_deleted} 条数据")

except mysql.connector.Error as err:
    print("数据库操作失败:", err)
    db.rollback()  # 发生错误时回滚

finally:
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'db' in locals() and db.is_connected():
        db.close()