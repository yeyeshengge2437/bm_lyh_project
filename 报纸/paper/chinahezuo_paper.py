import json
import time
from datetime import datetime
from DrissionPage import ChromiumPage, ChromiumOptions
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree
co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9116)

page = ChromiumPage()
page.get('http://szb.zh-hz.com/bz/html/index.html?date=2019-12-27&pageIndex=1&cid=1')
page.set.load_mode.none()
print(page.html)

paper = "中华合作时报"
headers = {
    'ADMIN_ALLOW': '',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'BROWER_LANGUAGE': 'zh-CN',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'UM_distinctid=191c64e7d978a6-06afa3fdf96918-26001e51-13c680-191c64e7d98b23; VISIT_TAG=1725863572920; JSESSIONID=CAB8DE96CC67FFE4EF27084A5A6ED927',
    'Origin': 'http://szb.zh-hz.com',
    'Pragma': 'no-cache',
    'Referer': 'http://szb.zh-hz.com/bz/html/index.html?date=2024-08-13&pageIndex=2&cid=1',
    'SCREEN': '900x1440',
    'SITE': 'zghzsb',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    '_identity': '5f6ed905-26cd-48c2-b7b4-63aa3ede4484',
}

data = {
    'index': 'bz_page',
    'query': '{"from":0,"size":100,"query":{"bool":{"must":[{"term":{"columns.id":1}},{"term":{"bz.date_date_sore":"2024-08-13"}}]}},"sort":[{"index_int_sore":{"order":"asc"}}]}',
}

response = requests.post('http://szb.zh-hz.com/data/query', headers=headers, data=data, verify=False)

res_data = response.json()
bm_num = res_data["hits"]["hits"]
for bm in bm_num:
    bm_name = bm["_source"]["name_ngram_sore"]
    bm_img = bm["_source"]["img_l"]["url_no_analyzer_sore"]
    bm_id = bm["_source"]["bz"]["id_no_analyzer_sore"]
    print(bm_id)
    data = {
        'index': 'bz_article',
        'query': '{"from":0,"size":15,"query":{"bool":{"must":[{"term":{'
                 '"bz_page.id_no_analyzer_sore":"594f23f2-d114-462d-ab58-a0dd3e8b91d5"}}]}},'
                 '"sort":[{"index_int_sore":{"order":"asc"}}]}',
    }

    response = requests.post('http://szb.zh-hz.com/data/query', headers=headers, data=data,
                             verify=False)
    res_data = response.json()
    print(res_data)

# def get_chuxiong_paper(paper_time, queue_id, webpage_id):
#     # 将today的格式进行改变
#     day = paper_time
#     paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
#     base_url = f'http://szb.zh-hz.com/bz/html/index.html?date={paper_time}&pageIndex=1&cid=1'
#     url = base_url
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         content = response.content.decode()
#         print(content)
#         html_1 = etree.HTML(content)
#         # 获取所有版面的的链接
#         all_bm = html_1.xpath("//div[@class='article-con']/ul[@class='banmian-wenzhang']/li/a")
#         for bm in all_bm:
#             # 版面名称
#             bm_name = "".join(bm.xpath("./text()")).strip()
#             # 版面链接
#             bm_url = 'http://szb.zh-hz.com/bz/html/' + ''.join(bm.xpath("./@href"))
#             # 获取版面详情
#             bm_response = requests.get(bm_url, headers=headers)
#             time.sleep(1)
#             bm_content = bm_response.content.decode()
#             bm_html = etree.HTML(bm_content)
#             # 版面的pdf
#             bm_img = "".join(bm_html.xpath("//div[@class='newspaper']/img[@class='newspaper-img']/@src"))
#
#             # 获取所有文章的链接
#             all_article = bm_html.xpath("//div[@class='article-r']/ul[@class='banmian-wenzhang']/li/a")
#             pdf_set = set()
#             for article in all_article:
#                 # 获取文章链接
#                 article_url = 'http://szb.zh-hz.com/bz/html/' + ''.join(article.xpath("./@href"))
#                 # 获取文章名称
#                 article_name = ''.join(article.xpath("./text()")).strip()
#                 create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 create_date = datetime.now().strftime('%Y-%m-%d')
#                 # 获取文章内容
#                 article_response = requests.get(article_url, headers=headers)
#                 time.sleep(1)
#                 article_content = article_response.content.decode()
#                 article_html = etree.HTML(article_content)
#                 # 获取文章内容
#                 content = ''.join(article_html.xpath("//div[@id='neirong']/div/p//text()")).strip()
#                 # 上传到测试数据库
#                 conn_test = mysql.connector.connect(
#                     host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
#                     user="col2024",
#                     password="Bm_a12a06",
#                     database="col",
#                 )
#                 cursor_test = conn_test.cursor()
#                 print(bm_name, article_name, bm_img, content)
#                 # if bm_img not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
#                 #     # 将报纸url上传
#                 #     up_pdf = upload_file_by_url(bm_img, paper, "pdf", "paper")
#                 #     pdf_set.add(bm_img)
#                 #     # 上传到报纸的图片或PDF
#                 #     insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"
#                 #
#                 #     cursor_test.execute(insert_sql,
#                 #                         (day, paper, bm_name, bm_img, bm_url, up_pdf, create_time, queue_id,
#                 #                          create_date, webpage_id))
#                 #     conn_test.commit()
#                 #
#                 # if judging_criteria(article_name, content):
#                 # # if 1:
#                 #
#                 #     # print(content)
#                 #     # return
#                 #
#                 #     # 上传到报纸的内容
#                 #     insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"
#                 #
#                 #     cursor_test.execute(insert_sql,
#                 #                         (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
#                 #                          create_date, webpage_id))
#                 #     conn_test.commit()
#
#                 cursor_test.close()
#                 conn_test.close()
#
#
#         success_data = {
#             'id': queue_id,
#             'description': '数据获取成功',
#         }
#         paper_queue_success(success_data)
#
#     else:
#         raise Exception(f'该日期没有报纸')
#
#
# get_chuxiong_paper('2024-08-22', 111, 1111)
