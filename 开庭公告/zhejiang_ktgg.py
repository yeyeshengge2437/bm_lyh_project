import re
import time
from a_ktgg_api import judge_repeat_case
import requests
from lxml import etree
import datetime
import mysql.connector
from tool.mysql_connection_pool import get_connection

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=E552FC688CF402DB9778675E446AFE48; https_waf_cookie=0c97ce0b-77ca-49961390febb99d957fc0576048cfd5f97a6',
    'Pragma': 'no-cache',
    'Referer': 'https://www.zjsfgkw.gov.cn/jkts/search/ktgglist.do',
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
origin = "浙江法院网"
origin_domain = "zjsfgkw.gov.cn"


def get_zjcourt_info(from_queue, webpage_id):
    params = {
        'fybh': '',
        'bg': '',
        'pageNo': '1',
    }
    response = requests.get('https://www.zjsfgkw.gov.cn/jkts/search/ktgglist.do', params=params, headers=headers)
    res_html = response.text
    time.sleep(2)
    html_res_1 = etree.HTML(res_html)
    page_str = ''.join(html_res_1.xpath("//div[@id='pagination']/span//text()"))
    page_num = ''.join(re.findall(r'共 (\d+) 条', page_str))
    tager_num = int(page_num) // 10 + 1
    for page in range(1, tager_num + 1):
        params = {
            'fybh': '',
            'bg': '',
            'pageNo': f'{page}',
        }

        response = requests.get('https://www.zjsfgkw.gov.cn/jkts/search/ktgglist.do', params=params, headers=headers)
        res = response.text
        time.sleep(2)
        html_res = etree.HTML(res)
        list_data = html_res.xpath("//div[@class='jsearch-result-box']")
        for data in list_data:
            court = ''.join(data.xpath(".//td[@class='td'][1]/text()")).strip()
            court_room = ''.join(data.xpath(".//td[@class='td'][2]/text()")).strip()
            open_time = ''.join(data.xpath(".//td[@class='td'][3]/text()")).strip()
            case_no = ''.join(data.xpath(".//td[@class='td'][5]/text()")).strip()
            cause = ''.join(data.xpath(".//td[@class='td'][6]/text()")).strip()
            room_leader = ''.join(data.xpath(".//td[@class='td'][8]/text()")).strip()
            members = ''.join(data.xpath(".//td[@class='td'][9]/text()")).strip() + ',' + ''.join(data.xpath(".//td[@class='td'][10]/text()")).strip()
            if judge_repeat_case(case_no):
                continue
            # print(f"法院：{court}，法庭：{court_room}，开庭时间：{open_time}，案号：{case_no}，案由：{cause}，审判长：{room_leader}，成员：{members}")
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 设置创建日期
            create_date = datetime.datetime.now().strftime('%Y-%m-%d')
            department = ''
            # 连接到测试库
            try:
                conn_test = get_connection()
                cursor_test = conn_test.cursor()
                # 将数据插入到表中
                insert_sql = "INSERT INTO col_case_open (case_no,  court, members, open_time, court_room, room_leader, department,  origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql, (
                    case_no, court, members, open_time, court_room, room_leader,
                    department,
                    origin,
                    origin_domain, create_time, create_date, from_queue, webpage_id))
                # print("插入成功")
                conn_test.commit()
                cursor_test.close()
                conn_test.close()
            except:
                print("数据库连接超时")
                continue


