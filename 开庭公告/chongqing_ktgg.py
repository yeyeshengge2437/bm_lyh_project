import datetime
import re
import time
import mysql.connector
import requests
from a_ktgg_api import judge_repeat_case
from tool.mysql_connection_pool import get_connection

courts = {
    "M00": "重庆市高级人民法院",
    "M10": "重庆市第一中级人民法院",
    "M13": "重庆市江北区人民法院",
    "M14": "重庆市沙坪坝区人民法院",
    "M17": "重庆市北碚区人民法院",
    "M1A": "重庆市长寿区人民法院",
    "M1D": "重庆市渝北区人民法院",
    "M1F": "重庆市合川区人民法院",
    "M1G": "重庆市潼南区人民法院",
    "M1H": "重庆市铜梁区人民法院",
    "M1J": "重庆市大足区人民法院",
    "M1L": "重庆市璧山区人民法院",
    "M1M": "重庆铁路运输法院",
    "M1O": "重庆自由贸易试验区人民法院",
    "M20": "重庆市第二中级人民法院",
    "M21": "重庆市万州区人民法院",
    "M22": "重庆市开州区人民法院",
    "M23": "忠县人民法院",
    "M24": "重庆市梁平区人民法院",
    "M25": "云阳县人民法院",
    "M26": "奉节县人民法院",
    "M27": "巫山县人民法院",
    "M28": "巫溪县人民法院",
    "M29": "城口县人民法院",
    "M30": "重庆市第三中级人民法院",
    "M31": "重庆市涪陵区人民法院",
    "M33": "垫江县人民法院",
    "M34": "重庆市南川区人民法院",
    "M35": "丰都县人民法院",
    "M36": "重庆市武隆区人民法院",
    "M40": "重庆市第四中级人民法院",
    "M41": "石柱县人民法院",
    "M42": "秀山县人民法院",
    "M43": "重庆市黔江区人民法院",
    "M44": "酉阳县人民法院",
    "M45": "彭水县人民法院",
    "M50": "重庆市第五中级人民法院",
    "M51": "重庆市渝中区人民法院",
    "M52": "重庆市南岸区人民法院",
    "M53": "重庆市九龙坡区人民法院",
    "M54": "重庆市巴南区人民法院",
    "M55": "重庆市大渡口区人民法院",
    "M57": "重庆市江津区人民法院",
    "M58": "重庆市永川区人民法院",
    "M59": "重庆市綦江区人民法院",
    "M5A": "重庆市荣昌区人民法院",
    "M60": "成渝金融法院"
}

cookies = {
    'JSESSIONID': 'B81C766A30AD3E4140C77BB3A0A835BD',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'JSESSIONID=B81C766A30AD3E4140C77BB3A0A835BD',
    'Origin': 'http://www.cqfygzfw.gov.cn',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.cqfygzfw.gov.cn/gggs/toListKtggNL.shtml?page=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
origin = "重庆法院公众服务网"
origin_domain = "cqfygzfw.gov.cn"


def get_cqcourt_info(from_queue, webpage_id):
    for court_code, court_name in courts.items():
        for day_num in range(0, 30 + 1):
            for page_num in range(1, 4 + 1):
                # 获取今天时间
                today = datetime.datetime.now()
                # 计算day_num天后的时间
                target_date = today + datetime.timedelta(days=day_num)
                # 格式化日期为YYYY-MM-DD
                formatted_date = str(target_date.strftime('%Y-%m-%d'))

                data = {
                    'fydm': f'{court_code}',
                    'kssj': f'{formatted_date}',
                    'jssj': f'{formatted_date}',
                    'page': f'{page_num}',
                }
                response = requests.post(
                    'http://www.cqfygzfw.gov.cn/gggs/ktgglistNL.shtml',
                    headers=headers,
                    data=data,
                    verify=False,
                )
                try:
                    res = response.json()
                except:
                    continue
                time.sleep(2)
                if res['count'] == 0:
                    continue
                datas = res['data']
                if not data:
                    continue
                for data_value in datas:
                    court_time = formatted_date
                    court_name = data_value["fymc"]
                    content = data_value["ggnr"]
                    case_num = data_value["ahqc"]
                    id_value = data_value["id"]
                    if judge_repeat_case(case_num):
                        continue
                    court_room = ''.join(re.findall(r'在(.*?)开庭审理', content))
                    if not court_room:
                        court_room = ''.join(re.findall(r'在(.*?)庭询、谈话', content))

                    data = {
                        'id': f'{id_value}',
                    }

                    response = requests.post(
                        'http://www.cqfygzfw.gov.cn/gggs/getKtggInfoNL.shtml',
                        headers=headers,
                        data=data,
                        verify=False,
                    )
                    try:
                        res_value = response.json()
                        time.sleep(2)
                        room_leader = res_value["fbrxm"]
                        url = f'http://www.cqfygzfw.gov.cn/gggs/getKtggInfoNL.shtml?id={id_value}'
                    except:
                        room_leader = ''
                        url = f'http://www.cqfygzfw.gov.cn/gggs/getKtggInfoNL.shtml?id={id_value}'
                    print(
                        f"开庭时间：{court_time}, 法院：{court_name}, 案号：{case_num}, 法庭：{court_room}, 承办人：{room_leader}, 内容：{content},详情链接：{url}, id：{id_value}")
                    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # 设置创建日期
                    create_date = datetime.datetime.now().strftime('%Y-%m-%d')
                    department = ''
                    # 连接到测试库
                    try:
                        conn_test = get_connection()
                        cursor_test = conn_test.cursor()
                        # 将数据插入到表中
                        insert_sql = "INSERT INTO col_case_open (url, case_no, content,  court,  open_time, court_room, room_leader, department,  origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s, %s,%s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql, (
                            url, case_num, content, court_name, court_time, court_room, room_leader,
                            department,
                            origin,
                             origin_domain, create_time, create_date, from_queue, webpage_id))
                        # print("插入成功")
                        conn_test.commit()
                        cursor_test.close()
                        conn_test.close()
                    except:
                        continue