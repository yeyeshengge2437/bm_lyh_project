import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "上海科技报"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'Hm_lvt_a1992d4f07ac862c4ac733402b6c202e=1728625766; paper_order_current_user_info=2|1:0|10:1728625807|29:paper_order_current_user_info|0:|563bf685b09c61f954a2c1b2a840ba4aebe503dc8bb9e1ed37829ad29e85115b',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}



def get_shanghaikeji_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    paper_time1 = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    base_url = f'https://www.shkjb.com/api/paper/issue/date/{paper_time}'
    url = base_url
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        issue = content["response"]["issue"]
        # 获取所有版面的的链接
        all_bm = ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']
        for bm in all_bm:
            # 版面链接
            bm_url = f'https://www.shkjb.com/api/paper/{paper_time1}/page/{bm}/article/list'
            bm_res = requests.get(bm_url, headers=headers)
            bm_json = bm_res.json()
            # 获取所有版面
            for bm_content in bm_json["response"]:
                # 版面名称
                bm_name = bm_content["title"]
                # 版面id
                bm_id = bm_content["zindex"]
                # 获取所有文章的链接
                article_url = f'https://www.shkjb.com/api/paper/media/content/{bm_id}/{issue}'
                article_res = requests.get(article_url, headers=headers)
                try:
                    article_json = article_res.json()
                except:
                    continue
                for article in article_json["response"]:
                    article_name = article["title"]
                    content_art = article["content"]
                    content_html = etree.HTML(content_art)
                    content = "".join(content_html.xpath("//text()")).strip()
                    bm_pdf = None
                    pdf_set = set()

                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')

                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col",
                    )
                    cursor_test = conn_test.cursor()
                    # print(bm_name, article_name, article_url, bm_pdf, content)
                    if judging_criteria(article_name, content):
                        # 将报纸url上传
                        up_pdf = None
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


# get_shanghaikeji_paper('2024-10-09', 111, 1111)
