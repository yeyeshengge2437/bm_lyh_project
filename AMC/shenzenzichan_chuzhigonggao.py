import os
import random
import re
import time
from datetime import datetime

import mysql.connector
from lxml import etree
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from AMC.api_paper import judge_bm_repeat, upload_file, judge_title_repeat, get_image, upload_file_by_url

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9150)


headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'sl-session=m9oQYDJV5WYNvULJ+kqzUg==',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.szamc.net/home/zcDispose',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def get_shenzenzichan_chuzhigonggao(queue_id, webpage_id):
    params = {
        'noticeType': '1',
        'pageIndex': '1',
        'pageSize': '10',
    }
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        response = requests.get('https://www.szamc.net/index/notice/getNoticeIndexList',  headers=headers, params=params)
        res_json = response.json()
        title_list = res_json["data"]
        img_set = set()
        name = "深圳资产管理有限公司"
        title_set = judge_title_repeat(name)
        for title in title_list:
            title_name = title["title"]
            title_date = title["addTime"]
            title_url = f"https://www.szamc.net/home/noticeInfo?id={title['id']}&noticeType=1"
            if title_url not in title_set:
                title_url1 = f'https://www.szamc.net/index/notice/getNoticeByIdList?id={title["id"]}&noticeType=1'
                title_res = requests.get(title_url1, headers=headers)
                res_title_json = title_res.json()
                content_html = res_title_json["data"]["data"]["contents"]
                content_html = re.sub(r'＜', '<', content_html)
                content_html = re.sub(r'＞', '>', content_html)
                title_ht = etree.HTML(content_html)
                title_content = "".join(title_ht.xpath("//text()"))
                title_content = re.sub(r'＆nbsp;', '', title_content)
                annex = title_ht.xpath("//a/@href | //img/@src")
                if annex:
                    files = []
                    original_url = []
                    for ann in annex:
                        if "http" not in ann:
                            ann = "https://www.szamc.net" + ann
                        file_type = ann.split('.')[-1]
                        if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z', 'jpg', 'png']:
                            file_url = upload_file_by_url(ann, "shenzen", file_type)
                            files.append(file_url)
                            original_url.append(ann)
                    print(original_url)
                else:
                    files = ''
                    original_url = ''
                if not files:
                    files = ''
                    original_url = ''
                files = str(files).replace("'", '"')
                original_url = str(original_url).replace("'", '"')

                image = get_image(page, title_url, "xpath=//div[@class='newsdetails ullist']")
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
                                        (
                                        title_url, title_date, name, title_name, title_content, title_url, content_html,
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

# get_shenzenzichan_chuzhigonggao(111, 222)