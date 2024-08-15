import hashlib
import os
import json
import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co = co.set_paths(local_port=9115)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错

page = ChromiumPage(co)

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


def upload_file_by_url(file_url, file_name, file_type, type="paper"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(file_url, headers=headers)
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


def get_md5_set(database, table_name):
    hash_value_set = set()
    con_test = mysql.connector.connect(
        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database=database
    )
    cursor = con_test.cursor()
    # 获取表中的MD5值
    cursor.execute(f"SELECT md5 FROM {table_name}")
    for row in cursor:
        hash_value_set.add(row[0])
    return hash_value_set


md5_set = get_md5_set("col", "col_paper_notice")
claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                         r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')
paper = "河南商报"

pdf_domain = 'http://news.cenews.com.cn/html'
today = datetime.now().strftime('%Y-%m/%d')


def paper_claims(database):
    url = f'http://www.hnshangbao.com/sbn/'
    page.get(url)
    time.sleep(1)
    if page.url_available:
        html_1 = etree.HTML(page.html)
        # 获取末版链接
        bm_last = ''.join(html_1.xpath("//div[@class='box-bd']/div[@class='page']/a[9]/@href"))
        # 正则匹配页面数
        page_num = re.findall(r'(\d+)', bm_last)[0]
        for i in range(int(page_num)):
            if i == 0:
                bm_url = 'http://www.hnshangbao.com/sbn/'
            else:
                bm_url = f'http://www.hnshangbao.com/sbn/page_{i + 1}.html'
            page.get(bm_url)
            time.sleep(1)
            if page.url_available:
                html_2 = etree.HTML(page.html)
                # 获取该页所有标题
                all_title = html_2.xpath("//div[@class='box-bd']/ul[@class='list']/li")
                for title in all_title:
                    # 标题名称
                    article_name = ''.join(title.xpath("./a/text()"))
                    # 标题链接
                    article_url = ''.join(title.xpath("./a/@href"))
                    # 发布时间
                    day = ''.join(title.xpath("./span[@class='datatime']/text()"))
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # 进行数据的去重
                    data_unique = f"文章标题：{article_name}, 发布时间：{day}"
                    # 数据去重
                    hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database=database,
                    )
                    cursor_test = conn_test.cursor()
                    if claims_keys.match(article_name) and hash_value not in md5_set:
                        md5_set.add(hash_value)
                        # 获取文章内容
                        page.get(article_url)
                        time.sleep(1)
                        article_html = etree.HTML(page.html)
                        # 获取文章内容
                        content = ''.join(article_html.xpath("//div[@class='details']//text()"))
                        # 获取时间
                        # day = ''.join(article_html.xpath("//div[@class='details']/p[1]/text()"))

                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id, md5) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (bm_url, day, paper, article_name, content, article_url, create_time,
                                             queue_id,
                                             create_date, webpage_id, hash_value))
                        conn_test.commit()

                    cursor_test.close()
                    conn_test.close()

        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        # 获取当前时间小时分钟
        now = datetime.now().strftime('%m-%d %H:%M')
        raise Exception(f'{now}程序出错，{page.url_available}')


if __name__ == '__main__':
    try:
        # 设置最大重试次数
        max_retries = 5
        retries = 0
        while retries < max_retries:
            value = paper_queue_next(webpage_url_list=['http://www.hnshangbao.com'])
            queue_id = value['id']
            webpage_id = value["webpage_id"]
            try:
                paper_claims("col")
                break
            except Exception as e:
                retries += 1
                fail_data = {
                    "id": queue_id,
                    "description": f"程序问题:{e}",
                }
                paper_queue_fail(fail_data)
                print(f"第{retries}次重试, 一小时后重试")
                time.sleep(3610)  # 等待1小时后重试
        page.close()
    except Exception as e:
        page.close()
