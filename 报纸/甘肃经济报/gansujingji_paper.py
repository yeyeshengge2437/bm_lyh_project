import os
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
import re

import os
import json
import requests

produce_url = "http://121.43.164.84:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False


def paper_queue_next(webpage_url_list=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if webpage_url_list is None:
        webpage_url_list = []

    url = test_url + "/website/queue/next"
    data = {
        "webpage_url_list": webpage_url_list
    }

    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    print(result)
    return result.get("value")['id']


def paper_queue_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = test_url + "/website/queue/success"
    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result.get("value")


def paper_queue_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    try:
        if data is None:
            data = {}
        url = test_url + "/website/queue/fail"
        data_str = json.dumps(data)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        return result.get("value")
    except Exception as err:
        print(err)
        return None


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


from_queue = paper_queue_next(webpage_url_list=['https://szb.gansudaily.com.cn/gsjjrb'])
claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                         r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')

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
                article_name = article.xpath("./h4/text()")[0]
                # 获取文章链接
                article_url = art_base_url + article.xpath("./@href")[0].strip('../../..')
                if claims_keys.match(article_name):
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
                            database="col"
                        )
                        cursor_test = conn_test.cursor()
                        day = datetime.now().strftime('%Y-%m-%d')
                        paper = "甘肃经济日报"
                        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        create_date = datetime.now().strftime('%Y-%m-%d')

                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time,from_queue, create_date) VALUES (%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (
                                                bm_url, day, paper, article_name, article_content, article_url,
                                                create_time,
                                                from_queue, create_date))

                        conn_test.commit()
                        if original_pdf not in pdf_set:
                            pdf_set.add(original_pdf)
                            pdf_url = upload_pdf_by_url(original_pdf, "1")
                            insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue,create_date) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                            cursor_test.execute(insert_sql,
                                                (day, paper, bm_name, original_pdf, bm_url, pdf_url, create_time,
                                                 from_queue, create_date))
                            conn_test.commit()
                        cursor_test.close()
                        conn_test.close()

    success_data = {
        'id': from_queue,
        'description': '成功',
    }
    paper_queue_success(success_data)
else:
    print("今天没有新文章")
    fail_data = {
        "id": from_queue,
        "description": "该天没有报纸",
    }
    paper_queue_fail(fail_data)
