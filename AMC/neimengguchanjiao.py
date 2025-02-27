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
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url, get_now_image
import requests
from lxml import etree
from bs4 import BeautifulSoup

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9181)

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://www.czcq.com.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.czcq.com.cn/czcq/property',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # 'Cookie': 'JSESSIONID=E5374AB3C74C3BE4FE1965BB4BDC7247; href=http%3A%2F%2Fwww.czcq.com.cn%2F; LLJL_List=N0101ZQ240002; uuid_49a6c050-3b8b-11eb-a27b-59d93a528836=86d78b07-44a2-4430-acf4-cbc1a0817bb8; accessId=49a6c050-3b8b-11eb-a27b-59d93a528836; CWEB-JSESSIONID=NjJmNDk4NTUtZDU2Zi00MDI5LTk2ZGMtNmNjNjk2OWZhM2Zj; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; qimo_seosource_49a6c050-3b8b-11eb-a27b-59d93a528836=%E7%AB%99%E5%86%85; qimo_seokeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; qimo_xstKeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; pageViewNum=3',
}
def remove_script_tags_safe(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup.find_all('script'):
        script.decompose()
    return str(soup)

def get_neimengguchanquanjiaoyi_zichanchaoshizhaiquan(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:

            img_set = set()
            name = '内蒙古产权交易中心_资产超市债权'
            title_set = judge_title_repeat(name)

            res = requests.get(
                'https://nmgcqjy.ejy365.com/FinanceReform/NewsIndex?firTypeName=%e8%b5%84%e4%ba%a7%e8%b6%85%e5%b8%82&secTypeName=%e5%80%ba%e6%9d%83&secID=10653&firID=10636&HeadId=4',
                headers=headers,
            )
            res_json = res.text
            res_json = etree.HTML(res_json)
            data_list = res_json.xpath("//div[@id='newsList']//div[@class='project_lists clearfix']/a")
            for data in data_list:
                time.sleep(1)
                page_url = ''.join(data.xpath("./@href"))
                page_url = 'https://nmgcqjy.ejy365.com' + page_url
                title_name = "".join(data.xpath("./span[1]/text()"))
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = "".join(data.xpath("./span[2]/text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)

                res = requests.get(page_url, headers=headers)
                html = res.text
                res_html = etree.HTML(html)
                time.sleep(2)

                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@class='news-content']//text()"))
                    # title_content = title_content.join(
                    #     res_html.xpath("//div[@id='tab1_content']//text() | //div[@id='tab1_content']//text()"))

                    annex = res_html.xpath("//div[@class='news-content']//@href | //div[@class='news-content']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'https://nmgcqjy.ejy365.com' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.strip()
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "neimenggu", file_type)
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
                    # title_html_info = res_html.xpath("//div[@class='product fl']")
                    content_1 = res_html.xpath("//div[@class='news-content']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    try:
                        image = get_image(page, title_url, "xpath=//div[@class='news-content']")
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
        page.close()
        raise Exception(e)


def get_neimengguchanquanjiaoyi_guapaixiangmuzhaiquan(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for page_num in range(1, 72):
            params = {
                'projectType': '债权',
                'orderKey': 'StartDate',
                'order': 'desc',
                'pageIndex': '1',
                'searchKids': '',
                'pageSize': '704',
            }
            img_set = set()
            name = '内蒙古产权交易中心_挂牌项目债权'
            title_set = judge_title_repeat(name)

            res = requests.get('https://nmgcqjy.ejy365.com/FinanceReform/ProjectList/', params=params, headers=headers)
            res_json = res.text
            res_json = etree.HTML(res_json)
            data_list = res_json.xpath("//div[@id='ProjectList']/a")
            for data in data_list:
                time.sleep(1)
                page_url = ''.join(data.xpath("./@href"))
                # page_url = 'https://nmgcqjy.ejy365.com' + page_url
                title_name = "".join(data.xpath("./span[1]/text()"))
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = "".join(data.xpath("./span[2]/text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)
                e_headers = {
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
                    # 'Cookie': 'SECKEY_ABVK=pVCx4qgwZHqZqA0X8E2YeAaT1GOz6GzBvC02fNGel5o%3D; BMAP_SECKEY=s8FlxG58qP9ZKAlckQkBoVk_sImOx7gpx65SQbadMURY7XCOqqNA7KNHFfuqKoNOVIhNFebnIDPesLO6Tes_XMWMSXGlBqHnhILK8uG-hEJQLdbmAxyyJdtkcDvxxj52XDJLhpkyaehF2HqHAaoHj3EJSHMZXI0HFwjO8htdR3yBbNFWFwYY4J1GtaHGiTph; cart=; Hm_lvt_575182d134dee4d26e03124da592d030=1740029607; HMACCOUNT=FDD970C8B3C27398; href=https%3A%2F%2Fwww.ejy365.com%2Finfo%2Fejy230259; _ga=GA1.1.1606555070.1740029608; hotlable=%5B%5D; qimoClientId=5878201740386650693; accessId=49a6c050-3b8b-11eb-a27b-59d93a528836; type=%E5%80%BA%E6%9D%83; area=%E5%B8%B8%E5%B7%9E; %E5%B8%B8%E5%B7%9E=1; Hm_lvt_7de38d8594a7cf1a574241f30c33446b=1740536797; Hm_lpvt_7de38d8594a7cf1a574241f30c33446b=1740536797; JSESSIONID=C557110B66CAFFF4BB03A36B196A83E1; _ga_ERPNN1LEDY=deleted; _ga_ERPNN1LEDY=deleted; %E6%88%BF%E5%9C%B0%E4%BA%A7=1; categoryname=%E5%80%BA%E6%9D%83; shiname=%E5%B7%B4%E5%BD%A6%E6%B7%96%E5%B0%94%E5%B8%82; %E5%80%BA%E6%9D%83=22; max_type_count=22; EJY-JSESSIONID=MWQzODUwMmYtYjdjZC00ZDdkLWI1OTMtNjdhMTkzM2Q1OGY5; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; sessionId=1d38502f-b7cd-4d7d-b593-67a1933d58f9; qimo_seosource_49a6c050-3b8b-11eb-a27b-59d93a528836=%E7%AB%99%E5%86%85; qimo_seokeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; qimo_xstKeywords_49a6c050-3b8b-11eb-a27b-59d93a528836=; _ga_ERPNN1LEDY=GS1.1.1740621016.15.1.1740623277.0.0.0; lljls=N0109ZQ240094%3B72fb5b9f1a2a463c84c4235c2e034497%3BN0111ZQ240048%3BN0124ZQ250002%3BN0117ZQ240141-2%3BN0124ZQ250009%3BZQZZCQ2020072803577%3BN0101ZQ240001%3BZQZZCQ2021020100912%3BZQZZCQ2020080603815%3BZQZZCQ2020080603814%3BZQZZCQ2020072803575%3B6b56f64b-32fb-45ff-be50-c7dd5bbfe785%3BN0117ZQ250006%3BN0117FC250054%3BN0131ZQ250004%3BN0109ZQ240093%3BN0109ZQ250004%3BN0109ZQ220071%3BN0109ZQ220062; uuid_49a6c050-3b8b-11eb-a27b-59d93a528836=acfb49dc-556a-45e6-a106-add526a8a2c4; Hm_lpvt_575182d134dee4d26e03124da592d030=1740623278; pageViewNum=110',
                }

                res = requests.get(page_url, headers=e_headers)
                html = res.text
                res_html = etree.HTML(html)
                time.sleep(2)
                iframes = res_html.xpath("//iframe/@src")

                print(iframes, type(iframes))
                for iframe in iframes:
                    if not iframe:
                        iframes.remove(str(iframe))
                if iframes:
                    res = requests.get(iframes[0], headers=e_headers)
                    iframe_html = res.text
                    iframe_html_etree = etree.HTML(iframe_html)
                    iframe_content = iframe_html_etree.xpath("//text()")


                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//div[@id='tab1_content']//text()"))
                    try:
                        title_content = title_content.join(iframe_content)
                    except:
                        pass

                    annex = res_html.xpath("//div[@id='tab1_content']//@href | //div[@id='tab1_content']//@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'https://nmgcqjy.ejy365.com' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.strip()
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "neimenggu", file_type)
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
                    # title_html_info = res_html.xpath("//div[@class='product fl']")
                    content_1 = res_html.xpath("//table[@id='table']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    content_html = re.sub(r'<!--第一位是竞买公告------------------------------.*</html>', '', content_html,  flags=re.DOTALL )
                    try:
                        content_html += '!@#' + iframe_html
                    except:
                        pass

                    try:
                        image = get_image(page, title_url, "xpath=//div[@id='tab1_content']")
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
        page.close()
        raise Exception(e)


# get_neimengguchanquanjiaoyi_zichanchaoshizhaiquan(111, 222)
# get_neimengguchanquanjiaoyi_guapaixiangmuzhaiquan(111, 222)
