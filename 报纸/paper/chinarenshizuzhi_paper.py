import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "组织人事报"
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.zuzhirenshi.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.zuzhirenshi.com/newspaper/index',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
def get_date(papaer_time):

    json_data = {
        'years': f'{papaer_time[0:4]}',
        'months': f'{papaer_time[5:7]}',
    }

    response = requests.post('https://www.zuzhirenshi.com/api/welcome/selectPastDianZiBao', headers=headers,
                             json=json_data)
    res_json = response.json()
    datas = res_json["data"]
    for data in datas:
        date = data["createTime"]
        if date == papaer_time:
            return data["id"]
    raise Exception(f'该日期没有报纸')


def get_chinarenshizuzhi_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_id = get_date(paper_time)
    json_data = {
        'id': f'{paper_id}',
    }

    response = requests.post('https://www.zuzhirenshi.com/api/welcome/dianZiBaoHomePage', headers=headers,
                             json=json_data)
    if response.status_code == 200:
        content = response.json()
        # 获取所有版面的的链接
        all_bm = content["data"]["dianzibaoShowList"]
        for bm in all_bm:
            # 版面名称
            bm_name = bm["columnName"]
            # 版面链接
            bm_url = "https://www.zuzhirenshi.com/newspaper/index"
            # 版面的pdf
            bm_pdf = "https://www.zuzhirenshi.com" + bm["areapdfPath"]


            # 获取所有文章的链接
            all_article = bm["areaCoordinateList"]
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = f'https://www.zuzhirenshi.com/newspaper/index?newspaperId={article["areaRelateinfoId"]}'
                # 获取文章名称
                article_name = article["newsName"]
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                params = {
                    'id': f'{article["newsId"]}',
                }

                response = requests.get('https://www.zuzhirenshi.com/api/welcome/selectNews', params=params,headers=headers)
                # 获取文章内容
                content_html = response.json()["data"]["newContent"]
                content = etree.HTML(content_html)
                content = ''.join(content.xpath("//p/text()"))
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


# get_chinarenshizuzhi_paper('2024-09-11', 111, 1111)
