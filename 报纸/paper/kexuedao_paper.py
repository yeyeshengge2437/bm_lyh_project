import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "科学导报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

date_dict = {'2024-09-20': 'http://www.kxdb.com/dzbk/show.php?itemid=289', '2024-09-13': 'http://www.kxdb.com/dzbk/show.php?itemid=286', '2024-09-10': 'http://www.kxdb.com/dzbk/show.php?itemid=284', '2024-09-06': 'http://www.kxdb.com/dzbk/show.php?itemid=281', '2024-09-03': 'http://www.kxdb.com/dzbk/show.php?itemid=280', '': '', '2024-08-30': 'http://www.kxdb.com/dzbk/show.php?itemid=278', '2024-08-27': 'http://www.kxdb.com/dzbk/show.php?itemid=275', '2024-08-23': 'http://www.kxdb.com/dzbk/show.php?itemid=274', '2024-08-20': 'http://www.kxdb.com/dzbk/show.php?itemid=267', '2024-08-16': 'http://www.kxdb.com/dzbk/show.php?itemid=266', '2024-08-13': 'http://www.kxdb.com/dzbk/show.php?itemid=265', '2024-08-09': 'http://www.kxdb.com/dzbk/show.php?itemid=264', '2024-08-06': 'http://www.kxdb.com/dzbk/show.php?itemid=263', '2024-08-05': 'http://www.kxdb.com/dzbk/show.php?itemid=262', '2024-07-30': 'http://www.kxdb.com/dzbk/show.php?itemid=260', '2024-07-26': 'http://www.kxdb.com/dzbk/show.php?itemid=252', '2024-07-23': 'http://www.kxdb.com/dzbk/show.php?itemid=251', '2024-07-19': 'http://www.kxdb.com/dzbk/show.php?itemid=250', '2024-07-16': 'http://www.kxdb.com/dzbk/show.php?itemid=249', '2024-07-12': 'http://www.kxdb.com/dzbk/show.php?itemid=248', '2024-07-09': 'http://www.kxdb.com/dzbk/show.php?itemid=247', '2024-07-05': 'http://www.kxdb.com/dzbk/show.php?itemid=246', '2024-07-02': 'http://www.kxdb.com/dzbk/show.php?itemid=243', '2024-06-28': 'http://www.kxdb.com/dzbk/show.php?itemid=235', '2024-06-25': 'http://www.kxdb.com/dzbk/show.php?itemid=234', '2024-06-21': 'http://www.kxdb.com/dzbk/show.php?itemid=233', '2024-06-18': 'http://www.kxdb.com/dzbk/show.php?itemid=232', '2024-06-14': 'http://www.kxdb.com/dzbk/show.php?itemid=231', '2024-06-07': 'http://www.kxdb.com/dzbk/show.php?itemid=230', '2024-06-04': 'http://www.kxdb.com/dzbk/show.php?itemid=229', '2024-05-31': 'http://www.kxdb.com/dzbk/show.php?itemid=228', '2024-05-28': 'http://www.kxdb.com/dzbk/show.php?itemid=226', '2024-05-24': 'http://www.kxdb.com/dzbk/show.php?itemid=224', '2024-05-21': 'http://www.kxdb.com/dzbk/show.php?itemid=221', '2024-05-17': 'http://www.kxdb.com/dzbk/show.php?itemid=220', '2024-05-14': 'http://www.kxdb.com/dzbk/show.php?itemid=217', '2024-05-10': 'http://www.kxdb.com/dzbk/show.php?itemid=216', '2024-05-07': 'http://www.kxdb.com/dzbk/show.php?itemid=214', '2024-04-30': 'http://www.kxdb.com/dzbk/show.php?itemid=211', '2024-04-26': 'http://www.kxdb.com/dzbk/show.php?itemid=210', '2024-04-23': 'http://www.kxdb.com/dzbk/show.php?itemid=208', '2024-04-19': 'http://www.kxdb.com/dzbk/show.php?itemid=205', '2024-04-16': 'http://www.kxdb.com/dzbk/show.php?itemid=204', '2024-04-12': 'http://www.kxdb.com/dzbk/show.php?itemid=201', '2024-04-09': 'http://www.kxdb.com/dzbk/show.php?itemid=199', '2024-04-02': 'http://www.kxdb.com/dzbk/show.php?itemid=197', '2024-03-29': 'http://www.kxdb.com/dzbk/show.php?itemid=196', '2024-03-26': 'http://www.kxdb.com/dzbk/show.php?itemid=193', '2024-03-22': 'http://www.kxdb.com/dzbk/show.php?itemid=192', '2024-03-19': 'http://www.kxdb.com/dzbk/show.php?itemid=189', '2024-03-15': 'http://www.kxdb.com/dzbk/show.php?itemid=187', '2024-03-12': 'http://www.kxdb.com/dzbk/show.php?itemid=184', '2024-03-08': 'http://www.kxdb.com/dzbk/show.php?itemid=183', '2024-03-05': 'http://www.kxdb.com/dzbk/show.php?itemid=179', '2024-03-01': 'http://www.kxdb.com/dzbk/show.php?itemid=178', '2024-02-27': 'http://www.kxdb.com/dzbk/show.php?itemid=177', '2024-02-23': 'http://www.kxdb.com/dzbk/show.php?itemid=175', '2024-02-20': 'http://www.kxdb.com/dzbk/show.php?itemid=173', '2024-02-06': 'http://www.kxdb.com/dzbk/show.php?itemid=169', '2024-02-02': 'http://www.kxdb.com/dzbk/show.php?itemid=167', '2024-01-30': 'http://www.kxdb.com/dzbk/show.php?itemid=166', '2024-01-26': 'http://www.kxdb.com/dzbk/show.php?itemid=165', '2024-01-23': 'http://www.kxdb.com/dzbk/show.php?itemid=164', '2024-01-19': 'http://www.kxdb.com/dzbk/show.php?itemid=161', '2024-01-16': 'http://www.kxdb.com/dzbk/show.php?itemid=159', '2024-01-12': 'http://www.kxdb.com/dzbk/show.php?itemid=156', '2024-01-09': 'http://www.kxdb.com/dzbk/show.php?itemid=155', '2024-01-03': 'http://www.kxdb.com/dzbk/show.php?itemid=150', '2023-12-29': 'http://www.kxdb.com/dzbk/show.php?itemid=149', '2023-12-26': 'http://www.kxdb.com/dzbk/show.php?itemid=148', '2023-12-22': 'http://www.kxdb.com/dzbk/show.php?itemid=144', '2023-12-19': 'http://www.kxdb.com/dzbk/show.php?itemid=142', '2023-12-15': 'http://www.kxdb.com/dzbk/show.php?itemid=141', '2023-12-12': 'http://www.kxdb.com/dzbk/show.php?itemid=139', '2023-12-08': 'http://www.kxdb.com/dzbk/show.php?itemid=137', '2023-12-05': 'http://www.kxdb.com/dzbk/show.php?itemid=135', '2023-12-01': 'http://www.kxdb.com/dzbk/show.php?itemid=133', '2023-11-28': 'http://www.kxdb.com/dzbk/show.php?itemid=131', '2023-11-24': 'http://www.kxdb.com/dzbk/show.php?itemid=130', '2023-11-21': 'http://www.kxdb.com/dzbk/show.php?itemid=127', '2023-11-17': 'http://www.kxdb.com/dzbk/show.php?itemid=125', '2023-11-14': 'http://www.kxdb.com/dzbk/show.php?itemid=124', '2023-11-10': 'http://www.kxdb.com/dzbk/show.php?itemid=120', '2023-11-07': 'http://www.kxdb.com/dzbk/show.php?itemid=118', '2023-11-03': 'http://www.kxdb.com/dzbk/show.php?itemid=117', '2023-10-31': 'http://www.kxdb.com/dzbk/show.php?itemid=115', '2023-10-27': 'http://www.kxdb.com/dzbk/show.php?itemid=113', '2023-10-25': 'http://www.kxdb.com/dzbk/show.php?itemid=112', '2023-10-20': 'http://www.kxdb.com/dzbk/show.php?itemid=109', '2023-10-18': 'http://www.kxdb.com/dzbk/show.php?itemid=108', '2023-10-13': 'http://www.kxdb.com/dzbk/show.php?itemid=105', '2023-10-10': 'http://www.kxdb.com/dzbk/show.php?itemid=103', '2023-09-26': 'http://www.kxdb.com/dzbk/show.php?itemid=102', '2023-09-22': 'http://www.kxdb.com/dzbk/show.php?itemid=99', '2023-09-19': 'http://www.kxdb.com/dzbk/show.php?itemid=97', '2023-09-15': 'http://www.kxdb.com/dzbk/show.php?itemid=96', '2023-09-12': 'http://www.kxdb.com/dzbk/show.php?itemid=93', '2023-09-08': 'http://www.kxdb.com/dzbk/show.php?itemid=91', '2023-09-05': 'http://www.kxdb.com/dzbk/show.php?itemid=88', '2023-09-01': 'http://www.kxdb.com/dzbk/show.php?itemid=87', '2023-08-29': 'http://www.kxdb.com/dzbk/show.php?itemid=84', '2023-08-25': 'http://www.kxdb.com/dzbk/show.php?itemid=83', '2023-08-22': 'http://www.kxdb.com/dzbk/show.php?itemid=81', '2023-08-18': 'http://www.kxdb.com/dzbk/show.php?itemid=79', '2023-08-15': 'http://www.kxdb.com/dzbk/show.php?itemid=77', '2023-08-11': 'http://www.kxdb.com/dzbk/show.php?itemid=75', '2023-08-08': 'http://www.kxdb.com/dzbk/show.php?itemid=72', '2023-08-04': 'http://www.kxdb.com/dzbk/show.php?itemid=71', '2023-08-01': 'http://www.kxdb.com/dzbk/show.php?itemid=69', '2023-07-28': 'http://www.kxdb.com/dzbk/show.php?itemid=67', '2023-07-25': 'http://www.kxdb.com/dzbk/show.php?itemid=65', '2023-07-21': 'http://www.kxdb.com/dzbk/show.php?itemid=64', '2023-07-18': 'http://www.kxdb.com/dzbk/show.php?itemid=61', '2023-07-14': 'http://www.kxdb.com/dzbk/show.php?itemid=58', '2023-07-11': 'http://www.kxdb.com/dzbk/show.php?itemid=57', '2023-07-07': 'http://www.kxdb.com/dzbk/show.php?itemid=55', '2023-07-04': 'http://www.kxdb.com/dzbk/show.php?itemid=52', '2023-06-30': 'http://www.kxdb.com/dzbk/show.php?itemid=53', '2023-06-27': 'http://www.kxdb.com/dzbk/show.php?itemid=47', '2023-06-21': 'http://www.kxdb.com/dzbk/show.php?itemid=45', '2023-06-16': 'http://www.kxdb.com/dzbk/show.php?itemid=43', '2023-06-13': 'http://www.kxdb.com/dzbk/show.php?itemid=41', '2023-06-09': 'http://www.kxdb.com/dzbk/show.php?itemid=39', '2023-06-06': 'http://www.kxdb.com/dzbk/show.php?itemid=36', '2023-06-02': 'http://www.kxdb.com/dzbk/show.php?itemid=35', '2023-05-30': 'http://www.kxdb.com/dzbk/show.php?itemid=33', '2023-05-26': 'http://www.kxdb.com/dzbk/show.php?itemid=31', '2023-05-23': 'http://www.kxdb.com/dzbk/show.php?itemid=29', '2023-05-19': 'http://www.kxdb.com/dzbk/show.php?itemid=27', '2023-05-16': 'http://www.kxdb.com/dzbk/show.php?itemid=26', '2023-05-12': 'http://www.kxdb.com/dzbk/show.php?itemid=23', '2023-05-09': 'http://www.kxdb.com/dzbk/show.php?itemid=21', '2023-04-28': 'http://www.kxdb.com/dzbk/show.php?itemid=19', '2023-04-25': 'http://www.kxdb.com/dzbk/show.php?itemid=17', '2023-04-23': 'http://www.kxdb.com/dzbk/show.php?itemid=4', '2023-04-21': 'http://www.kxdb.com/dzbk/show.php?itemid=2'}

def get_date():
    for i in range(1, 1 + 1):
        response = requests.get(f'http://www.kxdb.com/dzbk/list.php?catid=33&page={i}', headers=headers, verify=False)
        html = etree.HTML(response.content.decode())
        for data in html.xpath("//div[@class='catlist']/ul/li"):
            date = "".join(data.xpath("./i/text()"))
            if date not in date_dict:
                date_url = "".join(data.xpath("./a/@href"))
                date_dict[date] = date_url




def get_kexuedao_paper(paper_time, queue_id, webpage_id):
    get_date()
    # 将today的格式进行改变
    day = paper_time
    url = date_dict.get(paper_time)
    if url is None:
        raise Exception(f'该日期没有报纸')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode()
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@id='article']/p/a")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./text()")).strip()

            # 版面的pdf
            bm_pdf = "".join(bm.xpath("./@href"))
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
                up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                pdf_set.add(bm_pdf)
                # 上传到报纸的图片或PDF
                insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

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


# get_kexuedao_paper('2024-09-20', 111, 1111)
