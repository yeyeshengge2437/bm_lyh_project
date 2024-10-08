import os
import json
import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from api_paper import judging_criteria, paper_queue_success, judge_bm_repeat, paper_queue_delay, upload_file_by_url


paper = "半岛都市报"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}
pdf_domain = 'https://bddsb.bandao.cn/pc/bddsb/'
today = datetime.now().strftime('%Y-%m-%d')


def get_bandao_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    base_url = f'https://bddsb.bandao.cn/pc/bddsb/{paper_time}/'
    url = base_url + 'PageA01BC.htm'
    response = requests.get(url, headers=headers)
    time.sleep(2)
    if response.status_code == 200:
        content = response.text
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@class='banmianlist_box']/a")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./text()"))
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(2)
            bm_content = bm_response.text
            bm_html = etree.HTML(bm_content)
            bm_pdf = pdf_domain + "".join(bm_html.xpath("//div[@class='pdf']/a/@href")).strip("../")

            # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@id='mylink']/a[@class='overlink']")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./@neirong"))
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
                # print(bm_name, article_name, article_url, bm_pdf)

                if bm_pdf not in pdf_set and ("公告" in article_name and len(article_name) < 10) and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, "半岛都市", "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.text
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//td/div[@id='ozoom']/founder-content//text()"))

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


# get_bandao_paper('2019-08-12', 111, 2222)
