import os
import random
import time
from datetime import datetime

import mysql.connector
from lxml import etree
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from api_paper import judge_bm_repeat, upload_file, judge_title_repeat, get_image

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9230)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.ruijingamc.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}


def get_jiangxiruijin_zichantuijie(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for page_num in range(1, 4 + 1):
            response = requests.get(f'http://www.ruijingamc.com/asset/page/2/{page_num}', headers=headers, verify=False)
            res_json = response.json()
            title_list = res_json["data"]["list"]
            img_set = set()
            name = "江西瑞京金融资产管理有限公司_资产推介"
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = title["assetName"]
                title_date = title["startTime"]
                title_url = f"http://www.ruijingamc.com/#/available/{title['id']}"
                if title_url not in title_set:
                    page.get(title_url)
                    time.sleep(5)
                    res_detail_html_ = page.html
                    res_detail_html = etree.HTML(res_detail_html_)
                    content_1 = res_detail_html.xpath("//div[@class='container']")
                    content_html = ''
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    title_content = ''.join(res_detail_html.xpath("//div[@class='container']//text()"))

                    image = get_image(page, title_url, "xpath=//div[@class='container']")
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
                                            (
                                            title_url, title_date, name, title_name, title_content, title_url, content_html,
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


# get_jiangxiruijin_zichantuijie(111, 222)
