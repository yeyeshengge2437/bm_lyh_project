import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "新快报"
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Secure; think_lang=zh-cn; PHPSESSID=8f80f6de66823acb77e098813f9070dc; Qs_lvt_486572=1727231690%2C1728625964; Hm_lvt_1924177ad2e7e7298da96b4846fdf1d4=1727231691,1728625964; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_1924177ad2e7e7298da96b4846fdf1d4=1728626007; Qs_pv_486572=2635623288601626000%2C4030265734514032000%2C3890659615771407400%2C2012405519001911300%2C6374961972425731; Secure',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



def get_xinkuai_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    base_url = f'https://epaper.xkb.com.cn/getPlate/date/{paper_time}'
    url = base_url
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        # 获取所有版面的的链接
        all_bm = content['data']
        for bm in all_bm:
            # 版面名称
            bm_name = bm['version']
            # 版面链接
            bm_url = base_url + f"&edition={bm['edition']}"
            # 版面的pdf
            bm_pdf = None
            up_pdf = None
            # 获取所有文章的链接
            all_article = bm["coodrs"]
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = f"https://epaper.xkb.com.cn/view/{article['id']}"

                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.text
                article_content = article_content.replace('\\', '')
                article_html = etree.HTML(article_content)
                if article_html is None:
                    continue
                # 获取文章名称
                article_name = ''.join(article_html.xpath("//span[@class='fs14 blod']/text()")).strip()
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='news_content']/p/text()")).strip()
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


# get_xinkuai_paper('2017-01-12', 111, 1111)
