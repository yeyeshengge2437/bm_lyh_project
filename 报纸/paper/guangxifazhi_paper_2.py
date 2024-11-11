
import json
import time
from multiprocessing import Process
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    parse_pdf, judge_bm_repeat, judging_bm_criteria, paper_queue_next
from datetime import datetime
import mysql.connector
import requests


paper = "广西法治日报"
# co = ChromiumOptions()
# co = co.set_argument('--no-sandbox')
# co = co.headless()
# co.set_paths(local_port=9156)

headers = {
    'ADMIN_ALLOW': '',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'BROWER_LANGUAGE': 'zh-CN',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'Hm_lvt_9b2a01de93671e1d3edfbffeda9b89f9=1724146656; VISIT_TAG=1726623174026; JSESSIONID=AF604898867BC95AFD5439EFDD2C7057',
    'Origin': 'http://ipaper.pagx.cn',
    'Pragma': 'no-cache',
    'SCREEN': '900x1440',
    'SITE': 'gxfzb',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # 'myIdentity': 'eae02af2-0e49-4ed2-be21-a6ca25369a9f',
    'myIdentity': '9195459e-c0be-47fd-8c0f-552e11cba122',
}


def get_guangxifazhi_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    data_json = {"from":0,"size":999,"query":{"bool":{"must":[{"term":{"columns.id":1}},{"term":{"bz.date_date_sore":paper_time}}]}},"sort":[{"index_int_sore":{"order":"asc"}}]}
    data_json = json.dumps(data_json)
    data = {
        'index': 'bz_page',
        'query': data_json,
    }
    response = requests.post('http://ipaper.pagx.cn/data/query', headers=headers, data=data, verify=False)
    if response.status_code == 200:
        content = response.json()
        bm_list = content["hits"]["hits"]
        pdf_set = set()
        for bm in bm_list:
            bm_name = bm["_source"]["name_ngram_sore"]
            # bm_url = f'http://szb.zh-hz.com/bz/html/index.html?date={paper_time}&pageIndex={bm["_source"]["index_int_sore"]}&cid=1'
            bm_url = f'http://ipaper.pagx.cn/bz/html/index.html?date={paper_time}&pageIndex={bm["_source"]["index_int_sore"]}&cid=1'
            bm_pdf = bm["_source"]["pdf"]["url_no_analyzer_sore"]
            bm_id = bm["_id"]
            # 获取版面详情链接
            data_json = {"from":0,"size":15,"query":{"bool":{"must":[{"term":{"bz_page.id_no_analyzer_sore":bm_id}}]}},"sort":[{"index_int_sore":{"order":"asc"}}]}
            data_json = json.dumps(data_json)
            data = {
                'index': 'bz_article',
                'query': data_json,
            }
            bm_response = requests.post('http://ipaper.pagx.cn/data/query',  headers=headers, data=data, verify=False)

            if bm_response.status_code == 200:
                bm_content = bm_response.json()
                article_list = bm_content["hits"]["hits"]
                for article in article_list:
                    article_id = article["_id"]
                    article_url = f'http://ipaper.pagx.cn/bz/html/content.html?date={paper_time}&pageIndex={bm["_source"]["index_int_sore"]}&cid=1' + f"&articleId={article_id}&articleIndex=1"
                    article_name = article["_source"]["title_ngram_sore"]
                    content = article["_source"]["text1_fielddata"]
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
                    if bm_pdf not in pdf_set and judge_bm_repeat(paper, bm_url):
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



get_guangxifazhi_paper('2022-08-19', 111, 1111)

# methods = {
#     '广西法治日报': get_guangxifazhi_paper,
# }
#
#
# def get_paper_data():
#     while True:
#         try:
#             # 调用paper_queue_next函数并获取返回值
#             paper_queue = paper_queue_next(
#                 webpage_url_list=['https://ipaper.pagx.cn'])
#             # 检查返回值是否符合预期
#             if paper_queue is None or len(paper_queue) == 0:
#                 time.sleep(30)
#                 pass
#             else:
#                 webpage_name = paper_queue['webpage_name']
#                 queue_day = paper_queue['day']
#                 queue_id = paper_queue['id']
#                 webpage_id = paper_queue["webpage_id"]
#                 print(queue_day)
#                 try:
#                     methods[webpage_name](queue_day, queue_id, webpage_id)
#                 except Exception as e:
#                     if '该日期没有报纸' in str(e):
#                         print('该日期没有报纸')
#                         data = {
#                             "id": queue_id,
#                             'description': f'该日期没有报纸',
#                         }
#                         paper_queue_delay(data)
#                     else:
#                         print(f"{e}")
#                         fail_data = {
#                             "id": queue_id,
#                             'description': f'程序异常：{e}',
#                         }
#                         paper_queue_fail(fail_data)
#
#         except Exception as e:
#             time.sleep(360)
#             print(f"解析过程中发生错误: {e}")
#
#
# if __name__ == '__main__':
#     """
#     多进程5个
#     """
#     process_list = []
#     for i in range(5):
#         process = Process(target=get_paper_data, args=())
#         process_list.append(process)
#
#     for process in process_list:
#         process.start()
#
#     for process in process_list:
#         process.join()
