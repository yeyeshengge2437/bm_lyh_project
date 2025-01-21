import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree

paper = "中国房地产报"

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'PHPSESSID=ep8hogskiaqug0s5ffmkbdr4ou; Hm_lvt_67efac7eaac6d157b1e34ceb0dfc729b=1725609865,1725848690; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_67efac7eaac6d157b1e34ceb0dfc729b=1725849388',
    'Origin': 'https://flbook.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://flbook.com.cn/c/qfpXLBCarV',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def judge_date(paper_time):

    data = {
        'w': 'out',
        'h': 'bookshelf',
        'l': 'no',
        'type': 'init',
        'ascription': '665417',
        'booktype': '0',
    }

    response = requests.post('https://flbook.com.cn/api/', headers=headers, data=data)
    res_json = response.json()
    dates_books = res_json["data"]["books"]
    for date_book in dates_books:
        bz_date = date_book["updated"]
        if paper_time == bz_date:
            bz_param = bz_date.replace("-", "/")[:-3]
            bz_id = date_book["id"]
            bz_url = f'https://flbook.com.cn/upload/pages/{bz_param}/{bz_id}.html'
            return bz_url
        else:
            return False

def get_chinafangdichan_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    day = paper_time
    if judge_date(paper_time):
        bz_url = judge_date(paper_time)
        res_html = requests.get(bz_url, headers=headers)
        html = etree.HTML(res_html.text)
        # 获取所有的版面
        # bm_page = html.xpath("//div[@class='page']//@data-link")
        bm_page = html.xpath("//div[@class='page']")
        img_set = set()
        for page in bm_page:
            bm_img = ''.join(page.xpath(".//@data-bg"))
            # 使用re去除?后面的内容
            bm_img = re.sub(r'\?.*', '', bm_img)
            bm_img = "https:" + bm_img
            for title in page.xpath(".//@data-link"):
                article_url = title
                res_title = requests.get(title, headers=headers)
                title_html = etree.HTML(res_title.text)
                # 获取版面标题
                article_name = ''.join(title_html.xpath("//div[@class='piccontext']/h2/text()")).strip()
                if not article_name:
                    article_name = ''.join(title_html.xpath("//div[@class='left-item left-one pd20']/h5/text()")).strip()
                # 获取版面内容
                content = ''.join(title_html.xpath("//div[@class='picshow']//text()")).strip()
                if not content:
                    content = ''.join(title_html.xpath("//div[@class='content-para']//p//text()")).strip()

                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(article_name, bm_img, content)
                if bm_img not in img_set and judging_bm_criteria(article_name):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_img, paper, "img", "paper")
                    img_set.add(bm_img)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper,  original_img,  img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_img,  up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if judging_criteria(article_name, content):

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice ( day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                cursor_test.close()
                conn_test.close()
    else:
        raise Exception(f'该日期没有报纸')


# get_chinafangdichan_paper("2024-09-08", 111, 111)