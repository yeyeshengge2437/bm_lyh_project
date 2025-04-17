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
co.set_paths(local_port=9171)

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.xemas.com.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.xemas.com.cn/project-announcement.html?parent-uid=&self-uid=&type=total&sub-uid=',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'shiro-pm-YSSessionCache=2b41f572-ecb6-4d19-accc-c489231bc548',
}


def get_xiamenchanquanjiaoyizhongxin(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            params = {
                'size': '40',
                'page': '1',
                'getData': 'true',
                'getResource': 'true',
            }

            json_data = {
                'title': '债权',
            }

            img_set = set()
            name = '厦门产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.post('https://www.xemas.com.cn/cms/article/query',
                                params=params,
                                headers=headers,
                                json=json_data,
                                )
            # print(res.text)
            res_json = res.json()
            data_list = res_json["body"]["content"]

            for data in data_list:
                time.sleep(1)
                page_url = data["uid"]
                category_uid = data['categoryUid']
                # https://www.xemas.com.cn/project-announcement-details-newtwo.html?uid=7b52ae3f-9989-40d7-9775-93c2e43e4a72
                flag = data["categoryName"]
                print(flag)
                if flag == '成交公告':
                    page_url = 'https://www.xemas.com.cn/project-announcement-details-new.html?uid=' + page_url
                elif flag == '产权交易决策及批准信息':
                    page_url = 'https://www.xemas.com.cn/content-detail.html?parent-uid=' + category_uid
                # https://www.xemas.com.cn/content-detail.html?parent-uid=c3e7d3c5-5483-495a-9024-bcaecda17af7
                # https://www.xemas.com.cn/content-detail.html?parent-uid=c3e7d3c5-5483-495a-9024-bcaecda17af7
                else:
                    page_url = 'https://www.xemas.com.cn/project-announcement-details-newtwo.html?uid=' + page_url
                title_name = data["title"]
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = data['created']
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)
                res = data["userdefine7"]
                if not res:
                    continue
                res_html = etree.HTML(res)
                title_url = page_url
                if title_url not in title_set:
                    title_content = ''.join(res_html.xpath(".//text()"))

                    annex = res_html.xpath("//td[@id='download']/a//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'http://portal.xemas.com.cn/' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "xiamen", file_type)
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
                    # print(files, original_url)
                    # title_html_info = res_title_html.xpath("//div[@class='news_info_box']")
                    # content_1 = res_html.xpath("//div[@class='project-detail-left']")
                    content_html = res
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    # for con in content_1:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@id='notice-form']")
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


# get_xiamenchanquanjiaoyizhongxin(111, 222)
