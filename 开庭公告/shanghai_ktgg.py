import datetime
import time
import mysql.connector
from lxml import etree
import requests
from a_ktgg_api import judge_repeat_case
from tool.mysql_connection_pool import get_connection

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'secure; JSESSIONID=14FF2A7D19DEF0295A6E021265C0EE02',
    'Pragma': 'no-cache',
    'Referer': 'https://www.hshfy.sh.cn/shwfy/ssfww/ktgg.jsp',
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


def get_shcourt_info(from_queue, webpage_id):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    month_time = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    origin = "上海法院诉讼服务网"
    origin_domain = "hshfy.sh.cn"
    params = {
        'pagesnum': '1',
        'fyList': '',
        'spc': '',
        'yg': '',
        'bg': '',
        'ktrqks': f'{str(now_time)}',
        'ktrqjs': f'{str(month_time)}',
        'ah': '',
        'ktlx': '',
    }

    response = requests.get('https://www.hshfy.sh.cn/shwfy/ssfww/ktgg.jsp', params=params, headers=headers)
    res = response.text
    res_html = etree.HTML(res)
    page_num = ''.join(res_html.xpath("//div[@class='paging']//i[@class='blue']/text()"))
    if page_num.isalnum():
        total_num = int(page_num)
        pages = total_num // 6 + 1
        pages = pages // 2
        for page in range(1, pages + 1):
            print(page)
            params = {
                'pagesnum': f'{page}',
                'fyList': '',
                'spc': '',
                'yg': '',
                'bg': '',
                'ktrqks': f'{str(now_time)}',
                'ktrqjs': f'{str(month_time)}',
                'ah': '',
                'ktlx': '',
            }
            response = requests.get('https://www.hshfy.sh.cn/shwfy/ssfww/ktgg.jsp', params=params, headers=headers)
            time.sleep(3)
            res = response.text
            res_html = etree.HTML(res)
            kt_list = res_html.xpath("//tr")
            for kt in kt_list:
                court_name = ''.join(kt.xpath("./td[1]/a/@title")) + "法院"
                court_room = ''.join(kt.xpath("./td[2]/a/@title"))
                open_time = ''.join(kt.xpath("./td[3]/a/@title"))
                case_no = ''.join(kt.xpath("./td[4]/a/@title"))
                if judge_repeat_case(case_no):
                    continue
                case_name = ''.join(kt.xpath("./td[5]/a/@title"))
                department = ''.join(kt.xpath("./td[6]/a/@title"))
                room_leader = ''.join(kt.xpath("./td[7]/a/@title"))
                members = "原告/上诉人：" + ''.join(kt.xpath("./td[8]/a/@title")) + "，被告/被上诉人：" + ''.join(
                    kt.xpath("./td[9]/a/@title"))
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 设置创建日期
                create_date = datetime.datetime.now().strftime('%Y-%m-%d')
                # 连接到测试库
                try:
                    conn_test = get_connection()
                    cursor_test = conn_test.cursor()
                    # 将数据插入到表中
                    insert_sql = "INSERT INTO col_case_open (case_no, cause,  court,  open_time, court_room, room_leader, department, members, origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,%s,%s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql, (
                        case_no, case_name, court_name, open_time, court_room, room_leader,
                        department, members,
                        origin,
                        origin_domain, create_time, create_date, from_queue, webpage_id))
                    # print("插入成功")
                    conn_test.commit()
                    cursor_test.close()
                    conn_test.close()
                except:
                    continue
                print(
                    f"法院：{court_name}，法庭：{court_room}，开庭时间：{open_time}，案号：{case_no}，案由：{case_name}，庭长：{room_leader}，部门：{department}，当事人：{members}")


# get_shcourt_info(11, 22)