import os
import re
import time

import mysql.connector
import requests
from DrissionPage import ChromiumOptions, ChromiumPage
from lxml import etree

from AMC.api_paper import upload_file_by_url, get_image, get_now_image, upload_file

# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)
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
co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9138)
page = ChromiumPage(co)
page.set.load_mode.none()
cursor_test = conn_test.cursor()
cursor_test.execute(
    "SELECT id, page_url, original_files, files FROM col_paper_notice WHERE paper = '苏州资产管理有限公司'")

rows = cursor_test.fetchall()
for id, page_url, original_files, files in rows:
    if not files:
        res_title = requests.get(page_url, headers=headers)
        time.sleep(2)
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
                print(ann)
                if "http" not in ann:
                    ann = 'http://www.sz-amc.com' + ann
                file_type = ann.split('.')[-1]
                if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                 'png', 'jpg'] and 'upload' in ann:
                    file_url = upload_file_by_url(ann, "suzhou", file_type)
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
        insert_sql = "UPDATE col_paper_notice SET original_files = %s, files = %s WHERE id = %s"
        cursor_test.execute(insert_sql, (original_url, files, id))
        conn_test.commit()
        print(files, 11111, original_url)

cursor_test.close()
conn_test.close()
page.close()
