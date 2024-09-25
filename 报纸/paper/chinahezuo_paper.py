import json
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree

paper = "中华合作时报"
headers = {
    'ADMIN_ALLOW': '',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'BROWER_LANGUAGE': 'zh-CN',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'UM_distinctid=191c64e7d978a6-06afa3fdf96918-26001e51-13c680-191c64e7d98b23; zycna=1bGSLyfTkEoBAXPBugKmKOTu; VISIT_TAG=1726293016824; JSESSIONID=07613399CB9AE6F99A4348B717334B41',
    'Origin': 'http://szb.zh-hz.com',
    'Pragma': 'no-cache',
    'Referer': 'http://szb.zh-hz.com/bz/html/index.html?cid=1',
    'SCREEN': '900x1440',
    'SITE': 'zghzsb',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # '_identity': '5f6ed905-26cd-48c2-b7b4-63aa3ede4484',
    '_identity': '5f6ed905-26cd-48c2-b7b4-63aa3ede4484',
}


def get_chinahezuo_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    base_url = f'http://epaper.chuxiong.cn/{paper_time}/'
    url = base_url + 'node_01.html'
    data_json = {"from": 0, "size": 100, "query": {
        "bool": {"must": [{"term": {"columns.id": 1}}, {"term": {"bz.date_date_sore": paper_time}}]}},
                 "sort": [{"index_int_sore": {"order": "asc"}}]}
    data_json = json.dumps(data_json)
    data = {
        'index': 'bz_page',
        'query': data_json,
    }
    response = requests.post('http://szb.zh-hz.com/data/query', headers=headers, data=data, verify=False)
    if response.status_code == 200:
        content = response.json()
        bm_list = content["hits"]["hits"]
        pdf_set = set()
        for bm in bm_list:
            bm_name = bm["_source"]["name_ngram_sore"]
            bm_url = f'http://szb.zh-hz.com/bz/html/index.html?date={paper_time}&pageIndex={bm["_source"]["index_int_sore"]}&cid=1'
            bm_pdf = bm["_source"]["pdf"]["url_no_analyzer_sore"]
            bm_id = bm["_id"]
            # 获取版面详情链接
            data_json = {"from": 0, "size": 15,
                         "query": {"bool": {"must": [{"term": {"bz_page.id_no_analyzer_sore": bm_id}}]}},
                         "sort": [{"index_int_sore": {"order": "asc"}}]}
            data_json = json.dumps(data_json)
            data = {
                'index': 'bz_article',
                'query': data_json,
            }
            bm_response = requests.post('http://szb.zh-hz.com/data/query', headers=headers, data=data, verify=False)
            if bm_response.status_code == 200:
                bm_content = bm_response.json()
                try:
                    article_list = bm_content["hits"]["hits"]
                except:
                    article_list = []
                for article in article_list:
                    article_id = article["_id"]
                    article_url = bm_url + f"&articleId={article_id}&articleIndex=1"
                    article_name = article["_source"]["title_ngram_sore"]
                    content = article["_source"]["text1_fielddata"]
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

    else:
        raise Exception(f'该日期没有报纸')


# get_chinahezuo_paper('2023-11-21', 111, 1111)
