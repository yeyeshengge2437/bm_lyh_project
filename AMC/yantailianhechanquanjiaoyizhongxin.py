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
co.set_paths(local_port=9172)

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://www.ytcq.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.ytcq.com/searchlist.html?gjword=%E5%80%BA%E6%9D%83',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # 'Cookie': 'JSESSIONID=A495800E5806E9CA15B8F4B627FFCEE7',
}


def get_yantailianhechanquanjiaoyizhongxin(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            params = {
                'cmd': 'getInfolistahhm',
            }

            data = {
                'keyword': '债权',
                'pageIndex': '1',
                'pageSize': '30',
            }

            img_set = set()
            name = '烟台联合产权交易中心'
            title_set = judge_title_repeat(name)

            res = requests.post(
                'http://www.ytcq.com/EpointWebBuilder/searchlistAction_Custom.action',
                params=params,
                headers=headers,
                data=data,
                verify=False,
            )
            # print(res.text)
            res_json = res.json()
            # print(res_json)
            data_list = res_json["custom"]
            # 转为json模式
            data_list = json.loads(data_list)
            data_list = data_list["Table"]

            for data in data_list:
                time.sleep(1)
                # print(data)

                page_url = data["solution"]
                # http://www.ytcq.com/xmpd/002001/002001001/20240621/639e5e11-aed6-476e-a610-cfc8feda7927.html
                page_url = 'http://www.ytcq.com' + page_url
                title_name = data["title"]
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = data['date']
                # title_date = datetime.utcfromtimestamp(title_date // 1000).strftime('%Y-%m-%d')
                # print(page_url, title_name, title_date)

                res = requests.get(page_url,headers=headers,verify=False,)
                res = res.text
                res_html = etree.HTML(res)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                # # 使用re模块提取日期
                # title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                # if title_date:
                #     title_date = title_date[0]
                # else:
                #     title_date = ''
                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@class='pro-xiangmu l']//text() | //div[@class='ewb-info']//text()"))

                    annex = res_html.xpath("//div[@class='pro-tab-box']//@src | //a//@href | //div[@class='ewb-content']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'http://www.ytcq.com/' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'uploadfile' in ann:
                                file_url = upload_file_by_url(ann, "yantai", file_type)
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
                    content_1 = res_html.xpath("//div[@class='pro-xiangmu l'] | //div[@class='ewb-info']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    try:
                        image = get_image(page, title_url, "xpath=//div[@class='ewb-info'] | //body/div[@class='ewb-container']")
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


# get_yantailianhechanquanjiaoyizhongxin(111, 222)
