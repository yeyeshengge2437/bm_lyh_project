import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "中国纪检监察报"
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_trs_uv=m1n0z125_4878_bybu; HMF_CI=b51b612efcab0fb27c3cf129d01b6f57f9cc81ed33b9e6109db3dd05c0a07d30e57329e9b0f4965e6d33684674687b90b710359f359d7da20742fef2e71ca0f8ae; HMY_JC=d91b61a45f651d66acb10be91f0c6e65e2e99075b6ee85196ecbc046654f38da00,; _trs_ua_s_1=m28fwbwj_4878_6sqg; HBB_HC=24964091dfe18dabe54402bab839e0f6c0a6b8e5854e5b34841f6e5df2adaa9d9486714f935fc352c27a327bd9008a7fe5',
    'Origin': 'https://jjjcb.ccdi.gov.cn',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
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


def get_chinaminzu_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    data = {
        'docPubTime': f'{paper_time}',
    }
    cookies = get_paper_url_cookies('https://jjjcb.ccdi.gov.cn/epaper/')
    response = requests.post('https://jjjcb.ccdi.gov.cn/reader/layout/findBmMenu.do', headers=headers, data=data, cookies=cookies, verify=False)
    if response.status_code == 200:
        content = response.json()
        print(content)
        return
        # 获取所有版面的的链接
        all_bm = content
        for bm in all_bm:
            # 版面名称
            bm_name = bm['BC']
            # 版面链接
            bm_url = 'https://jjjcb.ccdi.gov.cn/epaper/' + bm['PDPATH']
            # 版面的pdf
            bm_pdf = 'https://jjjcb.ccdi.gov.cn/epaper/' + bm['PDPATH']

            # 获取所有文章的链接
            bm_str = bm['IRCATELOG']
            params = {
                'bc': f'{bm_str}',
                'docpubtime': f'{paper_time}',
            }

            response = requests.post('https://jjjcb.ccdi.gov.cn/reader/layout/getBmDetail.do', headers=headers, data=data, cookies=cookies, verify=False)
            all_article = response.json()

            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = f'https://jjjcb.ccdi.gov.cn/epaper/index.html?guid={article["ZB_GUID"]}'
                # 获取文章名称
                try:
                    article_name = ''.join(article['DOCTITLE'])
                except:
                    continue
                # 去除英文和特殊字符
                article_name = re.sub(r'[^\u4e00-\u9fa5]', '', article_name)
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                content = article['IR_ABSTRACT']
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                print(bm_name, article_name, article_url, bm_pdf, content)
                # if bm_pdf not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                #     # 将报纸url上传
                #     up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                #     pdf_set.add(bm_pdf)
                #     # 上传到报纸的图片或PDF
                #     insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"
                #
                #     cursor_test.execute(insert_sql,
                #                         (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                #                          create_date, webpage_id))
                #     conn_test.commit()
                #
                # if judging_criteria(article_name, content):
                # # if 1:
                #
                #     # print(content)
                #     # return
                #
                #     # 上传到报纸的内容
                #     insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"
                #
                #     cursor_test.execute(insert_sql,
                #                         (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                #                          create_date, webpage_id))
                #     conn_test.commit()

                cursor_test.close()
                conn_test.close()


        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        raise Exception(f'该日期没有报纸')


get_chinaminzu_paper('2024-10-13', 111, 1111)
