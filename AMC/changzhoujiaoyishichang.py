import json
import re
import time
import os
import random
import re
import time
from datetime import datetime
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url, get_now_image
import requests
from lxml import etree

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9179)

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://www.czcq.com.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.czcq.com.cn/czcq/property',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # 'Cookie': 'JSESSIONID=E5374AB3C74C3BE4FE1965BB4BDC7247; href=http%3A%2F%2Fwww.czcq.com.cn%2F; LLJL_List=N0101ZQ240002; uuid_49a6c050-3b8b-11eb-a27b-59d93a528836=86d78b07-44a2-4430-acf4-cbc1a0817bb8; accessId=49a6c050-3b8b-11eb-a27b-59d93a528836; CWEB-JSESSIONID=NjJmNDk4NTUtZDU2Zi00MDI5LTk2ZGMtNmNjNjk2OWZhM2Zj; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; qimo_seosource_49a6c050-3b8b-11eb-a27b-59d93a528836=%E7%AB%99%E5%86%85; qimo_seokeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; qimo_xstKeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; pageViewNum=3',
}



def get_changzhoujiaoyishichang(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            data = {
                'page': '1',
                'limit': '16',
                'projectType': 'ZQ',
                'tabIndex': '0',
                'ajaxClick': '3',
                'startPrice': '',
                'endPrice': '',
                'hotLabelCondition': '',
            }

            img_set = set()
            name = '常州交易市场'
            title_set = judge_title_repeat(name)

            res = requests.post('http://www.czcq.com.cn/czcq/property/list', headers=headers, data=data, verify=False)
            res_json = res.json()
            data_list = res_json["records"]
            for data in data_list:
                time.sleep(1)
                page_url = data["noticeUrl"]
                title_name = data["title"]
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = str(data["pubInWebDate"])
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)
                # https://hljcqjy.ejy365.com/ejy/detail?infoId=N0129GQ240059&bmStatus=%E6%8A%A5%E5%90%8D%E6%88%AA%E6%AD%A2&ggType=JYGG
                # res = requests.get(page_url, headers=headers)
                page.get(page_url)
                html = page.html
                res_html = etree.HTML(html)
                time.sleep(2)
                # print(res.text)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@class='product fl']//text()"))
                    title_content = title_content.join(res_html.xpath("//div[@id='tab1_content']//text() | //div[@id='tab1_content']//text()"))

                    annex = res_html.xpath("//div[@id='tab1_content']//@href | //div[@id='tab1_content']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'http://www.e-jy.com.cn/' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.strip()
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "changzhou", file_type)
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
                    # title_html_info = res_html.xpath("//div[@class='product fl']")
                    content_1 = res_html.xpath("//div[@class='ph12']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    print(content_html)
                    return
                    try:
                        image = get_image(page, title_url, "xpath=//div[@class='row clearfix']")
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


get_changzhoujiaoyishichang(111, 222)
