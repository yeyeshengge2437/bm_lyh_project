import os
import random
import time
from datetime import datetime

import mysql.connector
from lxml import etree
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

from api_paper import judge_bm_repeat, upload_file, judge_title_repeat, get_image
from bs4 import BeautifulSoup
import re


def remove_base64_src_attribute(html_content):
    """
    移除Base64图片的src属性，保留其他属性和标签
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    pattern = re.compile(r'^data:image/\w+;base64,')

    for img in soup.find_all('img', src=pattern):
        del img['src']  # 仅删除src属性

    return str(soup)

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9229)



headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.jxfamc.com/jxjrzc/zichanzhanshi/zczs.shtml',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



def get_jiangxizichan_zichanzhanshi(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    try:
        for page_num in range(1, 16 + 1):
            if page_num != 1:
                url = f'https://www.jxfamc.com/jxjrzc/zichanzhanshi/zczs/code_1_{page_num}.shtml'
            else:
                url = 'https://www.jxfamc.com/jxjrzc/zichanzhanshi/zczs/code_1.shtml'
            response = requests.get(url, headers=headers)
            res = response.content.decode()
            res_html = etree.HTML(res)
            title_list = res_html.xpath("//div[@class='item']/a[@class='title text-nowrap']")
            img_set = set()
            page_url = url
            name = "江西省金融资产管理股份有限公司_资产展示"
            title_set = judge_title_repeat(name)
            for title in title_list:
                title_name = ''.join(title.xpath("./text()"))
                title_date = ''
                title_url = ''.join(title.xpath("./@href"))
                # print(title_name, title_url)
                if title_url not in title_set:
                    title_id = ''.join(re.findall(r'\?id=(\d+)', title_url))
                    params = {
                        'assetId': f'{title_id}',
                    }
                    title_res = requests.get('https://www.jxjft.com/jxjk-server/jxjkpms/asset/getHtmlContent',
                                            params=params, headers=headers)
                    res_title_json = title_res.json()
                    content_html = res_title_json['result']['noticeHtmlContent']
                    content_tree = etree.HTML(content_html)
                    title_content = ''.join(content_tree.xpath("//text()"))
                    # print(title_content)

                    image = get_image(page, title_url, "xpath=//div[@class='bott']")
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
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
                                            (title_date, name, title_name, up_img, title_url, up_img, create_time, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                    else:
                        if os.path.exists(f'{image}.png'):
                            os.remove(f'{image}.png')

                    if title_url not in title_set:
                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_url, title_date, name, title_name, title_content, title_url, content_html,
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

# get_jiangxizichan_zichanzhanshi(111, 222)