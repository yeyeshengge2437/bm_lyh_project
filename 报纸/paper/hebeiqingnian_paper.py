import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "河北青年报"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'TS0174700e=013750c16cb13d59f95766f02f6d6bc4f2ed4ca83e060a2390c076f9daa05a9bbe8d01dd5be7dab7a904217ba27c268a7539720299',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



def get_hebeiqingnian_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    params = {
        'date': f'{paper_time}',
        'type': '1',
    }
    url = 'https://www.hbynet.net/news_paper/newsPaperByList.do'
    response = requests.get(url, params=params, headers=headers)
    time.sleep(3)
    if response.status_code == 200:
        content = response.json()
        all_bm = content["data"]["rows"]
        count = 0
        for bm in all_bm:
            count += 1
            # 版面名称
            bm_name = f"第{count}版"
            if 'http' in bm:
                bm_pdf = bm
            else:
                # 版面的pdf
                bm_pdf = 'https://www.hbynet.net' + bm
            # 版面链接
            bm_url = bm_pdf
            pdf_set = set()

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
            # print(bm_name, bm_pdf)
            if bm_pdf not in pdf_set and judge_bm_repeat(paper, bm_url):
                # 将报纸url上传
                up_pdf = upload_file_by_url(bm_pdf, paper, "jpg", "paper")
                pdf_set.add(bm_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

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


# get_hebeiqingnian_paper('2019-07-08', 111, 1111)
