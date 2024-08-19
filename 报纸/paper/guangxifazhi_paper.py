import os
import json
import re
import time
import pdfplumber
from datetime import datetime
from DrissionPage import ChromiumPage, ChromiumOptions
import mysql.connector
import requests
from lxml import etree

produce_url = "http://121.43.164.84:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False
co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9118)

# 构造实例
page = ChromiumPage(co)



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
    return result.get("value")


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


def upload_file_by_url(file_url, file_name, file_type, type="paper"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(file_url, headers=headers, verify=False)
    if r.status_code != 200:
        return "获取失败"
    pdf_path = f"{file_name}.{file_type}"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}
    url = 'http://121.43.164.84:29775' + f"/file/upload/file?type={type}"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    return result.get("value")["file_url"]


claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                         r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')
paper = "广西法制日报"

today = datetime.now().strftime('%Y-%m-%d')
# today = '2015-06/30'
queue_id = 1111
webpage_id = 1111


def get_guangxifazhi_paper(paper_time):
    # 将today的格式进行改变
    day = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    base_url = f'http://ipaper.pagx.cn/bz/html/'
    url = base_url + f'index.html?date={paper_time}&cid=1'
    page.get(url)
    data = page.html
    if page.url_available:
        bm_html = etree.HTML(data)
        bm_list = bm_html.xpath("//div[@class='article-con']/ul[@class='banmian-wenzhang']/li/a")
        for bm in bm_list:
            # 获取版面名称
            bm_name = ''.join(bm.xpath("./text()"))
            # 获取版面链接
            bm_url = base_url + ''.join(bm.xpath("./@href"))
            # 获取版面img
            bm_img = ''.join(bm_html.xpath("//div[@class='newspaper']/img[@class='newspaper-img']/@src")).replace("Z_",
                                                                                                                  "")
            # 获取版面下的内容
            page.get(bm_url)
            bm_data = page.html
            bm_html1 = etree.HTML(bm_data)
            bm_areaList = bm_html1.xpath("//div[@class='article-r']/ul[@class='banmian-wenzhang']/li/a")
            for bm_area in bm_areaList:
                # 获取文章名称
                article_name = ''.join(bm_area.xpath("./text()"))
                # 获取文章链接
                article_url = base_url + ''.join(bm_area.xpath("./@href"))

                pdf_set = set()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')

                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col_test",
                )
                cursor_test = conn_test.cursor()
                if bm_img not in pdf_set and ("公告" in article_name or claims_keys.match(article_name)):
                    # 将报纸img上传
                    up_img = upload_file_by_url(bm_img, "这是报纸", "img", "paper")
                    pdf_set.add(bm_img)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_img, bm_url, up_img, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if claims_keys.match(article_name):
                    # 获取文章内容
                    page.get(article_url)
                    article_data = page.html
                    article_html = etree.HTML(article_data)
                    content = ''.join(article_html.xpath("//div[@id='neirong']/div/p/text()"))
                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                cursor_test.close()
                conn_test.close()

    #     success_data = {
    #         'id': queue_id,
    #         'description': '数据获取成功',
    #     }
    #     paper_queue_success(success_data)
    #
    # else:
    #     # 获取当前时间小时分钟
    #     now = datetime.now().strftime('%m-%d %H:%M')
    #     raise Exception(f'{now}目前未有报纸，{response.status_code}')


get_guangxifazhi_paper(today)
# # 设置最大重试次数
# max_retries = 5
# retries = 0
# while retries < max_retries:
#     value = paper_queue_next(webpage_url_list=['http://epaper.zqcn.com.cn'])
#     queue_id = value['id']
#     webpage_id = value["webpage_id"]
#     try:
#         get_guangxifazhi_paper(today)
#         break
#     except Exception as e:
#         retries += 1
#         if retries == max_retries and "目前未有报纸" in e:
#             success_data = {
#                 'id': queue_id,
#                 'description': '今天没有报纸',
#             }
#             paper_queue_success(success_data)
#             break
#         else:
#             fail_data = {
#                 "id": queue_id,
#                 "description": f"出现问题:{e}",
#             }
#             paper_queue_fail(fail_data)
#             print(f'{e},等待一小时后重试...')
#             time.sleep(3610)  # 等待1小时后重试
