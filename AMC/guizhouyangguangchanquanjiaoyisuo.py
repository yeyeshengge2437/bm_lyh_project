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
co.set_paths(local_port=9187)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.prechina.net/project/project.php?class3=52',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'recordurl=%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject26427.html%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Findex.php%253Fclass3%253D52%2526page%253D100%2Chttps%253A%252F%252Fwww.prechina.net%252Fproject%252Fproject.php%253Fclass3%253D52',
}


def get_guizhouyangguangchanquanjiaoyisuo(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for page_num in range(1, 101):
            params = {
                'class3': '52',
                'page': f'{page_num}',
            }
            img_set = set()
            name = '贵州阳光产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.get('https://www.prechina.net/project/index.php', params=params, headers=headers)
            res_json = res.text
            res_json = etree.HTML(res_json)
            data_list = res_json.xpath("//li[@class='media media-lg border-bottom1']")
            for data in data_list:
                time.sleep(1)
                page_url = 'https://www.prechina.net/' + ''.join(data.xpath(".//h4/a/@href")).strip('..')
                # page_url = 'https://nmgcqjy.ejy365.com' + page_url
                title_name = "".join(data.xpath(".//h4/a/span/text()"))
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = "".join(
                    data.xpath("//div[@class='media-body']//span[3]/text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)

                res = requests.get(page_url, headers=headers)
                html = res.text
                res_html = etree.HTML(html)
                time.sleep(2)

                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//section[@class='met-editor clearfix']//text()"))


                    annex = res_html.xpath(
                        "//section[@class='met-editor clearfix']//@href | //section[@class='met-editor clearfix']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'http://www.prechina.net' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.strip()
                            ann = re.sub(r'\.\.', '', ann)
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                try:
                                    file_url = upload_file_by_url(ann, "guizhou", file_type)
                                except:
                                    print(ann)
                                    continue
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
                    # print(files, original_url)
                    # title_html_info = res_html.xpath("//div[@class='product fl']")
                    content_1 = res_html.xpath("//section[@class='met-editor clearfix']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    # print(content_html)
                    try:
                        try:
                            image = get_image(page, title_url, "xpath=//section[@class='met-editor clearfix']")
                        except:
                            print('截取当前显示区域')
                            image = get_now_image(page, title_url)
                    except:
                        image = ''
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
        try:
            page.close()
        except:
            pass
    except Exception as e:
        page.close()
        raise Exception(e)


# get_guizhouyangguangchanquanjiaoyisuo(111, 2222)
