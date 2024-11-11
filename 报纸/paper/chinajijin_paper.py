import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree
from urllib.parse import unquote


paper = "中国基金报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'Hm_lvt_35849f3b9042e6cb270e09a0d9350982=1725609338,1725854520; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_35849f3b9042e6cb270e09a0d9350982=1725854531',
    'Pragma': 'no-cache',
    'Referer': 'https://www.chnfund.com/epaper',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}



def get_chinajijin_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%m/%d/%Y')
    params = {
        'publishDate': f'{paper_time} 00:00:00',
    }
    base_url = f'https://www.chnfund.com/epaper'
    url = base_url
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有pdf
        all_pdf = html_1.xpath("//ul[@class='item-group ']/li[@class='item']/a/@href")
        pdf_set = set()
        for pdf in all_pdf:
            bm_pdf = 'https://www.chnfund.com' + pdf
            bm_pdf = bm_pdf.split('file=')[-1]
            bm_pdf = unquote(bm_pdf)
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
            # print(bm_name, article_name, bm_pdf, content)
            if bm_pdf not in pdf_set:
                # 将报纸url上传
                up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                pdf_set.add(bm_pdf)
                # print(bm_pdf, up_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, original_pdf,  pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s)"

                cursor_test.execute(insert_sql,
                                    (day, paper, bm_pdf,  up_pdf, create_time, queue_id,
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


# get_chinajijin_paper('2024-09-10', 111, 1111)
