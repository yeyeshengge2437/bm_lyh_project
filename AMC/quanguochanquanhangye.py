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
# co = co.set_argument('--no-sandbox')
# co = co.headless()
# co.set_paths(local_port=9169)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.cspea.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.cspea.com.cn/list?c=C05&s=A02,A03',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'Hm_lvt_8f877769194d47e9189ceb9767485623=1740043699; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_8f877769194d47e9189ceb9767485623=1740381634; JSESSIONID=PqYd3oT-n4GBAIiMvBol3VPebHahtMp0uH15seT8; UMKEY=PqYd3oT-n4GBAIiMvBol3VPebHahtMp0uH15seT8; CSPEA_AUTHKEY=15938554242; CSPEA_USER=%7B%22insCode%22:null,%22org%22:null,%22wechatCount%22:0,%22memberLevel%22:null,%22mobile%22:%2215938554242%22,%22industry%22:null,%22qqNumber%22:null,%22userName%22:%2215938554242%22,%22experience%22:null,%22userId%22:%2236fa538716354f289fbba42e31dd56b4%22,%22groupNumber%22:%220%22,%22memberExpiryDate%22:null,%22realName%22:null,%22userState%22:%220%22,%22phone%22:null,%22position%22:null,%22department%22:null,%22email%22:null%7D; ray_leech_token=1740380897',
}


def get_quanguochanquanhangye_zhaiquan(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    cookie_dict = {}
    page.get("https://www.cspea.com.cn")
    time.sleep(3)
    page.refresh()
    value_cookies = page.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']

    try:
        # for zq_type in ['C05', 'C06']:
        for zq_type in ['C06']:
            params = {
                'projectClassifyCode': f'{zq_type}',
                'businessStatus': 'A02,A03',
                'sortVal': 'publishDate',
                'sortRule': 'desc',
                'pageNum': '1',
                'pageSize': '200',
            }

            img_set = set()
            name = '全国产权行业信息化综合服务平台'
            title_set = judge_title_repeat(name)

            res = requests.post('https://www.cspea.com.cn/esApi/searchIndex', cookies=cookie_dict, headers=headers, data=params)
            # print(res.text)
            res_json = res.json()
            # print(res_json)
            data_list = res_json["entity"]["datas"]

            for data in data_list:
                time.sleep(1)
                # print(data)
                try:
                    page_url = data["projectCode"]
                except:
                    continue
                # https://www.cspea.com.cn/list/c02/G32024CQ1000223
                page_url = 'https://www.cspea.com.cn/list/c02/' + page_url
                title_name = data["projectText"]
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = int(data['publishDate'])
                title_date = datetime.utcfromtimestamp(title_date // 1000).strftime('%Y-%m-%d')
                title_url = page_url
                if title_url not in title_set:
                    print(page_url, title_name, title_date)
                    page.get(page_url)
                    time.sleep(4)
                    page.refresh()
                    res = page.html
                    res_html = etree.HTML(res)
                    # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                    # # 使用re模块提取日期
                    # title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                    # if title_date:
                    #     title_date = title_date[0]
                    # else:
                    #     title_date = ''

                    title_content = "".join(res_html.xpath("//div[@class='project-detail-left']//text()"))

                    annex = res_html.xpath("//div[@class='table-detail-info']/div[2]/table[5]/tbody/tr//a//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'https://files.cquae.com/' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'editorUpload' in ann:
                                file_url = upload_file_by_url(ann, "Upload", file_type)
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
                    # title_html_info = res_title_html.xpath("//div[@class='news_info_box']")
                    content_1 = res_html.xpath("//div[@class='project-detail-left']")
                    content_html = ''
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='project-detail-left']")
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


# get_quanguochanquanhangye_zhaiquan(111, 222)
