import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "石油金秋报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}



def get_shiyoujinqiu_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    base_url = f'http://news.cnpc.com.cn/epaper/jinqiu/{paper_time}/'
    url = base_url + 'index.htm'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode('gbk')
        html_1 = etree.HTML(content)
        count = 0
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//td//td[@class='default'][2]/a")
        for bm in all_bm:
            count +=1
            # 版面名称
            bm_name = f"第{count}版"
            # 版面链接
            bm_url = url
            # 版面的pdf
            bm_pdf = None
            up_pdf = None

            # 获取文章链接
            article_url = base_url + ''.join(bm.xpath("./@href"))
            # 获取文章名称
            article_name = ''.join(bm.xpath("./text()")).strip()
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            create_date = datetime.now().strftime('%Y-%m-%d')
            # 获取文章内容
            article_response = requests.get(article_url, headers=headers)
            time.sleep(1)
            article_content = article_response.content.decode('gbk')
            article_html = etree.HTML(article_content)
            # 获取文章内容
            content = ''.join(article_html.xpath("//span/font/con/text()")).strip()
            # 上传到测试数据库
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col",
            )
            cursor_test = conn_test.cursor()
            # print(bm_name, article_name, article_url, bm_pdf, content)

            if judging_criteria(article_name, content):

                # 上传到报纸的内容
                insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                     create_date, webpage_id))
                conn_test.commit()

                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
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


# get_shiyoujinqiu_paper('2023-02-25', 111, 1111)
