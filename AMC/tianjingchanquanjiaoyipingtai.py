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
co.set_paths(local_port=9206)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://trade.tpre.cn/finance-view/project-info/special-assets',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'SystemCode': 'FINANCE_WEB',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'uniflowSystemCode': 'INFORMATIONIZE',
}
headers_annex = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    # 'Referer': 'https://trade.tpre.cn/finance-view/project/formal-detail?id=bd498e1575e7168cd1b1a8dd4ce47234',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'SystemCode': 'FINANCE_WEB',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'uniflowSystemCode': 'INFORMATIONIZE',
}


def get_tianjingchanquanjiaoyipingtai(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for page_num in range(1, 70 + 1):
            params = {
                'propertyType': 'CREDITOR_RIGHTS',
                'type': '',
                'addressProvince': '',
                'addressCity': '',
                'sortord': '',
                'listingPriceBegin': '',
                'listingPriceEnd': '',
                'current': f'{page_num}',
                'size': '48',
                'projectCodeOrName': '',
                # '_unique': '1741173555926',
            }
            img_set = set()
            name = '天津产权交易平台'
            title_set = judge_title_repeat(name)

            res = requests.get('https://trade.tpre.cn/finance/biz/finance/project/anonymity/page', params=params,
                               headers=headers_annex)
            # print(res.text)
            res_json = res.json()
            data_list = res_json["data"]["records"]

            for data in data_list:
                time.sleep(1)
                type_ = data["type"]
                if type_ == 'FORMAL':
                    page_url = f'https://trade.tpre.cn/finance-view/project/formal-detail?id={data["pkId"]}'
                elif type_ == 'BUSINESS':
                    page_url = f'https://trade.tpre.cn/finance-view/project/attract?id={data["pkId"]}'
                else:
                    print(type_)
                    continue
                title_url = page_url
                if title_url not in title_set:
                    title_name = data["projectName"]
                    # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                    title_date = str(data["disclosureStartTime"])
                    # 20250212
                    # title_date = f"{title_date[:4]}-{title_date[4:6]}-{title_date[6:]}"
                    # 使用re模块提取日期
                    title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                    if title_date:
                        title_date = title_date[0]
                    else:
                        title_date = ''
                    # print(page_url, title_name, title_date)
                    annex_list = {}
                    params = {
                        'pkId': f'{data["pkId"]}',
                        # '_unique': '1744697742859',
                    }

                    response = requests.get(
                        'https://trade.tpre.cn/finance/biz/finance/formal/project-info-pkId/anmuas',
                        params=params,
                        headers=headers,
                    )
                    # print(response.json())
                    detail_json = response.json()
                    print(page_url)
                    print(f'https://trade.tpre.cn/finance/biz/finance/business/project-info/anmuas?pkId={data["pkId"]}')
                    print(detail_json)
                    try:
                        annex_img = detail_json["data"]["businessProjectDetailsVO"]["projectContent"]
                        # print(annex_img)
                    except:
                        annex_img = ''
                    if annex_img:
                        annex_img_html = etree.HTML(annex_img)
                        annex_img_list = annex_img_html.xpath("//img/@src")
                        # print(annex_img_list)
                        for annex_img_url in annex_img_list:
                            # \"/tpre-process-biz-rest/attachment/api/download/original-drawing/970ffa69-eb37-4b85-8317-2ffe4f784e68\"
                            # https://trade.tpre.cn/tpre-process-biz-rest/attachment/api/download/original-drawing/970ffa69-eb37-4b85-8317-2ffe4f784e68
                            # https://trade.tpre.cn/tpre-process-biz-rest/attachment/api/download/original-drawing/970ffa69-eb37-4b85-8317-2ffe4f784e68
                            annex_img_url = annex_img_url.replace('\"', '')
                            annex_img_url = annex_img_url.replace('\"', '')
                            annex_img_url = "https:/" + annex_img_url
                            annex_list[annex_img_url] = 'png'
                    try:
                        try:
                            annex_files = detail_json["data"]["businessProjectDetailsVO"]["attachmentTypeRelationVOList"][1]["attachmentList"]
                        except:
                            annex_files = detail_json["data"]["attachmentTypeRelationVOList"][4]["attachmentList"]
                    except Exception as e:
                        print('错误是', e)
                        annex_files = []
                    if annex_files:
                        for annex_file in annex_files:
                            annex_file_type = annex_file["attachmentSuffix"]
                            annex_file_url = 'https://trade.tpre.cn/tpre-process-biz-rest/attachment/api/download/anmuas/' + \
                                             annex_file["attachmentSource"]
                            # print(annex_file_type, annex_file_url)
                            annex_list[annex_file_url] = annex_file_type
                    print(annex_list)
                    # print(annex_list)
                    # return
                    page.get(page_url)
                    page.scroll.to_bottom()
                    time.sleep(3)
                    res_html = etree.HTML(page.html)
                    # title_list = res_html.xpath("//div[@class='rightListContent list-item']")


                    title_content = "".join(res_html.xpath("//div[@class='detail-wrap']//text()"))

                    # annex = res_html.xpath("//div[@class='detail-wrap']//@href | //div[@class='detail-wrap']//@src")
                    if annex_list:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann_url, ann_type in annex_list.items():
                            if not ann_url:
                                continue
                            # if "http" not in ann:
                            #     ann = 'https://jst.coamc.com.cn' + ann
                            file_type = ann_type
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg']:
                                file_url = upload_file_by_url(ann_url, "tianjing", file_type)
                                # file_url = 111
                                files.append(file_url)
                                original_url.append(ann_url)
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
                    content_1 = res_html.xpath("//div[@class='detail-wrap']")
                    content_html = ""
                    # print(content_html)
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    # content_html += transfer_info
                    # print(content_html)
                    # return
                    # https://trade.tpre.cn/finance-view/project/attract?id=924fec529df2e68d81e717324101f75b
                    # https://trade.tpre.cn/finance-view/project/formal-detail?id=924fec529df2e68d81e717324101f75b
                    try:
                        # //div[@id='text-container']
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='project-detail-web']/div[@class='detail-wrap'] | //div/div[@class='detail-wrap']")
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
                    if judge_bm_repeat(name, title_url):
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


# get_tianjingchanquanjiaoyipingtai(111, 222)
