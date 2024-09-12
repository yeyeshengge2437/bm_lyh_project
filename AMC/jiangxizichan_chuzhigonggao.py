import os
import random
import time
from datetime import datetime

import mysql.connector
from lxml import etree
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from AMC.api_paper import judge_bm_repeat, upload_file, judge_title_repeat, get_image

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9130)



headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'JSESSIONID=669FB9F02262454DA0AD8727B32C69FC',
    'Origin': 'https://www.jxfamc.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.jxfamc.com/jxjrzc/chuzhigonggao/czgg.shtml',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'type': '2',
    'pageNum': '1',
    'pageSize': '300',
}

def get_jiangxizichan_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        response = requests.post('https://www.jxfamc.com/u/dataopen/noticeList',  headers=headers, data=data)
        res_json = response.json()
        title_list = res_json["data"]
        img_set = set()
        page_url = 'https://www.jxfamc.com/jxjrzc/chuzhigonggao/czgg.shtml'
        name = "江西省金融资产管理股份有限公司"
        title_set = judge_title_repeat(name)
        for title in title_list:
            title_name = title["title"]
            title_date = title["publish"]
            title_url = f"https://www.jxfamc.com/jxjrzc/chuzhigonggao/czgg_content.shtml?id={title['id']}"
            if title_url not in title_set:
                title_url1 = f"https://www.jxfamc.com/u/dataopen/noticeList?id={title['id']}"
                title_res = requests.get(title_url1, headers=headers)
                res_title_json = title_res.json()
                content_html = res_title_json["data"][0]["content"]
                title_content = res_title_json["data"][0]["contentText"]

                image = get_image(page, title_url, "xpath=//div[@class='mainBox clearfix']")
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
                if image not in img_set and judge_bm_repeat(name, title_url):
                    # 将报纸url上传
                    up_img = upload_file(image, "png", "paper")
                    img_set.add(image)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (title_date, name, title_name, up_img, title_url, up_img, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()
                else:
                    if os.path.exists(f'{image}.png'):
                        os.remove(f'{image}.png')

                if title_url not in title_set:
                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (page_url, title_date, name, title_name, title_content, title_url, content_html,
                                         create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()
                    title_set.add(title_url)

                cursor_test.close()
                conn_test.close()
        page.close()
    except Exception as e:
        page.close()
        raise Exception(e)

# get_jiangxizichan_chuzhigonggao(111, 222)