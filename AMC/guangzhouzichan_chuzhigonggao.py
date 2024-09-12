import os
import random
import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url, get_now_image

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9136)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_guangzhouzichan_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for count in range(1, 2 + 1):
            if count == 1:
                page_url = f'https://www.guangzhouamc.com/asset/chuzhigonggao.html'
            else:
                page_url = f'https://www.guangzhouamc.com/asset/chuzhigonggao-{count}.html'
            response = requests.get(page_url, headers=headers)
            res = response.content.decode()
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//ul[@class='block_list']/li[@class='slide-top']/a")
            img_set = set()
            name = '广州资产管理有限公司'
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = "".join(
                    title.xpath("./h2/text()"))
                title_date = "".join(title.xpath("./p/text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                title_url = "https://www.guangzhouamc.com" + "".join(title.xpath("./@href"))
                # print(title_name,title_url)
                # return
                res_title = requests.get(title_url, headers=headers)
                res_title_html1 = res_title.content.decode()
                res_title_html = etree.HTML(res_title_html1)

                title_content = "".join(res_title_html.xpath(
                    "//div[@class='wrapper']//text()"))

                annex = res_title_html.xpath("//div[@class='wrapper']//a/@src")
                if annex:
                    files = []
                    original_url = []
                    for ann in annex:
                        ann = "https://www.guangzhouamc.com" + ann
                        file_type = ann.split('.')[-1]
                        if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z', ]:
                            file_url = upload_file_by_url(ann, "ningbofujian", file_type)
                            files.append(file_url)
                            original_url.append(ann)
                else:
                    files = ''
                    original_url = ''
                files = str(files)
                original_url = str(original_url)

                title_html_info = res_title_html.xpath(
                    "//div[@class='wrapper']")
                # content_1 = res_title_html.xpath("//div[@class='Introduce_details_nr wow fadeInUp animation']")
                content_html = ''
                for con in title_html_info:
                    content_html += etree.tostring(con, encoding='utf-8').decode()
                # for con in content_1:
                #     content_html += etree.tostring(con, encoding='utf-8').decode()
                try:
                    image = get_image(page, title_url,
                                      "xpath=//div[@class='wrapper']",
                                      left_offset=10, right_offset=20)
                except:
                    image = get_now_image(page, title_url)
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
                                        (page_url, title_date, name, title_name, title_content, title_url, content_html,
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

# get_guangzhouzichan_chuzhigonggao(111, 222)
