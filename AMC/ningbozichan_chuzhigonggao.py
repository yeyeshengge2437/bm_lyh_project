import os
import random
import time
from datetime import datetime

import mysql.connector
from lxml import etree
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from api_paper import judge_bm_repeat, upload_file, judge_title_repeat, get_image, upload_file_by_url

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9131)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Content-Length': '0',
    # 'Cookie': 'Hm_lvt_95c247cff9bc1f5531523b6efabbe798=1726107052; Hm_lpvt_95c247cff9bc1f5531523b6efabbe798=1726107052; HMACCOUNT=FDD970C8B3C27398',
    'Origin': 'http://www.nbfamc.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.nbfamc.com/List.html?menuId=44',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

params = {
    'limit': '400',
    'menuId': '44',
    'page': '1',
}


def get_ningbozichan_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        response = requests.post('http://www.nbfamc.com/queryArtList', params=params, headers=headers, verify=False)
        res_json = response.json()
        title_list = res_json["page"]["list"]
        img_set = set()
        page_url = 'http://www.nbfamc.com/List.html?menuId=44'
        name = "宁波金融资产管理股份有限公司"
        title_set = judge_title_repeat(name)
        for title in title_list:
            title_name = title["title"]
            title_date = title["pubDate"]
            title_url = f"http://www.nbfamc.com/zixunList.html?menuId=44&id={title['id']}"
            if title_url not in title_set:
                title_url1 = f"http://www.nbfamc.com/queryArticle?id={title['id']}"
                title_res = requests.post(title_url1, headers=headers, verify=False)
                res_title_json = title_res.json()
                content_html = res_title_json["jgSubject"]["content"]
                title_ht = etree.HTML(content_html)
                title_content = ''.join(title_ht.xpath("//text()"))
                annex = title_ht.xpath("//a/@href")
                if annex:
                    files = []
                    original_url = []
                    for ann in annex:
                        file_type = ann.split('.')[-1]
                        if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z', ]:
                            file_url = upload_file_by_url(ann, "ningbofujian", file_type)
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
                try:
                    image = get_image(page, title_url, "xpath=//div[@id='article']")
                except:
                    image = ''
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
                                        (title_url, title_date, name, title_name, title_content, title_url, content_html,
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

# get_ningbozichan_chuzhigonggao(111, 222)
