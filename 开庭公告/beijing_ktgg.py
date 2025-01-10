import datetime
import re
import time
from a_ktgg_api import judge_repeat_invest
import requests
from lxml import etree
import mysql.connector

cookies = {
    'thguid-r': '1711809233818742784',
    '__jsluid_s': '7ee7ac47e9431f68cf26dd0f82cfdbdd',
    'vh2PJqrvyx': 'MDAwM2IyYWYxZTQwMDAwMDAwMDQwUE9ofy8xNzM2MjY0MDQ1',
    '6JDgKK8lEy': 'MDAwM2IyYWYxZTQwMDAwMDAwMDMwXlUXHhAxNzM2MjY0MDQ1',
    'JSESSIONID': 'node0vlg89ue3ilbu1nfjtdqhqcojq8517265.node0',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'thguid-r=1711809233818742784; __jsluid_s=7ee7ac47e9431f68cf26dd0f82cfdbdd; vh2PJqrvyx=MDAwM2IyYWYxZTQwMDAwMDAwMDQwUE9ofy8xNzM2MjY0MDQ1; 6JDgKK8lEy=MDAwM2IyYWYxZTQwMDAwMDAwMDMwXlUXHhAxNzM2MjY0MDQ1; JSESSIONID=node0vlg89ue3ilbu1nfjtdqhqcojq8517265.node0',
    'Pragma': 'no-cache',
    'Referer': 'https://www.bjcourt.gov.cn/ktgg/index.htm?c=&court=&start=2025-01-07&end=2025-02-07&type=&p=2',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
origin = "北京法院审判信息网"
origin_domain = "bjcourt.gov.cn"


def get_bjcourt_info(from_queue, webpage_id):
    for page in range(1, 10):
        params = {
            'c': '',
            'court': '',
            'start': '2025-01-07',
            'end': '2025-02-07',
            'type': '',
            'p': f'{page}',
        }

        response = requests.get('https://www.bjcourt.gov.cn/ktgg/index.htm', params=params, headers=headers)
        res_html = etree.HTML(response.text)
        time.sleep(2)
        kt_list = res_html.xpath("//ul[@class='ul_news_long']/li")
        for kt in kt_list:
            url = "https://www.bjcourt.gov.cn/" + ''.join(kt.xpath("./a/@href"))
            if judge_repeat_invest(url):
                continue
            content = ''.join(kt.xpath("./a/@title"))
            month = ''.join(re.findall(r'(\d+)月', content))
            day = ''.join(re.findall(r'(\d+)日', content))
            hour = "".join(re.findall(r' (\d+:\d+)', content))
            open_time = f"2025-{month}-{day} {hour}"
            court = "".join(re.findall(r'\d+，(.*?法院)', content))
            court_name = re.sub(r'在', '', court)
            court_room = "".join(re.findall(r'法院(.*?)依法', content))
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 设置创建日期
            create_date = datetime.datetime.now().strftime('%Y-%m-%d')
            department = ''
            # 连接到测试库
            conn_test = mysql.connector.connect(
                host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database="col"
            )
            cursor_test = conn_test.cursor()
            # 将数据插入到表中
            insert_sql = "INSERT INTO col_case_open (court,  open_time, court_room, department, origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor_test.execute(insert_sql, (
                court_name, open_time, court_room,
                department,
                origin,
                origin_domain, create_time, create_date, from_queue, webpage_id))
            # print("插入成功")
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
            # print(f"时间：{open_time},法院：{court_name},法庭：{court_room},内容：{content},链接：{url}")

# get_bgcourt_info(111,222)
