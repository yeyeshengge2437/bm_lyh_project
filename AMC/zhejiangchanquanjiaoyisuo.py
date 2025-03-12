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
co.set_paths(local_port=9197)

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.zjpse.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.zjpse.com/page/s/prjs/zhjy/index',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Token': 'B1af691aM4ecU3BqfsR11qWCf0qQ8FnlGVjOppRWcZPFyOLeCv/xu8DOXJt2e6j8zYo3ymvrzX6Tm/IHbOKJpQ==',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'JSESSIONID=A89F7F5782FBD74A1D05EF0E85D64FE2; Hm_lvt_628522b6b63b6de4f51f8648857e4422=1739950116,1740041491,1741088278; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_628522b6b63b6de4f51f8648857e4422=1741088614',
}


def get_zhejiangchanquanjiaoyisuo(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            data = {
                'pageSize': '5',
                'pageNo': '1',
                'pllx': '',
                'ssjg': '',
                'jypl': '2D',
                'gpjg': '',
                'pljzsj': '',
                'sshy': '',
                'sortTag': '0',
            }
            img_set = set()
            name = '浙江产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.post('https://www.zjpse.com/page/s/prjs/zhjy/list', headers=headers, data=data)
            # print(res.text)
            res_json = res.text
            # print(res_json)
            res_html = etree.HTML(res_json)
            data_list = res_html.xpath("//div[@class='project_list']/ul/li")
            print(len(data_list))

            for data in data_list[1:]:
                time.sleep(1)
                # print(data)
                page_value = ''.join(data.xpath("./div[@class='title']/a[1]/@href"))
                if not page_value:
                    continue
                page_url = 'https://www.zjpse.com/' + page_value
                title_name = ''.join(data.xpath("./div[@class='title']/a[1]//text()"))
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = ''.join(data.xpath("./div[@class='cont']//text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                # print(page_url, title_name, title_date)

                response = requests.get(
                    page_url,
                    headers=headers,
                )
                transfer_info = response.text
                # transfer_html = etree.HTML(transfer_info)
                res_html = etree.HTML(transfer_info)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")

                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//ul[@class='monitor_tab_cont']//text()"))

                    annex = res_html.xpath("//ul[@class='monitor_tab_cont']//@href | //ul[@class='monitor_tab_cont']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'https://www.zjpse.com/' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.split('&')[0]
                            file_type = file_type.strip()
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'LbFiles' in ann:
                                file_url = upload_file_by_url(ann, "zhejiang", file_type)
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
                    content_1 = res_html.xpath("//ul[@class='monitor_tab_cont']")
                    content_html = ""
                    # print(content_html)
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    # content_html += transfer_info
                    try:
                        # //div[@id='text-container']
                        image = get_image(page, title_url,
                                          "xpath=//ul[@class='monitor_tab_cont']")
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

# get_zhejiangchanquanjiaoyisuo(111, 222)
