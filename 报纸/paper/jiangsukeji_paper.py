import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "江苏科技报"
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'PHPSESSID=ngls8b2819jub5sb6af0v0ila3',
    'Origin': 'http://www.jskjb.com:8081',
    'Pragma': 'no-cache',
    'Referer': 'http://www.jskjb.com:8081/xpaper/release/132484/145034.shtml',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_date(paper_time):
    year = paper_time[:4]
    month = paper_time[5:7]
    data = {
        'sy': f'{year}',
        'sm': f'{month}',
        'myent_id': '1',
    }
    response = requests.post('http://www.jskjb.com:8081/public/releasedate/index.shtml', headers=headers, data=data, verify=False,)
    if response.status_code == 200:
        content = response.content.decode()
        # 07,09,11,14,!07-132484/145034%09-133484/146037%11-133485/146052%14-133486/146065
        content = content.split('!')[-1]
        content_list = content.split('%')
        date_dict = {}
        for con_data in content_list:
            con_data = con_data.split('-')
            day = con_data[0]
            queue_id = con_data[1]
            date_time = f'{year}-{month}-{day}'
            date_url = f'http://www.jskjb.com:8081/xpaper/release/{queue_id}.shtml'
            date_dict[date_time] = date_url
        if paper_time in date_dict:
            return date_dict[paper_time]
        else:
            return None


# print(get_date('2024-10-07'))

def get_jiangsukeji_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    url = get_date(paper_time)
    if url is None:
        raise Exception(f'该日期没有报纸')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//tr[3]//table//table[1]//table//a")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./text()")).strip()
            # 版面链接
            bm_url = 'http://www.jskjb.com:8081/' + ''.join(bm.xpath("./@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_pdf = None

            # 获取所有文章的链接
            all_article = bm_html.xpath("//a[@class='yaowen']")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = 'http://www.jskjb.com:8081/' + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./span/text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode()
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@class='content-con']/p//text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, article_url, bm_pdf, content)
                if judging_criteria(article_name, content):
                    # 将报纸url上传
                    up_pdf = None
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


# get_jiangsukeji_paper('2024-08-21', 111, 1111)
