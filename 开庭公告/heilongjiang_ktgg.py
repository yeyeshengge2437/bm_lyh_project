from datetime import datetime
import time
from a_ktgg_api import judge_repeat_invest
import requests
import mysql.connector
from lxml import etree
from deepseek import deepseek_chat

cookies = {
    'security_session_verify': 'fae70c76ad45c6e3b506bc9ca936f3cb',
    '_gscu_107722155': '34945533f2itv510',
    '_gscbrs_107722155': '1',
    '_gscs_107722155': '35001728ugtuul10|pv:2',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    # 'Cookie': 'security_session_verify=fae70c76ad45c6e3b506bc9ca936f3cb; _gscu_107722155=34945533f2itv510; _gscbrs_107722155=1; _gscs_107722155=35001728ugtuul10|pv:2',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.hljcourt.gov.cn/ktgg/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}


def get_lhjcourt_info(from_queue, webpage_id):
    for page in range(0, 50 + 1):
        params = {
            'p': f'{page}',
            'st': '',
            'et': '',
        }

        response = requests.get('http://www.hljcourt.gov.cn/ktgg/index.php', params=params, headers=headers,
                                verify=False)
        time.sleep(1)
        html_con = response.text
        html = etree.HTML(html_con)
        kt_list = html.xpath("//div[@class='liebiao']/table/tbody/tr")
        for kt in kt_list:
            links = "http://www.hljcourt.gov.cn/ktgg/" + ''.join(kt.xpath("./td[@class='text-l']/div/a/@href"))
            links_in_db = judge_repeat_invest(links)
            if not links_in_db:
                trial_court = "黑龙江省高级人民法院"
                origin = "黑龙江法院网"
                origin_domain = "hljcourt.gov.cn"
                name = ''.join(kt.xpath("./td[@class='text-l']/div/a/text()"))
                if name == "2":
                    continue
                case_no = ''.join(kt.xpath("./td[3]/text()"))
                court_room = ''.join(kt.xpath("./td[4]/text()"))
                open_date = ''.join(kt.xpath("./td[5]/text()"))
                # print(f"案件名称:{name}, 链接:{links}, 案件号:{case_no}, 开庭地点:{court_room}, 开庭日期:{open_date}")
                res_detail = requests.get(links, headers=headers, verify=False)
                time.sleep(2)
                html_detail = etree.HTML(res_detail.text)
                ktgg_detail = html_detail.xpath("//div[@class='ggnr']//text()")
                content = ""
                for con in ktgg_detail:
                    if con:
                        content += con.strip()
                ktgg_content = ktgg_detail[3]
                ktgg_type = ktgg_detail[6]
                room_leader = ktgg_detail[8].strip("承办人：")
                try:
                    ktgg_other = ktgg_detail[14]
                except:
                    ktgg_other = ''

                cause = ''.join(deepseek_chat(f"获取这段信息里的案由，不要输出其他字段：{ktgg_content}")).strip(
                    "案由：")

                members = ''.join(
                    deepseek_chat(f"获取这段信息里的当事人注明原告和被告，不要输出其他字段：{ktgg_content}")).strip(
                    " ")

                # print(
                #     f"公告内容:{ktgg_content}, 案由：{cause}，公告类型:{ktgg_type}, 承办人:{room_leader}, 当事人:{members}，其他信息:{ktgg_other}")
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 设置创建日期
                create_date = datetime.now().strftime('%Y-%m-%d')
                department = ''
                # 连接到测试库
                try:
                    conn_test = mysql.connector.connect(
                        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
                    cursor_test = conn_test.cursor()
                    # 将数据插入到表中
                    insert_sql = "INSERT INTO col_case_open (url, case_no, content, cause, court, members, open_time, court_room, room_leader, department,  origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,  %s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql, (
                        links, case_no, content, cause, trial_court, members, open_date, court_room, room_leader,
                        department,
                        origin,
                        origin_domain, create_time, create_date, from_queue, webpage_id))
                    # print("插入成功")
                    conn_test.commit()
                    cursor_test.close()
                    conn_test.close()
                except:
                    continue


# get_lhjcourt_info(111, 222)
