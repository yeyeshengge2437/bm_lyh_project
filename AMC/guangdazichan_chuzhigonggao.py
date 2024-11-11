import os
import random
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
co.set_paths(local_port=9143)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'BMAP_SECKEY=iWqrkVy0Q7kYJzZvdMKuGbgPBlxL42nokaqG2cZmo9ushx2ynZAHcb0KVujaIfsQoM9Vbp_XvGnGr3N5HZG7s7D1guyacrMs0ZPYimgaymJsARXm8857jsXGa75rrnF3mV1jGlhCT6alLswOlo7b70Z43z9SwViQ8t7T3E3JfL2dfcTwry0lseqZfvWHXFvo; SECKEY_ABVK=iWqrkVy0Q7kYJzZvdMKuGd7CYGlk0aI0lsUdmh9rK2U%3D',
    'Pragma': 'no-cache',
    'Referer': 'https://www.cebamc.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_guangdazichan_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        response = requests.post('https://www.cebamc.com/api/v1/JO/NewsList.ashx?cPath=25,26,&CurrentPage=1&PageSize=300',  headers=headers)
        res_json = response.json()
        title_list = res_json["NewsList"]
        img_set = set()
        name = "光大金瓯资产管理有限公司"
        title_set = judge_title_repeat(name)
        for title in title_list:
            title_name = title["cTitle"]
            title_date = title["changeDate"]
            title_url = f"https://www.cebamc.com/#/assets/detail/{title['id']}?type=0"
            if title_url not in title_set:
                title_url1 = f"https://www.cebamc.com/api/v1/JO/NewsDetail.ashx?id={title['id']}"
                title_res = requests.get(title_url1, headers=headers)
                res_title_json = title_res.json()
                content_html = res_title_json["NewsDetail"][0]["cContent"]
                title_content = ''.join(etree.HTML(content_html).xpath("//text()"))
                html = etree.HTML(content_html)
                annex = html.xpath("//@href | //@src")
                if annex:
                    # print(page_url, annex)
                    files = []
                    original_url = []
                    for ann in annex:
                        if "http" not in ann:
                            ann = "https://www.cebamc.com" + ann
                        file_type = ann.split('.')[-1]
                        if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                         'png', 'jpg'] and "attached" in ann:
                            file_url = upload_file_by_url(ann, "guangda", file_type)
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

                try:
                    image = get_image(page, title_url, "xpath=//div[@class='article-container']")
                except:
                    image = get_image(page, title_url, "xpath=//div[@class='col col-6-6 f-left']")
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

# get_guangdazichan_chuzhigonggao(111, 222)