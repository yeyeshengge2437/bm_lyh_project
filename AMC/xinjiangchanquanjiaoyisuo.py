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
co.set_paths(local_port=9170)


headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://xjcqjy.ejy365.com/EJY/Project?projectType=001001001&HeadId=1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'cart=; Hm_lvt_575182d134dee4d26e03124da592d030=1740029607; HMACCOUNT=FDD970C8B3C27398; _ga=GA1.1.1606555070.1740029608; ASP.NET_SessionId=lonhiiavhb4f3lfvyisrtkso; Hm_lvt_6c6f927bbff1cfe5d356339000013a45=1740051217; sessionId=a69b8e4c-eed5-497b-a61d-e23829f04ec5; Hm_lpvt_575182d134dee4d26e03124da592d030=1740052057; _ga_ERPNN1LEDY=GS1.1.1740051977.2.1.1740052220.0.0.0; Hm_lpvt_6c6f927bbff1cfe5d356339000013a45=1740385679',
}


def get_xinjiangchanquanjiaoyisuo_zhaiquan(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['G3', 'PG3']:
        for zq_type in ['PG3']:
            params = {
                'projectType': '001001013',
                'cqywType': '',
                'district': '',
                'projectStatus': '',
                'maxPrice': '',
                'minPrice': '',
                'searchKids': '',
                'isImportant': '',
                'orderKey': 'FromDate',
                'order': 'desc',
                'pageIndex': '1',
                'pageSize': '50',
            }

            img_set = set()
            name = '新疆产权交易所有限责任公司'
            title_set = judge_title_repeat(name)

            res = requests.get('https://xjcqjy.ejy365.com/EJY/ProjectList/', params=params, headers=headers)
            # print(res.text)
            res_json = res.text
            html = etree.HTML(res_json)
            data_list = html.xpath("//tbody[@id='newHallList']/tr")
            for data in data_list:
                time.sleep(1)
                page_url = data.xpath("./td[2]//a/@href")[0]
                # print(page_url)
                if 'http' not in page_url:
                    page_url = 'https://xjcqjy.ejy365.com/' + page_url
                title_name = ''.join(data.xpath("./td[2]//a/text()"))
                title_date = ''.join(data.xpath("./td[4]/span//text()")).strip()
                # print(page_url, title_name, title_date)
                info_code = page_url.split('=')[-1]
                info_url = f'https://www.ejy365.com/info/{info_code}'
                page_url = info_url
                res = requests.get(info_url, headers=headers)
                time.sleep(1)
                res_html = etree.HTML(res.text)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                title_url = page_url
                if title_url not in title_set:
                # if 1:
                #     title_content = "".join(res_html.xpath("//div[@class='product-intro']//text()"))
                #     title_content = title_content.join(res_html.xpath("//div[@class='detail-con-left']//text()"))

                    annex = res_html.xpath("//table[@class='base-sw ke-zeroborder']//a//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'https://cqjy.ejy365.com/' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "xinjiang", file_type)
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
                    content_1 = res_html.xpath("//div[@id='tab1_content']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    content_html = re.sub(r'<h3>猜你喜欢</h3>.*', '', content_html, flags=re.DOTALL).strip()
                    tree_content = etree.HTML(content_html)
                    title_content = "".join(tree_content.xpath("//text()"))
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='base-container clearfix']")
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
        page.close()
    except Exception as e:
        try:
            page.close()
        except:
            pass
        raise Exception(e)


# get_xinjiangchanquanjiaoyisuo_zhaiquan(111, 222)
