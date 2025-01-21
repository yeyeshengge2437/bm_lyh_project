import json
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree

paper = "温州商报"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://szb.66wz.com',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'formdata': '1',
}


def get_wenzhoushang_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    data = {
        'digitalNewspaperMark': 'wzsb',
        'publishTime': paper_time,
    }
    response = requests.post(
         'http://szb.66wz.com/digitalNewspaper/web/layoutCatalog/listByDigitalNewspaperMarkAndPublishTime',
        headers=headers,
        data=data,
        verify=False,
    )
    if response.status_code == 200:
        content = response.json()
        bm_list = content["msg"]
        pdf_set = set()
        for bm in bm_list:
            if type(bm) is str:
                raise Exception(f'该日期没有报纸')
            bm_name = bm["editionName"]
            bm_url = f'http://szb.66wz.com/newspaper?mediaKey=wzsb&showArticleDetail=false&curEdition=01&publishTime={paper_time}'
            bm_pdf = 'http://szb.66wz.com/newspaperfile' + bm["pdfPath"]
            bm_id = bm["layoutCatalogId"]
            # 获取版面详情链接
            data = {
                'layoutCatalogId': str(bm_id),
            }
            bm_response = requests.post(
                'http://szb.66wz.com/digitalNewspaper/web/layoutDetail/listByLayoutCatalogId',
                headers=headers,
                data=data,
                verify=False,
            )
            if bm_response.status_code == 200:
                bm_content = bm_response.json()
                article_list = bm_content["msg"]
                for article in article_list:
                    article_id = article["layoutDetailId"]
                    article_url = f"http://szb.66wz.com/newspaper?mediaKey=wzsb&showArticleDetail=true&docId={article_id}&curEdition={article['edition']}&publishTime={paper_time}"
                    article_name = article["documentTitle"]
                    content = article["documentContent"]
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
                    # print(bm_name, article_name, article_url, bm_pdf, content)
                    if bm_pdf not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                        # 将报纸url上传
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
        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        raise Exception(f'该日期没有报纸')


# get_wenzhoushang_paper('2022-12-30', 111, 1111)
