import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "南充日报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'PHPSESSID=909956bcc233c1735f52e42040f0cda7',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}



def get_nanchong_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    base_url = f'http://xncrb.cnncw.cn/upload/ncrb/{paper_time}/{paper_time}-'
    url = base_url + 'A1.json'
    response = requests.get(url, headers=headers)
    time.sleep(1)
    if response.status_code == 200:
        content = response.json()

        # 获取所有版面的的链接
        all_bm = content["layoutlist"]
        for bm in all_bm:
            # 链接所需字段
            url_str = bm["pageno"]
            # 版面名称
            bm_name = bm["pagename"]
            # 版面链接
            bm_url = "http://xncrb.cnncw.cn" + bm["url"]

            bm_json_url = base_url + f"{url_str}.json"
            bm_html = requests.get(bm_json_url, headers=headers)
            time.sleep(1)
            bm_html = bm_html.json()
            # 获取所有文章的链接
            all_article = bm_html["infolist"]["list"]
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = "http://xncrb.cnncw.cn" + article["url"]
                # 获取文章名称
                article_name = article["title"]
                # 版面的pdf
                bm_pdf = "http://xncrb.cnncw.cn" + article["pdf"]
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_content = article["content"]
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//p/text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, article_url, bm_pdf, content)
                if bm_pdf not in pdf_set and judging_bm_criteria(article_name, bm_url, bm_url_in) and judge_bm_repeat(paper, bm_url):
                    try:
                        # 将报纸url上传
                        up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                    except:
                        up_pdf = ''
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


# get_nanchong_paper('2021-07-29', 111, 1111)
