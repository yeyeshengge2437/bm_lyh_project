import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co = co.set_paths(local_port=9250)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错


def get_paper_url_cookies(url):
    cookie_dict = {}
    page = ChromiumPage(co)
    page.get(url)
    value_cookies = page.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    page.close()
    return cookie_dict


paper = "潇湘晨报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}


def get_xiaoxiangchen_paper_new(paper_time, queue_id, webpage_id):
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'http://epaper.xxcb.cn/XXCBA/html/{paper_time}/'
    url = base_url + 'node_106.htm'
    page = ChromiumPage()
    tab_main = page.new_tab()
    tab_main.get(url)
    bm_eles = tab_main.eles("xpath=//div[@id='xbc_01']/ul/li/table/tbody/tr")
    pdf_set = set()
    for bm_ele in bm_eles:
        bm_name = bm_ele.text
        bm_url = bm_ele.ele("xpath=//td//a").attr('href')
        bm_url = re.sub(r'http://epaper\.xxcb\.cn/', '', bm_url)
        bm_url = base_url + bm_url
        pdf_url = bm_ele.ele("xpath=//td[2]//a").attr('href')
        pdf_url = re.sub(r'http://epaper\.xxcb\.cn/', '', pdf_url)
        bm_pdf = 'http://epaper.xxcb.cn/xxcba/' + pdf_url
        # print(bm_name, bm_url, pdf_url)
        tab = page.new_tab()
        tab.get(bm_url)

        article_eles = tab.eles("xpath=//div[@class='nav_con']//ul/li/a")
        tab_main_id = tab.tab_id
        for article_ele in article_eles:
            article_name = article_ele.text
            article_url = article_ele.attr('href')
            # print(article_url, article_name)
            tab_new = article_ele.click.for_new_tab(by_js=True)
            try:
                content = tab_new.ele('xpath=//*[@id="neir"]')
                content = content.text.strip('上一篇  下一篇  关闭本页').strip('下一篇  关闭本页').strip(
                    '上一篇  关闭本页')
            except:
                content = ''
            now_tab_id = tab_new.tab_id
            # print(content)
            page.get_tab(tab_main_id)
            page.close_tabs(now_tab_id)

            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            create_date = datetime.now().strftime('%Y-%m-%d')
            # 上传到测试数据库
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col",
            )
            cursor_test = conn_test.cursor()
            # print(bm_name, bm_url, pdf_url, article_name, article_url, content)
            if bm_pdf not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                # 将报纸url上传
                up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                pdf_set.add(bm_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                     create_date, webpage_id))
                conn_test.commit()

            if judging_criteria(article_name, content):
                # 上传到报纸的内容
                insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                     create_date, webpage_id))
                conn_test.commit()

            cursor_test.close()
            conn_test.close()

    tab_main.close()
    page.close()


def get_xiaoxiangchen_paper_old(paper_time, queue_id, webpage_id):
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'http://epaper.xxcb.cn/XXCBA/html/{paper_time}/'
    url = base_url + 'node_106.htm'
    page = ChromiumPage()
    tab_main = page.new_tab()
    tab_main.get(url)
    bm_eles = tab_main.eles("xpath=//div[@id='xbc_01']/ul/li/table/tbody/tr")
    pdf_set = set()
    for bm_ele in bm_eles:
        bm_name = bm_ele.text
        bm_url = bm_ele.ele("xpath=//td//a").attr('href')
        bm_url = re.sub(r'http://epaper\.xxcb\.cn/', '', bm_url)
        bm_url = base_url + bm_url
        pdf_url = bm_ele.ele("xpath=//td[2]//a").attr('href')
        pdf_url = re.sub(r'http://epaper\.xxcb\.cn/', '', pdf_url)
        bm_pdf = 'http://epaper.xxcb.cn/XXCBA/' + pdf_url
        # print(bm_name, bm_url, pdf_url)
        # print(bm_url, 11111111111111111)
        tab = page.new_tab()
        tab.get(bm_url)

        article_eles = tab.eles("xpath=//td/div/table//td[@class='default'][2]/a")
        tab_main_id = tab.tab_id
        for article_ele in article_eles:
            article_name = article_ele.text
            article_url = article_ele.attr('href')
            article_url = re.sub(r'http://epaper\.xxcb\.cn/', '', article_url)
            article_url = base_url + article_url
            # print(article_url, article_name)
            tab_new = article_ele.click.for_new_tab(by_js=True)
            try:
                content = tab_new.ele("xpath=//div[@id='ozoom']")
                content = content.text
            except:
                content = ''
            now_tab_id = tab_new.tab_id
            # print(content)
            page.get_tab(tab_main_id)
            page.close_tabs(now_tab_id)

            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            create_date = datetime.now().strftime('%Y-%m-%d')
            # 上传到测试数据库
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col",
            )
            cursor_test = conn_test.cursor()
            # print(bm_name, bm_url, bm_pdf, article_name, article_url, content)
            if bm_pdf not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                # 将报纸url上传
                up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                pdf_set.add(bm_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                     create_date, webpage_id))
                conn_test.commit()

            if judging_criteria(article_name, content):
                # 上传到报纸的内容
                insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                     create_date, webpage_id))
                conn_test.commit()

            cursor_test.close()
            conn_test.close()

    tab_main.close()
    page.close()


def get_xiaoxiangchen_paper(paper_time, queue_id, webpage_id):
    paper_time1 = datetime.strptime(paper_time, '%Y-%m-%d').date()
    date_str = '2011-08-07'

    # 将字符串转换为日期对象
    date_str = datetime.strptime(date_str, '%Y-%m-%d').date()

    # 判断日期是否在范围内
    if paper_time1 <= date_str:
        # print('使用旧方法')
        get_xiaoxiangchen_paper_old(paper_time, queue_id, webpage_id)
    else:
        # print('使用新方法')
        get_xiaoxiangchen_paper_new(paper_time, queue_id, webpage_id)


# get_xiaoxiangchen_paper('2009-11-17', 111, 1111)
# get_xiaoxiangcheng_paper_old('2009-11-17', 111, 1111)
