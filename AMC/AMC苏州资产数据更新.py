# 131
import base64
import json
import os
import re
import random

import mysql.connector
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, paper_queue_next, \
    paper_queue_success, upload_file_by_url

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'acw_tc=2760820617261086453028950e14451199475ed356bd9d44c76354c970a588; JSESSIONID=d298bdc0-a825-4587-95e5-fa609e45b418; sl-session=KCl7ZGWl42baWIXnIJcZvw==',
    'Pragma': 'no-cache',
    'Referer': 'https://www.sz-amc.com/business/Publicity?id=3&page=1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def guangdong_gai(queue_id, webpage_id):
    conn_test_1 = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col"
    )

    cursor_test_1 = conn_test_1.cursor()
    cursor_test_1.execute(
        "select id, page_url, content_html, original_files, files from col_paper_notice where paper = '苏州资产管理有限公司'")
    rows = cursor_test_1.fetchall()
    for id, page_url, content_html, original_files, files in rows:
        content_html1 = etree.HTML(content_html)
        annex = content_html1.xpath("//a/@href | //@src")
        # if annex:
        #     print(annex)
        if annex:
            # print(page_url, annex)
            files = []
            original_url = []
            for ann in annex:
                if "http" not in ann and len(ann) < 100:
                    ann = 'http://www.sz-amc.com' + ann
                elif "http" not in ann and len(ann) > 100:
                    ann = re.sub(r'data:image/png;base64,', '', ann)
                    num_img = random.randint(1, 999999)
                    # 解码Base64字符串为二进制数据
                    image_data = base64.b64decode(ann)
                    with open(f'{num_img}.png', 'wb') as f:
                        f.write(image_data)
                    file_url = upload_file(num_img, "png")
                    files.append(file_url)
                    original_url.append(file_url)
                    # 删除图片
                    if os.path.exists(f'{num_img}.png'):
                        os.remove(f'{num_img}.png')

                file_type = ann.split('.')[-1]
                if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                 'png', 'jpg'] and 'upload' in ann:
                    file_url = upload_file_by_url(ann, "suzhou", file_type)
                    # file_url = 111
                    files.append(file_url)
                    original_url.append(ann)
        else:
            files = ''
            original_url = ''
        if not files:
            files = ''
            original_url = ''
        files = str(files).replace("'", '"')
        original_url = str(original_url).replace("'", '"')
        # print(files, original_url)
        content_html = re.sub(r'src="[^"]*"', '', content_html)
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 上传到测试数据库
        conn_test = mysql.connector.connect(
            host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database="col",
        )
        cursor_test = conn_test.cursor()
        # print(queue_id, update_time, id)
        insert_sql = "UPDATE col_paper_page SET from_queue=%s, update_time=%s WHERE id = %s"
        cursor_test.execute(insert_sql, (queue_id, update_time, id))
        conn_test.commit()

        insert_sql = "UPDATE col_paper_notice SET from_queue=%s, update_time=%s, content_html=%s, original_files=%s, files=%s WHERE id = %s"
        cursor_test.execute(insert_sql, (queue_id, update_time, content_html, original_url, files, id))
        conn_test.commit()

        cursor_test.close()
        conn_test.close()
        # if update_time:
        #     continue
        # title_url = page_url
        # print(title_url)
        # print(title_url, original_files, files)
        # title_url = "https://www.sz-amc.com/index/newsInfo?articleId=2203"
        #
        # res_title = requests.get(title_url, headers=headers)
        # res_title_html1 = res_title.content.decode()
        #
        # title_json_html = \
        #     re.findall(r'<script>let notice = (.*);.*?let headerIndex = 3;</script>', res_title_html1, re.S)[0]
        # title_json_html = json.loads(title_json_html)
        # ann_file = title_json_html['filePath']
        # if ann_file:
        #     if original_files:
        #         print(original_files)
            #     original_files = json.loads(original_files)
            #     original_files.append(ann_file)
            #     file_type = ann_file.split('.')[-1]
            #     files = json.loads(files)
            #     file_url = upload_file_by_url(ann_file, "suzhou", file_type)
            #     files.append(file_url)
            #
            # else:
            #     files = []
            #     original_files = []
            #     file_type = ann_file.split('.')[-1]
            #     file_url = upload_file_by_url(ann_file, "suzhou", file_type)
            #     files.append(file_url)
            #     original_files.append(ann_file)
            # files = str(files).replace("'", '"')
            # original_files = str(original_files).replace("'", '"')
            # print(original_files, files)

            # update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #
            # # 上传到测试数据库
            # conn_test = mysql.connector.connect(
            #     host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            #     user="col2024",
            #     password="Bm_a12a06",
            #     database="col",
            # )
            # cursor_test = conn_test.cursor()
            # print(queue_id, update_time, id)
            # insert_sql = "UPDATE col_paper_page SET from_queue=%s, update_time=%s WHERE id = %s"
            # cursor_test.execute(insert_sql, (queue_id, update_time, id))
            # conn_test.commit()
            #
            # insert_sql = "UPDATE col_paper_notice SET from_queue=%s, update_time=%s, original_files=%s, files=%s WHERE id = %s"
            # cursor_test.execute(insert_sql, (queue_id, update_time, original_files, files, id))
            # conn_test.commit()
            #
            # cursor_test.close()
            # conn_test.close()

    cursor_test_1.close()
    conn_test_1.close()


# guangdong_gai(111, 222)

paper_queue = paper_queue_next(webpage_url_list=['https://www.sz-amc.com/business/Publicity?id=3'])
queue_id = paper_queue['id']
webpage_id = paper_queue["webpage_id"]
print(queue_id, webpage_id)
guangdong_gai(queue_id, webpage_id)
data = {
    "id": queue_id,
    'description': f'数据获取成功',
}
paper_queue_success(data=data)
# 1755487 16443

