import os
import json
import re
import time
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    parse_pdf, judge_bm_repeat
from datetime import datetime
from DrissionPage import ChromiumPage, ChromiumOptions
import mysql.connector
import requests
from lxml import etree

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9118)

paper = "广西法治日报"

today = datetime.now().strftime('%Y-%m-%d')


def get_guangxifazhi_paper(paper_time, queue_id, webpage_id):
    # 构造实例
    page = ChromiumPage(co)
    # 将today的格式进行改变
    day = paper_time
    base_url = f'http://ipaper.pagx.cn/bz/html/'
    url = base_url + f'index.html?date={paper_time}&cid=1'
    page.get(url)

    if page.url_available:
        data = page.html
        bm_html = etree.HTML(data)
        bm_list = bm_html.xpath("//div[@class='article-con']/ul[@class='banmian-wenzhang']/li/a")
        for bm in bm_list:
            # 获取版面名称
            bm_name = ''.join(bm.xpath("./text()"))
            # 获取版面链接
            bm_url = base_url + ''.join(bm.xpath("./@href"))
            # 获取版面pdf
            bm_pdf = ''.join(bm_html.xpath("//div[@class='newspaper']/img[@class='newspaper-img']/@src")).replace("Z_",
                                                                                                                  "")
            bm_pdf = bm_pdf.replace('jpg', 'pdf')

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

            if bm_pdf not in pdf_set and judge_bm_repeat(paper, bm_url):
                # 将报纸img上传
                up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                pdf_set.add(bm_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                     create_date, webpage_id))
                conn_test.commit()
            cursor_test.close()
            conn_test.close()
        page.quit()
        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        page.quit()
        raise Exception(f'该日期没有报纸')


# value = paper_queue_next(webpage_url_list=['https://ipaper.pagx.cn'])
# queue_id = value['id']
# webpage_id = value["webpage_id"]
# queue_id = 1111
# webpage_id = 2222
# get_guangxifazhi_paper('2024-08-22', queue_id, webpage_id)
