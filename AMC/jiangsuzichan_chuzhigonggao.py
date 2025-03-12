import os
import random
import time
from datetime import datetime

import mysql.connector
from lxml import etree
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from api_paper import judge_bm_repeat, upload_file, judge_title_repeat, get_image, get_now_image, upload_file_by_url

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9133)


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://www.jsamc.com.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.jsamc.com.cn/assets-promote/promote-information',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}




def get_jiangsuzichan_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for count in range(20, 36 + 1):
            json_data = {
                'body': {
                    'showStatus': 2,
                    'current': count,
                },
            }
            response = requests.post('https://www.jsamc.com.cn/prod-api/disposal_notice/homePage/list/v2', headers=headers, json=json_data)
            res_json = response.json()
            title_list = res_json["body"]["list"]
            img_set = set()
            page_url = 'https://www.jsamc.com.cn/assets-promote/promote-information'
            name = "江苏资产管理有限公司"
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = title["name"]
                title_date = title["showTime"]
                title_url = f"https://www.jsamc.com.cn/assets-promote/disposal-announcement/{title['id']}"
                if title_url not in title_set:
                    title_res = requests.get(title_url, headers=headers)
                    res_title = title_res.content.decode()
                    res_title_html = etree.HTML(res_title)
                    title_content = ''.join(res_title_html.xpath("//div[@class='assetsPost_contentContainer__EoCnw']//text()"))
                    title_html_info = res_title_html.xpath(
                        "//div[@class='assetsPost_postHeaderContainer__1M8R8']/h4")
                    content_1 = res_title_html.xpath("//div[@class='assetsPost_contentContainer__EoCnw']")
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
                                ann = 'https://www.jsamc.com.cn' + ann
                            else:
                                continue
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', ] and 'file' in ann:
                                file_url = upload_file_by_url(ann, "jiangsu", file_type)
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
                    image = get_image(page, title_url, "xpath=//div[@class='assetsPost_postContainer__2ziyr']")
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
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

# get_jiangsuzichan_chuzhigonggao(111, 222)