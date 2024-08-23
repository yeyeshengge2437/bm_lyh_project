import os
import re

import mysql.connector
import requests


def upload_file_by_url(file_url, file_name, file_type, type="paper"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(file_url, headers=headers)
    if r.status_code != 200:
        return "获取失败"
    pdf_path = f"{file_name}.{file_type}"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}
    url = "http://121.43.164.84:29875" + f"/file/upload/file?type={type}"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    return result.get("value")["file_url"]
# 连接到测试库
conn_test = mysql.connector.connect(
  host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
  user="col2024",
  password="Bm_a12a06",
  database="col"
)

cursor_test = conn_test.cursor()
def judging_criteria(title, article_content):
    """
    判断是否为债权公告
    :param title: 报纸的标题
    :param article_content: 报纸的内容
    :return:
    """
    explicit_claims = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                                 r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')

    explicit_not_claims = re.compile(
        r'(法院公告|减资公告|注销公告|清算公告|合并公告|出让公告|重组公告|调查公告|分立公告|重整公告|悬赏公告|注销登记公告)')

    possible_claims = re.compile(r'^(?=.*(公告|公 告|无标题|广告)).{1,10}$')

    possible_content = re.compile(r'.*(债权|债务|借款|催收)[^\W_]*(公告|通知)')
    if (explicit_claims.search(title) or possible_claims.search(title) or possible_content.search(
            article_content)) and not explicit_not_claims.search(title):
        return True
    else:
        return False
cursor_test.execute("SELECT id, title, content FROM col_paper_notice WHERE paper = '证券日报'")
rows = cursor_test.fetchall()
for id, title, content in rows:

    if not judging_criteria(title, content):
        print(id, title, content)
        # 删除不符合的内容
        cursor_test.execute("DELETE FROM col_paper_notice WHERE id = %s", (id,))
        conn_test.commit()


    # new_original_pdf = re.sub(r'\.\.\/\.\.', '', original_pdf)
    # pdf_url = upload_file_by_url(new_original_pdf, '1111', 'pdf')
    #
    # insert_sql = "UPDATE col_paper_page SET original_pdf = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (new_original_pdf, id))
    # conn_test.commit()
    # if status == 'doing':
    #     insert_sql = "UPDATE col_web_queue SET status = %s WHERE id = %s"
    #     cursor_test.execute(insert_sql, ('todo', id))
    #     conn_test.commit()


cursor_test.close()
conn_test.close()