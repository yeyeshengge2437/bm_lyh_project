import os
import json
import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat
import mysql.connector
import requests
from lxml import etree





paper = "四川经济日报"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

today = datetime.now().strftime('%Y-%m-%d')


def get_sichuanjingji_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    url = f'http://epaper.scjjrb.com/Media/scjjrb/{paper_time}'
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.content.decode()
        bm_html = etree.HTML(data)
        bm_list = bm_html.xpath("//li[@class='item']")
        for bm in bm_list:
            # 获取版面名称
            bm_name = ''.join(bm.xpath("./div[@class='titlebox']/span/text()"))
            # 获取版面链接
            bm_url = 'http://epaper.scjjrb.com' + ''.join(bm.xpath("./a/@href"))

            # 获取版面下的内容
            bm_response = requests.get(bm_url, headers=headers, verify=False)
            time.sleep(2)
            bm_data = bm_response.content.decode()
            bm_html1 = etree.HTML(bm_data)
            # 获取版面pdf
            bm_pdf = ''.join(bm_html1.xpath("//ul/li[@id='pdf_toolbar']/a/@href"))
            bm_areaList = bm_html1.xpath("//ul/li[@class='item2-menu-item']/a")
            for bm_area in bm_areaList:
                # 获取文章名称
                article_name = ''.join(bm_area.xpath("./text()")).strip()
                # 获取文章链接
                article_url = 'http://epaper.scjjrb.com' + ''.join(bm_area.xpath("./@href"))
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers, verify=False)
                time.sleep(2)
                article_data = article_response.text
                article_html = etree.HTML(article_data)
                content = ''.join(article_html.xpath("//div[@class='article-cont']/p//text()"))
                pdf_set = set()

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
                if bm_pdf not in pdf_set and ("公告" in article_name or "公 告" in article_name or judging_criteria(article_name, content)) and judge_bm_repeat(paper, bm_url):
                    # 将报纸img上传
                    up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
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


# paper_queue = paper_queue_next(
#             webpage_url_list=['https://epaper.scjjrb.com'])
# webpage_name = paper_queue['webpage_name']
# queue_day = paper_queue['day']
# queue_id = paper_queue['id']
# webpage_id = paper_queue["webpage_id"]
# get_sichuanjingji_paper(today, queue_id, webpage_id)
