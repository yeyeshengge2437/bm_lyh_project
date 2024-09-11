import random
import time
from datetime import datetime

import mysql.connector
from lxml import etree
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from AMC.api_paper import judge_bm_repeat, upload_file, judge_title_repeat

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9124)




def get_image(page, url, element):
    tab = page.new_tab()
    tab.get(url)
    tab.wait.ele_displayed(element)
    time.sleep(2)
    value = tab.ele(element).rect.corners
    top_left = value[0]
    bottom_right = value[2]
    # 将top_left元组中的浮点数转换为整数
    top_left1 = (int(top_left[0]), int(top_left[1]))
    # 将bottom_right元组中的浮点数转换为整数
    bottom_right1 = (int(bottom_right[0]), int(bottom_right[1]))
    length = bottom_right1[1] - top_left1[1]
    if length < 16000:
        bytes_str = tab.get_screenshot(as_bytes='png', left_top=top_left1, right_bottom=bottom_right1)
    else:
        bottom_right1 = (int(bottom_right[0]), 8000)
        bytes_str = tab.get_screenshot(as_bytes='png', left_top=top_left1, right_bottom=bottom_right1)
    # 随机的整数
    random_int = random.randint(0, 1000000)
    with open(f'{random_int}.png', 'wb') as f:
        f.write(bytes_str)
    tab.close()
    return random_int


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.zyamc.net',
    'Pragma': 'no-cache',
    'Referer': 'https://www.zyamc.net/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'pageNum': 1,
    'pageSize': 1000,
    'newsType': 4,
}

def get_zhongyuanzichan_chuzhigonggao(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        response = requests.post('https://www.zyamc.net/api/portal/news/list', headers=headers, json=json_data)
        res_json = response.json()
        title_list = res_json["data"]["content"]
        img_set = set()
        page_url = 'https://www.zyamc.net/#/asset-zone/4'
        name = "中原资产管理有限公司"
        title_set = judge_title_repeat(name)
        for title in title_list:
            title_name = title["newsTitle"]
            title_date = title["dateIssued"]
            title_url = f"https://www.zyamc.net/#/detail/{title['newsId']}"
            if title_url not in title_set:
                title_url1 = f"https://www.zyamc.net/api/portal/news/{title['newsId']}"
                title_res = requests.get(title_url1, headers=headers)
                res_title_json = title_res.json()
                content_html = res_title_json["data"]["newsContent"]
                content_etree = etree.HTML(content_html)
                title_content = ''.join(content_etree.xpath('//text()')).strip()

                image = get_image(page, title_url, '.news-container')
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
                # print(bm_name, article_name, article_url, bm_pdf, content)
                if image not in img_set and judge_bm_repeat(name, title_url):
                    # 将报纸url上传
                    up_img = upload_file(image, "png", "paper")
                    img_set.add(image)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (title_date, name, title_name, up_img, title_url, up_img, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if title_url not in title_set:
                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (page_url, title_date, name, title_name, title_content, title_url, content_html,
                                         create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()
                    title_set.add(title_url)

                cursor_test.close()
                conn_test.close()
        page.close()
    except Exception as e:
        page.close()
        raise Exception(e)

# get_zhongyuanzichan_chuzhigonggao(111,222)
