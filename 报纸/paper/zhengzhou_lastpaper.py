import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "郑州晚报"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'acw_tc=79cfe59a17272357540157663ed8d97fc696e2e3e9dc8590ddadb0a15a; Hm_lvt_72844f39ec52bc5384367f1464333554=1727235759; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_d44914adec844b7f75d0dc0dbb1f508b=1727235783; Hm_lpvt_d44914adec844b7f75d0dc0dbb1f508b=1727235783; Hm_lpvt_72844f39ec52bc5384367f1464333554=1727235923',
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



def get_zhengzhou_lastpaper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'https://zzwb.zynews.cn/html/{paper_time}/'
    url = base_url + 'node_102.htm'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            content = response.content.decode()
        except:
            raise Exception(f'该日期没有报纸')
        html_1 = etree.HTML(content)
        if html_1 is None:
            raise Exception(f'该日期没有报纸')
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//table[@class='newspaperDirectory']//table[3]/tbody/tr")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./td[@class='default']/a/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./td[@class='default']/a/@href")).strip('./')
            # 版面的pdf
            bm_pdf = 'https://zzwb.zynews.cn/' + "".join(
                bm.xpath("./td[2]/a/@href")).strip('../../..')

            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            try:
                bm_content = bm_response.content.decode()
            except:
                continue
            bm_html = etree.HTML(bm_content)
            if bm_html is None:
                continue

            # 获取所有文章的链接
            all_article = bm_html.xpath("//table[3]//td[@class='default'][2]/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./div/text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                try:
                    article_content = article_response.content.decode()
                except:
                    continue
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='ozoom']/founder-content/p/text()")).strip()
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


# get_zhengzhou_lastpaper('2013-02-28', 111, 1111)
