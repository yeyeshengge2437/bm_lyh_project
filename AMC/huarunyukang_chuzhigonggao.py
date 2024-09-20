import os
import random
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9128)




headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_1ba5df64758d4f917bed989cddb0939c=1726040160; HMACCOUNT=FDD970C8B3C27398; RCMS_VISITOR=faa1bbed-804c-4f63-bd6b-8cbd4703cffd; Hm_lpvt_1ba5df64758d4f917bed989cddb0939c=1726040172',
    'Pragma': 'no-cache',
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



def huarunyukang_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for count in range(1, 21):
            if count == 1:
                page_url = 'https://crykasset.com/Assets/index.html'
            else:
                page_url = f'https://crykasset.com/Assets/index_{count}.html'
            response = requests.get(page_url, headers=headers)
            res = response.content.decode()
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//li[@class='position-r']")
            img_set = set()
            name = '华润渝康资产管理有限公司'
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = "".join(title.xpath("./a/div[@class='title']/text()"))
                # title_date = "".join(title.xpath("./div[@class='more']/time[@class='date']/text()"))
                title_url = "https://crykasset.com" + "".join(title.xpath("./a/@href")).strip('..')
                if title_url not in title_set:
                    res_title = requests.get(title_url, headers=headers)
                    res_title_html1 = res_title.content.decode()
                    res_title_html = etree.HTML(res_title_html1)
                    title_date = "".join(res_title_html.xpath("//span[@class='time dtColor']/text()"))
                    title_content = "".join(res_title_html.xpath("//div[@class='RCMS_EDITOR']//text()"))
                    title_html_info = res_title_html.xpath("//div[@class='fl yk-detail-l']/div[@class='title']")
                    content_1 = res_title_html.xpath("//div[@class='RCMS_EDITOR']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    html = etree.HTML(content_html)
                    annex = html.xpath("//@href | //@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                parts = title_url.split('/')
                                base_url = '/'.join(parts[:5]) + '/'
                                ann = base_url + ann.strip('./')
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z']:
                                file_url = upload_file_by_url(ann, "huarun", file_type)
                                # file_url = 111
                                files.append(file_url)
                                original_url.append(ann)
                    else:
                        files = ''
                        original_url = ''
                    if not files:
                        files = ''
                        original_url = ''
                    files = str(files)
                    original_url = str(original_url)

                    image = get_image(page, title_url, "xpath=//div[@class='fl yk-detail-l']")
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
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
                                            (
                                                title_url, title_date, name, title_name, title_content, title_url,
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


# huarunyukang_chuzhigonggao(111, 222)
