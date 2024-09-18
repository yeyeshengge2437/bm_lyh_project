import os
import json
import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "开封日报"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

today = datetime.now().strftime('%Y-%m-%d')
# today = '2022-05-19'

def get_kaifeng_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    base_url = f'https://epaper.kf.cn/paper/kfrb/{paper_time}/'
    url = base_url + 'data.js'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.text
        data = re.findall(r'var data = (.*?) var', data, re.S)[0]
        datas = json.loads(data)
        for data in datas:
            # 获取版面名称
            bm_name = data.get("catalog")
            # 获取版面中的数字
            bm_num = int(re.findall(r'\d+', bm_name)[0]) - 1
            bm_url = base_url + f'newspaper.html?edition={bm_num}'
            # 获取版面图片
            bm_img = 'https://epaper.kf.cn/' + data.get("imgSrc")
            # 获取版面下的内容
            bm_areaList = data.get("areaList")
            for bm_area in bm_areaList:
                # 获取文章名称
                article_name = bm_area.get('title')
                # 获取文章链接
                article_url = bm_area.get('shareLink')
                # 获取文章内容
                content = bm_area.get('html')
                if not content:
                    continue
                html = etree.HTML(content)
                content = ''.join(html.xpath('//text()'))
                img_set = set()

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
                # print(bm_name, article_name, article_url, bm_img, content)
                if bm_img not in img_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                    # 将报纸img上传
                    up_img = upload_file_by_url(bm_img, "开封日报", "jpg", "paper")
                    img_set.add(bm_img)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_img, bm_url, up_img, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()


                if judging_criteria(article_name, content):
                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()


                cursor_test.close()
                conn_test.close()

        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        raise Exception(f'该日期没有报纸')

# get_kaifeng_paper('2022-12-12', 1111, 3333)
