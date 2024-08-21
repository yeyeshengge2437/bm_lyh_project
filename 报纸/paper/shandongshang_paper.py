import os
import json
import re
import time
from datetime import datetime
from api_paper import paper_queue_next, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url
import mysql.connector
import requests
from lxml import etree


claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                         r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')
paper = "山东商报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://dzb.subaoxw.com/html/2023-03/14/content_319257.htm',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}
pdf_domain = 'http://dzb.subaoxw.com/'
today = datetime.now().strftime('%Y-%m-%d')

def get_shandongshang_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'http://dzb.subaoxw.com/html/{paper_time}/'
    url = base_url + 'node_2.htm'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@id='scroll']/ul/li/div[@class='l']")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./a/text()"))
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./a/@href"))
            # 获取版面pdf
            bm_pdf = pdf_domain + ''.join(bm.xpath("./div[@class='right']/a[2]/@href")).strip("../../..")
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@class='listAll']/ul/li/div[@class='l']/span[@class='tit']")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./a/@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./a/text()"))
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')

                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//td/div[@id='ozoom']/founder-content//text()"))
                article_title = ''.join(article_html.xpath("//div[@class='content']/h1[@class='tit']/text()"))

                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col"
                )
                cursor_test = conn_test.cursor()
                if bm_pdf not in pdf_set and ("公告" in article_name or claims_keys.match(article_title) or "分类" in bm_name or "警界" in bm_name or "无标题" in article_name):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, "青岛晚报", "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    print(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if claims_keys.match(article_title):

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




