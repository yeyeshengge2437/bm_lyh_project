import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "那曲报"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'x-appid-header': '100058',
}


def get_naqu_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    params = {
        'paperTime': f'{paper_time}',
        'mode': '0',
        'typeId': '7',
        'pageSort': '0',
    }
    base_url = 'http://nq.electron.allmc.cn/api-electorn-paper/newspaper/getType'
    url = base_url
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        content = response.json()
        try:
            html_1 = content["datas"]["newspaperPageList"]
        except Exception as e:
            raise Exception(f'该日期没有报纸')
        # 获取所有版面的的链接
        all_bm = html_1
        for bm in all_bm:
            # 版面名称
            bm_name = bm['name']
            # 版面链接
            bm_url = f'http://nq.electron.allmc.cn/pc/index?paperTime={paper_time}&mode=0&typeId=7&pageSort={bm_name}'
            # 版面的pdf
            bm_pdf = None
            up_pdf = None
            # 获取所有文章的链接
            all_article = bm["pageDraftList"]
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = f'{bm_url}#aid={article["uuid"]}'
                # 获取文章名称
                article_name = article['title']
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                content = article["content"]
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, article_url, bm_pdf, content)

                if judging_criteria(article_name, content):

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
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


# get_naqu_paper('2024-10-05', 111, 1111)
