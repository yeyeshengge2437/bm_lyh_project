import os
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
import re


def upload_pdf_by_url(pdf_url, file_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(pdf_url, headers=headers)
    if r.status_code != 200:
        return "获取失败"
    pdf_path = f"{file_name}.pdf"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}

    url = 'http://121.43.164.84:29775' + "/file/upload/file?type=paper"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    return result.get("value")["file_url"]


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

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}
general_url = 'https://szb.gansudaily.com.cn/gsjjrb/pc/'
year_month = datetime.now().strftime('%Y%m')
date = datetime.now().strftime('%d')
base_url = f'https://szb.gansudaily.com.cn/gsjjrb/pc/layout/{year_month}/{date}/'
target_url = base_url + 'col01.html'
response = requests.get(target_url, headers=headers)
if response.status_code == 200:
    html_data = response.content.decode()
    html_1 = etree.HTML(html_data)

    # 获取所有版面
    banmian = html_1.xpath("//div[@class='nav-list']/ul/li/a[@class='btn btn-block']")
    for bm in banmian:
        bm_name = bm.xpath("./text()")[0]
        bm_url = base_url + bm.xpath("./@href")[0]
        bm_res = requests.get(bm_url, headers=headers)
        if bm_res.status_code == 200:
            html_2data = bm_res.content.decode()
            html_2 = etree.HTML(bm_res.content.decode())
            # 获取该页的PDF
            pdf_url1 = re.findall(r'<!-- <p id="pdfUrl" style="display:none">(.*?)</p> -->', html_2data)[0]
            original_pdf = general_url + pdf_url1.strip('../../..')
            print(original_pdf)
            # 获取所有版面下的所有文章
            articles = html_2.xpath("//div[@class='news-list']/ul/li[@class='resultList']/a")
            for article in articles:
                art_base_url = 'https://szb.gansudaily.com.cn/gsjjrb/pc/'
                # 获取文章名
                article_name = article.xpath("./h4/text()")[0]
                # 获取文章链接
                article_url = art_base_url + article.xpath("./@href")[0].strip('../../..')
                if any(keyword in article_name for keyword in claims_keys):
                    # 如果文章名中包含关键词，则进行下载
                    art_res = requests.get(article_url, headers=headers)
                    if art_res.status_code == 200:
                        html_3 = etree.HTML(art_res.content.decode())
                        # 获取文章内容
                        article_content = "".join(
                            html_3.xpath("//div[@class='detail-art']/div[@id='ozoom']/founder-content/p/text()"))
                        # 上传数据库
                        # 连接数据库
                        conn_test = mysql.connector.connect(
                            host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                            user="col2024",
                            password="Bm_a12a06",
                            database="col_test"
                        )
                        cursor_test = conn_test.cursor()
                        day = datetime.now().strftime('%Y-%m-%d')
                        paper = "甘肃经济日报"
                        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        create_date = datetime.now().strftime('%Y-%m-%d')
                        pdf_url = upload_pdf_by_url(original_pdf, "1")
                        print("++++++++++++++", pdf_url)
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, create_date) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (
                                            bm_url, day, paper, article_name, article_content, article_url, create_time,
                                            create_date))

                        conn_test.commit()
                        insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, create_date) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (day, paper, bm_name, original_pdf, bm_url, pdf_url, create_time,
                                             create_date))
                        conn_test.commit()
                        cursor_test.close()
                        conn_test.close()
else:
    print("改天没有新文章")
