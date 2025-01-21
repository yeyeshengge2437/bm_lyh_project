import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "福州日报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'wdcid=376155a31210c268; wdlast=1727254141; wdses=19bca0201e28f8cf; Hm_lvt_98493946d8fd72cd91eba6e749fe40e7=1727254142; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_98493946d8fd72cd91eba6e749fe40e7=1727254523',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



def get_fuzhou_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    year = paper_time[0:4]
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    base_url = f'https://mag.fznews.com.cn/fzrb/{year}/{paper_time}/{paper_time}_plist.htm'
    url = base_url
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode('gbk')
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//tr")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./td[1]/div[@class='bancititle']/a/span/text()")).strip()
            # 版面链接
            bm_url = f'https://mag.fznews.com.cn/fzrb/{year}/{paper_time}/' + ''.join(bm.xpath("./td[1]/div[@class='bancititle']/a/@href")).strip('./')
            # 版面的pdf
            bm_pdf = f'https://mag.fznews.com.cn/fzrb/{year}/{paper_time}/' + "".join(
                bm.xpath("./td[2]/a/@href")).strip('./')
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode('gbk')
            bm_html = etree.HTML(bm_content)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//area")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = f'https://mag.fznews.com.cn/fzrb/{year}/{paper_time}' + ''.join(article.xpath(".//@href")).strip('..')
                # 获取文章名称
                article_name = ''.join(article.xpath(".//@title")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode('gbk')
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='zhenwenzone']//text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, article_url, bm_pdf, content)
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


# get_fuzhou_paper('2024-08-22', 111, 1111)
