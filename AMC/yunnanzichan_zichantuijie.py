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
co.set_paths(local_port=9220)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Cookie': 'Secure; AYKJDATA=1742977650396; security_session_verify=6de2150939ed14504c133833f19e258c; srcurl=687474703a2f2f7777772e796e64616d632e636f6d2f6c6973742f636e50432f312f31382f6175746f2f31322f302e68746d6c; Secure; security_session_mid_verify=df85379301937610d00d188893eb3d23; JSESSIONID=DDAF46D69FE80AF288C2AE66FB343276'
}


cookies = {
    'Secure': '',
    'AYKJDATA': '1743141933997',
    'srcurl': '687474703a2f2f7777772e796e64616d632e636f6d2f6c6973742f636e50432f312f31382f6175746f2f31322f302e68746d6c',
    'security_session_verify': 'b0df7e620f4c9660f193c789b74dd9e3',
    'security_session_mid_verify': 'e405274e8825d13203dc7980952f04b6',
    'JSESSIONID': '1D48DD28CF3F954C844FFDD2C9FE3F23'
}

def get_yunnanzichan_zichantuijie(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for count in range(1, 1 + 1):
            page.get('http://www.yndamc.com/list/cnPC/1/18/auto/12/0.html')
            res = page.html
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//div[@class='assetsCList ajaxBox']/dl/dd")
            img_set = set()
            name = '云南省资产管理有限公司_资产推介'
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = "".join(
                    title.xpath(".//div/div//text()"))


                title_url = "http://www.yndamc.com/" + "".join(title.xpath("./a/@href"))
                if title_url not in title_set:
                    # print(title_name,title_url)
                    # return
                    page.get(title_url)
                    time.sleep(3)
                    res_title_html1 = page.html
                    res_title_html = etree.HTML(res_title_html1)
                    # 此处没有日期，需在详情中获取
                    title_date = "".join(res_title_html.xpath(".//div[@class='upTime']/text()"))
                    # 使用re模块提取日期
                    title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                    if title_date:
                        title_date = title_date[0]
                    else:
                        title_date = ''
                    title_content = "".join(res_title_html.xpath(
                        "//div[@class='assetsArticle']//text()"))
                    # title_content = re.sub(r'\.[bsp][^{]*\{.*?\}', '', title_content, flags=re.MULTILINE).strip()
                    annex = res_title_html.xpath("//@href | //@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'http://www.yndamc.com/' + ann
                            if 'download' in ann:
                                file_url = upload_file_by_url(ann, "yunnan", 'xlsx')
                                # file_url = 111
                                files.append(file_url)
                                original_url.append(ann)
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'temp' in ann:
                                file_url = upload_file_by_url(ann, "yunnan", file_type)
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
                    title_html_info = res_title_html.xpath(
                        "//div[@class='assetsArticle']")
                    # content_1 = res_title_html.xpath("//div[@id='articleContent']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    # for con in content_1:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    content_html = re.sub(r'<div class="pageUp">.*?</html> &#13;', '', content_html, flags=re.DOTALL).strip()
                    content_html = re.sub(r'<script>.*?</body></html>', '', content_html, flags=re.DOTALL).strip()
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='assetsArticle']", is_to_bottom=True)
                    except:
                        print('截取当前显示区域')
                        image = get_now_image(page, title_url)
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

# get_yunnanzichan_zichantuijie(111, 222)
