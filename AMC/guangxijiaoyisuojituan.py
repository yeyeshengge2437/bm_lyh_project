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
co.set_paths(local_port=9203)

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.gxcq.com.cn/list-154.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # 'Cookie': 'Hm_lvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1740710528,1741158406; Hm_lpvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1741158406; HMACCOUNT=FDD970C8B3C27398',
}


def get_guangxijiaoyisuojituan(queue_id, webpage_id):

    try:
        # for zq_type in ['C05', 'C06']:
        for page_num in range(1, 41 + 1):
            params = {
                's': 'httpapi',
                'id': '2',
                'appid': '1',
                'appsecret': 'PHPCMFA0EF8F01A56FF',
                'data[page]': f'{page_num}',
                'data[assetsTypeParent]': 'ZQ',
                'data[cate_id]': '154',
            }
            img_set = set()
            name = '广西交易所集团'
            title_set = judge_title_repeat(name)

            res = requests.get('http://www.gxcq.com.cn/index.php', params=params, headers=headers, verify=False)
            # print(res.text)
            res_json = res.json()
            res_html = res_json["data"]["project_html"]
            res_etree = etree.HTML(res_html)
            data_list = res_etree.xpath("//li")

            for data in data_list:
                time.sleep(1)
                page_url = ''.join(data.xpath("./a//@href"))
                title_name = ''.join(data.xpath("./a/h1/text()"))
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = ''.join(data.xpath("./a//span[3]/text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)
                try:
                    page = ChromiumPage(co)
                    page.set.load_mode.none()
                    time.sleep(4)
                    page.get(page_url)
                except Exception as e:
                    print('没有访问到')
                    continue
                page.scroll.to_bottom()
                time.sleep(3)
                # print(page.html)
                # return
                res_html = etree.HTML(page.html)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")

                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@class='txt-content-wrap']//text()"))

                    annex = res_html.xpath(
                        "//div[@class='txt-content-wrap']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'https://aaee.com.cn/' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.split('&')[0]
                            file_type = file_type.strip()
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'group1' in ann:
                                file_url = upload_file_by_url(ann, "guangxi", file_type)
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
                    content_1 = res_html.xpath("//div[@class='txt-content-wrap']")
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
                        # print('2222222')
                        # //div[@id='text-container']
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='txt-content-wrap']", is_to_bottom=True)
                        # print(image, '1234')
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


# get_guangxijiaoyisuojituan(111, 222)
