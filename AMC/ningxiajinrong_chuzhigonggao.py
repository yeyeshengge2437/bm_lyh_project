import os
import random
import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co = co.ignore_certificate_errors()  # 忽略证书错误
co.set_paths(local_port=9134)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=29EC36B549C606C2BE78941956D80910',
    'Pragma': 'no-cache',
    'Referer': 'https://nxfamc.com/jyzx/zctj1/1.htm',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_ningxiajinrong_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for count in range(0, 22):
            if count == 0:
                page_url = f'https://nxfamc.com/jyzx/zctj1.htm'
            else:
                num = 22 - count
                page_url = f'https://nxfamc.com/jyzx/zctj1/{num}.htm'
            response = requests.get(page_url, headers=headers, verify=False)
            res = response.content.decode()
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//div[@class='zctjlist2']/ul/li")
            img_set = set()
            name = '宁夏金融资产管理有限公司'
            title_set = judge_title_repeat(name)
            for title in title_list:
                # title_name = "".join(
                #     title.xpath("./div[@class='Announcement_nr']/div[@class='Announcement_title']//text()"))
                # title_date = "".join(title.xpath("./div[@class='more']/time[@class='date']/text()"))
                title_url = "https://nxfamc.com" + "".join(title.xpath("./div[@class='zctjlist2_con']/div[@class='a44']/a/@href")).strip('..')
                if title_url not in title_set:
                    # print(title_url)
                    # return
                    res_title = requests.get(title_url, headers=headers, verify=False)
                    res_title_html1 = res_title.content.decode()
                    res_title_html = etree.HTML(res_title_html1)
                    title_name = "".join(
                        res_title_html.xpath("//div[@class='title']/text()"))
                    title_date = "".join(res_title_html.xpath("//div[@class='fbsj']/text()"))
                    annex = res_title_html.xpath("//div[@class='fbsj']//a/@href")
                    if annex:
                        print(annex, title_url)
                    # 使用re模块提取日期
                    title_date = re.findall(r'\d{4}-\d{2}-\d{2}', title_date)
                    if title_date:
                        title_date = title_date[0]
                    else:
                        title_date = ''
                    title_content = "".join(res_title_html.xpath(
                        "//div[@class='v_news_content']//text()"))
                    title_html_info = res_title_html.xpath(
                        "//div[@class='detail_shuxing']")
                    content_1 = res_title_html.xpath("//div[@class='v_news_content']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()

                    image = get_image(page, title_url,
                                      "xpath=//div[@class='detail']",
                                      left_offset=10)
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
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_url, title_date, name, title_name, title_content, title_url, content_html,
                                             create_time, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                        title_set.add(title_url)

                    cursor_test.close()
                    conn_test.close()
        page.close()
    except Exception as e:
        page.close()
        raise Exception(e)

# get_ningxiajinrong_chuzhigonggao(111, 222)
