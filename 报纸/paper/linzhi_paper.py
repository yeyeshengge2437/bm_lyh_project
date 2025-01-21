import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "林芝报"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'http://www.linzhinews.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.linzhinews.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

params = {
    'pageNum': '1',
    'pageSize': '1000',
    'catalogId': '477181547507781',
    'siteId': '445057712832581',
}
def get_linzhi_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    response = requests.get('http://116.172.193.36:8090/api/cms/content/list', params=params, headers=headers, verify=False)
    res_json = response.json()
    pdf_set = set()
    for item in res_json["data"]["rows"]:
        date_str = item["publishDate"]
        date = re.findall(r'\d{4}-\d{2}-\d{2}', date_str)[0]
        if str(date) == paper_time:
            url = f'http://116.172.193.36:8090/api/cms/content/init/{item["catalogId"]}/article/{item["contentId"]}'

            response = requests.get(url, headers=headers, verify=False)
            res_json = response.json()
            res_html = res_json["data"]["contentHtml"]
            bm_imgs = re.findall('<img src="(.*?)" class="art-body-img"', res_html)
            for bm_img in bm_imgs:
                bm_name = '林芝报汉文版'
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                bm_url = bm_img
                cursor_test = conn_test.cursor()
                # print(bm_img)
                if bm_img not in pdf_set and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_img, paper, "jpg", "paper")
                    pdf_set.add(bm_img)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_img, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()
                cursor_test.close()
                conn_test.close()

    success_data = {
        'id': queue_id,
        'description': '数据获取成功',
    }
    paper_queue_success(success_data)




# get_linzhi_paper('2024-09-13', 111, 1111)
