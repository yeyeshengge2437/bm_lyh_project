"""
国家市场监督管理总局产品质量安全监督管理局---产品抽查
"""
import hashlib
import json
import time
from api_chief import judge_content_repeat
import requests
import mysql.connector

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '__jsluid_s=a28c7387f939020e9fa060ba11d6bab9; insert_cookie=35973550; JSESSIONID=0000ngdNGqiEyTMNuD6OFGoD7Xb:1dljhb9ov; com.jiaxincloud.mcs.cookie.username=web28415646457991930; jiaxinThirdJson=%7B%22cid%22%3A%22defaultUnLoginUserId%22%7D',
    'Origin': 'https://psp.e-cqs.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://psp.e-cqs.cn/ecqsNationalCheckWeb/jdcc/jdcc.jsp',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'encoding': 'true',
    'jsonValue': '{"serviceClassName":"com.itown.searchs.microservice.JdccService","methodName":"listTask","serviceObject":null,"type":null,"params":[]}',
}


def get_chanpinchoucha_data(queue_id, webpage_id):
    data = {
        'name': 'easyui',
        'subject': 'datagrid',
        'page': '1',
        'rows': '1000',
    }

    response = requests.post(
        'https://psp.e-cqs.cn/ecqsNationalCheckWeb/jsonClient.action',
        params=params,
        headers=headers,
        data=data,
    )

    res = response.json()
    data_list = res["returnValue"]["value"]
    count = int(res["transferableProperties"]["fspParameter"]["pagination"]["totalCount"])
    count_page = count // 1000 + 1
    origin = "国家市场监督管理总局产品质量安全监督管理局产品抽查"
    origin_domain = "https://psp.e-cqs.cn/ecqsNationalCheckWeb/jdcc/jdcc.jsp"
    con_set = judge_content_repeat(origin)
    for page in range(1, count_page - 70):
        print(page)
        data_page = {
            'name': 'easyui',
            'subject': 'datagrid',
            'page': str(page),
            'rows': '1000',
        }
        response = requests.post('https://psp.e-cqs.cn/ecqsNationalCheckWeb/jsonClient.action',
                                 params=params,
                                 headers=headers,
                                 data=data_page,
                                 )
        res_json = response.json()
        time.sleep(4)
        data_list = res_json["returnValue"]["value"]
        conn_test = mysql.connector.connect(
            host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database='col'
        )
        cursor_test = conn_test.cursor()
        for data in data_list:
            title = data["org_name"] + "产品质量抽查信息"
            content = {
                "企业名称": data["org_name"],
                "所在省": "".join(data["province_name"]),
                "产品名称": ''.join(data['prod_name']),
                "产品详细名称": ''.join(data['prod_name_1']),
                "规格型号": ''.join(str(data.get("models")) if str(data.get('models')) else None),
                "产品等级": ''.join(str(data.get("prod_level")) if str(data.get('prod_level')) else None),
                "生产日期/批号": ''.join(str(data.get("prod_date")) if str(data.get('prod_date')) else None),
                "抽查结果": ''.join(data["effect"]),
                "承检机构": ''.join(data["org"]),
                "抽查时间": ''.join(str(data.get("org_date")) if str(data.get('org_date')) else None),
                "抽查类型": ''.join(data["chou"]),
                "抽样单位": ''.join(data["chou_name"]),
                "主要不合格项目": ''.join(str(data.get("no_hege")) if str(data.get('no_hege')) else None),
                "抽样来源": ''.join(str(data.get("chou_laiyuan")) if str(data.get('chou_laiyuan')) else None),
            }
            content = str(content)
            path = "当前位置 / 首页 / 产品质量监督抽查信息查询"
            source = "产品质量监督抽查信息查询"
            # print(content)
            if content not in con_set:
                create_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                # 进行数据的去重
                data_unique = f"文章标题：{title}, 文章内容：{content}, 来源：{source}"
                # 数据去重
                hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
                insert_sql = "INSERT INTO col_chief_public (title,content, path,  source,origin, origin_domain, create_date,from_queue, webpage_id,md5_key) VALUES (%s,%s, %s, %s,%s,%s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql, (
                    title,  content,  path,source,
                    origin, origin_domain, create_date, queue_id, webpage_id, hash_value))

                conn_test.commit()
                con_set.add(content)
        cursor_test.close()
        conn_test.close()


# get_chanpinchoucha(111, 222)
