import json
import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "中国石油报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}



def get_chinashiyou_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'http://epaper.cnpc.com.cn/zgsyb/{paper_time}/'
    url = base_url
    response = requests.get(url, headers=headers)
    pdf_set = set()
    if response.status_code == 200:
        content = response.content.decode('gbk')
        content = ''.join(re.findall(r'var epaperObject = (.*?);', content))
        try:
            content_json = json.loads(content)
        except:
            raise Exception(f'该日期没有报纸')
        page_v = content_json.keys()
        page_num = re.findall(r'page_\d+', str(page_v))
        for page in page_num:
            bm_name = content_json[page]["alias"]
            bm_url = base_url
            bm_img = base_url + 'res/' + content_json[page]["img_url"]
            bm_list = content_json[page]["data"]
            for bm in bm_list:
                article_url = base_url
                article_name = bm["title"]
                try:
                    content = bm["content"]
                    content_html = etree.HTML(content)
                    content = "".join(content_html.xpath("//p/text()"))
                except:
                    content = ''

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
                # print(bm_name, article_name, article_url, bm_img, content)
                if bm_img not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_img, paper, "jpg", "paper")
                    pdf_set.add(bm_img)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_img, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if judging_criteria(article_name, content):
                # if 1:

                    # print(content)
                    # return

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                cursor_test.close()
                conn_test.close()


            success_data = {
                'id': queue_id,
                'description': '数据获取成功',
            }
            paper_queue_success(success_data)

    else:
        raise Exception(f'该日期没有报纸')


# get_chinashiyou_paper('2024-01-02', 111, 1111)
