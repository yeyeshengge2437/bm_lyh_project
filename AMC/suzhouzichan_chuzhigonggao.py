import json
import os
import random
import re
import time
from datetime import datetime
import base64
import mysql.connector
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions
from api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9132)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'acw_tc=2760820617261086453028950e14451199475ed356bd9d44c76354c970a588; JSESSIONID=d298bdc0-a825-4587-95e5-fa609e45b418; sl-session=KCl7ZGWl42baWIXnIJcZvw==',
    'Pragma': 'no-cache',
    'Referer': 'https://www.sz-amc.com/business/Publicity?id=3&page=1',
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


def get_suzhouzichan_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for count in range(0, 40):
            page_url = f'https://www.sz-amc.com/business/Publicity?id=3&page={count}'
            response = requests.get(page_url, headers=headers)
            res = response.content.decode()
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//div[@class='detail']/ul")
            img_set = set()
            name = '苏州资产管理有限公司'
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = "".join(
                    title.xpath("./li/a/div[@class='title-small']/h5/text()"))
                title_date = "".join(title.xpath(".//div[@class='date']/text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                title_url = "https://www.sz-amc.com" + "".join(title.xpath("./li/a/@href"))
                if title_url not in title_set:
                # if 1:
                    res_title = requests.get(title_url, headers=headers)
                    res_title_html1 = res_title.content.decode()
                    res_title_html = etree.HTML(res_title_html1)

                    title_content_html = re.findall(r'<script>(.*?)</script>', res_title_html1, re.S)[0]
                    title_content_html = re.findall(r'"noticeContent":(.*?),"status"', title_content_html, re.S)[0]
                    # 将字符串转为b''
                    title_content_html = title_content_html.encode()
                    # 将Unicode转义序列（如\u4E00）转换
                    title_content_html = title_content_html.decode('unicode_escape')
                    title_content_html = re.sub(r'\\', '', title_content_html)
                    title_content_html2 = etree.HTML(title_content_html)

                    title_content = "".join(title_content_html2.xpath(
                        "//text()"))
                    annex = title_content_html2.xpath("//a/@href | //@src")
                    # if annex:
                    #     print(annex)
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann and len(ann) < 100:
                                ann = 'http://www.sz-amc.com' + ann
                            elif "http" not in ann and len(ann) > 100:
                                ann = re.sub(r'data:image/png;base64,', '', ann)
                                num_img = random.randint(1, 999999)
                                # 解码Base64字符串为二进制数据
                                image_data = base64.b64decode(ann)
                                with open(f'{num_img}.png', 'wb') as f:
                                    f.write(image_data)
                                file_url = upload_file(num_img, "png")
                                files.append(file_url)
                                original_url.append(file_url)
                                # 删除图片
                                if os.path.exists(f'{num_img}.png'):
                                    os.remove(f'{num_img}.png')

                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "suzhou", file_type)
                                # file_url = 111
                                files.append(file_url)
                                original_url.append(ann)
                        tab = page.new_tab()
                        tab.get(title_url)
                        tab.wait(2)
                        href = tab.ele("xpath=//a[@id='download']").attr('href')
                        if "http" in href:
                            original_url.append(href)
                            file_type = href.split('.')[-1]
                            file_url = upload_file_by_url(href, "suzhou", file_type)
                            files.append(file_url)
                        tab.close()

                    else:
                        files = ''
                        original_url = ''
                    if not files:
                        files = ''
                        original_url = ''
                    files = str(files).replace("'", '"')
                    original_url = str(original_url).replace("'", '"')
                    # print(files, original_url)
                    title_html_info = res_title_html.xpath(
                        "//h4[@class='list-title']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    content_html = content_html + title_content_html.strip('\"')
                    content_html = re.sub(r'src="[^"]*"', '', content_html)

                    image = get_image(page, title_url,
                                      "xpath=//div[@class='description news-detail']", down_offset=80)
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
                    # print(name, title_name, title_url, image, title_content)
                    # print(files, original_url)
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
                                            title_url, title_date, name, title_name, title_content, title_url, content_html,
                                            create_time, original_url, files, queue_id,
                                            create_date, webpage_id))
                        conn_test.commit()
                        title_set.add(title_url)

                    cursor_test.close()
                    conn_test.close()
        page.quit()
    except Exception as e:
        try:
            page.quit()
        except:
            pass
        raise Exception(e)


# get_suzhouzichan_chuzhigonggao(111, 222)
