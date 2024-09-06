import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree



paper = "辽沈晚报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_77002c6b9fe15a5136bbe06f933886b8=1724036433; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_77002c6b9fe15a5136bbe06f933886b8=1724036814',
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

today = datetime.now().strftime('%Y-%m-%d')


# today = '202401/11'


def get_liaoshen_lastpaper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m/%d')
    base_url = f'https://epaper.lnd.com.cn/lswbepaper/pc/layout/{paper_time}/'
    url = base_url + 'node_A01.html'
    response = requests.get(url, headers=headers, verify=False)
    time.sleep(2)
    if response.status_code == 200:
        data = response.content.decode()
        bm_html = etree.HTML(data)
        bm_list = bm_html.xpath("//div[@class='Chunkiconbox']/div[@class='Chunkiconlist']/p")
        for bm in bm_list:
            # 获取版面名称
            bm_name = ''.join(bm.xpath("./a[1]/text()"))
            # 获取版面链接
            bm_url = base_url + ''.join(bm.xpath("./a[1]/@href"))
            # 获取版面图片
            bm_pdf = 'https://epaper.lnd.com.cn/lswbepaper/pc/' + ''.join(bm.xpath("./a[2]/@href")).strip("../../..")
            # 获取版面下的内容
            bm_response = requests.get(bm_url, headers=headers, verify=False)
            time.sleep(2)
            bm_data = bm_response.content.decode()
            bm_html1 = etree.HTML(bm_data)
            bm_areaList = bm_html1.xpath("//div[@id='ScroLeft']/div[@class='newslist']/ul/li")
            for bm_area in bm_areaList:
                # 获取文章名称
                article_name = ''.join(bm_area.xpath("./h3/a/text()"))
                # 获取文章链接
                article_url = 'https://epaper.lnd.com.cn/lswbepaper/pc/' + ''.join(bm_area.xpath("./h3/a/@href")).strip(
                    "../../..")
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers, verify=False)
                time.sleep(2)
                content = ''
                if article_response.status_code == 200:
                    article_data = article_response.content.decode()
                    article_html = etree.HTML(article_data)
                    if article_html:
                        content = ''.join(article_html.xpath("//div[@class='newsdetatext']/founder-content/p//text()"))
                pdf_set = set()

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
                # print(bm_name, article_name, content, bm_pdf)
                if bm_pdf not in pdf_set and judge_bm_repeat(paper, bm_url):
                    # 将报纸img上传
                    up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper", verify=False)
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

        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        raise Exception(f'该日期没有报纸')



# paper_queue = paper_queue_next(
#             webpage_url_list=['https://epaper.lnd.com.cn'])
# webpage_name = paper_queue['webpage_name']
# queue_day = paper_queue['day']
# queue_id = paper_queue['id']
# webpage_id = paper_queue["webpage_id"]
# time = '2024-01-11'
# get_liaoshen_lastpaper('2018-10-18', 111, 111)
