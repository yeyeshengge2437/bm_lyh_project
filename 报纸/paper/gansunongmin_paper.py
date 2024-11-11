import os
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree
import re
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}
paper = "甘肃农民报"
general_url = 'https://szb.gansudaily.com.cn/gsnmb/pc/'
today = datetime.now().strftime('%Y-%m-%d')


def get_gansunongmin_paper_new(paper_time, queue_id, webpage_id):
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m/%d')
    base_url = f'https://szb.gansudaily.com.cn/gsnmb/pc/layout/{paper_time}/'
    target_url = base_url + 'col01.html'
    response = requests.get(target_url, headers=headers)
    pdf_set = set()
    if response.status_code == 200:
        html_data = response.content.decode()
        html_1 = etree.HTML(html_data)

        # 获取所有版面
        banmian = html_1.xpath("//div[@class='nav-list']/ul/li/a[@class='btn btn-block']")
        for bm in banmian:
            bm_name = bm.xpath("./text()")[0]
            bm_url = base_url + bm.xpath("./@href")[0]
            bm_res = requests.get(bm_url, headers=headers)
            time.sleep(2)
            if bm_res.status_code == 200:
                html_2data = bm_res.content.decode()
                html_2 = etree.HTML(bm_res.content.decode())
                # 获取该页的PDF
                pdf_url1 = re.findall(r'<!-- <p id="pdfUrl" style="display:none">(.*?)</p> -->', html_2data)[0]
                original_pdf = general_url + pdf_url1.strip('../../..')

                # 获取所有版面下的所有文章
                articles = html_2.xpath("//div[@class='news-list']/ul/li[@class='resultList']/a")
                for article in articles:
                    art_base_url = 'https://szb.gansudaily.com.cn/gsnmb/pc/'
                    # 获取文章名
                    article_name = ''.join(article.xpath(".//text()")).strip()
                    # 获取文章链接
                    article_url = art_base_url + article.xpath("./@href")[0].strip('../../..')
                    # 如果文章名中包含关键词，则进行下载
                    art_res = requests.get(article_url, headers=headers)
                    time.sleep(2)
                    try:
                        html_3 = etree.HTML(art_res.content.decode())
                        # 获取文章内容
                        article_content = "".join(
                            html_3.xpath("//div[@class='detail-art']/div[@id='ozoom']/founder-content/p/text()"))
                    except:
                        article_content = ''
                    conn_test = mysql.connector.connect(
                        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
                    cursor_test = conn_test.cursor()

                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # print(bm_name, article_name, original_pdf, article_url, article_content)
                    if original_pdf not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                        pdf_set.add(original_pdf)
                        pdf_url = upload_file_by_url(original_pdf, paper, 'pdf')
                        insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue,create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (day, paper, bm_name, original_pdf, bm_url, pdf_url, create_time,
                                             queue_id, create_date, webpage_id))
                        conn_test.commit()

                    if judging_criteria(article_name, article_content):


                            insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time,from_queue, create_date, webpage_id) VALUES (%s,%s, %s,%s,%s, %s, %s, %s, %s, %s)"

                            cursor_test.execute(insert_sql,
                                                (
                                                    bm_url, day, paper, article_name, article_content, article_url,
                                                    create_time,
                                                    queue_id, create_date, webpage_id))

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


def get_gansunongmin_paper_old(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m/%d')
    base_url = f'https://szb.gansudaily.com.cn/gsnmb/{paper_time}/'
    url = base_url + 'col01.html'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        if not html_1:
            raise Exception(f'该日期没有报纸')
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//ul[@id='layoutlist']/li[@class='posRelative']")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./a/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./a/@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_pdf = bm_html.xpath('//*[@id="pdfUrl"]/text()')
            if bm_pdf:
                bm_pdf = bm_pdf[0]
            else:
                continue

            # 获取所有文章的链接
            all_article = bm_html.xpath("//ul[@id='articlelist']/li[@class='clearfix']/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='ozoom']/founder-content//text()")).strip()
                # print(bm_name, article_name, article_url, bm_pdf, content)

                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                if bm_pdf not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if judging_criteria(article_name, content):
                # if 1:

                    # print(content)
                    # return

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


def get_gansunongmin_paper(paper_time, queue_id, webpage_id):
    paper_time1 = datetime.strptime(paper_time, '%Y-%m-%d').date()
    date_str = '2022-08-31'

    # 将字符串转换为日期对象
    date_str = datetime.strptime(date_str, '%Y-%m-%d').date()

    # 判断日期是否在范围内
    if paper_time1 <= date_str:
        get_gansunongmin_paper_old(paper_time, queue_id, webpage_id)
    else:
        get_gansunongmin_paper_new(paper_time, queue_id, webpage_id)


# get_gansunongmin_paper('2021-08-06', 1, 1)
