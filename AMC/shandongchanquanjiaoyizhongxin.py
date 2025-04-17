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
co.set_paths(local_port=9176)

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://www.sdcqjy.com',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_shandongchanquanjiaoyizhongxin(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for page_num in range(35):
            time.sleep(2)
            data = {
                'page': f'{page_num}',
                'type': 'all',
                'keyword': '债权',
            }
            img_set = set()
            name = '山东产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.post('http://www.sdcqjy.com/search/getdata', headers=headers, data=data, verify=False)
            res_json = res.text
            html = etree.HTML(res_json)
            # print(res_json)
            data_list = html.xpath("//table[@class='table-all']/tbody/tr")
            for data in data_list:
                time.sleep(1)
                link_info = ''.join(data.xpath(".//a[@class='name']/@onclick"))
                link_json = re.findall(r'linkToDetail\((.*?)\)', link_info)
                if not link_json:
                    continue
                link_json = json.loads(link_json[0])
                data_status = link_json['dataStatus']
                link_id = link_json['id']
                if data_status == '已发布':
                    page_url = f"http://www.sdcqjy.com/zccz/article/cjgg/{link_id}"
                elif data_status == '挂牌公告':
                    continue
                elif data_status == '--':
                    page_url = f"http://www.sdcqjy.com/bidding/bidprice/{link_id}"
                elif data_status == '招商':
                    page_url = f"http://www.sdcqjy.com/proj/yqcl/{link_id}"
                else:
                    page_url = f"http://www.sdcqjy.com/proj/tc/{link_id}"
                title_url = page_url
                if title_url not in title_set:
                    title_name = link_json['name']
                    # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                    title_date = link_json['publishTime']
                    # 使用re模块提取日期
                    title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                    if title_date:
                        title_date = title_date[0]
                    else:
                        title_date = ''
                    print(page_url, title_name, title_date, data_status)
                    # https://hljcqjy.ejy365.com/ejy/detail?infoId=N0129GQ240059&bmStatus=%E6%8A%A5%E5%90%8D%E6%88%AA%E6%AD%A2&ggType=JYGG

                    res = requests.get(page_url, headers=headers)
                    res_html = etree.HTML(res.text)
                    time.sleep(2)
                    # title_list = res_html.xpath("//div[@class='rightListContent list-item']")

                    title_content = "".join(res_html.xpath("//div[@class='pro_title_main']//text()"))
                    title_content = title_content.join(res_html.xpath("//div[@class='module-item']//text()"))
                    title_content = title_content.join(res_html.xpath("//div[@class='art_cont']//text()"))
                    annex = res_html.xpath("//div[@id='biddingPageCont']//@href | //div[@class='module-item']//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'http://www.e-jy.com.cn/' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.strip()
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'noauthorizefiles' in ann:
                                file_url = upload_file_by_url(ann, "shandong", file_type)
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
                    title_html_info = res_html.xpath("//div[@class='pro_title_main'] | //div[@class='art_cont'] | //div[@class='module-item']")
                    content_1 = res_html.xpath("//div[@id='biddingPageCont']")
                    content_html = ''
                    for con in title_html_info:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    if not title_content:
                        cont_ = etree.HTML(content_html)
                        if cont_:
                            title_content = ''.join(cont_.xpath("//text()"))
                    # print(title_content)
                    try:
                        image = get_image(page, title_url, "xpath=//div[@class='main_container'] | //div[@class='art_cont']")
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


# get_shandongchanquanjiaoyizhongxin(111, 222)
