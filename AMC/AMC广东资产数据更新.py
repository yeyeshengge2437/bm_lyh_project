# 131
import os
import re

import mysql.connector
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import etree
from AMC.api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, paper_queue_next, \
    paper_queue_success

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASP.NET_SessionId=o3lcjpumzjmshqghd5kx013x',
    'Pragma': 'no-cache',
    'Referer': 'https://www.utrustamc.com/czgg/list.aspx?page=2',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def guangdong_gai(queue_id, webpage_id):
    conn_test_1 = mysql.connector.connect(
        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col"
    )

    cursor_test_1 = conn_test_1.cursor()
    cursor_test_1.execute(
        "select id, page_url, update_time from col_paper_notice where paper = '广东粤财资产管理有限公司'")
    rows = cursor_test_1.fetchall()
    for id, page_url, update_time in rows:
        if '18282' in page_url:
            continue
        if update_time:
            continue
        title_url = page_url
        print(title_url)
        # print(title_name,title_date,title_url)
        res_title = requests.get(title_url, headers=headers)
        time.sleep(1)
        res_title_html1 = res_title.content.decode()
        res_title_html = etree.HTML(res_title_html1)
        title_content = "".join(res_title_html.xpath("//div[@class='NewsInfo']/article//text()"))
        title_html_info = res_title_html.xpath("//div[@class='TitleInfo']")
        content_1 = res_title_html.xpath("//div[@class='NewsInfo']/article")
        content_html = ''
        for con in title_html_info:
            content_html += etree.tostring(con, encoding='utf-8').decode()
        for con in content_1:
            content_html += etree.tostring(con, encoding='utf-8').decode()
        detail_url = res_title_html.xpath("//div[@class='info_pro']//a/@href")
        for det_url in detail_url:
            if 'Assetinquiry' not in det_url:
                continue
            det_url = "https://www.utrustamc.com" + det_url
            res_det = requests.get(det_url, headers=headers)
            time.sleep(2)
            res_det_html = res_det.content.decode()
            res_det_html = etree.HTML(res_det_html)
            det_html_info = "".join(res_det_html.xpath("//div[@class='SearchDetail']//text()"))
            title_content += det_html_info
            det_html = res_det_html.xpath("//div[@class='SearchDetail']")
            det_content = ''
            for det in det_html:
                det_content += etree.tostring(det, encoding='utf-8').decode()
            content_html += det_content

        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 上传到测试数据库
        conn_test = mysql.connector.connect(
            host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database="col",
        )
        cursor_test = conn_test.cursor()
        print(queue_id, update_time, id)
        insert_sql = "UPDATE col_paper_page SET from_queue=%s, update_time=%s WHERE id = %s"
        cursor_test.execute(insert_sql, (queue_id, update_time, id))
        conn_test.commit()

        insert_sql = "UPDATE col_paper_notice SET from_queue=%s, update_time=%s, content=%s, content_html=%s WHERE id = %s"
        cursor_test.execute(insert_sql, (queue_id, update_time, title_content, content_html, id))
        conn_test.commit()

        cursor_test.close()
        conn_test.close()

    cursor_test_1.close()
    conn_test_1.close()


# guangdong_gai(111, 222)

paper_queue = paper_queue_next(webpage_url_list=['https://www.utrustamc.com/czgg/list.aspx#SubMenu'])
queue_id = paper_queue['id']
webpage_id = paper_queue["webpage_id"]
print(queue_id, webpage_id)
guangdong_gai(queue_id, webpage_id)
data = {
    "id": queue_id,
    'description': f'数据获取成功',
}
paper_queue_success(data=data)
# 1752755 16472
# https://www.utrustamc.com/czgg/info.aspx?itemid=18282
