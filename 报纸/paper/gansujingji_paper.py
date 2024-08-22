import os
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url
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
paper = "甘肃经济日报"
general_url = 'https://szb.gansudaily.com.cn/gsjjrb/pc/'
today = datetime.now().strftime('%Y-%m-%d')
def get_gansujingji_paper(paper_time, queue_id, webpage_id):
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m/%d')
    base_url = f'https://szb.gansudaily.com.cn/gsjjrb/pc/layout/{paper_time}/'
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
                    art_base_url = 'https://szb.gansudaily.com.cn/gsjjrb/pc/'
                    # 获取文章名
                    article_name = ''.join(article.xpath(".//text()")).strip()
                    # 获取文章链接
                    article_url = art_base_url + article.xpath("./@href")[0].strip('../../..')
                    # 如果文章名中包含关键词，则进行下载
                    art_res = requests.get(article_url, headers=headers)
                    time.sleep(2)
                    if art_res.status_code == 200:
                        html_3 = etree.HTML(art_res.content.decode())
                        # 获取文章内容
                        article_content = "".join(
                            html_3.xpath("//div[@class='detail-art']/div[@id='ozoom']/founder-content/p/text()"))
                    else:
                        article_content = ''
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
                    cursor_test = conn_test.cursor()

                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')

                    if original_pdf not in pdf_set and ("公告" in article_name or judging_criteria(article_name, article_content)):
                        pdf_set.add(original_pdf)
                        pdf_url = upload_file_by_url(original_pdf, "1", 'pdf')
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

# paper_queue = paper_queue_next(
#             webpage_url_list=['https://szb.gansudaily.com.cn/gsjjrb'])
# queue_id = paper_queue['id']
# webpage_id = paper_queue["webpage_id"]
# # queue_id = '1111111111'
# # webpage_id = '2222'
# get_gansujingji_paper(today, queue_id, webpage_id)



