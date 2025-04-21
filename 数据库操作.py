import re
import time

import requests

from a_mysql_connection_pool import get_connection


def guanxi():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url, day, update_time  FROM col_paper_notice WHERE paper = '广西交易所集团';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        update_time = i[3]
        if update_time:
            continue
        try:
            url_id = re.findall(r'Detail/(.*?)\.html', page_url)[0]
        except:
            print("!!!!!!!!!!!!!!!!", page_url)
            continue
        headers_time = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Client-Id': 'gxcq',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'http://ljs.gxcq.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            # 'Cookie': 'Hm_lvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1744954682; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1744956119',
        }
        if 'projectToManageDetail' in page_url:
            params = {
                'id': f'{url_id}',
                # 'n': '0.5039649294161339',
            }

            response_ = requests.get(
                'http://ljs.gxcq.com.cn/api/dscq-project/project/detail',
                params=params,
                headers=headers_time,
                verify=False,
            )
            time.sleep(1)
            print(page_url)
            print(url_id)
            print(response_.json())
            title_date = response_.json()["data"]["announcementStartTime"]
            print(title_date)
        else:
            params = {
                'assetsId': f'{url_id}',
                # 'n': '0.5039649294161339',
            }

            response_ = requests.get(
                'http://ljs.gxcq.com.cn/api/dscq-project/assets-detail/normal-detail',
                params=params,
                headers=headers_time,
                verify=False,
            )
            time.sleep(1)
            print(page_url)
            print(url_id)
            title_date = response_.json()["data"]["bidActivity"]["publishDate"]
            print(title_date)
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(
            "UPDATE col_paper_notice SET day = %s, update_time = %s WHERE id = %s",
            (title_date, update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
    cursor.close()
    connection.close()


guanxi()
