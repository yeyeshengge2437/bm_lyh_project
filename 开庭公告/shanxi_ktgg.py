import datetime
import re
import time
import mysql.connector
import requests
from a_ktgg_api import judge_repeat_case

chinese_num_map = {
    '二十日': "20日", '二十一日': "21日", '二十二日': "22日", '二十三日': "23日", '二十四日': "24日",
    '二十五日': "25日", '二十六日': "26日", '二十七日': "27日", '二十八日': "28日", '二十九日': "29日",
    '三十日': "30日", '三十一日': "31日", '十日': "10日", '十一日': "11日", '十二日': "12日", '十三日': "13日",
    '十四日': "14日", '十五日': "15日", '十六日': "16日", '十七日': "17日",
    '十八日': "18日", '十九日': "19日",
    '一日': "1日", '二日': "2日", '三日': "3日", '四日': "4日", '五日': "5日", '六日': "6日", '七日': "7日",
    '八日': "8日", '九日': "9日",
    '十一月': "11月", '十二月': "12月", '一月': "1月", '二月': "2月", '三月': "3月", '四月': "4月", '五月': "5月",
    '六月': "6月", '七月': "7月", '八月': "8月", '九月': "9月",
    '十月': "10月", "〇": '0', "一": '1', "二": '2', "三": '3', "四": '4', "五": '5', "六": '6', "七": '7', "八": '8',
    "九": '9'
}


def chinese_to_arabic(date_str):
    for chinese, arabic in chinese_num_map.items():
        date_str = date_str.replace(chinese, arabic)
    return date_str


cookies = {
    'JSESSIONID': '65BE0DF10785CEDB5A010146249B6F74',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'JSESSIONID=65BE0DF10785CEDB5A010146249B6F74',
    'Origin': 'http://sxgaofa.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://sxgaofa.cn/sxssfw/ktgg/toListKtggNL.shtml',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_sxcourt_1_info(from_queue, webpage_id):
    origin = '陕西法院诉讼服务网'
    origin_domain = 'sxgaofa.cn'
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    month_time = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')

    data = {
        'fydm': '',
        'kssj': f'{str(now_time)}',
        'jssj': f'{str(month_time)}',
        'page': '1',
    }

    response = requests.post(
        'http://sxgaofa.cn/sxssfw/ktgg/ktggList.shtml;jsessionid=65BE0DF10785CEDB5A010146249B6F74',
        headers=headers,
        data=data,
        verify=False,
    )
    json_value = response.json()
    page_court = json_value.get('pageCount')
    for page_num in range(1, page_court + 1):
        data = {
            'fydm': '',
            'kssj': f'{str(now_time)}',
            'jssj': f'{str(month_time)}',
            'page': f'{page_num}',
        }
        res = requests.post(
            'http://sxgaofa.cn/sxssfw/ktgg/ktggList.shtml;jsessionid=65BE0DF10785CEDB5A010146249B6F74',
            headers=headers,
            data=data,
            verify=False,
        )
        value = res.json()
        time.sleep(2)
        for item in value.get('data'):
            case_no = item.get('ahqc')
            if judge_repeat_case(case_no):
                continue
            content = item.get('ggnr')
            court = item.get('fymc')
            start_time_1 = ''.join(re.findall(r'本院定于(.*?)到', content))
            start_time_2 = chinese_to_arabic(start_time_1)
            open_time = start_time_2.replace('年', '-').replace('月', '-').replace('日', ' ')
            court_room = ''.join(re.findall(rf'在(.*?)开庭审理', content))

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
            insert_sql = "INSERT INTO col_case_open (case_no,  court,  open_time, court_room,  department,  origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor_test.execute(insert_sql, (
                case_no, court, open_time, court_room,
                department,
                origin,
                origin_domain, create_time, create_date, from_queue, webpage_id))
            # print("插入成功")
            conn_test.commit()
            cursor_test.close()
            conn_test.close()
