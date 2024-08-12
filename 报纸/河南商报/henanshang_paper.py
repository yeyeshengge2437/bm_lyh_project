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
co = co.set_paths(local_port=9113)
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


value = paper_queue_next(webpage_url_list=['http://www.hnshangbao.com'])
queue_id = value['id']
webpage_id = value["webpage_id"]

# success_data = {
#         'id': queue_id,
#         'description': '成功',
#     }
# paper_queue_success(success_data)
#
# fail_data = {
#         "id": queue_id,
#         "description": "程序问题",
#     }
# paper_queue_fail(fail_data)

claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                         r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')
paper = "河南商报"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    # 'Cookie': '_D_SID=F24136CE5C75C18DEC65BB8604657EF8; ASPSESSIONIDCQASTBCR=FIFNLPLAOHIKEGAMHBCKHGAI; Hm_lvt_9bdfc3c6e0ff45e87458a4ae354c3134=1723443187; HMACCOUNT=FDD970C8B3C27398; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219145380fa6581-0d28aa3ec9d9a7-26001e51-1296000-19145380fa7974%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxNDUzODBmYTY1ODEtMGQyOGFhM2VjOWQ5YTctMjYwMDFlNTEtMTI5NjAwMC0xOTE0NTM4MGZhNzk3NCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219145380fa6581-0d28aa3ec9d9a7-26001e51-1296000-19145380fa7974%22%7D; __bid_n=19145380fd57456ccc7292; Hm_lpvt_9bdfc3c6e0ff45e87458a4ae354c3134=1723443596',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

pdf_domain = 'http://news.cenews.com.cn/html'
today = datetime.now().strftime('%Y-%m/%d')


def paper_claims():
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
                all_title = html_2.xpath("//div[@class='box-bd']/ul[@class='list']/li/a")
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
                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col_test",
                    )
                    cursor_test = conn_test.cursor()
                    if claims_keys.match(article_name):
                        # 获取文章内容
                        page.get(article_url)
                        time.sleep(1)
                        article_html = etree.HTML(page.html)
                        # 获取文章内容
                        content = ''.join(article_html.xpath("//div[@class='details']//text()"))
                        # 获取时间
                        # day = ''.join(article_html.xpath("//div[@class='details']/p[1]/text()"))

                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()

                    cursor_test.close()
                    conn_test.close()

        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        fail_data = {
            "id": queue_id,
            "description": f"页面状态:{page.url_available}",
        }
        paper_queue_fail(fail_data)


paper_claims()

# # 设置最大重试次数
# max_retries = 5
# retries = 0
# while retries < max_retries:
#     try:
#         paper_claims(today)
#         break
#     except Exception as e:
#         retries += 1
#         fail_data = {
#             "id": queue_id,
#             "description": f"程序问题:{e}",
#         }
#         paper_queue_fail(fail_data)
#         time.sleep(3610)  # 等待1小时后重试
