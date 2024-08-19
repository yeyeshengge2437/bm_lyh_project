import os
import json
import re
import time
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
co.set_paths(local_port=9117)

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




claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                         r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)$')
paper = "中国经济时报"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}



today = datetime.now().strftime('%Y-%m-%d')
# today = '2019-10-25'
# queue_id = 1111
# webpage_id = 1111

def get_chinajingji_paper(paper_time):
    params = {
        'date': paper_time,
        'btn_sch_date': '搜索',
    }
    # 将today的格式进行改变
    day = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    base_url = f'https://jjsb.cet.com.cn/'
    url = 'https://jjsb.cet.com.cn/DigitaNewspaper.aspx'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//td[2]/div/a")
        print(len(all_bm))
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./text()"))
            bm_name = re.sub(r'[ \t\r\n\f\v]+', '', bm_name)
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_pdf = base_url + "".join(bm_html.xpath("//td[3]/div/a/@href"))[1:]
            # 获取所有文章的链接
            all_article = bm_html.xpath("//div/ul/li/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
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
                if bm_pdf not in pdf_set and ("公告" in article_name or claims_keys.match(article_name)):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, "这是报纸", "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if claims_keys.match(article_name):
                    # 获取文章内容
                    page.get(article_url)
                    time.sleep(1)
                    article_content = page.html
                    article_html = etree.HTML(article_content)
                    # 获取文章内容
                    content = ''.join(article_html.xpath("//span[@id='Labelcontent']//text()"))

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()


                cursor_test.close()
                conn_test.close()
        page.close()

        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        # 获取当前时间小时分钟
        now = datetime.now().strftime('%m-%d %H:%M')
        raise Exception(f'{now}暂未获取到今日报纸{response.status_code}')




# 设置最大重试次数
max_retries = 5
retries = 0
while retries < max_retries:
    value = paper_queue_next(webpage_url_list=['https://jjsb.cet.com.cn'])
    queue_id = value['id']
    webpage_id = value["webpage_id"]
    try:
        get_chinajingji_paper(today)
        break
    except Exception as e:
        retries += 1
        if retries == max_retries and "暂未获取到今日报纸" in str(e):
            success_data = {
                'id': queue_id,
                'description': '今日没有报纸',
            }
            paper_queue_success(success_data)
            break
        else:
            fail_data = {
                "id": queue_id,
                "description": f"问题:{e}",
            }
            paper_queue_fail(fail_data)
            print("等待一小时后重试...")
            time.sleep(3610)  # 等待1小时后重试
page.close()
