import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree

co = ChromiumOptions()
co = co.set_paths().auto_port()
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错




paper = "市场导报"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'security_session_verify=2d778e64f62cc60e13d1c5f3e2a0cb3e; security_session_mid_verify=37eb62fefd8a664ece6f9ea61a24d470; PHPSESSID=24b61f110672e0fefb0337831d06d75d',
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



def get_shichangdao_paper(paper_time, queue_id, webpage_id):

    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    base_url = f'https://epaper.zjscdb.com/shtml/scdb/{paper_time}/'
    url = base_url + 'index.shtml'
    cookie_dict = {}
    page = ChromiumPage(co)
    tab = page.new_tab()
    tab.get(url)
    value_cookies = tab.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    tab.close()
    response = requests.get(url, cookies=cookie_dict, headers=headers)
    if response.status_code == 200:
        try:
            content = response.content.decode("gbk")
        except:
            raise Exception(f'该日期没有报纸')
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@id='scrollDiv']/ul/li")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./a/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./a/@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers, cookies=cookie_dict)
            time.sleep(1)
            try:
                bm_content = bm_response.content.decode('gbk')
            except:
                bm_content = bm_response.content
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_img = 'https://epaper.zjscdb.com' + "".join(bm_html.xpath("//img[@id='imgPage']/@src"))
            bm_img = re.sub('b_', '', bm_img)

            # 获取所有文章的链接
            all_article = bm_html.xpath("//dl[@class='Rcon']/dd/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers, cookies=cookie_dict)
                time.sleep(1)
                article_content = article_response.content.decode('gbk')
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//td[@id='DivDisplay']/div[@class='f-14 height-25']//text()")).strip()
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


# get_shichangdao_paper('2023-09-08', 111, 1111)
