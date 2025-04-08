import pymysql
from pymysql import Error
from a_mysql_connection_pool import get_connection

def delete_records():
    # 数据库连接配置（替换为实际值）
    db_config = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'your_database',
        'charset': 'utf8mb4'
    }

    # 定义要删除的条件值
    target_paper = '湖南省财信资产管理有限公司_资产推介'

    try:
        # 建立数据库连接
        connection = get_connection()
        cursor = connection.cursor()

        # 定义 SQL 语句模板（使用参数化查询防止 SQL 注入）
        delete_queries = [
            "DELETE FROM col_paper_page WHERE paper = %s",
            "DELETE FROM col_paper_notice WHERE paper = %s"
        ]

        # 执行删除操作
        for query in delete_queries:
            cursor.execute(query, (target_paper,))
            print(f"Deleted {cursor.rowcount} rows from table with query: {query}")

        # 提交事务
        connection.commit()

    except Error as e:
        print(f"数据库错误: {e}")
        # 发生错误时回滚
        if connection:
            connection.rollback()
    finally:
        # 关闭连接
        if connection:
            cursor.close()
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    delete_records()