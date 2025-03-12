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
co.set_paths(local_port=9190)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    # 'Cookie': 'JSESSIONID=49B045CF0B2DF12E9630B8A885E54C26; Hm_lvt_6eda7fc02dd514d4aa276037c947668f=1739963032,1740040980; HWWAFSESID=629717395942b88b17; HWWAFSESTIME=1741223999066; Hm_lvt_865d7b41bbb886391b9a558ea304692d=1739963069,1740990818,1741224051; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_865d7b41bbb886391b9a558ea304692d=1741227792',
}


def get_guangzhouchanquanjiaoyisuo(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        # for zq_type in ['C05', 'C06']:
        for page_num in range(1, 76):
            params = {
                'to': 'cmsUtrSearchAll',
                'pageIndex': f'{page_num}',
                'sysEname': 'MGZL',
                'queryKey': '债权',
            }

            img_set = set()
            name = '广州产权交易所'
            title_set = judge_title_repeat(name)

            res = requests.get('http://gz.gemas.com.cn/portal/page', params=params,headers=headers, verify=False)
            # print(res.text)
            res_json = res.text
            res_html = etree.HTML(res_json)
            data_list = res_html.xpath("//table[@class='table']/tbody/tr")


            for data in data_list:
                time.sleep(1)
                # print(data)
                page_url = ''.join(data.xpath(".//@href"))
                if not page_url:
                    continue
                elif 'portal/page' not in page_url or 'seId' in page_url:
                    continue
                title_name = ''.join(data.xpath(".//a//text()"))
                # import datetime; print(datetime.datetime.utcfromtimestamp(1740326400000 // 1000).strftime('%Y-%m-%d'))
                title_date = ''.join(data.xpath("./td[4]//text()"))
                # 使用re模块提取日期
                title_date = re.findall(r'\d{4}-\d{1,2}-\d{2}', title_date)
                if title_date:
                    title_date = title_date[0]
                else:
                    title_date = ''
                # print(page_url, title_name, title_date)
                page.get(page_url)
                time.sleep(2)
                page_html = page.html
                if '该项目已归档' in page_html:
                    continue
                # http://gz.gemas.com.cn/portal/page?to=proUtrm&proId=eb0f12d1170f44ab88b17e51d8e268fb&packId=
                pro_id = ''.join(re.findall(r'&proId=(.*?)&p', page_url))
                # print(pro_id)
                flag = True
                if 'proUtrm' in page_url:
                    flag = False
                    res_html_ = ''
                    params = {
                        'to': 'proUtrmDetail',
                        'sortCode': 'sw_zq',
                        'infoId': f'{pro_id}',
                        'proId': f'{pro_id}',
                        'packId': '',
                    }
                    target_res = requests.post('http://gz.gemas.com.cn/portal/page', params=params, headers=headers, verify=False)
                    target_html = target_res.text
                    # print(target_html)
                    # target_etree = etree.HTML(target_html)
                    res_html_ += target_html

                    params = {
                        'to': 'proUtrmpub',
                        'proId': f'{pro_id}',
                        'packId': '',
                        # 'bailPrice': '120000000',
                    }

                    trade_res = requests.post('http://gz.gemas.com.cn/portal/page', params=params, headers=headers,
                                             verify=False)
                    trade_html = trade_res.text
                    # trade_etree = etree.HTML(trade_html)
                    res_html_ += trade_html

                    params = {
                        'to': 'proAtta',
                        'proId': f'{pro_id}',
                        'packId': '',
                    }

                    ann_res = requests.post('http://gz.gemas.com.cn/portal/page', params=params,
                                             headers=headers, verify=False)
                    ann_html = ann_res.text
                    # ann_etree = etree.HTML(ann_html)
                    # print(ann_html)
                    res_html_ += ann_html
                else:
                    params = {
                        'to': 'proUtrg',
                        'proId': f'{pro_id}',
                    }

                    response = requests.get('http://gz.gemas.com.cn/portal/page', params=params, headers=headers,
                                            verify=False)
                    res_html_ = response.text
                res_html = etree.HTML(res_html_)
                title_url = page_url
                if title_url not in title_set:
                    if flag:
                        title_content = "".join(res_html.xpath("//div[@id='dePage']/table//text()"))
                        annex = res_html.xpath("//div[@id='dePage']/table//@href | //div[@id='dePage']/table//@src")
                    else:
                        title_content = "".join(res_html.xpath("//text()"))
                        annex = res_html.xpath("//@href | //@src")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if not ann:
                                continue
                            if "http" not in ann:
                                ann = 'https://www.gduaee.com' + ann
                            file_type = ann.split('.')[-1]
                            file_type = file_type.strip()
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "guangzhou", file_type)
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
                    content_html = ""
                    if flag:
                        content_1 = res_html.xpath("//div[@id='dePage']/table")

                        # print(content_html)
                        # for con in title_html_info:
                        #     content_html += etree.tostring(con, encoding='utf-8').decode()
                        for con in content_1:
                            content_html += etree.tostring(con, encoding='utf-8').decode()
                    else:
                        content_html += res_html_
                    # print(content_html)
                    # return
                    try:
                        # //div[@id='text-container']
                        image = get_image(page, title_url,
                                          "xpath=//div[@id='tabcontent'] | //div[@id='czlc']//div[@id='dePage']/table")
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


# get_guangzhouchanquanjiaoyisuo(111, 222)
