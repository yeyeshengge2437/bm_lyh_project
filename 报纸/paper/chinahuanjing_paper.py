
import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat
import mysql.connector
import requests
from lxml import etree



paper = "中国环境报"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    # 'Cookie': 'Hm_lvt_231ab2c8aa13bfdeaf7f1ca0820e590d=1723441009; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_231ab2c8aa13bfdeaf7f1ca0820e590d=1723441045',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://news.cenews.com.cn/html/2024-08/08/node_2.htm',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

pdf_domain = 'http://news.cenews.com.cn/html/'
today = datetime.now().strftime('%Y-%m/%d')


def get_chinahuanjiang_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'http://news.cenews.com.cn/html/{paper_time}/'
    url = base_url + 'node_2.htm'
    response = requests.get(url, headers=headers)
    time.sleep(1)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//tbody/tr/td[@class='px12']/a[@id='pageLink']")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./text()"))
            # 版面链接
            bm_url = base_url + "".join(bm.xpath("./@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)
            # 版面PDF
            bm_pdf = pdf_domain + "".join(bm_html.xpath("//td[@class='px12'][3]/a/@href")).strip('../..')

            # 获取所有文章的链接
            all_article = bm_html.xpath("//td[2]/table/tbody/tr/td[2]/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath(".//text()"))
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='ozoom']/founder-content/p/text()"))
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                if bm_pdf not in pdf_set and judging_criteria(article_name, content) and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, "chinahuanjing", "pdf", "paper")
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


# # 设置最大重试次数
# max_retries = 5
# retries = 0
# while retries < max_retries:
#     value = paper_queue_next(webpage_url_list=['https://epaper.cenews.com.cn'])
#     queue_id = value['id']
#     webpage_id = value["webpage_id"]
#     try:
#         get_chinahuanjiang_paper(today)
#         break
#     except Exception as e:
#         retries += 1
#         if retries == max_retries:
#             month_day = datetime.now().strftime('%Y-%m-%d')
#             success_data = {
#                 'id': queue_id,
#                 'description': f'{month_day}没有报纸',
#             }
#             paper_queue_success(success_data)
#             break
#         else:
#
#             fail_data = {
#                 "id": queue_id,
#                 "description": f"{e}",
#             }
#             paper_queue_fail(fail_data)
#             time.sleep(3610)  # 等待1小时后重试
