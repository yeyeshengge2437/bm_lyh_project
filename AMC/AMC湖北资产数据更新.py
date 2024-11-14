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
from DrissionPage import ChromiumPage, ChromiumOptions
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9129)
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
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
        "select id, day, page_url from col_paper_page where paper = '湖北省资产管理有限公司'")
    rows = cursor_test_1.fetchall()
    for id, day, page_url in rows:
        cursor_test_1.execute("delete from col_paper_page where id = %s", (id,))
        conn_test_1.commit()


            # print(id, day, page_url)
            # title_url = page_url
            # if title_url:
            #     res_title = requests.get(title_url, headers=headers)
            #     res_title_html1 = res_title.content.decode()
            #     res_title_html = etree.HTML(res_title_html1)
            #     title_date = "".join(res_title_html.xpath("//div[@class='date']//text()"))
            #     # 使用re模块提取日期
            #     title_date = re.findall(r'\d{4}-\d{2}-\d{2}', title_date)
            #     if title_date:
            #         title_date = title_date[0]
            #     else:
            #         title_date = ''
            #     title_content = "".join(res_title_html.xpath(
            #         "//div[@class='Introduce_details_nr wow fadeInUp animation']//text()"))
            #     title_html_info = res_title_html.xpath(
            #         "//div[@class='Introduce_details_title wow fadeInUp animation']")
            #     content_1 = res_title_html.xpath("//div[@class='Introduce_details_nr wow fadeInUp animation']")
            #     content_html = ''
            #     for con in title_html_info:
            #         content_html += etree.tostring(con, encoding='utf-8').decode()
            #     for con in content_1:
            #         content_html += etree.tostring(con, encoding='utf-8').decode()
            #     page = ChromiumPage(co)
            #     image = get_image(page, title_url,
            #                       "xpath=//div[@class='inside_content']/div[@class='w1200 Introduce_details']",
            #                       left_offset=10, down_offset=80)
            #     update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #     create_date = datetime.now().strftime('%Y-%m-%d')
            #     # 上传到测试数据库
            #     conn_test = mysql.connector.connect(
            #         host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            #         user="col2024",
            #         password="Bm_a12a06",
            #         database="col",
            #     )
            #     cursor_test = conn_test.cursor()
            #     # print(bm_name, article_name, article_url, bm_pdf, content)
            #     if 1:
            #         # 将报纸url上传
            #         up_img = upload_file(image, "png", "paper")
            #         # img_set.add(image)
            #         # 上传到报纸的图片或PDF
            #         insert_sql = "UPDATE col_paper_page SET original_img=%s, img_url=%s, update_time=%s, from_queue=%s, webpage_id=%s WHERE id=%s"
            #
            #         cursor_test.execute(insert_sql, (up_img, up_img, update_time, queue_id, webpage_id, id))
            #         conn_test.commit()
            #     # else:
            #     #     if os.path.exists(f'{image}.png'):
            #     #         os.remove(f'{image}.png')
            #
            #     if 1:
            #         # 上传到报纸的内容
            #         insert_sql = "UPDATE col_paper_notice SET content=%s, content_html=%s, update_time=%s, from_queue=%s, webpage_id=%s WHERE id=%s"
            #
            #         cursor_test.execute(insert_sql,
            #                             (title_content, content_html, update_time, queue_id, webpage_id, id))
            #         conn_test.commit()
            #
            #     cursor_test.close()
            #     conn_test.close()

    cursor_test_1.close()
    conn_test_1.close()


guangdong_gai(111, 222)

# paper_queue = paper_queue_next(webpage_url_list=['https://hubeiamc.com/Asset_Disposal_Announcement.html'])
# queue_id = paper_queue['id']
# webpage_id = paper_queue["webpage_id"]
# print(queue_id, webpage_id)
# guangdong_gai(queue_id, webpage_id)
# data = {
#     "id": queue_id,
#     'description': f'数据获取成功',
# }
# paper_queue_success(data=data)
# 1756418 16466


#    1756878

