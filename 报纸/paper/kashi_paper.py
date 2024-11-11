import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "喀什日报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Secure; Secure; Hm_lvt_be699decd08c19ae87871cfb3496cdba=1726816183,1728437753; Hm_lpvt_be699decd08c19ae87871cfb3496cdba=1728437753; HMACCOUNT=FDD970C8B3C27398; Secure; Hm_lvt_305524cc5e0541af5c129c802ff36993=1726816188,1728437758; Hm_lpvt_305524cc5e0541af5c129c802ff36993=1728437758',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

date_dict = {'2024-10-04': 'http://www.zgkashi.com/c/2024-10-04/1056671.shtml', '2024-10-01': 'http://www.zgkashi.com/c/2024-10-01/1056211.shtml', '2024-09-30': 'http://www.zgkashi.com/c/2024-09-30/1055945.shtml', '2024-09-28': 'http://www.zgkashi.com/c/2024-09-28/1055585.shtml', '2024-09-27': 'http://www.zgkashi.com/c/2024-09-27/1055380.shtml', '2024-09-26': 'http://www.zgkashi.com/c/2024-09-26/1055231.shtml', '2024-09-25': 'http://www.zgkashi.com/c/2024-09-25/1055088.shtml', '2024-09-24': 'http://www.zgkashi.com/c/2024-09-24/1054898.shtml', '2024-09-23': 'http://www.zgkashi.com/c/2024-09-23/1054699.shtml', '2024-09-20': 'http://www.zgkashi.com/c/2024-09-20/1054275.shtml', '2024-09-19': 'http://www.zgkashi.com/c/2024-09-19/1054138.shtml', '2024-09-18': 'http://www.zgkashi.com/c/2024-09-18/1053903.shtml', '2024-09-14': 'http://www.zgkashi.com/c/2024-09-14/1053150.shtml', '2024-09-13': 'http://www.zgkashi.com/c/2024-09-13/1052901.shtml', '2024-09-12': 'http://www.zgkashi.com/c/2024-09-12/1052734.shtml', '2024-09-11': 'http://www.zgkashi.com/c/2024-09-11/1052496.shtml', '2024-09-10': 'http://www.zgkashi.com/c/2024-09-10/1052336.shtml', '2024-09-09': 'http://www.zgkashi.com/c/2024-09-09/1052132.shtml', '2024-09-06': 'http://www.zgkashi.com/c/2024-09-06/1051569.shtml'}


def get_date():
    response = requests.get('http://www.zgkashi.com/yw/sp/', headers=headers, verify=False)
    if response.status_code == 200:
        content = response.content.decode()
        html = etree.HTML(content)
        dates = html.xpath("//div[@id='liebiao']/ul/li")
        for date in dates:
            date_url = 'http://www.zgkashi.com' + "".join(date.xpath("./h3/a/@href"))
            date_str = "".join(date.xpath("./div[@class='tail']/span/text()"))
            date_time = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', date_str)[0]
            if date_time not in date_dict:
                date_dict[date_time] = date_url
    return date_dict


def get_kashi_paper(paper_time, queue_id, webpage_id):
    get_date()
    # 将today的格式进行改变
    day = paper_time
    if paper_time not in date_dict:
        raise Exception(f'该日期没有报纸')
    url = date_dict.get(paper_time)
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@id='news-con']/p/img")
        count = 0
        for bm in all_bm:
            count += 1
            # 版面名称
            bm_name = f'第{count}版'

            # 版面的pdf
            bm_pdf = 'http://www.zgkashi.com' + "".join(bm.xpath("./@src"))
            # 版面链接
            bm_url = bm_pdf
            pdf_set = set()

            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            create_date = datetime.now().strftime('%Y-%m-%d')

            # 上传到测试数据库
            conn_test = mysql.connector.connect(
                host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col",
            )
            cursor_test = conn_test.cursor()
            # print(bm_name, bm_pdf)
            if bm_pdf not in pdf_set and judge_bm_repeat(paper, bm_url):
                # 将报纸url上传
                up_pdf = upload_file_by_url(bm_pdf, paper, "png", "paper")
                pdf_set.add(bm_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

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


# get_kashi_paper('2024-10-01', 111, 1111)
