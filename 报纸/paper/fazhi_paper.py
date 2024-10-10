from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
import mysql.connector
import time
from datetime import datetime
import os
import json
import requests
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat

paper = '法制日报'

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9112)




def get_fazhi_paper(paper_time, queue_id, webpage_id):
    # 构造实例
    page = ChromiumPage(co)
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    structure_url = f"http://epaper.legaldaily.com.cn/fzrb/content/{paper_time}/"
    des_url = f'http://epaper.legaldaily.com.cn/fzrb/content/{paper_time}/Page01TB.htm'
    # 创建pdf文件路径集合
    pdf_path = set()
    # 打开网页
    page.get(des_url)
    if page.url_available:
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


            # 遍历所有标题
            for title in all_titles:
                # 判断标题是否有公告等字样
                if '公告' in title.text:
                    # 获取标题对应的链接
                    title_name = ''.join(title.xpath("./text()"))
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
                    if paper_pdf_url not in pdf_path and judge_bm_repeat(paper, bm_link):
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
                        if judging_criteria(title_name, content):
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
                                                    page_url, day, paper, title_name, content, ann_link, create_time,
                                                    queue_id,
                                                    create_date, webpage_id))
                            conn_test.commit()
                            cursor_test.close()
                            conn_test.close()
        page.quit()
        success_data = {
            "id": queue_id,
            "description": "数据获取成功"
        }
        paper_queue_success(success_data)

    else:
        page.quit()
        raise Exception(f'该日期没有报纸')

# get_fazhi_paper('2024-09-05', 111, 222)
