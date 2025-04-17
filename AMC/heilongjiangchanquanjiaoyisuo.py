import json
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
co.set_paths(local_port=9174)

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://hljcqjy.ejy365.com/EJY/Project?searchKids=%E5%80%BA%E6%9D%83',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'cart=; Hm_lvt_575182d134dee4d26e03124da592d030=1740029607; HMACCOUNT=FDD970C8B3C27398; _ga=GA1.1.1606555070.1740029608; ASP.NET_SessionId=tmhm0jp4c2u35clg1rafvvr2; Hm_lvt_6c6f927bbff1cfe5d356339000013a45=1740036324; sessionId=a17790ec-f35e-4393-af1e-265133453e8f; Hm_lpvt_575182d134dee4d26e03124da592d030=1740446476; _ga_ERPNN1LEDY=GS1.1.1740445177.7.1.1740446860.0.0.0; Hm_lpvt_6c6f927bbff1cfe5d356339000013a45=1740467825',
}



def get_heilongjiangchanquanjiaoyisuo(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            params = {
                'projectType': '',
                'maxPrice': '',
                'minPrice': '',
                'searchKids': '债权',
                'orderKey': 'FromDate',
                'order': 'desc',
                'pageIndex': '1',
                'pageSize': '20',
            }

            img_set = set()
            name = '黑龙江产权交易中心'
            title_set = judge_title_repeat(name)

            res = requests.get('https://hljcqjy.ejy365.com/EJY/ProjectList/', params=params, headers=headers)
            res_json = res.text
            html = etree.HTML(res_json)
            # print(res_json)
            data_list = html.xpath("//div[@class='box']")
            for data in data_list:
                time.sleep(1)
                page_url = "https://hljcqjy.ejy365.com" + ''.join(data.xpath("./div[@class='title']/a/@href"))
                title_name = ''.join(data.xpath("./div[@class='title']/a/text()"))
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = ''.join(data.xpath("./div[@class='item time']//text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)
                # https://hljcqjy.ejy365.com/ejy/detail?infoId=N0129GQ240059&bmStatus=%E6%8A%A5%E5%90%8D%E6%88%AA%E6%AD%A2&ggType=JYGG
                info_id = re.findall(r'infoId=(.*?)&', page_url)[0]
                bm_status = re.findall(r'bmStatus=(.*?)&', page_url)[0]
                gg_type = re.findall(r'ggType=(.*)', page_url)[0]
                params = {
                    'infoId': f'{info_id}',
                    'bmStatus': f'{bm_status}',
                    'ggType': f'{gg_type}',
                }
                res = requests.get('https://hljcqjy.ejy365.com/ejy/detail', params=params,  headers=headers)
                res_html = etree.HTML(res.text)
                time.sleep(2)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@class='channel-box']//text()"))

                    annex = res_html.xpath("//div[@class='channel-box']//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann or "HTTP" not in ann:
                                ann = 'http://www.e-jy.com.cn/' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.strip()
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "heilongjiang", file_type)
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
                    print(files, original_url)
                    # title_html_info = res_title_html.xpath("//div[@class='news_info_box']")
                    content_1 = res_html.xpath("//div[@class='channel-box']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    try:
                        image = get_image(page, title_url, "xpath=//div[@class='channel-box']")
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


# get_heilongjiangchanquanjiaoyisuo(111, 222)
