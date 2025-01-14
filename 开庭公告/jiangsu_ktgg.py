import datetime
import time
import mysql.connector
import requests
from a_ktgg_api import judge_repeat_case
from tool.mysql_connection_pool import get_connection

# 请求 URL
url = "https://ssfw.jsfy.gov.cn/lawsuit/api/case-center/v1/court/main/getCourtAnnouncementInfo"

# 请求头
headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "x-requested-with": "XMLHttpRequest"
}
def get_jscourt_info(from_queue, webpage_id):
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    year_time = (datetime.datetime.now() + datetime.timedelta(days=-365)).strftime('%Y%m%d')
    origin = '江苏法院诉讼服务网'
    origin_domain = 'ssfw.jsfy.gov.cn'
    # 请求体
    data = {
        "ah": "",
        "captcha": "w4yd",
        "captchaId": "387c3d742430494fac045f797723e717",
        "curPage": 1,
        "fydm": "320000",
        "ktrqBegin": f"{str(year_time)}",
        "ktrqEnd": f"{str(now_time)}",
        "pageSize": "20",
        "searchType": "2"
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    value1 = response.json()
    pages = value1["data"]["pages"]
    for page in range(1, pages+1):
        data = {
            "ah": "",
            "captcha": "w4yd",
            "captchaId": "387c3d742430494fac045f797723e717",
            "curPage": page,
            "fydm": "320000",
            "ktrqBegin": f"{str(year_time)}",
            "ktrqEnd": f"{str(now_time)}",
            "pageSize": "20",
            "searchType": "2"
        }
        response = requests.post(url, headers=headers, json=data)
        time.sleep(2)
        # 打印响应结果
        if response.status_code == 200:
            value_list = response.json()["data"]["records"]
            for value in value_list:
                court_name = value.get('fymc')
                case_no = value.get('ah')
                if judge_repeat_case(case_no):
                    continue
                brief = value.get('aymc')
                members = value.get('dsr')
                open_time = value.get('ktrq') + ' ' + value.get('kssj')
                court_room = value.get('ktdd')
                room_leader = value.get('hycy')
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 设置创建日期
                create_date = datetime.datetime.now().strftime('%Y-%m-%d')
                department = ''
                # 连接到测试库
                try:
                    conn_test = get_connection()
                    cursor_test = conn_test.cursor()
                    # 将数据插入到表中
                    insert_sql = "INSERT INTO col_case_open (case_no, cause,  court,  open_time, court_room, room_leader, department, members, origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,%s,%s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql, (
                        case_no, brief, court_name, open_time, court_room, room_leader,
                        department,members,
                        origin,
                        origin_domain, create_time, create_date, from_queue, webpage_id))
                    # print("插入成功")
                    conn_test.commit()
                    cursor_test.close()
                    conn_test.close()
                except:
                    print("数据库连接超时")
                    continue
                # print(f'法院：{court_name}, 案号：{case_no}, 案由：{brief}, 当事人：{members}, 开庭时间：{open_time}, 法庭：{court_room}, 承办人：{room_leader}')
        else:
            print(f"请求失败，状态码: {response.status_code}")
