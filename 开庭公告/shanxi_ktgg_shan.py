import datetime
import re
import time
import mysql.connector
import requests
from lxml import etree

cookies = {
    'clientlanguage': 'zh_CN',
    'JSESSIONID': '60C78754C8A56A05AAC4E847967341D8',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'clientlanguage=zh_CN; JSESSIONID=60C78754C8A56A05AAC4E847967341D8',
    'Pragma': 'no-cache',
    'Referer': 'https://www.shanxify.gov.cn/ktggPage.jspx?channelId=307&listsize=192&pagecur=1&pagego=add',
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

def get_sxcourt_info_shan(from_queue, webpage_id):
    for page in range(1, 180 + 1):
        params = {
            'channelId': '307',
            'listsize': '192',
            'pagecur': f'{page}',
            'pagego': 'add',
        }
        origin = "山西法院诉讼服务网"
        origin_domain = "shanxify.gov.cn"
        response = requests.get('https://www.shanxify.gov.cn/ktggPage.jspx', params=params, cookies=cookies, headers=headers)
        res = response.text
        res_html = etree.HTML(res)
        kt_list = res_html.xpath("//div[@class='text']/ul/li")
        for kt in kt_list:
            text = ''.join(kt.xpath("./a/text()"))
            url = ''.join(kt.xpath("./a/@href"))
            con_res = requests.get(url, cookies=cookies, headers=headers)
            time.sleep(2)
            con_res_html = etree.HTML(con_res.text)
            content = ''.join(con_res_html.xpath("//div[@class='text']/h1//text()"))
            open_time = ''.join(re.findall("(.*?)在", content))
            court_name = ''.join(re.findall("在(.*?法院)", content))
            court_room = ''.join(re.findall("法院(.*?)开庭", content))
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
            insert_sql = "INSERT INTO col_case_open ( court,  open_time, court_room, department,content, origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor_test.execute(insert_sql, (
                court_name, open_time, court_room,
                department, content,
                origin,
                origin_domain, create_time, create_date, from_queue, webpage_id))
            # print("插入成功")
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
            print(f"开庭时间：{open_time}, 法院：{court_name}, 地点：{court_room}, 内容：{content}, 链接：{url}")
