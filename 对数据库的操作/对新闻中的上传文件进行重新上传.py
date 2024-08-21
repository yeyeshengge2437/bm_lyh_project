import os

import mysql.connector
import requests

produce_url = "http://121.43.164.84:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False


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
    url = produce_url + f"/file/upload/file?type={type}"
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

# 查询时间为2024-8-20到2024-8-21之间的数据
cursor_test.execute(
    "select id, original_img, img_url from col_paper_page where (img_url like 'https://res.debtop.com/col/test/paper/202408/20/%' or img_url like 'https://res.debtop.com/col/test/paper/202408/21/%')")
rows = cursor_test.fetchall()
for id, original_img, img_url in rows:
    print(id, original_img, img_url)
    # img_url_new = upload_file_by_url(original_img, f"{id}", "img", "paper")
    # insert_sql = "UPDATE col_paper_page SET img_url = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (img_url_new, id))
    # conn_test.commit()

cursor_test.close()
conn_test.close()
