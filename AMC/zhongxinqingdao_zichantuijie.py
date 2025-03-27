import os
import random
import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
from api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url, get_now_image

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9219)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '__jsluid_h=d6a50128c73a34b4b3070e20f222621c',
    'Pragma': 'no-cache',
    'Referer': 'http://www.qdamc.citic/announcement-54-1-5.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}


def get_zhongxinqingdao_zichantuijie(queue_id, webpage_id):
    page = ChromiumPage(co)
    # page.set.headers(headers=headers)
    page.set.load_mode.none()
    try:
        for count in range(1, 1 + 1):
            page_url = f'http://www.qdamc.citic/announcement-6-1.html'
            response = requests.get(page_url, headers=headers)
            res = response.content.decode()
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//div[@class='main gonggaobox fix']/ul/li/a")
            img_set = set()
            name = '中信青岛资产管理有限公司_资产推介'
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = "".join(
                    title.xpath(".//div[@class='t1 ellipsis-2']//text()"))

                title_url = "http://www.qdamc.citic/" + "".join(title.xpath("./@href"))
                if title_url not in title_set:
                    # print(title_name,title_url)
                    # return
                    res_title = requests.get(title_url, headers=headers)
                    res_title_html1 = res_title.content.decode()
                    res_title_html = etree.HTML(res_title_html1)
                    title_date = "".join(res_title_html.xpath("//div[@class='main2']/div[@class='info']//text()"))
                    # 使用re模块提取日期
                    title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                    if title_date:
                        title_date = title_date[0]
                    else:
                        title_date = ''
                    title_content = "".join(res_title_html.xpath(
                        "//div[@class='main2']/div[@class='newshow']//text()"))

                    annex = res_title_html.xpath("//div[@class='main2']/div[@class='newshow']//a/@href | //div[@class='main2']/div[@class='newshow']//@src")
                    if annex:
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = "http://www.qdamc.citic/" + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z', 'jpg'] and 'uploads' in ann:
                                file_url = upload_file_by_url(ann, "ningbofujian", file_type)
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

                    title_html_info = res_title_html.xpath(
                        "//div[@class='intit']")
                    content_1 = res_title_html.xpath("//div[@class='main2']/div[@class='newshow']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    tab = page.new_tab()
                    tab.get('http://www.qdamc.citic/')
                    tab.close()
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='news_sec article-block articleShow']", left_offset=10)
                    except:
                        print('截取当前显示区域')
                        image = get_now_image(page, title_url)
                    print(files, original_url)
                    return
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
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
                                            (title_date, name, title_name, up_img, title_url, up_img, create_time, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                    else:
                        if os.path.exists(f'{image}.png'):
                            os.remove(f'{image}.png')

                    if title_url not in title_set:
                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time,original_files, files, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_url, title_date, name, title_name, title_content, title_url, content_html,
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

# get_zhongxinqingdao_zichantuijie(111, 222)
