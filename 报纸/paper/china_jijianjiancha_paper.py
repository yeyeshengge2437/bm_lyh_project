import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "中国纪检监察报"

cookies = {
    '_trs_uv': 'm1n0z125_4878_bybu',
    'HMF_CI': '54765e3444b6c3aa62cbd8d93c971ae99e2d41a6b2a3ef842210c7e802c50e37aa4acd09d4ebeeaee6ee2bf884e8e5e9094857a797af6ea6b0c19056bd22b0822f',
    'HMY_JC': 'bc87e5c196239f6c0f439e3dc46d3d38b063f3cde9c8c38668b3df48aa8006ddd4,',
    '_trs_ua_s_1': 'm5z2ar4b_4878_5fig',
    'HBB_HC': 'cf5cf3f72868c8525424cf9171eab053d492b6386c73c4369ae651ad6c38a4b8b0927d25ace4dde8a33b977a1997aefbf4',
}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_trs_uv=m1n0z125_4878_bybu; HMF_CI=54765e3444b6c3aa62cbd8d93c971ae99e2d41a6b2a3ef842210c7e802c50e37aa4acd09d4ebeeaee6ee2bf884e8e5e9094857a797af6ea6b0c19056bd22b0822f; HMY_JC=bc87e5c196239f6c0f439e3dc46d3d38b063f3cde9c8c38668b3df48aa8006ddd4,; _trs_ua_s_1=m5z2ar4b_4878_5fig; HBB_HC=cf5cf3f72868c8525424cf9171eab053d492b6386c73c4369ae651ad6c38a4b8b0927d25ace4dde8a33b977a1997aefbf4',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



def get_chuxiong_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    data = {
        'docPubTime': f'{paper_time}',
    }
    url = 'https://jjjcb.ccdi.gov.cn/reader/layout/findBmMenu.do'
    response = requests.post(url, headers=headers, data=data, cookies=cookies)
    if response.status_code == 200:
        content = response.json()
        print(content)
        return
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@class='nav-list']/ul/li")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./a[@class='btn btn-block']/text()")).strip()
            # 版面链接
            bm_url = ''.join(bm.xpath("./a[@class='btn btn-block']/@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_pdf = 'http://epaper.chuxiong.cn/' + "".join(bm_html.xpath("//div[@class='nav-list']/ul/li/a[@class='pdf']/@href")).strip('../..')

            # 获取所有文章的链接
            all_article = bm_html.xpath("//ul/li[@class='resultList']/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = 'http://epaper.chuxiong.cn/' + ''.join(article.xpath("./@href")).strip('../..')
                # 获取文章名称
                article_name = ''.join(article.xpath("./h4/text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='ozoom']/founder-content/p/text()")).strip()
                # # 上传到测试数据库
                # conn_test = mysql.connector.connect(
                #     host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                #     user="col2024",
                #     password="Bm_a12a06",
                #     database="col",
                # )
                # cursor_test = conn_test.cursor()
                print(bm_name, article_name, article_url, bm_pdf, content)
                # if bm_pdf not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                #     # 将报纸url上传
                #     up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                #     pdf_set.add(bm_pdf)
                #     # 上传到报纸的图片或PDF
                #     insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"
                #
                #     cursor_test.execute(insert_sql,
                #                         (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                #                          create_date, webpage_id))
                #     conn_test.commit()
                #
                # if judging_criteria(article_name, content):
                # # if 1:
                #
                #     # print(content)
                #     # return
                #
                #     # 上传到报纸的内容
                #     insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"
                #
                #     cursor_test.execute(insert_sql,
                #                         (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                #                          create_date, webpage_id))
                #     conn_test.commit()
                #
                # cursor_test.close()
                # conn_test.close()


        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        raise Exception(f'该日期没有报纸')


get_chuxiong_paper('2025-01-16', 111, 1111)
