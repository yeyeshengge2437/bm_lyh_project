import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "第一财经日报"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'acw_tc=0a47314f17274253765725934e003bfd633a343f1516d08227e5f36b8431af; Hm_lvt_80b762a374ca9a39e4434713ecc02488=1727425377; HMACCOUNT=FDD970C8B3C27398; yu_id=43888c3fbf4841b981d1080f8246956a; _ga=GA1.1.601846244.1727425377; connect.sid=s%3AGJeHhXvYCeLNgCEI70ddwjDoLi_rCcI0.QnoXZQFcQmYEXSVVdlZNUquNQK5pcPBpzuBQ%2BwSk1Qg; tfstk=gWfihY4ULOJ1bnHBcyR_nEHkXWed5VOXPihvDIK4LH-IXchOuSPc0ib93lOOiMjRuPtY5KIhui-BunJ20wkeYEkwbZd9ojXFin8NusLViMOwhOKvXnAclg4L27FR5NOXUuE8wNJE6ZAX0Sd4w-LTe0Z827Fd5NOXguBvyiLh6Ete7E827yYezHlZ7i-wLD8kPI-V0i7U-Ete0IRqZp0eXiS1Tlt_kLMx3x5HSdxoMHcmirLMI37wxeTCtS9M4N-nguU1HN-DA_rLKwsRQGLCm7qHaTshiLR0s0TGLaAeXQPi5359oaBcrumvROSGTKfLlR_hihvP_p0rMBRBuiJcducJSCBHE1X_lD7N2hXy1Z3uXwvlKLTeLqDw6TQRGL5as0tpFEjHeOqosgSP9vkrVNhXEl6ohx9wRex866O7Ajafg143-YWWQeTawy4nhx9wRex8-yDzVd8B77C..; _ga_BW57C8STG3=GS1.1.1727425377.1.1.1727425572.0.0.0; Hm_lpvt_80b762a374ca9a39e4434713ecc02488=1727425573',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}



def get_diyicaijing_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m/%d')
    base_url = f'https://www.yicai.com/epaper/pc/{paper_time}/'
    url = base_url + 'node_A01.html'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        if html_1 is None:
            raise Exception(f'该日期没有报纸')
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@class='Chunkiconlist']/p/a")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_pdf = 'https://www.yicai.com/epaper/pc/' + "".join(bm_html.xpath("//div[@class='newsconimg']/img/@src")).strip('../..')
            bm_pdf = re.sub(r'\.1', '', bm_pdf)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@class='newslist']/ul/li/h3/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@class='newsdetatext']/founder-content/p/text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, article_url, bm_pdf, content)
                if bm_pdf not in pdf_set  and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, paper, "jpg", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

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


# get_diyicaijing_paper('2019-09-16', 111, 1111)
