import os
import random
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
co.set_paths(local_port=9125)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASP.NET_SessionId=o3lcjpumzjmshqghd5kx013x',
    'Pragma': 'no-cache',
    'Referer': 'https://www.utrustamc.com/czgg/list.aspx?page=2',
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


def guangdongzichan_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        count = 1
        while True:
            page_url = f'https://www.utrustamc.com/czgg/list.aspx?page={count}#SubMenu'
            response = requests.get(page_url, headers=headers)
            res = response.content.decode()
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//ul[@class='NewsList2 flexbw']/li/a")
            if count == 20:
                break
            else:
                count += 1
            img_set = set()
            name = '广东粤财资产管理有限公司'
            title_set = judge_title_repeat(name)
            # title_set = set()
            for title in title_list:
                title_name = "".join(title.xpath("./aside[@class='ti f24 dot1']/text()"))
                title_date = "".join(title.xpath("./div[@class='more']/time[@class='date']/text()"))
                title_url = "https://www.utrustamc.com" + "".join(title.xpath("./@href"))
                if title_url not in title_set:
                    # print(title_name,title_date,title_url)
                    res_title = requests.get(title_url, headers=headers)
                    res_title_html1 = res_title.content.decode()
                    res_title_html = etree.HTML(res_title_html1)
                    title_content = "".join(res_title_html.xpath("//div[@class='NewsInfo']/article//text()"))
                    title_html_info = res_title_html.xpath("//div[@class='TitleInfo']")
                    content_1 = res_title_html.xpath("//div[@class='NewsInfo']/article")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    detail_url = res_title_html.xpath("//div[@class='info_pro']//a/@href")
                    for det_url in detail_url:
                        if 'Assetinquiry' not in det_url:
                            continue
                        det_url = "https://www.utrustamc.com" + det_url
                        res_det = requests.get(det_url, headers=headers)
                        res_det_html = res_det.content.decode()
                        res_det_html = etree.HTML(res_det_html)
                        det_html_info = "".join(res_det_html.xpath("//div[@class='SearchDetail']//text()"))
                        title_content += det_html_info
                        det_html = res_det_html.xpath("//div[@class='SearchDetail']")
                        det_content = ''
                        for det in det_html:
                            det_content += etree.tostring(det, encoding='utf-8').decode()
                        content_html += det_content

                    image = get_image(page, title_url, '.NewsInfo', left_offset=10)
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col_test",
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
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_url, title_date, name, title_name, title_content, title_url,
                                             content_html,
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


# guangdongzichan_chuzhigonggao(111, 222)
