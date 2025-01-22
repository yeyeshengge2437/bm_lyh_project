import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests

from lxml import etree



paper = "山西经济日报"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_db36c250178069764b8184d985410e0a=1727167091; security_session_verify=6709a5ed5f4c3dbea7e2305edc771a2f; srcurl=687474703a2f2f7777772e73786a6a622e636e2f737a622f68746d6c2f323032322d31312f30322f636f6e74656e745f3234353431382e68746d; security_session_mid_verify=1fe8a28dde9bbf10bf6767c70b4ba608',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}
from DrissionPage import ChromiumPage, ChromiumOptions
co = ChromiumOptions()
co = co.set_paths(local_port=9242)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错
def get_paper_url_cookies(url):
    cookie_dict = {}
    page = ChromiumPage(co)
    page.get(url)
    value_cookies = page.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    page.close()
    return cookie_dict



def get_shanxijingji_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y-%m/%d')
    base_url = f'http://www.sxjjb.cn/szb/html/{paper_time}/'
    url = base_url + 'node_2.htm'
    cookies = get_paper_url_cookies(url)
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        if html_1 is None:
            raise Exception(f'该日期没有报纸')
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//table[2]//tr[2]//tr/td[@class='default']")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./a[@id='pageLink']/text()")).strip()
            # 版面链接
            bm_url = base_url + ''.join(bm.xpath("./a[@id='pageLink']/@href")).strip('./')
            # 版面的pdf
            bm_pdf = 'http://www.sxjjb.cn/szb/' + "".join(
                bm.xpath("./following-sibling::td/a/@href")).strip('../../..')

            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers, cookies=cookies)
            time.sleep(1)
            bm_content = bm_response.content.decode()
            bm_html = etree.HTML(bm_content)


            # 获取所有文章的链接
            all_article = bm_html.xpath("//tr[4]//div//td[@class='default'][2]/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = base_url + ''.join(article.xpath("./@href")).strip('../..')
                # 获取文章名称
                article_name = ''.join(article.xpath("./div/text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                art_cookies = get_paper_url_cookies(article_url)
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers, cookies=art_cookies)
                time.sleep(1)
                # try:
                article_content = article_response.content.decode()
                # except:
                #     continue
                article_html = etree.HTML(article_content)
                if article_html is None:
                    content = ''
                else:
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
                if bm_pdf not in pdf_set and judging_bm_criteria(article_name, bm_url, bm_url_in) and judge_bm_repeat(paper, bm_url):
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


# get_shanxijingji_paper('2024-11-06', 111, 1111)
