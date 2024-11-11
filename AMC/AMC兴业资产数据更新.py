# 131
import json
import os
import re

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
    'Pragma': 'no-cache',
    'Referer': 'http://www.ciamc.com.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
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
        "select id, page_url, update_time, original_files, files from col_paper_notice where paper = '兴业资产管理有限公司'")
    rows = cursor_test_1.fetchall()
    for id, page_url, update_time, original_files, files in rows:
        # if update_time:
        #     continue
        title_url = page_url
        res_title = requests.get(title_url, headers=headers)
        res_title_html1 = res_title.content.decode()
        res_title_html = etree.HTML(res_title_html1)


        title_html_info = res_title_html.xpath(
            "//div[@class='detail']/div[@class='detail-title']")
        content_1 = res_title_html.xpath("//div[@class='detail']/div[@class='detail-body']")
        content_html = ''
        for con in title_html_info:
            content_html += etree.tostring(con, encoding='utf-8').decode()
        for con in content_1:
            content_html += etree.tostring(con, encoding='utf-8').decode()
        html = etree.HTML(content_html)
        annex = html.xpath("//@href | //@src")
        if annex:
            # print(page_url, annex)
            files = []
            original_url = []
            for ann in annex:
                if "http" not in ann:
                    ann = 'http://www.ciamc.com.cn' + ann
                file_type = ann.split('.')[-1]
                if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                 'png', 'jpg'] and 'ciamc' in ann:
                    file_url = upload_file_by_url(ann, "xingye", file_type)
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

        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 上传到测试数据库
        conn_test = mysql.connector.connect(
            host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database="col",
        )
        cursor_test = conn_test.cursor()
        print(queue_id, update_time, id)
        insert_sql = "UPDATE col_paper_page SET from_queue=%s, update_time=%s WHERE id = %s"
        cursor_test.execute(insert_sql, (queue_id, update_time, id))
        conn_test.commit()

        insert_sql = "UPDATE col_paper_notice SET from_queue=%s, update_time=%s, original_files=%s, files=%s WHERE id = %s"
        cursor_test.execute(insert_sql, (queue_id, update_time, original_url, files, id))
        conn_test.commit()

        cursor_test.close()
        conn_test.close()

    cursor_test_1.close()
    conn_test_1.close()


# guangdong_gai(111, 222)

paper_queue = paper_queue_next(webpage_url_list=['http://www.ciamc.com.cn/ciamc/insetInfo/disposal-Notice.html'])
queue_id = paper_queue['id']
webpage_id = paper_queue["webpage_id"]
print(queue_id, webpage_id)
guangdong_gai(queue_id, webpage_id)
data = {
    "id": queue_id,
    'description': f'数据获取成功',
}
paper_queue_success(data=data)
# 1753205
