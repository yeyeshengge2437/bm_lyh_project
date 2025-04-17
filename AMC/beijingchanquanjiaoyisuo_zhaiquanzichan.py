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
co.set_paths(local_port=9166)

cookies = {
    '__jsluid_s': '7f71097b1651f22cd58bcb96c8ee8893',
    '__jsl_clearance_s': '1744769305.757|0|Eg5%2BKeEQ98UF0WTMbRxo3zOCz4c%3D',
    'csrftoken': 'c987c5f9-d9c1-4eab-88d6-50b05e35083d',
    'JSESSIONID': '9B6C85611337FB44ADD1E99B9641C42B',
}


headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.cbex.com.cn/xm/zqzc/ypl/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '__jsluid_s=7f71097b1651f22cd58bcb96c8ee8893; csrftoken=c987c5f9-d9c1-4eab-88d6-50b05e35083d; __jsl_clearance_s=1740378841.215|0|Sij6vAJORmHSzXpl8MAXl5vMDXc%3D',
}


def get_beijingchanquanjiaoyi_zhaiquanzichan(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    cookie_dict = {}
    # page.get("https://www.cbex.com.cn/onss-api/jsonp/project/search")
    # time.sleep(3)
    # value_cookies = page.cookies()
    # for key in value_cookies:
    #     cookie_dict[key['name']] = key['value']
    # print(cookie_dict)
    try:
        for zq_type in ['G3', 'PG3', 'TJ3']:
        # for zq_type in ['PG3']:
            if zq_type == 'G3' or zq_type == 'PG3':
                params = {
                    # 'callback': 'jQuery01495191642176319_1740378992052',
                    'fromPage': '1',
                    'pageSize': '2000',
                    'businessType': 'ZQ',
                    'disclosureType': f'{zq_type}',
                    'sortProperty': 'disclosuretime',
                    'sortDirection': '1',
                    'mark': 'xm',
                    # 'csrftoken': '-799914037',
                    # '_': '1740378992053',
                }
            else:
                params = {
                    # 'callback': 'jQuery02000546915719298_1744769826749',
                    'fromPage': '1',
                    'pageSize': '2000',
                    'businessType': 'TJ',
                    'disclosureType': 'TJ3',
                    'assetType': 'tj_jrzq',
                    'sortProperty': 'disclosuretime',
                    'sortDirection': '1',
                    # '_': '1744769826751',
                }

            img_set = set()
            name = '北京产权交易所_债权资产'
            title_set = judge_title_repeat(name)

            res = requests.get('https://www.cbex.com.cn/onss-api/jsonp/project/search',
                               headers=headers, cookies=cookies, params=params)
            # print(res.text)
            # return
            res_json = res.json()
            data_list = res_json["data"]["data"]

            for data in data_list:
                time.sleep(1)
                page_url = data['url']
                if 'http' not in page_url:
                    page_url = 'https://www.cbex.com.cn' + page_url
                title_name = data['name']
                title_date = data['disclosuretime']
                # print(page_url, title_name, title_date)

                page.get(page_url)
                time.sleep(1)
                res = page.html
                res_html = etree.HTML(res)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@id='project-table-box']//text() | //div[@class='main']//text()"))

                    annex = res_html.xpath("//li[@class='infoShow']//a/@href | //div[@id='project-table-box']//a/@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'https://otc.cbex.com/' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'editorUpload' in ann:
                                file_url = upload_file_by_url(ann, "beijingchanquan", file_type)
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
                    content_1 = res_html.xpath("//div[@id='project-table-box'] | //div[@class='main']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@id='project-table-box'] | //div[@class='main']")
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
            page.close()
        except:
            pass
        raise Exception(e)


# get_beijingchanquanjiaoyi_zhaiquanzichan(111, 222)
