import os
import json
import re
import time
from datetime import datetime
import hashlib
import json
import mysql.connector
import requests
from lxml import etree
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria


def get_md5_set(database, table_name):
    hash_value_set = set()
    con_test = mysql.connector.connect(
        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database=database
    )
    cursor = con_test.cursor()
    # 获取表中的MD5值
    cursor.execute(f"SELECT md5 FROM {table_name}")
    for row in cursor:
        hash_value_set.add(row[0])
    return hash_value_set


md5_set = get_md5_set("col", "col_paper_notice")




paper = "青岛晚报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'sto-id-20480-epaper_guanhai_pool=FCDDGHHLFAAA; UM_distinctid=19145614b0885-053d503dfc301e-26001e51-13c680-19145614b09171f; CNZZDATA1279173235=2016012637-1723445890-%7C1723445918',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
pdf_domain = 'https://epaper.guanhai.com.cn/conpaper/qdwb/'
today = datetime.now().strftime('%Y-%m-%d')

def get_qingdao_lastpaper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'https://epaper.guanhai.com.cn/conpaper/qdwb/html/{paper_time}/'
    url = base_url + 'node_1.htm?v=1'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content1 = response.content.decode()
        html_1 = etree.HTML(content1)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//table[@id='bmdhTable']/tbody/tr")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./td[@class='default']/a[@id='pageLink']/text()"))
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./td[@class='default']/a[@id='pageLink']/@href"))
            # 获取版面pdf
            bm_pdf = pdf_domain + ''.join(bm.xpath("./td[2]/a/@href")).strip('../../../')
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//tbody/tr/td[@class='default'][2]/div/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()"))
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 进行数据的去重
                data_unique = f"文章标题：{str(article_name)}, 版面链接：{str(bm_url)}"
                # 数据去重
                hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//td/div[@id='ozoom']/founder-content//text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col"
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, content, bm_pdf)
                if bm_pdf not in pdf_set and judging_bm_criteria(article_name) and hash_value not in md5_set:
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, "青岛晚报", "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if judging_criteria(article_name, content) and hash_value not in md5_set:
                    md5_set.add(hash_value)


                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id, md5) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id, hash_value))
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


# get_qingdao_lastpaper("2024-08-27", 1111,2222)

