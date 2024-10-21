import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "中国民族报"
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://210.12.104.26:81',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}



def get_chinaminzu_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    data = {
        'docPubTime': f'{paper_time}',
    }
    response = requests.post('http://210.12.104.26:81/reader/layout/findBmMenuPub.do', headers=headers, data=data, verify=False)
    if response.status_code == 200:
        try:
            content = response.json()
        except:
            raise Exception(f'该日期没有报纸')
        # 获取所有版面的的链接
        all_bm = content
        for bm in all_bm:
            # 版面名称
            bm_name = bm['BC']
            # 版面链接
            bm_url = 'http://210.12.104.26:81/epaper/' + bm['PDPATH']
            # 版面的pdf
            bm_pdf = 'http://210.12.104.26:81/epaper/' + bm['PDPATH']

            # 获取所有文章的链接
            bm_str = bm['IRCATELOG']
            params = {
                'bc': f'{bm_str}',
                'docpubtime': f'{paper_time}',
            }

            response = requests.get('http://210.12.104.26:81/reader/layout/getBmDetailPub.do', params=params,
                                    headers=headers, verify=False)
            all_article = response.json()

            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = f'http://210.12.104.26:81/epaper/?id={article["ZB_GUID"]}&time={paper_time}'
                # 获取文章名称
                try:
                    article_name = ''.join(article['DOCTITLE'])
                except:
                    continue
                # 去除英文和特殊字符
                article_name = re.sub(r'[^\u4e00-\u9fa5]', '', article_name)
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                try:
                    content = article['IR_ABSTRACT']
                except:
                    content = ''
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
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
                # if 1:

                    # print(content)
                    # return

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


# get_chinaminzu_paper('2021-08-03', 111, 1111)
