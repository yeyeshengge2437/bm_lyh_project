import os
import time
import re
import mysql.connector
from lxml import etree
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url
import requests

def get_date_num(paper_time):
    year = paper_time.split('-')[0]
    month = paper_time.split('-')[1]
    day_num = paper_time.split('-')[2]

    headers = {
        'accept': 'application/xml, text/xml, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    url = f'https://kjb.zjol.com.cn/html/{year}-{month}/paper_existed.xml'
    response = requests.get(url, headers=headers)
    data = response.content.decode()
    date_a = {}
    # 匹配日期
    date_match = re.findall(r'<period_date>(\b\d{4}-\d{2}-\d{2}\b)</period_date>.*?<front_page>(.*?)</front_page>', data, re.S)
    for date in date_match:
        date_a[date[0]] = date[1]
    if date_a.get(paper_time):
        return date_a[paper_time]
    else:
        return False

claims_keys = re.compile(r'.*(?:债权|转让|受让|处置|招商|营销|信息|联合|催收|催讨).*'
                       r'(?:通知书|告知书|通知公告|登报公告|补登公告|补充公告|拍卖公告|公告|通知)')
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

paper = "科技金融时报"
def get_kejijinrong_paper(paper_time, queue_id, webpage_id):
    node_key = get_date_num(paper_time)
    if not node_key:
        raise Exception(f'该日期没有报纸')
    # 获取当前年月
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_pdf_url = "https://kjb.zjol.com.cn/"
    base_url = f'https://kjb.zjol.com.cn/html/{paper_time}/'
    url = base_url + f'{node_key}'
    response = requests.get(url, headers=headers)
    time.sleep(2)
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
            time.sleep(2)
            bm_html = etree.HTML(r.content.decode())
            title_urls = bm_html.xpath("//div[@class='main-ed-map']/map/area/@href")
            display_title_urls = bm_html.xpath("//ul[@class='main-ed-articlenav-list']/li/a")
            have_key = False
            if len(title_urls) > len(display_title_urls) * 2:
                have_key = True
            # 连接数据库
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col"
            )
            cursor_test = conn_test.cursor()

            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            create_date = datetime.now().strftime('%Y-%m-%d')
            for title in title_urls:
                title_url = base_url + title
                # 获取文章内容
                res = requests.get(title_url, headers=headers)
                time.sleep(2)

                title_html = etree.HTML(res.content.decode())
                # 获取文章标题
                title_name = "".join(title_html.xpath("//div[@class='main-article-alltitle']//text()")).strip()
                # 获取文章内容
                content = "".join(title_html.xpath(
                    "//div[@class='main-article-content']/div[@id='ozoom']/founder-content/p//text()")).strip()
                # 获取文章标题含内容
                title_content = title_name + "\n" + content

                # 判断是否包含关键词
                if judging_criteria(title_name, article_content=content):
                    have_key = True
                    # 上传到数据库
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, title_name, content, title_url, create_time,queue_id, create_date, webpage_id))

                    conn_test.commit()

            if have_key:
                # 获取pdf_url
                original_pdf = base_pdf_url + bm_pdf
                pdf_url = upload_file_by_url(original_pdf, "这是报纸", 'pdf')
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time,from_queue, create_date, webpage_id) VALUES (%s,%s, %s,%s,%s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (day, paper, bm_name, original_pdf, bm_url, pdf_url, create_time,queue_id,
                                     create_date, webpage_id))
                conn_test.commit()


            cursor_test.close()
            conn_test.close()

        success_data = {
            'id': queue_id,
            'description': '成功',
        }
        paper_queue_success(success_data)
    else:
        raise Exception(f'程序出错')


# queue_id = 111
# webpage_id = 1111
# time1 = '2024-04-16'
# print(get_kejijinrong_paper(time1, queue_id, webpage_id))

