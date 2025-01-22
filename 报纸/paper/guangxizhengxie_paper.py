import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "广西政协报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}



def get_guangxizhengxie_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m-%d')
    base_url = f'http://www.gxzxbxwzx.com.cn/dzszb/szbcf/index.html?day={paper_time}'
    url = base_url
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@class='szb-list-right-top-right']/ul/a")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./li/text()")).strip()
            # 版面链接
            bm_url = 'http://www.gxzxbxwzx.com.cn/' + ''.join(bm.xpath("./@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_img = 'http://www.gxzxbxwzx.com.cn' + "".join(bm_html.xpath("//img[@class='bm-img']/@src"))

            # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@class='szb-list-right-top-left']/div[3]/ul/li/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = 'http://www.gxzxbxwzx.com.cn' + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                if article_html is None:
                    continue
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@class='szb-main-right']/div[2]/div[2]/div[2]/p//text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, article_url, bm_img, content)
                if bm_img not in pdf_set and judging_bm_criteria(article_name, bm_url, bm_url_in) and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_img, paper, "png", "paper")
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


# get_guangxizhengxie_paper('2022-03-17', 111, 1111)
