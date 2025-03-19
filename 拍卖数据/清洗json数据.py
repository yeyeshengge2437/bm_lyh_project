import json
import re
from api_paimai import judge_repeat_attracting, judge_repeat
from a_mysql_connection_pool import get_connection
import mysql.connector

try:
    with open("tb_all_url_data.json", "r") as file:
        datas = json.load(file)
except FileNotFoundError:
    print("文件不存在！")
except json.JSONDecodeError:
    print("JSON 格式错误！")
for data in datas:
    # print(data['url'], data['url_name'], data['start'])
    url = data['url']
    url_name = data['url_name']
    start = data['start']
    if 'mn_detail' in url or 'mnItemId' in url:
        continue
        print(url, url_name, start)
        try:
            url_new = re.findall(r'https://zc-paimai\.taobao\.com/zc/mn_detail\.htm\?id=\d+', url)[0]
        except:
            url_new = re.findall(r'https://zc-paimai\.taobao\.com/zc/mn_detail\.htm\?mnItemId=\d+', url)[0]
        if not judge_repeat_attracting(url_new):
            conn_test = get_connection()
            cursor_test = conn_test.cursor()
            # 上传文件
            insert_sql = "INSERT INTO col_judicial_auctions_investing (url, title) VALUES (%s,%s)"

            cursor_test.execute(insert_sql, (
                url_new, url_name))
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
            print(url_new)
    elif start == '已结束' and 'auction' in url or 'sf_item' in url:
        print(url, url_name, start)
        url_new = re.findall(r'https://susong-item\.taobao\.com/auction/\d+\.htm', url)
        if url_new:
            url_new = url_new[0]
        else:
            url_new = re.findall(r'https://zc-item\.taobao\.com/auction/\d+\.htm', url)
            if url_new:
                url_new = url_new[0]
            else:
                url_new = re.findall(r'https://sf-item\.taobao\.com/sf_item/\d+\.htm', url)
                if url_new:
                    url_new = url_new[0]
        value_1, value_2 = judge_repeat(url_new)
        if not value_1:
            conn_test = get_connection()
            cursor_test = conn_test.cursor()
            # 上传文件
            insert_sql = "INSERT INTO col_judicial_auctions (url, title, state) VALUES (%s,%s, %s)"

            cursor_test.execute(insert_sql, (
                url_new, url_name, start))
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
            print(url_new)



