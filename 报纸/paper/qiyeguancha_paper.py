import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "企业观察报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASPSESSIONIDCQCBDSQA=JLNEOCMCPLDEJKPEFBJEDGGA',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
date_dict = {'2024-09-23': 'http://baozhi.cneo.com.cn/index.Asp?Nid=566', '2024-09-18': 'http://baozhi.cneo.com.cn/index.Asp?Nid=565', '2024-09-09': 'http://baozhi.cneo.com.cn/index.Asp?Nid=564', '2024-09-02': 'http://baozhi.cneo.com.cn/index.Asp?Nid=563', '2024-08-26': 'http://baozhi.cneo.com.cn/index.Asp?Nid=562', '2024-08-19': 'http://baozhi.cneo.com.cn/index.Asp?Nid=561', '2024-08-12': 'http://baozhi.cneo.com.cn/index.Asp?Nid=560', '2024-08-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=559', '2024-07-29': 'http://baozhi.cneo.com.cn/index.Asp?Nid=558', '2024-07-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=557', '2024-07-15': 'http://baozhi.cneo.com.cn/index.Asp?Nid=556', '2024-07-08': 'http://baozhi.cneo.com.cn/index.Asp?Nid=555', '2024-07-01': 'http://baozhi.cneo.com.cn/index.Asp?Nid=554', '2024-06-24': 'http://baozhi.cneo.com.cn/index.Asp?Nid=553', '2024-06-17': 'http://baozhi.cneo.com.cn/index.Asp?Nid=552', '2024-06-11': 'http://baozhi.cneo.com.cn/index.Asp?Nid=551', '2024-06-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=550', '2024-06-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=549', '2024-06-03': 'http://baozhi.cneo.com.cn/index.Asp?Nid=548', '2024-05-13': 'http://baozhi.cneo.com.cn/index.Asp?Nid=547', '2024-04-29': 'http://baozhi.cneo.com.cn/index.Asp?Nid=546', '2024-04-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=545', '2024-04-15': 'http://baozhi.cneo.com.cn/index.Asp?Nid=543', '2024-04-01': 'http://baozhi.cneo.com.cn/index.Asp?Nid=542', '2024-03-25': 'http://baozhi.cneo.com.cn/index.Asp?Nid=541', '2024-03-18': 'http://baozhi.cneo.com.cn/index.Asp?Nid=540', '2024-03-11': 'http://baozhi.cneo.com.cn/index.Asp?Nid=539', '2024-03-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=538', '2024-02-26': 'http://baozhi.cneo.com.cn/index.Asp?Nid=537', '2024-02-21': 'http://baozhi.cneo.com.cn/index.Asp?Nid=536', '2024-02-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=535', '2024-01-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=534', '2024-01-16': 'http://baozhi.cneo.com.cn/index.Asp?Nid=533', '2024-01-09': 'http://baozhi.cneo.com.cn/index.Asp?Nid=532', '2023-12-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=531', '2023-12-18': 'http://baozhi.cneo.com.cn/index.Asp?Nid=530', '2023-12-11': 'http://baozhi.cneo.com.cn/index.Asp?Nid=529', '2023-12-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=528', '2023-11-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=527', '2023-11-20': 'http://baozhi.cneo.com.cn/index.Asp?Nid=526', '2023-11-13': 'http://baozhi.cneo.com.cn/index.Asp?Nid=525', '2023-11-08': 'http://baozhi.cneo.com.cn/index.Asp?Nid=524', '2023-10-30': 'http://baozhi.cneo.com.cn/index.Asp?Nid=523', '2023-10-23': 'http://baozhi.cneo.com.cn/index.Asp?Nid=522', '2023-10-16': 'http://baozhi.cneo.com.cn/index.Asp?Nid=521', '2023-10-07': 'http://baozhi.cneo.com.cn/index.Asp?Nid=520', '2023-09-25': 'http://baozhi.cneo.com.cn/index.Asp?Nid=519', '2023-09-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=518', '2023-09-11': 'http://baozhi.cneo.com.cn/index.Asp?Nid=517', '2023-09-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=516', '2023-08-28': 'http://baozhi.cneo.com.cn/index.Asp?Nid=515', '2023-08-21': 'http://baozhi.cneo.com.cn/index.Asp?Nid=514', '2023-08-14': 'http://baozhi.cneo.com.cn/index.Asp?Nid=513', '2023-08-07': 'http://baozhi.cneo.com.cn/index.Asp?Nid=512', '2023-07-31': 'http://baozhi.cneo.com.cn/index.Asp?Nid=511', '2023-07-24': 'http://baozhi.cneo.com.cn/index.Asp?Nid=510', '2023-07-17': 'http://baozhi.cneo.com.cn/index.Asp?Nid=509', '2023-07-10': 'http://baozhi.cneo.com.cn/index.Asp?Nid=508', '2023-07-03': 'http://baozhi.cneo.com.cn/index.Asp?Nid=507', '2023-06-26': 'http://baozhi.cneo.com.cn/index.Asp?Nid=506', '2023-06-19': 'http://baozhi.cneo.com.cn/index.Asp?Nid=505', '2023-06-12': 'http://baozhi.cneo.com.cn/index.Asp?Nid=504', '2023-06-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=503', '2023-05-31': 'http://baozhi.cneo.com.cn/index.Asp?Nid=502', '2023-05-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=501', '2023-05-15': 'http://baozhi.cneo.com.cn/index.Asp?Nid=500', '2023-05-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=499', '2023-04-25': 'http://baozhi.cneo.com.cn/index.Asp?Nid=498', '2023-04-17': 'http://baozhi.cneo.com.cn/index.Asp?Nid=497', '2023-04-10': 'http://baozhi.cneo.com.cn/index.Asp?Nid=496', '2023-04-03': 'http://baozhi.cneo.com.cn/index.Asp?Nid=495', '2023-03-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=494', '2023-03-20': 'http://baozhi.cneo.com.cn/index.Asp?Nid=493', '2023-03-13': 'http://baozhi.cneo.com.cn/index.Asp?Nid=492', '2023-03-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=491', '2023-02-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=490', '2023-02-20': 'http://baozhi.cneo.com.cn/index.Asp?Nid=489', '2023-02-13': 'http://baozhi.cneo.com.cn/index.Asp?Nid=488', '2023-02-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=487', '2023-01-16': 'http://baozhi.cneo.com.cn/index.Asp?Nid=486', '2023-01-09': 'http://baozhi.cneo.com.cn/index.Asp?Nid=485', '2023-01-03': 'http://baozhi.cneo.com.cn/index.Asp?Nid=484', '2022-12-26': 'http://baozhi.cneo.com.cn/index.Asp?Nid=483', '2022-12-19': 'http://baozhi.cneo.com.cn/index.Asp?Nid=482', '2022-12-12': 'http://baozhi.cneo.com.cn/index.Asp?Nid=481', '2022-12-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=480', '2022-11-28': 'http://baozhi.cneo.com.cn/index.Asp?Nid=479', '2022-11-21': 'http://baozhi.cneo.com.cn/index.Asp?Nid=478', '2022-11-14': 'http://baozhi.cneo.com.cn/index.Asp?Nid=477', '2022-11-07': 'http://baozhi.cneo.com.cn/index.Asp?Nid=476', '2022-10-31': 'http://baozhi.cneo.com.cn/index.Asp?Nid=475', '2022-10-23': 'http://baozhi.cneo.com.cn/index.Asp?Nid=474', '2022-10-17': 'http://baozhi.cneo.com.cn/index.Asp?Nid=473', '2022-10-10': 'http://baozhi.cneo.com.cn/index.Asp?Nid=472', '2022-09-29': 'http://baozhi.cneo.com.cn/index.Asp?Nid=471', '2022-09-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=465', '2022-08-08': 'http://baozhi.cneo.com.cn/index.Asp?Nid=464', '2022-08-01': 'http://baozhi.cneo.com.cn/index.Asp?Nid=463', '2022-07-25': 'http://baozhi.cneo.com.cn/index.Asp?Nid=462', '2022-07-18': 'http://baozhi.cneo.com.cn/index.Asp?Nid=461', '2022-07-11': 'http://baozhi.cneo.com.cn/index.Asp?Nid=460', '2022-07-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=459', '2022-06-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=458', '2022-06-20': 'http://baozhi.cneo.com.cn/index.Asp?Nid=457', '2022-06-13': 'http://baozhi.cneo.com.cn/index.Asp?Nid=456', '2022-06-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=455', '2022-05-30': 'http://baozhi.cneo.com.cn/index.Asp?Nid=454', '2022-05-23': 'http://baozhi.cneo.com.cn/index.Asp?Nid=453', '2022-05-16': 'http://baozhi.cneo.com.cn/index.Asp?Nid=452', '2022-05-09': 'http://baozhi.cneo.com.cn/index.Asp?Nid=451', '2022-05-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=450', '2022-04-25': 'http://baozhi.cneo.com.cn/index.Asp?Nid=449', '2022-04-18': 'http://baozhi.cneo.com.cn/index.Asp?Nid=448', '2022-04-11': 'http://baozhi.cneo.com.cn/index.Asp?Nid=447', '2022-04-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=446', '2022-03-28': 'http://baozhi.cneo.com.cn/index.Asp?Nid=445', '2022-03-21': 'http://baozhi.cneo.com.cn/index.Asp?Nid=444', '2022-03-14': 'http://baozhi.cneo.com.cn/index.Asp?Nid=443', '2022-03-07': 'http://baozhi.cneo.com.cn/index.Asp?Nid=442', '2022-02-28': 'http://baozhi.cneo.com.cn/index.Asp?Nid=441', '2022-02-21': 'http://baozhi.cneo.com.cn/index.Asp?Nid=440', '2022-02-16': 'http://baozhi.cneo.com.cn/index.Asp?Nid=439', '2022-01-24': 'http://baozhi.cneo.com.cn/index.Asp?Nid=438', '2022-01-17': 'http://baozhi.cneo.com.cn/index.Asp?Nid=437', '2022-01-10': 'http://baozhi.cneo.com.cn/index.Asp?Nid=436', '2022-01-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=435', '2021-12-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=434', '2021-12-21': 'http://baozhi.cneo.com.cn/index.Asp?Nid=433', '2021-12-13': 'http://baozhi.cneo.com.cn/index.Asp?Nid=432', '2021-12-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=431', '2021-11-30': 'http://baozhi.cneo.com.cn/index.Asp?Nid=430', '2021-11-23': 'http://baozhi.cneo.com.cn/index.Asp?Nid=429', '2021-11-16': 'http://baozhi.cneo.com.cn/index.Asp?Nid=428', '2021-11-09': 'http://baozhi.cneo.com.cn/index.Asp?Nid=427', '2021-11-02': 'http://baozhi.cneo.com.cn/index.Asp?Nid=426', '2021-10-26': 'http://baozhi.cneo.com.cn/index.Asp?Nid=425', '2021-10-19': 'http://baozhi.cneo.com.cn/index.Asp?Nid=424', '2021-09-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=423', '2021-09-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=422', '2021-09-14': 'http://baozhi.cneo.com.cn/index.Asp?Nid=421', '2021-09-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=420', '2021-08-31': 'http://baozhi.cneo.com.cn/index.Asp?Nid=419', '2021-08-24': 'http://baozhi.cneo.com.cn/index.Asp?Nid=418', '2021-08-16': 'http://baozhi.cneo.com.cn/index.Asp?Nid=417', '2021-08-10': 'http://baozhi.cneo.com.cn/index.Asp?Nid=416', '2021-08-02': 'http://baozhi.cneo.com.cn/index.Asp?Nid=415', '2021-07-26': 'http://baozhi.cneo.com.cn/index.Asp?Nid=414', '2021-07-19': 'http://baozhi.cneo.com.cn/index.Asp?Nid=413', '2021-07-12': 'http://baozhi.cneo.com.cn/index.Asp?Nid=412', '2021-07-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=411', '2021-06-28': 'http://baozhi.cneo.com.cn/index.Asp?Nid=410', '2021-06-21': 'http://baozhi.cneo.com.cn/index.Asp?Nid=409', '2021-06-15': 'http://baozhi.cneo.com.cn/index.Asp?Nid=408', '2021-06-07': 'http://baozhi.cneo.com.cn/index.Asp?Nid=407', '2021-05-31': 'http://baozhi.cneo.com.cn/index.Asp?Nid=406', '2021-05-24': 'http://baozhi.cneo.com.cn/index.Asp?Nid=405', '2021-05-17': 'http://baozhi.cneo.com.cn/index.Asp?Nid=404', '2021-05-11': 'http://baozhi.cneo.com.cn/index.Asp?Nid=403', '2021-05-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=402', '2021-04-26': 'http://baozhi.cneo.com.cn/index.Asp?Nid=401', '2021-04-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=400', '2021-04-13': 'http://baozhi.cneo.com.cn/index.Asp?Nid=399', '2021-04-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=398', '2021-03-31': 'http://baozhi.cneo.com.cn/index.Asp?Nid=396', '2021-03-15': 'http://baozhi.cneo.com.cn/index.Asp?Nid=395', '2021-03-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=394', '2021-03-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=393', '2021-02-05': 'http://baozhi.cneo.com.cn/index.Asp?Nid=392', '2021-01-29': 'http://baozhi.cneo.com.cn/index.Asp?Nid=391', '2021-01-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=390', '2021-01-15': 'http://baozhi.cneo.com.cn/index.Asp?Nid=389', '2021-01-08': 'http://baozhi.cneo.com.cn/index.Asp?Nid=388', '2021-01-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=387', '2020-12-25': 'http://baozhi.cneo.com.cn/index.Asp?Nid=386', '2020-12-18': 'http://baozhi.cneo.com.cn/index.Asp?Nid=385', '2020-12-11': 'http://baozhi.cneo.com.cn/index.Asp?Nid=384', '2020-12-04': 'http://baozhi.cneo.com.cn/index.Asp?Nid=383', '2020-11-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=382', '2020-11-20': 'http://baozhi.cneo.com.cn/index.Asp?Nid=381', '2020-11-13': 'http://baozhi.cneo.com.cn/index.Asp?Nid=380', '2020-11-06': 'http://baozhi.cneo.com.cn/index.Asp?Nid=379', '2020-10-29': 'http://baozhi.cneo.com.cn/index.Asp?Nid=378', '2020-10-23': 'http://baozhi.cneo.com.cn/index.Asp?Nid=377', '2020-10-16': 'http://baozhi.cneo.com.cn/index.Asp?Nid=376', '2020-09-25': 'http://baozhi.cneo.com.cn/index.Asp?Nid=375', '2020-09-18': 'http://baozhi.cneo.com.cn/index.Asp?Nid=373', '2020-09-09': 'http://baozhi.cneo.com.cn/index.Asp?Nid=371', '2020-08-24': 'http://baozhi.cneo.com.cn/index.Asp?Nid=369', '2020-08-10': 'http://baozhi.cneo.com.cn/index.Asp?Nid=32', '2020-09-21': 'http://baozhi.cneo.com.cn/index.Asp?Nid=363', '2020-09-22': 'http://baozhi.cneo.com.cn/index.Asp?Nid=364', '2020-09-27': 'http://baozhi.cneo.com.cn/index.Asp?Nid=356', '2020-08-09': 'http://baozhi.cneo.com.cn/index.Asp?Nid=31', '2020-07-26': 'http://baozhi.cneo.com.cn/index.Asp?Nid=30', '2018-03-19': 'http://baozhi.cneo.com.cn/index.Asp?Nid=19', '2012-02-29': 'http://baozhi.cneo.com.cn/index.Asp?Nid=18'}

def get_date():
    for i in range(1, 3):
        url = f'http://baozhi.cneo.com.cn/review.asp?Page={i}'
        response = requests.get(url,headers=headers, verify=False)
        content = response.content.decode('gbk')
        html = etree.HTML(content)
        all_paper = html.xpath("//div[@class='review_list']/ul/li")
        for paper in all_paper:
            paper_time = "".join(paper.xpath("./p/a/img/@src")).strip()
            paper_time = re.findall(r'/uploads/image/(\d+)/\d+\..*', paper_time)[0]
            paper_time = f"{paper_time[0:4]}-{paper_time[4:6]}-{paper_time[6:8]}"
            paper_url = "http://baozhi.cneo.com.cn/" + "".join(paper.xpath("./span/a/@href"))
            if paper_time not in date_dict:
                date_dict[paper_time] = paper_url





def get_qiyeguancha_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    get_date()

    if paper_time in date_dict:
        url = date_dict.get(paper_time)
    else:
        raise Exception(f'该日期没有报纸')
    day = paper_time

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode('gbk')
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@id='index_f_list']/ul/li/a")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./text()")).strip()
            # 版面链接
            bm_url = 'http://baozhi.cneo.com.cn/' + ''.join(bm.xpath("./@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode('gbk')
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_pdf = 'http://baozhi.cneo.com.cn' + "".join(bm_html.xpath("//span[@class='fr pdf_down']/a/@href"))

            # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@id='index_a_list']//a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = 'http://baozhi.cneo.com.cn/' + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                try:
                    article_content = article_response.content.decode('gbk')
                except:
                    continue
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='Zoom']/p//text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
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


# get_qiyeguancha_paper('2018-07-17', 111, 1111)
