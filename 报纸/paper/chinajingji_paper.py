import os
import json
import re
import time
from datetime import datetime
from DrissionPage import ChromiumPage, ChromiumOptions
import mysql.connector
import requests
from lxml import etree
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths().auto_port()





paper = "中国经济时报"
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
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}



today = datetime.now().strftime('%Y-%m-%d')


def get_chinajingji_paper(paper_time, queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    # 取消所有的弹出框
    page.set.auto_handle_alert()
    try:
        params = {
            'date': paper_time,
            'btn_sch_date': '搜索',
        }
        # 将today的格式进行改变
        day = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
        base_url = f'https://jjsb.cet.com.cn/'
        url = 'https://jjsb.cet.com.cn/DigitaNewspaper.aspx'
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            content = response.content.decode()
            html_1 = etree.HTML(content)
            # 获取所有版面的的链接
            all_bm = html_1.xpath("//td[2]/div/a")
            for bm in all_bm:
                # 版面名称
                bm_name = "".join(bm.xpath("./text()"))
                bm_name = re.sub(r'[ \t\r\n\f\v]+', '', bm_name)
                # 版面链接
                bm_url = base_url + ''.join(bm.xpath("./@href"))
                # 获取版面详情
                bm_response = requests.get(bm_url, headers=headers)
                time.sleep(1)
                bm_content = bm_response.content.decode()
                bm_html = etree.HTML(bm_content)
                # 版面的pdf
                bm_pdf = base_url + "".join(bm_html.xpath("//td[3]/div/a/@href"))[1:]
                # 获取所有文章的链接
                all_article = bm_html.xpath("//div/ul/li/a")
                pdf_set = set()
                for article in all_article:
                    # 获取文章链接
                    article_url = base_url + ''.join(article.xpath("./@href"))
                    # 获取文章名称
                    article_name = ''.join(article.xpath("./text()")).strip()
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # 获取文章内容
                    page.get(article_url)
                    time.sleep(1)
                    article_content = page.html
                    article_html = etree.HTML(article_content)
                    # 获取文章内容
                    content = ''.join(article_html.xpath("//div/div[3]/span//text()"))
                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col",
                    )
                    cursor_test = conn_test.cursor()
                    # print(bm_name, article_name, bm_pdf, content)
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


                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
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
    except Exception as e:
        page.quit()
        raise Exception(e)



# get_chinajingji_paper('2024-08-23', 1111,2222)

# # 设置最大重试次数
# max_retries = 5
# retries = 0
# while retries < max_retries:
#     value = paper_queue_next(webpage_url_list=['https://jjsb.cet.com.cn'])
#     queue_id = value['id']
#     webpage_id = value["webpage_id"]
#     try:
#         get_chinajingji_paper(today)
#         break
#     except Exception as e:
#         retries += 1
#         if retries == max_retries and "暂未获取到今日报纸" in str(e):
#             success_data = {
#                 'id': queue_id,
#                 'description': '今日没有报纸',
#             }
#             paper_queue_success(success_data)
#             break
#         else:
#             fail_data = {
#                 "id": queue_id,
#                 "description": f"问题:{e}",
#             }
#             paper_queue_fail(fail_data)
#             print("等待一小时后重试...")
#             time.sleep(3610)  # 等待1小时后重试

