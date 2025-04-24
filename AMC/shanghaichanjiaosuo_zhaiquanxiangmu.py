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
co.set_paths(local_port=9165)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219516e16e7b1616-0c64c8ddefd8ab8-26011b51-1296000-19516e16e7c1ed9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%7D%2C%22%24device_id%22%3A%2219516e16e7b1616-0c64c8ddefd8ab8-26011b51-1296000-19516e16e7c1ed9%22%7D; jwtStrToken=eyJhbGciOiJIUzUxMiJ9.eyJleHAiOjE3Mzk4NTI4NTksImlhdCI6MTczOTg0NTY1OX0.nPg4wHDb64zHhj72VZCL0AGp0s-Uahi0zXWT4_p_ZCcB6YsiYiq97B44fVnNdDfvskaoR4Qk_2seYymYckmy8w',
    'Origin': 'https://www.suaee.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.suaee.com/suaeeHome/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'projectType': 'suaeeHome',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sourcecode': 'SUAEE',
}


def get_shanghaichanjiangsuo_zhaiquanxiangmu(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    json_data = {
        'projectQtlx': 'ZHAIQUAN',
        'projectType': 'ZHAIQUAN',
        'isGw': True,
        'xmbh': '',
        'xmmc': '',
        'szdqs': '',
        'pageQuery': {
            'pageIndex': 1,
            'pageSize': 20,
        },
    }

    try:
        img_set = set()
        name = '上海联合产权交易所债权项目'
        title_set = judge_title_repeat(name)
        res = requests.post('https://www.suaee.com/manageprojectweb/foreign/project/queryAllNew',
                           headers=headers, json=json_data)
        res_json = res.json()
        data_list = res_json["data"]["data"]
        for data in data_list:
            page_url = data["xmurl"]
            title_url = page_url
            if title_url not in title_set:
                title_name = data["xmmc"]
                title_date_num = data["gpksrq"]
                title_date = str(datetime.fromtimestamp(title_date_num / 1000).strftime("%Y-%m-%d"))
                page.get(page_url)
                time.sleep(10)
                res = page.html
                res_html = etree.HTML(res)
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''

                # print(title_name,title_url)
                # return
                title_content = "".join(res_html.xpath(
                    "//div[@class='project_detail']//text()"))
                # 附件需要再此调用接口！！！！
                params_num = re.findall(r'xmid=(\d+)', title_url)[0]
                # print(title_url, params_num)
                params = {
                    'xmid': f'{params_num}',
                    'gplx': '',
                    'type': '',
                    'imgType': '',
                }

                response = requests.get(
                    'https://www.suaee.com/manageproject/foreign/creditorRights/getCreditorRightsAnnounceDetail',
                    params=params,
                    headers=headers,
                )
                res_json = response.json()
                files = []
                original_url = []
                fj_info_list = res_json["data"]["gsfj"]
                for fj_info in fj_info_list:
                    filename = fj_info["filename"]
                    file_type = filename.split('.')[-1]
                    filepath = fj_info["filepath"]
                    fj_url = f"https://www.suaee.com/manageserver/fileDow?type=2&filePath={filepath}&fileName={filename}"
                    file_url = upload_file_by_url(fj_url, "shanghaichanjiaosuo", file_type)
                    # file_url = 111
                    files.append(file_url)
                    original_url.append(fj_url)
                if not files:
                    files = ''
                    original_url = ''
                files = str(files).replace("'", '"')
                original_url = str(original_url).replace("'", '"')
                # title_html_info = res_title_html.xpath("//div[@class='news_info_box']")
                content_1 = res_html.xpath("//div[@class='project_detail']")
                content_html = ''
                # for con in title_html_info:
                #     content_html += etree.tostring(con, encoding='utf-8').decode()
                for con in content_1:
                    content_html += etree.tostring(con, encoding='utf-8').decode()
                try:
                    image = get_image(page, title_url,
                                      "xpath=//div[@class='project_detail']")
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
        try:
            page.quit()
        except:
            pass
    except Exception as e:
        try:
            page.quit()
        except:
            pass
        raise Exception(e)


# get_shanghaichanjiangsuo_zhaiquanxiangmu(111, 222)
