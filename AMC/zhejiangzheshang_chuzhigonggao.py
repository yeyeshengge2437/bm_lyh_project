"""
浙江浙商证券股份有限公司,每日更新时获取前50页的数据
"""
import os
import random
import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from AMC.api_paper import judging_bm_criteria, judge_bm_repeat, upload_file_by_url, judge_title_repeat, upload_file

from DrissionPage import ChromiumPage, ChromiumOptions
co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9123)



def get_image(page, url, title_name):
    tab = page.new_tab()
    tab.get(url)
    tab.wait.ele_displayed(".info-lf")
    value = tab.ele(".info-lf").rect.corners
    top_left = value[0]
    bottom_right = value[2]
    # 将top_left元组中的浮点数转换为整数
    top_left1 = (int(top_left[0]), int(top_left[1]))
    # 将bottom_right元组中的浮点数转换为整数
    bottom_right1 = (int(bottom_right[0]), int(bottom_right[1]))
    length = bottom_right1[1] - top_left1[1]
    if length < 20000:
        bytes_str = tab.get_screenshot(as_bytes='png', left_top=top_left1, right_bottom=bottom_right1)
    else:
        bottom_right1 = (int(bottom_right[0]), 8000)
        bytes_str = tab.get_screenshot(as_bytes='png', left_top=top_left1, right_bottom=bottom_right1)
    # 随机的整数
    random_int = random.randint(0, 1000000)
    with open(f'{random_int}.png', 'wb') as f:
        f.write(bytes_str)
    tab.close()
    return random_int


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'sessions_site_=89gaif667p3l8e63dqq9p1c9ak8tdrsr; UM_distinctid=191da9b0417bb6-0301e98d1b6524-26001151-13c680-191da9b04189b6; CNZZDATA1281158231=614975122-1725949478-%7C1725949620',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_zhejiangzheshang_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    count = 1
    while True:
        page_url = f'https://www.zsamc.com/index.php/infor/index/20/0/{count}.html'
        response = requests.get(page_url, headers=headers)
        img_set = set()
        res_html = response.content.decode()
        time.sleep(1)
        html = etree.HTML(res_html)
        title_list = html.xpath("//div[@id='list-ajax']/div[@class='shoot']/a")
        title_num = len(title_list)
        if count == 50:
            page.close()
            break
        else:
            count += 1
        name = "浙江省浙商资产管理有限公司"
        title_set = judge_title_repeat(name)
        for title in title_list:
            title_name = "".join(title.xpath("./div[@class='shoot-ls-rg']/p[@class='shoot-ls-tit tit-20']/text()"))
            title_url = "".join(title.xpath("./@href"))
            if title_url not in title_set:
                title_date = "".join(title.xpath("./div[@class='shoot-ls-rg']/div[@class='shoot-ls-btn']/text()")).strip()
                # 使用re匹配日期
                title_date = re.findall(r'\d{4}-\d{2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                res_title = requests.get(title_url, headers=headers)
                time.sleep(1)
                res_title_html = res_title.content.decode()
                html_title = etree.HTML(res_title_html)
                title_content = "".join(html_title.xpath("//div[@class='info-cont tit-16']//text()"))
                con_html = html_title.xpath("//div[@class='info-lf']")
                # if not con_html:
                #     con_html = html.xpath("//div[@class='TRS_Editor']")
                content_html1 = ''
                for con in con_html:
                    content_html1 += etree.tostring(con, encoding='utf-8').decode()
                html1 = etree.HTML(content_html1)
                title_html = html1.xpath("//div[@class='info-lf']/p[@class='info-tit']")
                info_time = html1.xpath("//div[@class='info-cent']/p[@class='info-time tit-16']")
                content_1 = html1.xpath("//div[@class='info-cont tit-16']")
                content_html = ''
                for con in title_html:
                    content_html += etree.tostring(con, encoding='utf-8').decode()
                for con in info_time:
                    content_html += etree.tostring(con, encoding='utf-8').decode()
                for con in content_1:
                    content_html += etree.tostring(con, encoding='utf-8').decode()

                content_as = html_title.xpath("//div[@class='info-cont tit-16']//a/@href")
                for content_a in content_as:
                    if "htm" not in content_a:
                        print(content_a)
                image = get_image(page, title_url, title_name)
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

# get_zhejiangzheshang_chuzhigonggao(111,1111)