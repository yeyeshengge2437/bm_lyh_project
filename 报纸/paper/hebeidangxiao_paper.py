import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree

paper = "河北党校报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '_gscu_1321609988=28437110we1szf14; Hm_lvt_fc19c432c6dd37e78d6593b2756fb674=1728437111,1728956597; Hm_lpvt_fc19c432c6dd37e78d6593b2756fb674=1728956597; HMACCOUNT=FDD970C8B3C27398; _gscbrs_1321609988=1; _gscs_1321609988=28956597lh7okt14|pv:1; _yfx_session_10000019=%7B%22_yfx_firsttime%22%3A%221728437110570%22%2C%22_yfx_lasttime%22%3A%221728956597529%22%2C%22_yfx_visittime%22%3A%221728956597529%22%2C%22_yfx_domidgroup%22%3A%221728956597529%22%2C%22_yfx_domallsize%22%3A%22100%22%2C%22_yfx_cookie%22%3A%2220241009092510574953895827662525%22%2C%22_yfx_returncount%22%3A%221%22%7D',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}
date_dict = {'2024-10-05': 'http://www.hebdx.com/2024-10/05/c53a40a7-5052-4e03-ba46-7a8a2bfee931.pdf',
             '2024-09-20': 'http://www.hebdx.com/2024-09/20/b5503221-036d-4c10-a781-53de97316eaf.pdf',
             '2024-09-05': 'http://www.hebdx.com/2024-09/05/30cab02c-0a4d-41c6-90a4-caa14af7adc4.pdf',
             '2024-07-05': 'http://www.hebdx.com/2024-07/05/83a92974-ccd3-46d0-b467-95e198954d97.pdf',
             '2024-06-20': 'http://www.hebdx.com/2024-06/20/57c055a7-1deb-4466-8c61-bb44634b7dd8.pdf',
             '2024-06-05': 'http://www.hebdx.com/2024-06/05/8634f60d-4ebf-4e1d-88b5-be71d5166fe9.pdf',
             '2024-05-20': 'http://www.hebdx.com/2024-05/20/e7eed100-d112-4b90-aa82-5ea6f4b88304.pdf',
             '2024-05-05': 'http://www.hebdx.com/2024-05/05/014beebe-8c57-4263-9a3d-a39e207b88fe.pdf',
             '2024-04-20': 'http://www.hebdx.com/2024-04/20/0d07ca42-6172-4db8-aff6-c8fae6025b2d.pdf',
             '2024-04-05': 'http://www.hebdx.com/2024-04/05/d90ddc46-161f-4d02-9756-1415144e3487.pdf',
             '2024-03-20': 'http://www.hebdx.com/2024-03/20/a9e7da84-333e-4dfa-ae15-661ee54f47ce.pdf',
             '2024-03-05': 'http://www.hebdx.com/2024-03/05/9ebb0507-32f4-4968-aa4d-8256ea8c766e.pdf',
             '2024-01-05': 'http://www.hebdx.com/2024-01/05/55813b58-166e-4b0f-9f44-ce145e3331da.pdf',
             '2023-12-20': 'http://www.hebdx.com/2023-12/20/de3477e3-6d33-4e96-bb9f-52cc88e9195d.pdf',
             '2023-12-05': 'http://www.hebdx.com/2023-12/05/4aadea4b-0450-4fef-b225-efbe122724ee.pdf',
             '2023-11-20': 'http://www.hebdx.com/2023-11/20/cfb628cb-d45f-42bd-bf6d-09e51326bbc8.pdf',
             '2023-11-05': 'http://www.hebdx.com/2023-11/05/6df78c00-4a8b-4a7e-965f-f912af53d3c9.pdf',
             '2023-10-20': 'http://www.hebdx.com/2023-10/20/881b6e3c-17b5-471d-8192-8174c11d7af0.pdf',
             '2023-10-05': 'http://www.hebdx.com/2023-10/05/e6c7dd2e-d768-4ff6-b74b-10b250d384e1.pdf',
             '2023-09-20': 'http://www.hebdx.com/2023-09/20/b476a33a-5a66-4c89-80a8-c4e29ce3a6d6.pdf',
             '2023-09-05': 'http://www.hebdx.com/2023-09/05/f1c81c13-2c58-4e75-bb27-31016d960a2b.pdf',
             '2023-07-05': 'http://www.hebdx.com/2023-07/05/7cb67c92-d937-4cc1-8793-80937f1b6b4c.pdf',
             '2023-06-20': 'http://www.hebdx.com/2023-06/20/830000fa-7f66-459d-abb5-b218f462ab9d.pdf',
             '2023-06-05': 'http://www.hebdx.com/2023-06/05/83f5f1d4-ee60-46bc-b4a7-0601b46ca669.pdf',
             '2023-05-20': 'http://www.hebdx.com/2023-05/20/548851a9-b4ac-41fb-bcf9-2fd5feaa8328.pdf',
             '2023-05-05': 'http://www.hebdx.com/2023-05/05/28e962b7-134e-48ed-aa7e-247a3dc2b803.pdf',
             '2023-04-20': 'http://www.hebdx.com/2023-04/20/59953c0e-a6d9-4c1c-9c3c-7605abe5608e.pdf',
             '2023-04-05': 'http://www.hebdx.com/2023-04/05/19db48a9-96c5-47a7-ad07-fe6f16fd76f2.pdf',
             '2023-03-20': 'http://www.hebdx.com/2023-03/20/e52eedb9-e841-4c41-b140-65731a4072c8.pdf',
             '2023-03-05': 'http://www.hebdx.com/2023-03/05/db251ec0-f841-4951-8132-8156c3e84b23.pdf',
             '2023-01-05': 'http://www.hebdx.com/2023-01/05/eb9107dd-52f6-4876-a8ab-acdc4d4f17d9.pdf',
             '2022-12-20': 'http://www.hebdx.com/2022-12/20/20cdd957-ccf0-4bbc-85fc-1179bc9f2ba1.pdf',
             '2022-12-15': 'http://www.hebdx.com/2022-12/15/ee4abb01-3456-4e75-b849-8c4a7d115842.pdf',
             '2022-12-05': 'http://www.hebdx.com/2022-12/05/315a5973-3799-4d48-85c0-bd61a470e391.pdf',
             '2022-11-20': 'http://www.hebdx.com/2022-11/20/a776d191-e563-41c3-bb89-14e4eefd0450.pdf',
             '2022-11-05': 'http://www.hebdx.com/2022-11/05/801bfae3-a7d2-41d1-9c75-0c782435b899.pdf',
             '2022-10-20': 'http://www.hebdx.com/2022-10/20/0de56ef6-1de6-4995-b81b-6c301de7c98e.pdf',
             '2022-10-05': 'http://www.hebdx.com/2022-10/05/a5edfaf5-afe0-4226-8fe6-cfce024cb7ca.pdf',
             '2022-09-20': 'http://www.hebdx.com/2022-09/20/bfc1d6f7-f0e4-4bba-9070-08cf38d38788.pdf',
             '2022-09-05': 'http://www.hebdx.com/2022-09/05/fa1efbfc-0725-4873-903d-98dd11f799eb.pdf',
             '2022-07-05': 'http://www.hebdx.com/2022-07/05/bee5086c-af51-4c73-b85c-ccca90721b93.pdf',
             '2022-06-21': 'http://www.hebdx.com/2022-06/21/48bb3c2d-4fad-48b4-9f35-4f9646a1dbbc.pdf',
             '2022-06-05': 'http://www.hebdx.com/2022-06/05/b5a16cf7-bb3c-4c51-bce7-80688373efe7.pdf',
             '2022-05-20': 'http://www.hebdx.com/2022-05/20/fe77bda4-57b0-4cb4-9a85-1dff115a39b9.pdf',
             '2022-05-05': 'http://www.hebdx.com/2022-05/05/2f4fc2c2-c953-42a8-89e7-da619ea8bf9c.pdf',
             '2022-04-20': 'http://www.hebdx.com/2022-04/20/5c1f0462-87c3-4d6f-9b4e-f5861c233e3a.pdf',
             '2022-04-05': 'http://www.hebdx.com/2022-04/05/62d5f6fa-1ef2-4de0-882c-64e8efe0d3e6.pdf',
             '2022-03-22': 'http://www.hebdx.com/2022-03/22/14b27b20-cf73-4d1f-8465-2e87a3eaa85c.pdf',
             '2022-03-06': 'http://www.hebdx.com/2022-03/16/14815324-2191-4b72-b179-40ca2e4eb053.pdf',
             '2022-01-05': 'http://www.hebdx.com/2022-03/16/f751ddb9-6a38-4aa4-8312-3fa6c16ef3eb.pdf',
             '2021-12-21': 'http://www.hebdx.com/2022-03/16/e05163f5-7666-41a0-a2a4-f6b0c3fecf86.pdf',
             '2021-12-06': 'http://www.hebdx.com/2022-03/16/3812ea4e-26a1-45cf-8ebe-6b1b103c9f17.pdf',
             '2021-11-22': 'http://www.hebdx.com/2022-03/16/017a25b9-9fae-42ef-963d-1818e0d032ce.pdf',
             '2021-11-05': 'http://www.hebdx.com/2022-03/16/dbe729da-292e-4c71-a1ea-b92597298c35.pdf',
             '2021-10-20': 'http://www.hebdx.com/2022-03/16/279febe0-9ce8-4773-85e9-8182bf95e87d.pdf',
             '2021-10-08': 'http://www.hebdx.com/2022-03/16/735f339b-7ac9-4e9a-9d6d-17331dc30a07.pdf',
             '2021-09-22': 'http://www.hebdx.com/2022-03/16/1d345f43-71fd-4246-8fbd-ecc3678683f7.pdf',
             '2021-09-05': 'http://www.hebdx.com/2022-03/16/01411bcf-b6b2-4bd1-9d8c-fb1665d1e6a1.pdf',
             '2021-07-07': 'http://www.hebdx.com/2022-03/16/0952a784-0d20-4904-ac73-a723fb53d54f.pdf',
             '2021-06-21': 'http://www.hebdx.com/2022-03/16/cf70ba57-a63e-484b-91e1-b45639e90650.pdf',
             '2021-06-05': 'http://www.hebdx.com/2022-03/16/3d12c168-e2ca-44d7-a9af-5225937e1ced.pdf',
             '2021-05-20': 'http://www.hebdx.com/2022-03/16/8765a7df-1791-4488-ad87-61bf808389bc.pdf',
             '2021-05-06': 'http://www.hebdx.com/2022-03/16/849018ea-f5bd-468f-9a48-3eb2f9245701.pdf',
             '2021-04-20': 'http://www.hebdx.com/2022-03/16/9fd7299c-e64e-467e-8f7d-c3bcd0edcd97.pdf',
             '2021-04-06': 'http://www.hebdx.com/2022-03/16/4b66a687-a1e6-4764-8271-cdab7aba7904.pdf',
             '2021-03-22': 'http://www.hebdx.com/2022-03/16/7c90a24d-d6cc-470c-b898-6b7524473656.pdf',
             '2021-03-07': 'http://www.hebdx.com/2022-03/16/921d7f03-9a76-42d3-bb64-499051cc7b70.pdf',
             '2021-03-11': 'http://www.hebdx.com/2022-03/16/6c5c9fef-1ed6-4cbd-a5fb-2e1841f9d458.pdf',
             '2021-02-26': 'http://www.hebdx.com/2021-02/26/5e25a810-612a-42db-9286-7b58a09c4d4c.pdf'}


def get_date():
    for i in range(1, 1 + 1):
        if i == 1:
            url = 'http://www.hebdx.com/node_358332.htm'
        else:
            url = f'http://www.hebdx.com/node_358332_{i}.htm'
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            content = response.content.decode()
            html_1 = etree.HTML(content)
            # 获取所有pdf的的链接
            all_pdf = html_1.xpath("//div[@class='list']/li")
            for pdf in all_pdf:
                pdf_str = "".join(pdf.xpath("./span/text()")).strip()
                # 匹配日期2024-10-05 07:05:10
                pdf_time = re.findall(r'\d{4}-\d{2}-\d{2}', pdf_str)[0]
                pdf_url = "".join(pdf.xpath("./a/@href"))
                if pdf_time not in date_dict:
                    date_dict[pdf_time] = pdf_url
    return date_dict


def get_hebeidangxiao_paper(paper_time, queue_id, webpage_id):
    # 将today的格式进行改变
    day = paper_time
    if paper_time > '2024-10-05':
        get_date()
    if paper_time not in date_dict and paper_time <= '2024-10-05':
        raise Exception(f'该日期没有报纸')
    if paper_time in date_dict:
        bm_pdf = date_dict[paper_time]
        bm_name = paper_time
        bm_url = bm_pdf
        pdf_set = set()

        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        create_date = datetime.now().strftime('%Y-%m-%d')
        # 上传到测试数据库
        conn_test = mysql.connector.connect(
            host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
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
        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

# get_hebeidangxiao_paper('2024-10-05', 111, 1111)
