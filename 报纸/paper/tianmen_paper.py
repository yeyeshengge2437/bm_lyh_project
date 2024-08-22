
import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url
import mysql.connector
import requests
from lxml import etree



paper = "天门日报"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

today = datetime.now().strftime('%Y-%m-%d')
def get_tianmen_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    base_url = f'https://tmrb.tmwcn.com/tmrb/{paper_time}/html/'
    url = base_url + 'index.htm'
    response = requests.get(url, headers=headers)
    time.sleep(2)
    if response.status_code == 200:
        content = response.content.decode()

        html_1 = etree.HTML(content)
        # 获取末版链接
        bm_last = ''.join(html_1.xpath("//div[@class='page_bottom']/a[4]/@href"))
        # 正则匹配页面数
        page_num = re.findall(r'(\d+)', bm_last)[0]
        for i in range(int(page_num) + 1):
            if i == 0:
                bm_url = base_url + 'index.htm'
            else:
                bm_url = base_url + 'page_' + "0" + str(i) + '.htm'
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)
            # 版面名称
            bm_name = "".join(bm_html.xpath("//div[@class='b_bot']/text()")).strip()
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            create_date = datetime.now().strftime('%Y-%m-%d')
            # 获取该版面的所有标题
            all_article = bm_html.xpath("//a[@class='bmdh_con_a']")
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章标题
                article_title = ''.join(article.xpath("./text()"))
                res_content = requests.get(article_url, headers=headers)
                time.sleep(2)
                article_html = etree.HTML(res_content.content.decode())
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@class='bmnr_con_con']/div[@id='zoom']/text()"))

                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col"
                )
                cursor_test = conn_test.cursor()
                if judging_criteria(article_title, content):  # 如果标题匹配，则上传

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_title, content, article_url, create_time, queue_id,
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


