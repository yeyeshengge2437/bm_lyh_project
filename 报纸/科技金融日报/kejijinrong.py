import os
import time
import re
import mysql.connector
import requests
from lxml import etree
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
    print(result.get("value"))
    fr.close()
    os.remove(pdf_path)
    return result.get("value")["file_url"]


# claims_keys = [
#     '债权通知书', '债权告知书', '债权通知公告', '债权登报公告', '债权补登公告', '债权补充公告', '债权拍卖公告', '债权公告', '债权通知',
#     '转让通知书', '转让告知书', '转让通知公告', '转让登报公告', '转让补登公告', '转让补充公告', '转让拍卖公告', '转让公告', '转让通知',
#     '受让通知书', '受让告知书', '受让通知公告', '受让登报公告', '受让补登公告', '受让补充公告', '受让拍卖公告', '受让公告', '受让通知',
#     '处置通知书', '处置告知书', '处置通知公告', '处置登报公告', '处置补登公告', '处置补充公告', '处置拍卖公告', '处置公告', '处置通知',
#     '招商通知书', '招商告知书', '招商通知公告', '招商登报公告', '招商补登公告', '招商补充公告', '招商拍卖公告', '招商公告', '招商通知',
#     '营销通知书', '营销告知书', '营销通知公告', '营销登报公告', '营销补登公告', '营销补充公告', '营销拍卖公告', '营销公告', '营销通知',
#     '信息通知书', '信息告知书', '信息通知公告', '信息登报公告', '信息补登公告', '信息补充公告', '信息拍卖公告', '信息公告', '信息通知',
#     '联合通知书', '联合告知书', '联合通知公告', '联合登报公告', '联合补登公告', '联合补充公告', '联合拍卖公告', '联合公告', '联合通知',
#     '催收通知书', '催收告知书', '催收通知公告', '催收登报公告', '催收补登公告', '催收补充公告', '催收拍卖公告', '催收公告', '催收通知',
#     '催讨通知书', '催讨告知书', '催讨通知公告', '催讨登报公告', '催讨补登公告', '催讨补充公告', '催讨拍卖公告', '催讨公告', '催讨通知'
# ]
claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                       r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)')
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}
value = paper_queue_next(webpage_url_list=['http://kjb.zjol.com.cn'])
from_queue = value['id']
webpage_id = value["webpage_id"]
try:
    # 获取当前年月
    year_month = datetime.now().strftime('%Y-%m')
    # 获取当前日期
    date = datetime.now().strftime('%d')
    base_pdf_url = "https://kjb.zjol.com.cn/"


    base_url = f'https://kjb.zjol.com.cn/'
    # 获取今日的链接
    res_url = requests.get('https://kjb.zjol.com.cn/', headers=headers)
    html_content = res_url.content.decode()
    url = re.findall(r'URL=(.*?)">', html_content)[0]
    url_data = re.findall(r'html/(.*?)/node_\d+\.htm', url)[0]
    actual_data = datetime.now().strftime('%Y-%m/%d')
    if url_data != actual_data:
        success_data = {
            'id': from_queue,
            'description': '今日没有报纸',
        }
        paper_queue_success(success_data)
    else:
        url = base_url + url
        base_url = re.sub(r'node_\d+\.htm', '', url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = etree.HTML(response.content.decode())
            # 获取当日报纸的所有版面
            all_bm = html.xpath("//div[@class='main-ednav-nav']/dl")
            for bm in all_bm:
                bm_link = ''.join(bm.xpath("./dt/a[@id='pageLink']/@href"))
                bm_name = ''.join(bm.xpath("./dt/a[@id='pageLink']/text()"))
                bm_pdf = ''.join(bm.xpath("./dd/img[2]/@filepath"))
                bm_pdf = bm_pdf.strip("../../..")
                # 获取版面下的所有文章连接
                bm_url = base_url + bm_link
                r = requests.get(bm_url, headers=headers)
                bm_html = etree.HTML(r.content.decode())
                title_urls = bm_html.xpath("//div[@class='main-ed-map']/map/area/@href")
                display_title_urls = bm_html.xpath("//ul[@class='main-ed-articlenav-list']/li/a")
                have_key = False
                if len(title_urls) > len(display_title_urls) * 2:
                    have_key = True
                    print(f"显示的标题数量为{len(display_title_urls)}，实际标题数量为{len(title_urls)}，存在隐藏标题")
                # 连接数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col"
                )
                cursor_test = conn_test.cursor()
                day = datetime.now().strftime('%Y-%m-%d')
                paper = "科技金融日报"
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                for title in title_urls:
                    title_url = base_url + title
                    # 获取文章内容
                    res = requests.get(title_url, headers=headers)

                    title_html = etree.HTML(res.content.decode())
                    # 获取文章标题
                    title_name = "".join(title_html.xpath("//div[@class='main-article-alltitle']//text()")).strip()
                    # 获取文章内容
                    content = "".join(title_html.xpath(
                        "//div[@class='main-article-content']/div[@id='ozoom']/founder-content/p//text()")).strip()
                    # 获取文章标题含内容
                    title_content = title_name + "\n" + content

                    # 判断是否包含关键词
                    if claims_keys.match(title_name):
                        have_key = True
                        # 上传到数据库
                        # 将数据插入到表中
                        # 上传到数据库
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (bm_url, day, paper, title_name, content, title_url, create_time,from_queue, create_date, webpage_id))

                        conn_test.commit()

                if have_key:
                    # 获取pdf_url
                    original_pdf = base_pdf_url + bm_pdf
                    pdf_url = upload_pdf_by_url(original_pdf, "1")
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time,from_queue, create_date, webpage_id) VALUES (%s,%s, %s,%s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, original_pdf, bm_url, pdf_url, create_time,from_queue,
                                         create_date, webpage_id))
                    conn_test.commit()
                    print("pdf已经上传")

                cursor_test.close()
                conn_test.close()

            success_data = {
                'id': from_queue,
                'description': '成功',
            }
            paper_queue_success(success_data)
        else:
            print("网页问题")
            success_data = {
                'id': from_queue,
                'description': "该天没有报纸",
            }
            paper_queue_success(success_data)
except Exception as e:
    print(f"错误原因: {e}")
    fail_data = {
        'id': from_queue,
        'description': f"错误原因: {e}",
    }

    paper_queue_fail(fail_data)