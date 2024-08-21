import os
import json
import re
import time
from datetime import datetime
from DrissionPage import ChromiumPage, ChromiumOptions
import mysql.connector
import requests
from lxml import etree
from api_paper import paper_queue_next, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9116)

# 构造实例
page = ChromiumPage(co)

claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                         r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')
paper = "洛阳日报"

pdf_domain = 'https://lyrb.lyd.com.cn/'
today = datetime.now().strftime('%Y-%m-%d')


def get_luoyang_paper(paper_time, queue_id, webpage_id):
    """
    获取洛阳日报的数据
    洛阳日报以2014年为节点，14年前后版本发生变化
    日期格式为：XXXX-XX/XX
    :param paper_time:
    :return:
    """
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')

    # 如果paper_time的日期在2014年12月1号之前的
    # 将字符串转换为datetime对象
    paper_time1 = datetime.strptime(paper_time, '%Y-%m/%d')
    # 定义2014年12月1号的datetime对象
    cutoff_date = datetime.strptime('2014-12/01', '%Y-%m/%d')
    pdf_set = set()

    if paper_time1 > cutoff_date:
        base_url = f'https://lyrb.lyd.com.cn/html2/{paper_time}/'
        url = base_url + 'node_3.htm'
        page.get(url)
        html_1 = etree.HTML(page.html)
        # 获取所有版面的的链接
        all_bm = html_1.xpath(
            "//tbody/tr[1]/td[1]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./td[@class='default']/a[@id='pageLink']/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./td[@class='default']/a[@id='pageLink']/@href"))
            # 版面的pdf
            bm_pdf = pdf_domain + "".join(bm.xpath("./td[2]/a/@href")).strip('../../..')
            # 获取版面详情
            page.get(bm_url)
            time.sleep(1)
            bm_content = page.html
            bm_html = etree.HTML(bm_content)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//ul[@class='main-ed-articlenav-list']/li/a")
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')

                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col_test",
                )
                cursor_test = conn_test.cursor()
                if bm_pdf not in pdf_set and ("公告" in article_name or claims_keys.match(article_name)):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, "这是报纸", "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if claims_keys.match(article_name):
                    # 获取文章内容
                    page.get(article_url)
                    time.sleep(1)
                    article_content = page.html
                    article_html = etree.HTML(article_content)
                    # 获取文章内容
                    content = ''.join(article_html.xpath("//div[@id='ozoom']/founder-content//text()"))

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time,
                                         queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                cursor_test.close()
                conn_test.close()
        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)
        page.close()
    else:
        base_url = f'https://lyrb.lyd.com.cn/html/{paper_time}/'

        url = base_url + 'node_4105.htm'
        page.get(url)
        html_1 = etree.HTML(page.html)
        # 获取所有版面的的链接
        all_bm = html_1.xpath(
            "//table[2]/tbody/tr/td[1]/table[3]/tbody/tr")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./td[@class='default'][1]/a[@id='pageLink']/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./td[@class='default'][1]/a[@id='pageLink']/@href"))
            # 版面的pdf
            bm_pdf = pdf_domain + "".join(bm.xpath("./td[@class='default'][2]/a/@href")).strip('../../..')
            # 获取版面详情
            page.get(bm_url)
            time.sleep(1)
            bm_content = page.html
            bm_html = etree.HTML(bm_content)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//tbody/tr[1]/td/table[3]/tbody/tr/td/table/tbody/tr/td[@class='default']/a")

            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath(".//text()")).strip()
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
                if bm_pdf not in pdf_set and ("公告" in article_name or claims_keys.match(article_name)):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, "这是报纸", "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if claims_keys.match(article_name):
                    # 获取文章内容
                    page.get(article_url)
                    time.sleep(1)
                    article_content = page.html
                    article_html = etree.HTML(article_content)
                    # 获取文章内容
                    content = ''.join(article_html.xpath("//tbody/tr/td/div[@id='ozoom']//text()"))

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
        page.close()



