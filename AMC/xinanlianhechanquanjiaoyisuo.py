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
co.set_paths(local_port=9208)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Client-Id': 'swuee',
    'Connection': 'keep-alive',
    # 'Content-Length': '0',
    'Origin': 'https://www.swuee.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.swuee.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'Hm_lvt_5f2e770b4cfb5b1de3c1697628d1054e=1739965640,1740032795,1741248115; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_bf302c82522bf3f68fce269ee8a433e8=1739965640,1740032795,1741248115; Hm_lpvt_5f2e770b4cfb5b1de3c1697628d1054e=1741248226; Hm_lpvt_bf302c82522bf3f68fce269ee8a433e8=1741248226',
}


def get_xinanlianhechanquanjiaoyisuo(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for page_num in range(1, 23 + 1):
            params = {
                'size': '30',
                'current': f'{page_num}',
                'q': '',
                'orderBy': '',
                'order': '',
                'minPrice': '',
                'maxPrice': '',
                'typeCode': '',
                'city': '',
                'county': '',
                'operationId': '1408017492266409986',
                'state': '',
                'assetsFeature': '',
                'parentId': '',
                'associationId': '',
                'deptId': '',
                'assetsFeatureParentId': '',
                'assetsFeatureChildId': '',
            }

            img_set = set()
            name = '西南联合产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.post('https://www.swuee.com/api/dscq-project/search/page', params=params, headers=headers)
            # print(res.text)
            res_json = res.json()
            data_list = res_json["data"]["records"]

            for data in data_list:
                time.sleep(1)
                page_url = f'https://www.swuee.com/#/projectDetail/{data["id"]}.html'
                title_name = data["assetsName"]
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = data["publishDate"]
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)
                page.get(page_url)
                time.sleep(1)
                page.scroll.to_bottom()
                time.sleep(2)
                value_html = page.html
                # print(value_html)
                # return
                res_html = etree.HTML(value_html)
                title_url = page_url
                if title_url not in title_set:
                    title_content = ''.join(res_html.xpath("//div[@id='tab5']/div[@class='content-border']//text()"))

                    annex = res_html.xpath("//div[@id='tab5']/div[@class='content-borer']//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'http://portal.xemas.com.cn/' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "xiamen", file_type)
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
                    # title_html_info = res_title_html.xpath("//div[@class='news_info_box']")
                    content_1 = res_html.xpath("//div[@id='tab5']/div[@class='content-border']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    # print(content_html)
                    # return
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@id='tab5']/div[@class='content-border']")
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
        try:
            page.close()
        except:
            pass
    except Exception as e:
        try:
            page.close()
        except:
            pass
        raise Exception(e)


# get_xinanlianhechanquanjiaoyisuo(111, 222)
