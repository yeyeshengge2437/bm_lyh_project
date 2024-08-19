import os
import json
import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree

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
paper = "辽沈晚报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_77002c6b9fe15a5136bbe06f933886b8=1724036433; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_77002c6b9fe15a5136bbe06f933886b8=1724036814',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

today = datetime.now().strftime('%Y%m/%d')


# today = '202401/11'


def get_liaoshen_lastpaper(paper_time):
    # 将today的格式进行改变
    day = datetime.strptime(paper_time, '%Y%m/%d').strftime('%Y-%m-%d')
    base_url = f'https://epaper.lnd.com.cn/lswbepaper/pc/layout/{paper_time}/'
    url = base_url + 'node_A01.html'
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.content.decode()
        bm_html = etree.HTML(data)
        bm_list = bm_html.xpath("//div[@class='Chunkiconbox']/div[@class='Chunkiconlist']/p")
        for bm in bm_list:
            # 获取版面名称
            bm_name = ''.join(bm.xpath("./a[1]/text()"))
            # 获取版面链接
            bm_url = base_url + ''.join(bm.xpath("./a[1]/@href"))
            # 获取版面图片
            bm_pdf = 'https://epaper.lnd.com.cn/lswbepaper/pc/' + ''.join(bm.xpath("./a[2]/@href")).strip("../../..")
            # 获取版面下的内容
            bm_response = requests.get(bm_url, headers=headers, verify=False)
            bm_data = bm_response.content.decode()
            bm_html1 = etree.HTML(bm_data)
            bm_areaList = bm_html1.xpath("//div[@id='ScroLeft']/div[@class='newslist']/ul/li")
            for bm_area in bm_areaList:
                # 获取文章名称
                article_name = ''.join(bm_area.xpath("./h3/a/text()"))
                # 获取文章链接
                article_url = 'https://epaper.lnd.com.cn/lswbepaper/pc/' + ''.join(bm_area.xpath("./h3/a/@href")).strip(
                    "../../..")
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers, verify=False)
                article_data = article_response.content.decode()
                article_html = etree.HTML(article_data)
                content = ''.join(article_html.xpath("//div[@class='newsdetatext']/founder-content/p//text()"))
                pdf_set = set()

                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')

                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                if bm_pdf not in pdf_set and ("公告" in article_name or claims_keys.match(article_name)):
                    # 将报纸img上传
                    up_pdf = upload_file_by_url(bm_pdf, "这是报纸", "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if claims_keys.match(article_name):
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
        # 获取当前时间小时分钟
        now = datetime.now().strftime('%m-%d %H:%M')
        raise Exception(f'{now}目前未有报纸，{response.status_code}')


# 设置最大重试次数
max_retries = 5
retries = 0
while retries < max_retries:
    value = paper_queue_next(webpage_url_list=['https://epaper.lnd.com.cn'])
    queue_id = value['id']
    webpage_id = value["webpage_id"]
    try:
        get_liaoshen_lastpaper(today)
        break
    except Exception as e:
        retries += 1
        if retries == max_retries and "目前未有报纸" in e:
            success_data = {
                'id': queue_id,
                'description': '今天没有报纸',
            }
            paper_queue_success(success_data)
            break
        else:
            fail_data = {
                "id": queue_id,
                "description": f"出现问题:{e}",
            }
            paper_queue_fail(fail_data)
            print(f'{e},等待一小时后重试...')
            time.sleep(3610)  # 等待1小时后重试
