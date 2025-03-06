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

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9188)

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.sotcbb.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.sotcbb.com/xmgg?id=xmggjrzczrzspl',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_f77f76774e4072f82fa9bd84dc8788fd=1739963567,1740035618; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_014a81f17d0f563e80b3dc58463ea8dc=1739963567,1740035618; Hm_lpvt_014a81f17d0f563e80b3dc58463ea8dc=1740711017; Hm_lpvt_f77f76774e4072f82fa9bd84dc8788fd=1740711017; SECKEY_ABVK=pVCx4qgwZHqZqA0X8E2YeGMsal3cCRwn0mn2rKepECI%3D; BMAP_SECKEY=s8FlxG58qP9ZKAlckQkBoeqpuHQH4nwfz-W3zEz20Ptlbel6s60VbGqua4PCYoTsL3NoX-ggILlUTocQCC4yShm40xdNnmFP66LBGwKiWy4o0QmRjQovPhr-Ep8dNmcUzkhEkUbcfs0Wm8iYPKfhaxRsL3Hfbr7aRkScXf7q-PwU23kZWGN1qy92edDJ6rDD',
}


def get_shenzhenlianhechanquanjiaoyisuo(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    # cookie_dict = {}
    # page.get("https://www.cspea.com.cn")
    # time.sleep(3)
    # page.refresh()
    # value_cookies = page.cookies()
    # for key in value_cookies:
    #     cookie_dict[key['name']] = key['value']

    try:
        # for zq_type in ['C05', 'C06']:
        for page_num in range(1, 6):
            json_data = {
                'channelIds': [
                    '3230',
                ],
                'projectMoneyRanges': [],
                'projectSubjections': [],
                'projectSources': [],
                'projectStatus': None,
                'releaseTimeBegin': None,
                'releaseTimeEnd': None,
                'title': None,
                'pageNum': page_num,
                'pageSize': 100,
                'dataType': 1,
                'targetColumnIds': [
                    '3965',
                ],
            }

            img_set = set()
            name = '深圳联合产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.post(
                'https://www.sotcbb.com/api/v1/sotcbb/local/project/list',
                headers=headers,
                json=json_data,
            )
            # print(res.text)
            res_json = res.json()
            # print(res_json)
            data_list = res_json["data"]["content"]

            for data in data_list:
                time.sleep(1)
                # print(data)
                try:
                    page_url = f'https://www.sotcbb.com/bdDetail.htm?contentId={data["objectId"]}&channelId=3230&id={data["contentId"]}'
                except:
                    continue
                title_name = data["title"]
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = data["registerFrom"]
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                print(page_url, title_name, title_date)
                params = {
                    'projectId': f'{data["projectNo"]}',
                    'contentId': f'{data["contentId"]}',
                }
                res_1 = requests.get(
                    'https://www.sotcbb.com/api/v1/sotcbb/local/project/projectNo/detail',
                    params=params,
                    headers=headers,
                )
                time.sleep(2)
                res_1 = res_1.json()
                try:
                    res_html_1 = res_1["data"]["content"]
                except:
                    continue
                res_html = etree.HTML(res_html_1)
                title_url = page_url
                if title_url not in title_set:
                    title_content = "".join(res_html.xpath("//text()"))

                    annex = res_html.xpath("//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'https://file.szggzy.com' + ann
                            try:
                                # https://file.szggzy.com/tradeapi/file/gd-file/unified_download?fileId=ff8080819112f5860191b22cd9f37c8a&attname=%E6%A0%87%E7%9A%84%E8%B5%84%E4%BA%A7%E6%B8%85%E5%8D%95.pdf&isOutNet=true
                                file_type = ann.split('.')[-1]
                                try:
                                    file_type = file_type.split('&')[0]
                                except:
                                    continue
                            except:
                                continue
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'unified_download' in ann:
                                file_url = upload_file_by_url(ann, "shenzhen", file_type)
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
                    content_html = res_html_1
                    # for con in title_html_info:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    # for con in content_1:
                    #     content_html += etree.tostring(con, encoding='utf-8').decode()
                    # print(content_html)
                    # return
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='vab-main_content']")
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
                    try:
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
                    except Exception as e:
                        continue
                    cursor_test.close()
                    conn_test.close()
            page.close()
    except Exception as e:
        page.close()
        raise Exception(e)


# get_shenzhenlianhechanquanjiaoyisuo(111, 222)
