import os
import json
import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria, zhengquan_criteria
import mysql.connector
import requests
from lxml import etree


paper = "证券日报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    # 'Cookie': 'acw_tc=0b6e705217240488564015271e3e6d38f36878daddd5a285a5fcd2791dbce4; Hm_lvt_63dcca6ee91813e5f435c35c310757f8=1724048857; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_9d18b05458bf388fcb38b0778469e76d=1724048857; __utma=61717624.2020133750.1724048869.1724048869.1724048869.1; __utmc=61717624; __utmz=61717624.1724048869.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; Hm_lvt_9ad5291ccdbd67ec8d39a921b7b5a320=1724048869; Hm_lpvt_63dcca6ee91813e5f435c35c310757f8=1724048886; Hm_lpvt_9d18b05458bf388fcb38b0778469e76d=1724048886; __utmb=61717624.4.10.1724048869; Hm_lpvt_9ad5291ccdbd67ec8d39a921b7b5a320=1724048886',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://epaper.zqrb.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

today = datetime.now().strftime('%Y-%m-%d')


def get_zhengquan_paper(paper_time,queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'http://epaper.zqrb.cn/html/{paper_time}/'
    url = base_url + 'node_2.htm'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@id='pgn']/table/tbody/tr/td[2]")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./a[@id='pageLink']/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./a[@id='pageLink']/@href")).strip('./')
            # 版面的pdf
            bm_pdf = 'http://epaper.zqrb.cn/' + "".join(bm.xpath("./div/a/@href")).strip('../../..')
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(2)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@id='pgt']/table/tbody/tr/td[@class='default'][2]")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./a/@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./a/div/text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                if article_html is None:
                    continue
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@class='neiye']/div[@class='neiyee']/p/text()"))
                # print(bm_name, article_name, article_url, bm_pdf, content)

                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                if bm_pdf not in pdf_set and zhengquan_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if zhengquan_criteria(article_name):

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


# get_zhengquan_paper('2020-08-22', 111, 222)
