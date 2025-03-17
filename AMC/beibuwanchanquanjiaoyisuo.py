import re
import time
import os
import random
import re
import time
from datetime import datetime
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url, get_now_image
import requests
from lxml import etree

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9207)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Language': 'zh_CN',
    'Pragma': 'no-cache',
    'Referer': 'https://bbwcq.com/projects?pageNumber=2&pageSize=12&proTypeSearch=3&bidTypeSearch=6&areaCtyCode=%E5%85%A8%E9%83%A8&keyWord=&priceLow=0&priceHigh=0&status=0&orderType=0&orderBy=desc',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'sl-session=Rwq6FgeYymfCt6FEfvzmIw==',
}


def get_beibuwanchanquanjiaoyisuo(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['G3', 'PG3']:
        for page_num in range(1, 6 + 1):
            params = {
                'pageNumber': f'{page_num}',
                'pageSize': '100',
                'proTypeSearch': '3',
                'bidTypeSearch': '6',
                'areaCtyCode': '全部',
                'priceLow': '0',
                'priceHigh': '0',
                'status': '0',
                'orderType': '0',
                'orderBy': 'desc',
                'lawRelatedType': '0',
                'isHongGuiList': '0',
            }

            img_set = set()
            name = '北部湾产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.get('https://bbwcq.com/java/api/projectPage', params=params, headers=headers)
            # print(res.text)
            res_json = res.json()
            data_list = res_json["data"]["list"]
            for data in data_list:
                time.sleep(1)
                page_url = data["ejyProjectUrl"]
                if not page_url:
                    continue
                title_name = data["proName"]
                title_date = data["pubStartTime"]
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)
                res = requests.get(page_url, headers=headers)
                time.sleep(1)
                res_html = etree.HTML(res.text)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@class='product-intro']//text()"))
                    title_content = title_content.join(res_html.xpath("//div[@class='detail-con-left']//text()"))

                    annex = res_html.xpath("//div[@class='detail-con-left']//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'https://cqjy.ejy365.com/' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "xinjiang", file_type)
                                # file_url = 111
                                files.append(file_url)
                                original_url.append(ann)
                    else:
                        files = ''
                        original_url = ''
                    if not files:
                        files = ''
                        original_url = ''
                    files = str(files).replace("'", '"')
                    original_url = str(original_url).replace("'", '"')
                    print(files, original_url)
                    title_html_info = res_html.xpath("//div[@class='product-intro']")
                    content_1 = res_html.xpath("//div[@class='detail-con-left']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    content_html = re.sub(r'<!--第一位是竞买公告-->.*</html>', '', content_html,  flags=re.DOTALL )
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='base-container clearfix']")
                    except:
                        print('截取当前显示区域')
                        image = get_now_image(page, title_url)
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # print(title_name, title_date, title_url, title_content, files, original_url)
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
                                            (title_date, name, title_name, up_img, title_url, up_img, create_time,
                                             queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                    else:
                        if os.path.exists(f'{image}.png'):
                            os.remove(f'{image}.png')

                    if title_url not in title_set:
                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time,original_files, files, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_url, title_date, name, title_name, title_content, title_url,
                                             content_html,
                                             create_time, original_url, files, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                        title_set.add(title_url)

                    cursor_test.close()
                    conn_test.close()
        page.close()
    except Exception as e:
        try:
            page.quit()
        except:
            pass
        raise Exception(e)


# get_beibuwanchanquanjiaoyisuo(111, 222)
