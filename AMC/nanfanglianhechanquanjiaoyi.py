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
co.set_paths(local_port=9183)

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.csuaee.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.csuaee.com.cn/searchItem.html?keyword=%E5%80%BA%E6%9D%83',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'language': 'zh-cn',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'Hm_lvt_1aac8492a1c45f4949e13dc855f617ee=1740019778; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_c4f40a0013c2cb0ccb4ad6cf20361123=1740019817; Hm_lpvt_c4f40a0013c2cb0ccb4ad6cf20361123=1740638630; Hm_lpvt_1aac8492a1c45f4949e13dc855f617ee=1740638630',
}


def get_nanfanglianhechanquanjiaoyi(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    cookie_dict = {}
    page.get("https://www.cspea.com.cn")
    time.sleep(3)
    page.refresh()
    value_cookies = page.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']

    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            json_data = {
                'pageIndex': 1,
                'pageSize': 450,
                'categoryId': '',
                'price': '',
                'area': '',
                'status': '',
                'handType': '',
                'keyword': '',
                'keyword1': '债权',
                'isOrg': '',
            }

            img_set = set()
            name = '南方联合产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.post(
                'https://www.csuaee.com.cn/api/article/web/getItemsList',
                headers=headers,
                json=json_data,
            )
            # print(res.text)
            res_json = res.json()
            # print(res_json)
            data_list = res_json["Content"]

            for data in data_list:
                time.sleep(1)
                # print(data)
                try:
                    page_url = data["linkUrl"]
                    page_url = 'https://www.csuaee.com.cn' + page_url
                except:
                    continue
                title_name = data["name"]
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = data["handBeginDate"]

                print(page_url, title_name, title_date)

                res_1 = requests.get(page_url, headers=headers)
                time.sleep(2)
                res_1 = res_1.text
                res_html = etree.HTML(res_1)
                iframes = res_html.xpath("//iframe/@src")
                if not iframes:
                    continue
                tag_url = 'https://www.csuaee.com.cn/' + iframes[0]
                page.get(tag_url)
                time.sleep(3)
                html_1 = page.html
                res_html = etree.HTML(html_1)
                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//text()"))

                    annex = res_html.xpath("//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'https://www.csuaee.com.cn' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'UserFiles' in ann:
                                file_url = upload_file_by_url(ann, "nanfang", file_type)
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
                    # title_html_info = res_title_html.xpath("//div[@class='news_info_box']")
                    content_1 = res_html.xpath("//div[@class='project-detail-left']")
                    content_html = html_1
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    # for con in content_1:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    # print(content_html)
                    # return
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='provision-detail']")
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
        page.close()
        raise Exception(e)

# get_nanfanglianhechanquanjiaoyi(111, 222)
