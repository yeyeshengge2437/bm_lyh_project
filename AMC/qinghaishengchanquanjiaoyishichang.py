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
co.set_paths(local_port=9184)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://www.qhcqjy.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.qhcqjy.com/.do',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    # 'Cookie': '__51vcke__3IzgAZJGzpMWGYLN=1a02177c-3072-5fdb-ab89-7e6c4dc7f8f9; __51vuft__3IzgAZJGzpMWGYLN=1740016677201; JSESSIONID=5B9377AA9C65B02970BD412768E9D1B2; __51uvsct__3IzgAZJGzpMWGYLN=3; __vtins__3IzgAZJGzpMWGYLN=%7B%22sid%22%3A%20%220de45209-9374-54ea-ba78-f50822de294e%22%2C%20%22vd%22%3A%202%2C%20%22stt%22%3A%2012345%2C%20%22dr%22%3A%2012345%2C%20%22expires%22%3A%201740644375595%2C%20%22ct%22%3A%201740642575595%7D',
}


def get_qinghaishengchanquanjiaoyishichang(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    # cookie_dict = {}
    # page.get("https://www.cspea.com.cn")
    # time.sleep(3)
    # page.refresh()
    # value_cookies = page.cookies()
    # for key in value_cookies:
    #     cookie_dict[key['name']] = key['value']

    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            data = {
                'checkType': '',
                'para': 'search',
                'id': '',
                'classCode': '',
                'type': '',
                'searchType': 'item',
                'searchKeys': 'ծȨ',
            }

            img_set = set()
            name = '青海省产权交易市场'
            title_set = judge_title_repeat(name)

            res = requests.post('http://www.qhcqjy.com/info.do', headers=headers, data=data, verify=False)
            # print(res.text)
            res_json = res.text
            res_json = etree.HTML(res_json)
            # print(res_json)
            data_list = res_json.xpath("//td[@class='tab_xw2']/a")

            for data in data_list:
                time.sleep(1)
                # print(data)
                page_url = 'http://www.qhcqjy.com' + ''.join(data.xpath("./@href"))
                # title_name = ''.join(data.xpath("./text()"))
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                # title_date = data["handBeginDate"]


                res_1 = requests.get(page_url, headers=headers)
                time.sleep(2)
                res_1 = res_1.text
                res_html = etree.HTML(res_1)
                title_url = page_url
                if title_url not in title_set:
                    title_name = ''.join(res_html.xpath("//div[@class='news_ct_l']/h1/text()"))
                    title_date = ''.join(res_html.xpath("//div[@class='news_ct_l']/div[@class='dp']/text()"))
                    # 使用re模块提取日期
                    title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                    if title_date:
                        title_date = title_date[0]
                    else:
                        title_date = ''
                    title_content = "".join(res_html.xpath("//div[@class='news_ct_l']//text()"))
                    print(title_name, title_url, title_date)
                    annex = res_html.xpath("//div[@class='news_ct_l']//@href | //div[@class='news_ct_l']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'http://www.qhcqjy.com.cn' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "qinghai", file_type)
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
                    content_1 = res_html.xpath("//div[@class='news_ct_l']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    # print(content_html)
                    # return
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='news_ct_l']")
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

# get_qinghaishengchanquanjiaoyishichang(111, 222)
