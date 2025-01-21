
import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "中国企业报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_3bb60c17c72330abae82c999626cf10f=1724054770; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_b2d32dbc529d46f8e5e1180fd6c011af=1724054860; Hm_lpvt_b2d32dbc529d46f8e5e1180fd6c011af=1724054870; Hm_lpvt_3bb60c17c72330abae82c999626cf10f=1724054889',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

today = datetime.now().strftime('%Y-%m/%d')


def get_chinaqiye_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'http://epaper.zqcn.com.cn/content/{paper_time}/'
    url = base_url + 'node_2.htm'
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.content.decode()
        bm_html = etree.HTML(data)
        if bm_html is None:
            raise Exception(f'该日期没有报纸')
        bm_list = bm_html.xpath("//td[@class='mulu04']/table/tbody/tr")
        for bm in bm_list:
            # 获取版面名称
            bm_name = ''.join(bm.xpath("./td[@class='default2']/a[@id='pageLink']/text()"))
            # 获取版面链接
            bm_url = base_url + ''.join(bm.xpath("./td[@class='default2']/a[@id='pageLink']/@href")).strip('./')
            # 获取版面pdf
            bm_pdf = 'http://epaper.zqcn.com.cn/' + ''.join(bm.xpath("./td[2]/a/@href")).strip('../../../')
            # 获取版面下的内容
            bm_response = requests.get(bm_url, headers=headers, verify=False)
            time.sleep(2)
            bm_data = bm_response.content.decode()
            bm_html1 = etree.HTML(bm_data)
            if bm_html1 is None:
                continue
            bm_areaList = bm_html1.xpath("//ul[@class='list01']/li/a")
            for bm_area in bm_areaList:
                # 获取文章名称
                article_name = ''.join(bm_area.xpath("./div/text()"))
                # 获取文章链接
                article_url = base_url + ''.join(bm_area.xpath("./@href"))
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers, verify=False)
                time.sleep(2)
                try:
                    article_data = article_response.content.decode()
                except:
                    continue
                article_html = etree.HTML(article_data)
                content = ''.join(article_html.xpath("//div[@id='ozoom']/founder-content/p/text()"))
                pdf_set = set()
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
                # print(bm_name, article_name, article_url, content, bm_pdf)
                if bm_pdf not in pdf_set and (judging_bm_criteria(article_name)) and judge_bm_repeat(paper, bm_url):
                    # 将报纸img上传
                    up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if judging_criteria(article_name, content):
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
        raise Exception(f'该日期没有报纸')


# get_chinaqiye_paper("2016-05-17", 11,  11)
