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
from api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url, get_now_image
import requests
from lxml import etree

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9192)

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=utf-8',
    'Pragma': 'no-cache',
    'Referer': 'https://www.ovupre.com/list/19.html?proName=&sysEname=&proNo=&proType=&pubStartTime=&pubEndTime=&cityProv=%E6%9C%AA%E9%80%89%E6%8B%A9&cityCity=%E6%9C%AA%E9%80%89%E6%8B%A9&pid=&cid=&zoneName=&exceptionStatus=0&pageNum=2&type=new',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_visited=1; PHPSESSID=ad0mliauaf3ghsqdus2bep238f; _view=1; _session=1',
}


def get_wuhanguanggulianhejiaoyisuo(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            params = {
                'pageSize': '120',
                'pageNo': '1',
                'index': '6',
                'KEY_XMMC': '',
                'KEY_XMBH': '',
                'KSRQ_KS': '',
                'KSRQ_JS': '',
                'SZDQ': '',
                'SZCS': '',
                'proType': '',
            }
            img_set = set()
            name = '武汉光谷联合产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.get('https://www.ovupre.com/index/new_getxxmm.html', params=params, headers=headers)
            # print(res.text)
            res_json = res.json()
            data_list = res_json["rows"]

            for data in data_list:
                time.sleep(1)
                # print(data)
                page_url = data["URL"]
                if not page_url:
                    continue
                title_name = data["XMMC"]
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))


                # https://otc.ovupre.com/xmzx.html#/complexDetail?XMID=122030
                xm_id = re.findall(r'\?XMID=(\d+)', page_url)
                if xm_id:
                    xm_id = xm_id[0]
                else:
                    continue

                json_data = {
                    'XMID': f'{xm_id}',
                }
                response = requests.post('https://otc.ovupre.com/si/prjs/complex/detail', headers=headers, json=json_data)
                info_json = response.json()
                ann_json = info_json["data"]["XmMap"]["XMFJList"]
                # print(ann_json, '附件数据')
                annex = []
                for ann_ in ann_json:
                    ann_url = ann_["url"]
                    annex.append(ann_url)

                # print(annex)
                page.get(page_url)
                time.sleep(3)
                # print(page.html)
                res_html = etree.HTML(page.html)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                title_date = ''.join(res_html.xpath("//div[@class='detail-info']//text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, xm_id, title_date)
                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@class='default-detail-box']//text()"))
                    # https://otc.ovupre.com/si/LbFiles?type=xxpl_xmfj&id=34869&fname=%25E5%2580%25BA%25E6%259D%2583%25E6%25B8%2585%25E5%258D%2595.pdf&index=3
                    # annex = res_html.xpath("//div[@class='default-detail-box']//@href | //div[@class='default-detail-box']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'https://otc.ovupre.com/si' + ann
                            file_type = ann.split('.')[-1]
                            file_type = re.sub(r'&.*', '', file_type)
                            file_type = file_type.strip()
                            # print(file_type)
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'LbFiles' in ann:
                                file_url = upload_file_by_url(ann, "wuhan", file_type)
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
                    content_1 = res_html.xpath("//div[@class='default-detail-box']")
                    content_html = ""
                    # print(content_html)
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    # content_html += transfer_info
                    # print(content_html)
                    # return
                    try:
                        # //div[@id='text-container']
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='default-detail-box']")
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

# get_wuhanguanggulianhejiaoyisuo(111, 222)
