from api_chief import judge_url_repeat
import hashlib
import json
import re
import time
from datetime import datetime

import mysql.connector
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import redis
from lxml import etree

# 连接redis数据库
redis_conn = redis.Redis()

co = ChromiumOptions()
co = co.set_paths(local_port=9120)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错


def get_xinwen_queue_url(zhao_type, num=None):
    page = ChromiumPage(co)
    page.get('http://qxzh.samr.gov.cn/qxzh/qxxxcx/web.jsp')
    # 等待页面加载完成
    page.wait.ele_displayed('.car_ul')
    if zhao_type == '汽车':
        page_html = etree.HTML(page.html)
        # 获取共有多少页
        page_num = page_html.xpath("//span[@class='totalPages']/span/text()")
        if num:
            page_num = num
        for i in range(1, int(page_num[0]) + 1):
            url_html = etree.HTML(page.html)
            all_url = url_html.xpath("//ul[@id='car_ul']/li/a")
            for url1 in all_url:
                url = ''.join(url1.xpath("./@href"))
                # 将获取到的url放到redis中的set集合
                redis_conn.rpush('canquechanpinzhaohui_car', url)
            page.ele("下一页", index=1).click(by_js=True)
            page.wait.ele_displayed('.car_ul')
    if zhao_type == '消费品':
        page.ele('缺陷消费品召回查询').click(by_js=True)
        page.wait.ele_displayed('.consume_ul')
        page_html = etree.HTML(page.html)
        page_num = page_html.xpath("//div[@id='consume_page']/span[@class='totalPages']/span/text()")
        for i in range(1, int(page_num[0]) + 1):
            url_html = etree.HTML(page.html)
            all_url = url_html.xpath("//ul[@id='consume_ul']/li/a")
            for url1 in all_url:
                url = ''.join(url1.xpath("./@href"))
                # 将获取到的url放到redis中的set集合
                redis_conn.rpush('canquechanpinzhaohui_xiaofei', url)
            page.ele("下一页", index=2).click(by_js=True)
            page.wait.ele_displayed('.car_ul')
    page.quit()


def get_gonggao_data(zhao_type):
    origin = '国家市场监督管理总局缺陷产品召回技术中心'
    if zhao_type == '汽车':
        url = 'https://www.samrdprc.org.cn/qczh/qczhgg1/'
    if zhao_type == '消费品':
        url = 'https://www.samrdprc.org.cn/xfpzh/xfpzhgg/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': '__jsluid_s=9b3541d3f25dce5832dccd993f39c22c; Hm_lvt_4a7eae9fd2d18b99a2593c5fce797578=1724401814,1724645064; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_4a7eae9fd2d18b99a2593c5fce797578=1724659871',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    url1 = url + 'index.html'
    res = requests.get(url1, headers=headers, verify=False)
    html = etree.HTML(res.content.decode())
    page_num = ''.join(html.xpath("//div[@class='page']//text()"))
    page_num = ''.join(re.findall(r'var countPage = (\d+)//共多少页', page_num))
    for i in range(1, int(page_num) + 1):
        if i == 1:
            new_url = url + 'index.html'
        else:
            new_url = url + f'index_{i - 1}.html'
        response = requests.get(new_url, headers=headers, verify=False)
        time.sleep(2)
        html = etree.HTML(response.content.decode())
        urls = html.xpath("//div[@class='boxl_ul']/ul/li/a")
        for url2 in urls:
            url2 = url + ''.join(url2.xpath("./@href")).strip('./')
            response2 = requests.get(url2, headers=headers, verify=False)
            time.sleep(2)
            html = etree.HTML(response2.content.decode())
            title = ''.join(html.xpath("//div[@class='show_tit']/h1/text()"))
            content = ''.join(html.xpath("//div[@class='table']/table/tbody//text()")).strip()
            if content == '':
                content = ''.join(html.xpath("//div[@class='TRS_Editor']/span//text()")).strip()
            if content == '':
                content = ''.join(html.xpath("//div[@class='TRS_Editor']/div/p//text()")).strip()
            if content == '':
                content = ''.join(html.xpath("//div[@class='TRS_Editor']/div/span/font//text()")).strip()
            con_html = html.xpath("//div[@class='table']")
            content_html = ''
            for con in con_html:
                content_html += etree.tostring(con, encoding='utf-8').decode()
            article_path = ''.join(html.xpath("//div[@class='local']//text()")).strip()
            pub_date = ''.join(html.xpath("//div[@class='show_tit2']//text()")).strip()
            # 使用re匹配xxxx-xx-xx年月日
            pub_date = re.findall(r'\d{4}-\d{2}-\d{2}', pub_date)[0]
            # # 附件
            # origin_annexs = html.xpath("//div[@class='show_txt']//a/@href")
            # if origin_annexs:
            #     pass
            source = ''.join(html.xpath("//div[@class='tita fl']/text()")).strip()
            origin_domain = 'https://www.samrdprc.org.cn/'
            uni_data = f'{str(title), str(content), str(pub_date), str(origin_domain)}'
            md5_key = hashlib.md5(json.dumps(uni_data).encode('utf-8')).hexdigest()
            create_date = datetime.now().strftime('%Y-%m-%d')
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database='col_test',
            )
            cursor_test = conn_test.cursor()
            if judge_url_repeat(url):
                insert_sql = "INSERT INTO col_chief_public (title,title_url, content,content_html, path,  source,pub_date, origin, origin_domain,create_date, MD5) VALUES (%s,%s, %s, %s,%s, %s, %s, %s, %s,%s,%s)"
                cursor_test.execute(insert_sql, (
                    title, url2, content, content_html, article_path,
                    source, pub_date,
                    origin, origin_domain, create_date, md5_key))

                conn_test.commit()
            cursor_test.close()
            conn_test.close()


def get_xinwen_data(db, queue_id, webpage_id, database="col_test", num_page=None):
    if redis_conn.llen(db) == 0 and db == 'canquechanpinzhaohui_car':
        get_xinwen_queue_url(zhao_type='汽车', num=num_page)
    if redis_conn.llen(db) == 0 and db == 'canquechanpinzhaohui_xiaofei':
        get_xinwen_queue_url(zhao_type='消费品', num=num_page)
    origin = '国家市场监督管理总局缺陷产品召回技术中心'
    while redis_conn.llen(db) != 0:
        url = redis_conn.lpop(db).decode()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': '__jsluid_s=9b3541d3f25dce5832dccd993f39c22c; Hm_lvt_4a7eae9fd2d18b99a2593c5fce797578=1724401814,1724645064; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_4a7eae9fd2d18b99a2593c5fce797578=1724645541',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        res = requests.get(url, headers=headers, verify=False)
        time.sleep(1)
        html = etree.HTML(res.content.decode())
        title = ''.join(html.xpath("//div[@class='show_tit']/h1/text()"))
        content = ''.join(html.xpath("//div[@class='TRS_Editor']/p/text()")).strip()
        if content == '':
            content = ''.join(html.xpath("//div[@class='TRS_Editor']/span//text()")).strip()
        if content == '':
            content = ''.join(html.xpath("//div[@class='TRS_Editor']/div/p//text()")).strip()
        if content == '':
            content = ''.join(html.xpath("//div[@class='TRS_Editor']/div/span/font//text()")).strip()
        con_html = html.xpath("//div[@class='TRS_Editor']")
        content_html = ''
        for con in con_html:
            content_html += etree.tostring(con, encoding='utf-8').decode()
        article_path = ''.join(html.xpath("//div[@class='local']//text()")).strip()
        pub_date = ''.join(html.xpath("//div[@class='show_tit2']//text()")).strip()
        # 使用re匹配xxxx-xx-xx年月日
        pub_date = re.findall(r'\d{4}-\d{2}-\d{2}', pub_date)[0]
        # # 附件
        # origin_annexs = html.xpath("//div[@class='show_txt']//a/@href")
        # if origin_annexs:
        #     pass
        source = ''.join(html.xpath("//div[@class='tita fl']/text()")).strip()
        origin_domain = 'https://www.samrdprc.org.cn/'
        uni_data = f'{str(title), str(content), str(pub_date), str(origin_domain)}'
        md5_key = hashlib.md5(json.dumps(uni_data).encode('utf-8')).hexdigest()
        create_date = datetime.now().strftime('%Y-%m-%d')
        conn_test = mysql.connector.connect(
            host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database=database
        )
        cursor_test = conn_test.cursor()
        if judge_url_repeat(url):
            insert_sql = "INSERT INTO col_chief_public (title,title_url, content,content_html, path,  source,pub_date, origin, origin_domain,create_date, md5_key, from_queue, webpage_id) VALUES (%s,%s, %s,%s,%s, %s,%s, %s, %s,%s, %s, %s,%s)"
            cursor_test.execute(insert_sql, (
                title, url, content, content_html, article_path,
                source, pub_date,
                origin, origin_domain, create_date, md5_key, queue_id, webpage_id,))

            conn_test.commit()
        cursor_test.close()
        conn_test.close()


def get_data():
    db_name = ['canquechanpinzhaohui_car', 'canquechanpinzhaohui_xiaofei']
    for db in db_name:
        get_xinwen_data(db, database="col_test")
