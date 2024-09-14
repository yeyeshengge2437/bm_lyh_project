import hashlib
import json
import re
from datetime import datetime
from api_chief import paper_queue_next, paper_queue_success, paper_queue_fail
import mysql.connector
import time
import execjs
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
from list_wenshu import city_data, year_data, chufa_type

co = ChromiumOptions()
co = co.set_paths().auto_port()
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '__jsluid_s=97ef77e01505c53919b77048e0d148c5; Hm_lvt_54db9897e5a65f7a7b00359d86015d8d=1722564716,1724919146; Hm_lpvt_54db9897e5a65f7a7b00359d86015d8d=1724919146; HMACCOUNT=FDD970C8B3C27398; SHAREJSESSIONID=7a857d55-1dcc-450c-b0e9-bd09157a6582',
    'Origin': 'https://cfws.samr.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://cfws.samr.gov.cn/list.html?21_s=110101',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_ciphertext():
    with open("wenshu.js", encoding='utf-8') as f:
        code = f.read()
        ctx = execjs.compile(code)
    ciphertext = ctx.call("cipher")
    return ciphertext


def get_data_num(query):
    data = {
        'pageSize': '200',
        'pageNum': '1',
        'queryCondition': str(query),
        'sortFields': '',
        'ciphertext': get_ciphertext()
    }
    response = requests.post('https://cfws.samr.gov.cn/queryDoc', headers=headers, data=data)
    time.sleep(0.4)

    data = response.json()
    if data['result']:
        data = data['result']
        try:
            data_num = data['queryResult']['resultCount']
        except:
            data_num = 0
        return int(data_num)
    else:
        return 0


def judge_url_repeat(origin):
    """
    判断链接是否重复
    :param origin: 数据来源
    :return:
    """
    # 创建版面链接集合
    url_set = set()
    # 连接数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    cursor_test.execute(f"SELECT id, url FROM col_punish WHERE origin='{origin}'")
    rows = cursor_test.fetchall()
    for id, title_url in rows:
        url_set.add(title_url)
    cursor_test.close()
    conn_test.close()
    return url_set


def parse_data(url_set, query, queue_id, webpage_id):
    data = {
        'pageSize': '200',
        'pageNum': '1',
        'queryCondition': str(query),
        'sortFields': '',
        'ciphertext': get_ciphertext()
    }
    response = requests.post('https://cfws.samr.gov.cn/queryDoc', headers=headers, data=data)
    time.sleep(0.5)
    conn_test = mysql.connector.connect(
        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database='col',
    )
    data = response.json()
    if data['result']:
        try:
            data = data['result']
            data = data['queryResult']['resultList']
            print(data)
            origin = '中国市场监管行政处罚文书网'
            origin_domain = 'https://cfws.samr.gov.cn/'
            for detail in data:
                wf_fact = ''
                content_detail = ''
                title_url = 'https://cfws.samr.gov.cn/detail.html?docid=' + detail['1']
                if title_url not in url_set:
                    url_set.add(title_url)


                    if detail.get('1'):
                        data = {
                            "ciphertext": get_ciphertext(),
                            "docid": detail['1']
                        }
                        content_res = requests.post('https://cfws.samr.gov.cn/getDoc', headers=headers, data=data)
                        time.sleep(0.5)
                        content_data = content_res.json()

                        if content_data['result']:
                            value = content_data['result']
                            content_detail = f"处罚类型:{value['i4']}"
                            wf_fact = value['i5']
                    content_data = detail['7']
                    decision_wsh = detail['2']
                    punish_organ = detail['14']
                    chufatime = detail['23']
                    name = detail['30']
                    puish_date = chufatime[:4] + '-' + chufatime[4:6] + '-' + chufatime[6:]
                    content_detail = f'当事人名称:{name},处罚机关:{decision_wsh}, 处罚日期:{puish_date}, 处罚内容:{content_data}, 处罚依据:{wf_fact}' + content_detail
                    # 将格式xxxxxxxx 转为xxxx-xx-xx


                    uni_data = f'{str(decision_wsh), str(puish_date)}'
                    md5_key = hashlib.md5(json.dumps(uni_data).encode('utf-8')).hexdigest()
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    print(name, title_url, decision_wsh, content_data, wf_fact, punish_organ, puish_date, content_detail)
                    cursor_test = conn_test.cursor()
                    insert_sql = "INSERT INTO col_punish (name, url, decision_wsh, punish_content,wf_fact, punish_organ, punish_date,content_detail,create_date, origin, origin_domain, md5_key, from_queue, webpage_id) VALUES (%s,%s, %s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s)"
                    cursor_test.execute(insert_sql, (
                        name, title_url, decision_wsh, content_data, wf_fact, punish_organ, puish_date, content_detail,
                        create_date,
                        origin, origin_domain, md5_key, queue_id, webpage_id))
                    conn_test.commit()
                    cursor_test.close()


        except Exception as e:
            time.sleep(10)
            pass
        conn_test.close()



def get_shichangjianguanchufawenshu_data(queue_id, webpage_id):
    query = []
    url_set = judge_url_repeat('中国市场监管行政处罚文书网')
    for city in city_data:
        query.append(city)
        parse_data(url_set, query, queue_id, webpage_id)
        if get_data_num(query) > 200:
            for year in year_data:
                query.append(year)
                parse_data(url_set, query, queue_id, webpage_id)
                if get_data_num(query) > 200:
                    for chufa in chufa_type:
                        query.append(chufa)
                        parse_data(url_set, query, queue_id, webpage_id)
                        query.remove(chufa)
                # elif 0 < get_data_num(query) <= 200:
                #     parse_data(url_set, query, queue_id, webpage_id)
                # else:
                #     pass
                query.remove(year)
        # elif 0 < get_data_num(query) <= 200:
        #     parse_data(url_set, query, queue_id, webpage_id)
        # else:
        #     pass
        query.remove(city)


while True:
    paper_queue = paper_queue_next(webpage_url_list=['https://cfws.samr.gov.cn/list.html?49_ss=16'])
    if paper_queue is None or len(paper_queue) == 0:
        print('暂无任务')
        time.sleep(1800)
        pass
    else:
        queue_id = paper_queue['id']
        webpage_id = paper_queue["webpage_id"]
        webpage_url = paper_queue["webpage_url"]
        try:
            get_shichangjianguanchufawenshu_data(queue_id, webpage_id)
            data = {
                "id": queue_id,
                'description': f'数据获取成功',
            }
            paper_queue_success(data=data)
        except Exception as e:
            print(e)
            data = {
                "id": queue_id,
                'description': f'程序异常:{e}',
            }
            paper_queue_fail(data=data)
