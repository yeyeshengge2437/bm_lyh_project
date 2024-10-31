import os
import random
import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9135)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '__jsluid_s=cdfab3d82845437d2566ae0973248874; Hm_lvt_15f7cbbd8a4562c45b5b1e4ee76ed715=1726125558; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_15f7cbbd8a4562c45b5b1e4ee76ed715=1726126240; XSRF-TOKEN=eyJpdiI6IndmM28xR0xDYkdvQVdwVkg1K1pjakE9PSIsInZhbHVlIjoiNmZkQXFrQ3Z4aVROaDh5Mk4rSzZNbGFSRnlXRERja1RwcnV6TWpyVjRLUTMxZWdFZm5ZUHE3QUNYV2NBaTlrYiIsIm1hYyI6ImZkNTUyYjk2ODRhNDIxYjhhNzE1M2U2MWE4NGY5NTYxNjRhYzkyODliN2IzMmQ5OWI3Zjc4MTRiYTk4NGE4NGIifQ%3D%3D; alps_session=eyJpdiI6IkxNTlNmVWtFU2FUWUtOY2lcL3Y1UmlBPT0iLCJ2YWx1ZSI6ImxrMVQ3eEdcLzFkdXE1K3MwTkRFcUJWRmN5UkhqNkZvR1pJU2Nzckh3b042b0s5aVhSUXRJNXYyOWs5YUpGV3ZIIiwibWFjIjoiNWY2MjUyY2ZkODhjZDBmOTVkMzM1OGY3NDNkOWM2ZmFjMjQ2MWU3ZjkwYzYxNzcxMmFlOTI4YzA0MjE3Y2ZkYSJ9',
    'Pragma': 'no-cache',
    'Referer': 'https://www.snfamc.com/news/notice',
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


def get_shanxijinrong_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for count in range(1, 18 + 1):
            page_url = f'https://www.snfamc.com/news/notice?page={count}'
            response = requests.get(page_url, headers=headers)
            res = response.content.decode()
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//div[@class='zixun-2 wow fadeInUp']/ul[@class='list-unstyled']/li")
            img_set = set()
            name = '陕西金融资产管理股份有限公司'
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = "".join(
                    title.xpath("./a/text()"))
                title_date = "".join(title.xpath("./span/text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                title_url = "https://www.snfamc.com" + "".join(title.xpath("./a/@href"))
                if title_url not in title_set:
                    # print(title_name,title_url)
                    # return
                    res_title = requests.get(title_url, headers=headers)
                    res_title_html1 = res_title.content.decode()
                    res_title_html = etree.HTML(res_title_html1)

                    title_content = "".join(res_title_html.xpath(
                        "//div[@class='about-right-p']/p//text()"))

                    annex = res_title_html.xpath("//div[@class='about-right-p']//@href | //div[@class='about-right-p']//@src")
                    if annex:
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = "https://www.snfamc.com" + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpeg'] and "posts" in ann:
                                file_url = upload_file_by_url(ann, "shanxijin", file_type)
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

                    title_html_info = res_title_html.xpath(
                        "//div[@class='about-right-p']")
                    # content_1 = res_title_html.xpath("//div[@class='Introduce_details_nr wow fadeInUp animation']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    # for con in content_1:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()

                    image = get_image(page, title_url,
                                      "xpath=//div[@class='about-right-p']",
                                      left_offset=10, down_offset=40)
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col",
                    )
                    cursor_test = conn_test.cursor()
                    # print(bm_name, article_name, article_url, bm_pdf, content)
                    if image not in img_set and judge_bm_repeat(name, title_url):
                        # 将报纸url上传
                        up_img = upload_file(image, "png", "paper")
                        img_set.add(image)
                        # 上传到报纸的图片或PDF
                        insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_date, name, title_name, up_img, title_url, up_img, create_time, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                    else:
                        if os.path.exists(f'{image}.png'):
                            os.remove(f'{image}.png')

                    if title_url not in title_set:
                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time,original_files, files, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_url, title_date, name, title_name, title_content, title_url,
                                             content_html,
                                             create_time, original_url, files, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                        title_set.add(title_url)

                    cursor_test.close()
                    conn_test.close()
        page.close()
    except Exception as e:
        page.close()
        raise Exception(e)

# get_shanxijinrong_chuzhigonggao(111, 222)
