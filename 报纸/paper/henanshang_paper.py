import os
import json
import re
import time
from datetime import datetime, timedelta
import pdfplumber
import mysql.connector
import requests
from lxml import etree
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    parse_pdf, judge_bm_repeat

paper = "河南商报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

pdf_domain = 'https://newpaper.dahe.cn/hnsb/'
today = datetime.now().strftime('%Y-%m-%d')


def get_henanshang_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'https://newpaper.dahe.cn/hnsb/html/{paper_time}/'
    url = base_url + 'node_1.htm'
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//ul[@class='layout-catalogue-list']/li[@class='layout-catalogue-item']")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./a[1]/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./a[1]/@href"))
            # 版面的pdf
            bm_pdf = pdf_domain + "".join(bm.xpath("./a[@class='pdf']/@href")).strip('../../..')

            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers, verify=False)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)


            pdf_set = set()
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
            if bm_pdf not in pdf_set and judge_bm_repeat(paper, bm_url):
                up_pdf = upload_file_by_url(bm_pdf, "河南商报", "pdf", "paper")
                pdf_set.add(bm_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                     create_date, webpage_id))
                conn_test.commit()
                # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@class='pic-box fl']/map/area")
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./@title")).strip()
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers, verify=False)
                time.sleep(2)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(
                    article_html.xpath("//div[@class='info']/div[@id='articleContent']//text()"))
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


# paper_claims(today)

# # 设置最大重试次数
# max_retries = 5
# retries = 0
# while retries < max_retries:
#     value = paper_queue_next(webpage_url_list=['https://newpaper.dahe.cn/hnsb/html'])
#     queue_id = value['id']
#     webpage_id = value["webpage_id"]
#     try:
#         get_henanshang_paper(today)
#         break
#     except Exception as e:
#         retries += 1
#         if retries == max_retries and "目前未有报纸" in str(e):
#             success_data = {
#                 'id': queue_id,
#                 'description': '今天没有报纸',
#             }
#             paper_queue_success(success_data)
#             break
#         else:
#
#             fail_data = {
#                 "id": queue_id,
#                 "description": f"出现问题:{e}",
#             }
#             paper_queue_fail(fail_data)
#             print(f'{e}, 等待一小时后重试...')
#             time.sleep(3610)  # 等待1小时后重试

# ####################################
# # 获取近两年的日期进行遍历
# # 获取当前时间
# now = datetime.now()
#
# # 设置起始年份和月份
# start_year = now.year - 1
# start_month = now.month
# current_date = datetime(start_year, start_month, 1)
#
# # 当前日期
# formatted_date = current_date.strftime('%Y-%m/%d')
#
# # 打印起始日期
# print("起始日期:", formatted_date)
#
# # 遍历近两年的日期
# while current_date <= now:
#     # 计算下一天的日期
#     current_date += timedelta(days=1)
#     # 更新格式化的日期
#     formatted_date = current_date.strftime('%Y-%m/%d')
#     print(formatted_date)
#     paper_claims(formatted_date)
#     time.sleep(10)
