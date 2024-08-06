
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
import mysql.connector
import time
from datetime import datetime
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

not_claims_keys = ['法院公告', '减资公告', '注销公告', '清算公告', '合并公告', '出让公告', '重组公告', '调查公告', '分立公告', '重整公告', '悬赏公告', '注销登记公告']
paper = '法制日报'
day = datetime.now().strftime('%Y-%m-%d')
create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
create_date = datetime.now().strftime('%Y-%m-%d')
co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9112)
from_queue = paper_queue_next(webpage_url_list=['http://epaper.legaldaily.com.cn/fzrb'])
# 构造实例
page = ChromiumPage(co)
# 获取当前年月日,格式为20240801
now = datetime.now()
date_str = now.strftime('%Y%m%d')
structure_url = f"http://epaper.legaldaily.com.cn/fzrb/content/{date_str}/"
# des_url = structure_url + 'PageArticleIndexBT.htm'
des_url = 'http://epaper.legaldaily.com.cn/fzrb/content/20240806/Page01TB.htm'

# 打开网页
page.get(des_url)
if page.url != des_url:
    print("该天没有报纸")
    fail_data = {
        "id": from_queue,
        "description": "该天没有报纸",
    }
    paper_queue_fail(fail_data)
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
        # 遍历所有文章标题
        for title in all_titles:

            # 遍历所有标题
            for title in all_titles:
                # 判断标题是否有公告等字样
                if '公告' in title.text:
                    # 获取标题对应的链接
                    link = title.xpath("./@href")[0]
                    ann_link = structure_url + link
                    page.get(ann_link)
                    ann_html = etree.HTML(page.html)

                    # 获取pdf地址
                    paper_pdf = ann_html.xpath("//tr[2]/td/table/tbody/tr/td[8]/a[@class='14']/@href")[0]
                    paper_pdf = paper_pdf.strip('../../')
                    paper_pdf_url = 'http://epaper.legaldaily.com.cn/fzrb/' + paper_pdf
                    if paper_pdf_url not in pdf_path:
                        pdf_path.add(paper_pdf_url)
                        file_name = paper_pdf.strip('.pdf').replace("/", "_")
                        value = upload_pdf_by_url(paper_pdf_url, file_name=file_name)
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
                            insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date) VALUES (%s,%s, %s, %s,%s, %s, %s, %s, %s)"

                            cursor_test.execute(insert_sql, (
                                day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue,
                                create_date))
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
                            insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date) VALUES (%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                            cursor_test.execute(insert_sql,
                                                (
                                                page_url, day, paper, title, content, ann_link, create_time, from_queue,
                                                create_date))
                            conn_test.commit()
                            cursor_test.close()
                            conn_test.close()
            success_data = {
                "id": from_queue,
            }
            paper_queue_success(success_data)





