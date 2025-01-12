
import datetime
import time
import mysql.connector
import requests
from a_ktgg_api import judge_repeat_case

# 请求 URL
url = "https://ssfw.xzfy.gov.cn/lawsuit/api/case-center/v1/third/court/external/getCourtAnnouncementInfo"

# 请求头
headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "x-requested-with": "XMLHttpRequest"
}


def get_xzcourt_info(from_queue, webpage_id):
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    year_time = (datetime.datetime.now() + datetime.timedelta(days=-365)).strftime('%Y%m%d')
    origin = '徐州诉讼服务网'
    origin_domain = 'ssfw.xzfy.gov.cn'
    # 请求体
    data = {
        "ah": "",  # 根据实际情况填写
        "curPage": 1,
        "ktrqBegin": f"{now_time}",
        "pageSize": 15,
        "slfy": "3203"
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    value1 = response.json()
    pages = value1["data"]["pages"]
    for page in range(1, pages + 1):
        data = {
            "ah": "",  # 根据实际情况填写
            "curPage": page,
            "ktrqBegin": f"{now_time}",
            "pageSize": 15,
            "slfy": "3203"
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
                brief = value.get('ay')
                members = value.get('dsr')
                open_time = value.get('ktrq') + ' ' + value.get('kssj')
                court_room = value.get('ktft')
                room_leader = value.get('hycy')
                department = value.get('cbbmDesc')
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 设置创建日期
                create_date = datetime.datetime.now().strftime('%Y-%m-%d')
                try:
                    conn_test = mysql.connector.connect(
                        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
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
                    continue
                # print(
                #     f'法院：{court_name}, 案号：{case_no}, 案由：{brief}, 当事人：{members}, 开庭时间：{open_time}, 法庭：{court_room}, 承办人：{room_leader}')
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print("响应内容:", response.text)


# get_jscourt_info(11, 22)
