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
co.set_paths(local_port=9210)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ga=GA1.1.1606555070.1740029608; Hm_lvt_7de38d8594a7cf1a574241f30c33446b=1740536797; _ga_ERPNN1LEDY=deleted; _ga_ERPNN1LEDY=deleted; cart=; qimoClientId=6181641741573012907; EJY-JSESSIONID=MjAyMmQ5ZTctYzQwOC00OTlkLTg1NDAtOWExZTY5MTM1ODQ1; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; uuid_49a6c050-3b8b-11eb-a27b-59d93a528836=855ed560-42a1-42a1-863d-7ca53f661f28; Hm_lvt_575182d134dee4d26e03124da592d030=1740029607,1740723217,1741161561,1741573016; HMACCOUNT=FDD970C8B3C27398; sessionId=2022d9e7-c408-499d-8540-9a1e69135845; qimo_seosource_49a6c050-3b8b-11eb-a27b-59d93a528836=%E7%AB%99%E5%86%85; qimo_seokeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; qimo_xstKeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; href=https%3A%2F%2Fwww.ejy365.com%2Fjygg_more%3Fproject_type%3DZQ; accessId=49a6c050-3b8b-11eb-a27b-59d93a528836; Hm_lpvt_575182d134dee4d26e03124da592d030=1741573118; pageViewNum=3; _ga_ERPNN1LEDY=GS1.1.1741573016.23.1.1741573218.0.0.0',
}


def get_quanguochanquanjiaoyizhongxin(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['G3', 'PG3']:
        for page_num in range(1, 20 + 1):
            if page_num == 1:
                params = {
                    'project_type': 'ZQ',
                }
            else:
                params = {
                    'project_type': 'ZQ',
                    'page': f'{page_num}',
                }

            img_set = set()
            name = '全国产权交易中心'
            title_set = judge_title_repeat(name)

            res = requests.get('https://www.ejy365.com/jygg_more', params=params, headers=headers)
            # print(res.text)
            res_json = res.text
            html = etree.HTML(res_json)
            data_list = html.xpath("//ul[@id='cqjyUl']/li")
            for data in data_list:
                time.sleep(1)
                page_url = ''.join(data.xpath("./div[@class='title']/a/@href"))
                title_name = ''.join(data.xpath("./div[@class='title']/a/text()")).strip()
                # title_date = ''.join(data.xpath("./td[4]/span//text()")).strip()
                print(page_url, title_name)

                res = requests.get(page_url, headers=headers)
                time.sleep(1)
                res_html = etree.HTML(res.text)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                title_url = page_url
                if title_url not in title_set:
                    title_date = ''.join(res_html.xpath("//div[@class='detail-info-notice']//text()")).strip()
                    # 使用re模块提取日期
                    title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                    if title_date:
                        title_date = title_date[0]
                    else:
                        title_date = ''
                    title_content = "".join(res_html.xpath("//div[@class='product-intro']//text()"))
                    title_content = title_content.join(res_html.xpath("//div[@class='detail-con-left']//text()"))

                    annex = res_html.xpath("//table[@class='base-sw ke-zeroborder']//a//@href | //div[@id='d-bdgk']//@href | //div[@id='tab1_content']//@href")
                    if annex:
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'https://cqjy.ejy365.com/' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "china", file_type)
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
                    title_html_info = res_html.xpath("//div[@class='product-intro']")
                    content_1 = res_html.xpath("//div[@class='detail-con-left']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    content_html = re.sub(r'<!--第一位是竞买公告-->.*</html>', '', content_html, flags=re.DOTALL)
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='base-container clearfix']")
                    except:
                        print('截取当前显示区域')
                        image = get_now_image(page, title_url)
                    # print(files, original_url)
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
            page.quit()
        except:
            pass
        raise Exception(e)


# get_quanguochanquanjiaoyizhongxin(111, 222)
