import re
import mysql.connector

conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
cursor_test = conn_test.cursor()

# 从col_chief_public中获取content和content_html的内容
cursor_test.execute("SELECT id, content, content_html  FROM col_chief_public")
results = cursor_test.fetchall()
for (id, content, content_html) in results:
    print(id, content, content_html)
    # content_html = re.sub(r'<script[^>]*>([\s\S]*?)<\/script>', '', str(content_html))
    #
    # content_html = re.sub(r'<p>扫一扫在手机打开当前页面</p>', '', str(content_html), re.S)
    # content = re.sub(r'var\s+\$\s*=\s*jQuery;[\s\S]*?扫一扫在手机打开当前页面', '', str(content))
    # cursor_test.execute("UPDATE col_chief_public SET content_html = %s, content = %s WHERE id = %s", (content_html, content, id))
    # conn_test.commit()

cursor_test.close()
conn_test.close()
# cursor_test.execute("SELECT id, content, content_html  FROM col_chief_public")
# result = cursor_test.fetchall()
# # cursor_test.execute("SELECT id, content_html  FROM col_chief_public WHERE id = 8449")
# for (content_html, content,id) in result:
#     # 使用正则表达式替换错误的内容
#     id = id
#     content_html = re.sub(r'<script[^>]*>([\s\S]*?)<\/script>', '', str(content_html))
#
#     content_html = re.sub(r'<p>扫一扫在手机打开当前页面</p>', '', str(content_html), re.S)
#     # 忽略空格和换行符
#     content = re.sub(r'var\s+\$\s*=\s*jQuery;[\s\S]*?扫一扫在手机打开当前页面', '', str(content))
#
#     print(id,content, content_html)
#     # 将修改后的内容更新到col_chief_public表中
#
#     cursor_test.execute("UPDATE col_chief_public SET content_html = %s, content = %s WHERE id = %s", (content_html, content, id))
#     # 提交事务
# conn_test.commit()
# cursor_test.close()
# conn_test.close()