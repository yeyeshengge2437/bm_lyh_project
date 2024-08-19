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
co.set_paths(local_port=9116)

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
paper = "洛阳日报"

pdf_domain = 'https://lyrb.lyd.com.cn/'
today = datetime.now().strftime('%Y-%m/%d')


# today = '2014-12/01'


def date_conversion(date):
    # 日期格式正则表达式
    date = str(date)
    date_pattern = re.compile(r'^\d{4}-\d{2}/\d{2}$')
    if date_pattern.match(date):
        return date
    else:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date = date_obj.strftime('%Y-%m/%d')
        return date


def get_luoyang_paper(paper_time):
    """
    获取洛阳日报的数据
    洛阳日报以2014年为节点，14年前后版本发生变化
    日期格式为：XXXX-XX/XX
    :param paper_time:
    :return:
    """
    paper_time = date_conversion(paper_time)

    # 将today的格式进行改变
    day = datetime.strptime(paper_time, '%Y-%m/%d').strftime('%Y-%m-%d')

    # 如果paper_time的日期在2014年12月1号之前的
    # 将字符串转换为datetime对象
    paper_time1 = datetime.strptime(paper_time, '%Y-%m/%d')
    # 定义2014年12月1号的datetime对象
    cutoff_date = datetime.strptime('2014-12/01', '%Y-%m/%d')
    pdf_set = set()

    if paper_time1 > cutoff_date:
        base_url = f'https://lyrb.lyd.com.cn/html2/{paper_time}/'
        url = base_url + 'node_3.htm'
        page.get(url)
        html_1 = etree.HTML(page.html)
        # 获取所有版面的的链接
        all_bm = html_1.xpath(
            "//tbody/tr[1]/td[1]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./td[@class='default']/a[@id='pageLink']/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./td[@class='default']/a[@id='pageLink']/@href"))
            # 版面的pdf
            bm_pdf = pdf_domain + "".join(bm.xpath("./td[2]/a/@href")).strip('../../..')
            # 获取版面详情
            page.get(bm_url)
            time.sleep(1)
            bm_content = page.html
            bm_html = etree.HTML(bm_content)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//ul[@class='main-ed-articlenav-list']/li/a")
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
                    content = ''.join(article_html.xpath("//div[@id='ozoom']/founder-content//text()"))

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time,
                                         queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                cursor_test.close()
                conn_test.close()
        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)
        page.close()
    else:
        base_url = f'https://lyrb.lyd.com.cn/html/{paper_time}/'

        url = base_url + 'node_4105.htm'
        page.get(url)
        html_1 = etree.HTML(page.html)
        # 获取所有版面的的链接
        all_bm = html_1.xpath(
            "//table[2]/tbody/tr/td[1]/table[3]/tbody/tr")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./td[@class='default'][1]/a[@id='pageLink']/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./td[@class='default'][1]/a[@id='pageLink']/@href"))
            # 版面的pdf
            bm_pdf = pdf_domain + "".join(bm.xpath("./td[@class='default'][2]/a/@href")).strip('../../..')
            # 获取版面详情
            page.get(bm_url)
            time.sleep(1)
            bm_content = page.html
            bm_html = etree.HTML(bm_content)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//tbody/tr[1]/td/table[3]/tbody/tr/td/table/tbody/tr/td[@class='default']/a")

            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath(".//text()")).strip()
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
                    content = ''.join(article_html.xpath("//tbody/tr/td/div[@id='ozoom']//text()"))

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
        page.close()


# 设置最大重试次数
max_retries = 5
retries = 0
while retries < max_retries:
    value = paper_queue_next(webpage_url_list=['https://epaper.tianjinwe.com/mrxb'])
    queue_id = value['id']
    webpage_id = value["webpage_id"]
    try:
        get_luoyang_paper(today)
        break
    except Exception as e:
        retries += 1
        if retries == max_retries:
            success_data = {
                'id': queue_id,
                'description': '今天没有报纸',
            }
            paper_queue_success(success_data)
            page.close()
            break
        else:
            fail_data = {
                "id": queue_id,
                "description": f"出现问题:{e}",
            }
            paper_queue_fail(fail_data)
            print(f"{e},一小时后重试...")
            time.sleep(3610)  # 等待1小时后重试
