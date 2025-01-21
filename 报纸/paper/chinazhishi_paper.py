"""
中国知识产权报
"""
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree

paper = "中国知识产权报"

headers = {
    'ADMIN_ALLOW': '',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'BROWER_LANGUAGE': 'zh-CN',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'VISIT_TAG=1725610013367; JSESSIONID=8E0A400D140ED695E6AD660AA96F4EA3',
    'Origin': 'https://sz.iprchn.com',
    'Pragma': 'no-cache',
    'SCREEN': '900x1440',
    'SITE': 'zsb',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'myIdentity': 'f2c4f110-80ab-47ee-a917-6ad30cdf79f0',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
def get_chinazhishi_paper(paper_time, queue_id, webpage_id, bm_url_in=None):

    data = {
        'date': paper_time,
        'columnId': '1',
    }

    # 获取版面信息
    response = requests.post('https://sz.iprchn.com/bz/queryPageByDate', headers=headers, data=data)
    time.sleep(1)
    res_data = response.json()
    try:
        jsons_data = res_data["data"]
    except:
        raise Exception(f'该日期没有报纸')
    if jsons_data:
        jsons_data = jsons_data["pages"]
        pdf_set = set()
        page_index = 1
        for json_data in jsons_data:
            # 获取版面名称
            bm_name = json_data["name"]
            # 获取版面pdf
            bm_pdf_url = json_data["pdfFilePath"]
            bm_pdf = 'https://sz.iprchn.com/dataFile' + bm_pdf_url
            # 获取版面链接
            bm_url_id = json_data["id"]
            bm_url = f'https://sz.iprchn.com/bz/html/index.html?date={paper_time}&pageIndex={page_index}&cid=1'
            bm_data = {
                'pageId': bm_url_id,
            }
            bm_res = requests.post('https://sz.iprchn.com/bz/queryArticleByPage', headers=headers, data=bm_data)
            time.sleep(1)
            bm_res_data = bm_res.json()
            bms_data = bm_res_data["data"]["articles"]
            for bm_data in bms_data:
                # 获取文章标题
                article_name = bm_data["title"]
                title_id = bm_data["id"]
                index = bm_data["index"]
                page_id = bm_data["pageId"]
                # 文章链接
                article_url = bm_url + f'&articleId={title_id}&articleIndex={index}&pageId={page_id}'
                # 获取文章链接
                content = bm_data["text"]
                # 上传到测试数据库
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
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
                                        (paper_time, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if judging_criteria(article_name, content):
                    # if 1:

                    # print(content)
                    # return

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, paper_time, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                cursor_test.close()
                conn_test.close()

            page_index += 1
    else:
        raise Exception(f'该日期没有报纸')


# get_chinazhishi_paper("2023-12-03", 111, 222)