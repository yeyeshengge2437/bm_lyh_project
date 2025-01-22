import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree

paper = "联合日报"
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'JSESSIONID=BC1B4BB3D5F4EA071BC781688C6F1BC0; JSESSIONID=BC1B4BB3D5F4EA071BC781688C6F1BC0; JIDENTITY=8fe2fd55-a459-4421-a24c-68f8d0fb77e2; Hm_lvt_878e88c641265eda8b64cc7fa6ff4697=1728370146; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_878e88c641265eda8b64cc7fa6ff4697=1728370273',
    'Origin': 'https://app.lhwww.com.cn',
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


def get_lianhe_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')

    for i in range(1, 4 + 1):
        url = 'https://app.lhwww.com.cn/epaperPc/initEpaperData'

        data = {
            'editionId': f'{i}',
            'periodsName': f'{paper_time}',
        }

        response = requests.post(url, headers=headers, data=data, verify=False)
        try:
            bm_data = response.json()
        except:
            raise Exception(f'该日期没有报纸')
        # 版面名称
        bm_name = f'第{i}版'
        # 版面链接
        bm_url = "https://app.lhwww.com.cn/dzb"
        # 版面的pdf
        bm_pdf = bm_data["data"]["img"]
        # 获取所有文章的链接
        all_article = bm_data["data"]["navSelf"]
        pdf_set = set()
        for article in all_article:
            # 获取文章链接
            article_url = "https://app.lhwww.com.cn/dzb"
            # 获取文章名称
            article_name = article["title"]
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            create_date = datetime.now().strftime('%Y-%m-%d')
            # 获取文章内容
            article_response = requests.get(f'https://app.lhwww.com.cn/content/{article["contentId"]}', headers=headers, verify=False)
            time.sleep(1)
            article_content = article_response.json()

            # 获取文章内容
            try:
                content = article_content["data"]["txtCleanHtml"]
            except:
                content = ''
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
                # 将报纸url上传
                up_pdf = upload_file_by_url(bm_pdf, paper, "jpg", "paper")
                pdf_set.add(bm_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (day, paper, bm_name, bm_pdf, bm_pdf, up_pdf, create_time, queue_id,
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


# get_lianhe_paper('2024-11-19', 111, 1111)
