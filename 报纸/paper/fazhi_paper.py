from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
import mysql.connector
import time
from datetime import datetime
import os
import json
import requests
from api_paper import paper_queue_next, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url




claims_keys = [
    '债权通知书', '债权告知书', '债权通知公告', '债权登报公告', '债权补登公告', '债权补充公告', '债权拍卖公告', '债权公告', '债权通知',
    '转让通知书', '转让告知书', '转让通知公告', '转让登报公告', '转让补登公告', '转让补充公告', '转让拍卖公告', '转让公告', '转让通知',
    '受让通知书', '受让告知书', '受让通知公告', '受让登报公告', '受让补登公告', '受让补充公告', '受让拍卖公告', '受让公告', '受让通知',
    '处置通知书', '处置告知书', '处置通知公告', '处置登报公告', '处置补登公告', '处置补充公告', '处置拍卖公告', '处置公告', '处置通知',
    '招商通知书', '招商告知书', '招商通知公告', '招商登报公告', '招商补登公告', '招商补充公告', '招商拍卖公告', '招商公告', '招商通知',
    '营销通知书', '营销告知书', '营销通知公告', '营销登报公告', '营销补登公告', '营销补充公告', '营销拍卖公告', '营销公告', '营销通知',
    '信息通知书', '信息告知书', '信息通知公告', '信息登报公告', '信息补登公告', '信息补充公告', '信息拍卖公告', '信息公告', '信息通知',
    '联合通知书', '联合告知书', '联合通知公告', '联合登报公告', '联合补登公告', '联合补充公告', '联合拍卖公告', '联合公告', '联合通知',
    '催收通知书', '催收告知书', '催收通知公告', '催收登报公告', '催收补登公告', '催收补充公告', '催收拍卖公告', '催收公告', '催收通知',
    '催讨通知书', '催讨告知书', '催讨通知公告', '催讨登报公告', '催讨补登公告', '催讨补充公告', '催讨拍卖公告', '催讨公告', '催讨通知'
]


paper = '法制日报'

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9112)

# 构造实例
page = ChromiumPage(co)
# 获取当前年月日,格式为20240801
date_str = datetime.now().strftime('%Y%m%d')

def get_fazhi_paper(paper_time, queue_id, webpage_id):
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    structure_url = f"http://epaper.legaldaily.com.cn/fzrb/content/{paper_time}/"
    des_url = f'http://epaper.legaldaily.com.cn/fzrb/content/{paper_time}/Page01TB.htm'
    # 打开网页
    page.get(des_url)
    if page.url != des_url:
        raise Exception(f'该日期没有报纸')
    else:
        html = etree.HTML(page.html)
        # 获取所有版面
        all_bm = html.xpath("//table[3]/tbody/tr/td/a[@class='atitle']")
        # 遍历所有版面
        for bm in all_bm:
            # 获取版面名称
            bm_name = bm.xpath("./text()")[0]
            # 获取版面链接
            bm_link = bm.xpath("./@href")[0]
            bm_link = structure_url + bm_link
            page.get(bm_link)
            bm_html = etree.HTML(page.html)
            # 获取所有文章标题
            all_titles = bm_html.xpath("//table[5]/tbody/tr/td[2]/a[@class='atitle']")
            # 创建pdf文件路径集合
            pdf_path = set()

            # 遍历所有标题
            for title in all_titles:
                # 判断标题是否有公告等字样
                if '公告' in title.text:
                    # 获取标题对应的链接
                    link = title.xpath("./@href")[0]
                    ann_link = structure_url + link
                    page.get(ann_link)
                    ann_html = etree.HTML(page.html)
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')

                    # 获取pdf地址
                    paper_pdf = ann_html.xpath("//tr[2]/td/table/tbody/tr/td[8]/a[@class='14']/@href")[0]
                    paper_pdf = paper_pdf.strip('../../')
                    paper_pdf_url = 'http://epaper.legaldaily.com.cn/fzrb/' + paper_pdf
                    if paper_pdf_url not in pdf_path:
                        pdf_path.add(paper_pdf_url)
                        file_name = paper_pdf.strip('.pdf').replace("/", "_")
                        value = upload_file_by_url(paper_pdf_url, file_name=file_name, file_type='pdf')
                        if value:
                            # 上传到数据库
                            conn_test = mysql.connector.connect(
                                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                                user="col2024",
                                password="Bm_a12a06",
                                database="col"
                            )
                            cursor_test = conn_test.cursor()
                            name = bm_name
                            pdf_url = value
                            page_url = bm_link
                            original_pdf = paper_pdf_url

                            # 将数据插入到表中
                            insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date,webpage_id) VALUES (%s,%s,%s, %s, %s,%s, %s, %s, %s, %s)"

                            cursor_test.execute(insert_sql, (
                                day, paper, name, original_pdf, page_url, pdf_url, create_time, queue_id,
                                create_date, webpage_id))
                            conn_test.commit()
                            cursor_test.close()
                            conn_test.close()

                    # 获取公告内容
                    ann_contents = ann_html.xpath(
                        "//span[2]/table[2]/tbody/tr/td/table[2]/tbody/tr/td//br/following-sibling::text()[1]")
                    for content in ann_contents:
                        if any(key in content for key in claims_keys):
                            conn_test = mysql.connector.connect(
                                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                                user="col2024",
                                password="Bm_a12a06",
                                database="col"
                            )
                            page_url = ann_link
                            cursor_test = conn_test.cursor()
                            insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s, %s,%s,%s, %s, %s, %s, %s, %s)"

                            cursor_test.execute(insert_sql,
                                                (
                                                    page_url, day, paper, title, content, ann_link, create_time,
                                                    queue_id,
                                                    create_date, webpage_id))
                            conn_test.commit()
                            cursor_test.close()
                            conn_test.close()
        page.close()
        success_data = {
            "id": queue_id,
            "description": "数据获取成功"
        }
        paper_queue_success(success_data)


# # 设置最大重试次数
# max_retries = 5
# retries = 0
# while retries < max_retries:
#     value = paper_queue_next(webpage_url_list=['http://epaper.legaldaily.com.cn/fzrb'])
#     from_queue = value['id']
#     webpage_id = value["webpage_id"]
#     try:
#         get_fazhi_paper(date_str)
#         break
#     except Exception as e:
#         retries += 1
#         if retries == max_retries and "目前暂未有今天报纸" in str(e):
#             success_data = {
#                 'id': from_queue,
#                 'description': '今天没有报纸',
#             }
#             paper_queue_success(success_data)
#             break
#         else:
#
#             fail_data = {
#                 "id": from_queue,
#                 "description": f"出现问题:{e}",
#             }
#             paper_queue_fail(fail_data)
#             time.sleep(3610)  # 等待1小时后重试
