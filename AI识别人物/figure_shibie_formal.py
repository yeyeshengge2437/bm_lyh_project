import json
import re
from datetime import datetime

import mysql.connector
from AI接口.deepseek import deepseek_chat, deepseek_people
from AI接口.chatgpt_4mini import gpt_freechat
from api_ai import ai_parse_next, ai_parse_success, ai_parse_fail


def save_database_people(all_info, from_id, paper_id, input_key):
    name = all_info.get("姓名")
    name_old = all_info.get("曾用名")
    gender = all_info.get("性别")
    id_num = all_info.get("身份证号")
    address = all_info.get("住址")
    role = all_info.get("角色")
    company = all_info.get("关联公司")
    office = all_info.get("职务")
    relationship = all_info.get("人物关系")
    asset = all_info.get("名下资产")
    is_died = all_info.get("是否去世")
    other = all_info.get("其他")
    # 获取当前时间
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 上传到测试数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 上传到报纸的内容
    insert_sql = "INSERT INTO col_paper_people (name, former_name, gender, id_num, address, role, company, office, relationship, asset, is_died, other, create_time, from_id, paper_id, input_key) VALUES (%s,%s,%s,%s, %s, %s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

    cursor_test.execute(insert_sql,
                        (name, name_old, gender, id_num, address, role, company, office, relationship, asset, is_died,
                         other, create_time, from_id, paper_id, input_key))
    conn_test.commit()


def save_database_company(all_info, from_id, paper_id, input_key):
    company_name = all_info.get("公司名称")
    nickname = all_info.get("别称")
    former_name = all_info.get("曾用名")
    uscc = all_info.get("统一社会信用代码")
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 上传到测试数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 上传到报纸的内容
    insert_sql = "INSERT INTO col_paper_company (company_name, nickname, former_name, uscc, create_time, from_id, paper_id, input_key) VALUES (%s,%s,%s,%s, %s, %s,%s,%s)"

    cursor_test.execute(insert_sql,
                        (company_name, nickname, former_name, uscc, create_time, from_id, paper_id, input_key))
    conn_test.commit()


# 深度求索识别人的信息
def deepseek_identify_people(chat_text):
    a, b, value = deepseek_chat(
        chat_text + "提取文中所有个人的关键字包含：姓名（不重复），曾用名，性别（没有填''），身份证号，住址，角色（此人在此公告中的角色），关联公司（与该人有关联的公司，不得为空），职务，人物关系，名下资产，是否去世，其他（与该人有关的信息）。缺失值用''表示。不要遗漏个人信息（不要文末联系人信息），不要总结和前置语。格式为：姓名:潘静如,曾用名:潘静,性别: 女,身份证号: 440106197908020026,住址: 广州市天河区珠江新城华夏路,角色: 担保人,关联公司: 揭阳市榕城区合润化工经营部,职务: 法人,人物关系: 系潘婷之女,名下资产: 2000万,是否去世: 否,其他:无;")
    value = re.sub(r'\n', '', value)
    value = re.sub(r' ', '', value)
    print("个人信息识别：" + value)
    companies = []
    for block in value.split(';'):
        print(block)
        if not block:
            continue
        name = re.findall(r'姓名:(.*?),', block)[0]
        former_name = re.findall(r'曾用名:(.*?),', block)[0]
        gender = re.findall(r'性别:(.*?),', block)[0]
        id_num = re.findall(r'身份证号:(.*?),', block)[0]
        address = re.findall(r'住址:(.*?),', block)[0]
        role = re.findall(r'角色:(.*?),', block)[0]
        company_name = re.findall(r'关联公司:(.*?),', block)[0]
        office = re.findall(r'职务:(.*?),', block)[0]
        relationship = re.findall(r'人物关系:(.*?),', block)[0]
        asset = re.findall(r'名下资产:(.*?),', block)[0]
        is_dead = re.findall(r'是否去世:(.*?),', block)[0]
        other = re.findall(r'其他:(.*)', block)[0]
        if name == '':
            continue

        company_info = {
            '姓名': name,
            '曾用名': former_name,
            '性别': gender,
            '身份证号': id_num,
            '住址': address,
            '角色': role,
            '关联公司': company_name,
            '职务': office,
            '人物关系': relationship,
            '名下资产': asset,
            '是否去世': is_dead,
            '其他': other,
        }
        companies.append(company_info)

    return companies

    # 打印结果
    # for company in companies:
    #     save_database_people(company, from_id, paper_id, input_key)


def gpt_identify_company(chat_text):
    # chat_4识别公司信息
    a, b, value = deepseek_chat(
        chat_text + "\n提取文中所有公司的关键字包含：名称（人名不要提取），别称（简称），以及曾用名（原名），和统一社会信用代码，没有的字段放回无。不要遗漏公司，不要总结和前置语。格式为：公司名称：某某有限公司,别称：无,曾用名：无,统一社会信用代码：无;")
    # value = '公司名称：中国长城资产管理股份有限公司上海市分公司,别称：无,曾用名：无,统一社会信用代码：无'
    # 分割数据
    value = re.sub(r'\n', '', value)
    value = re.sub(r' ', '', value)
    print("公司名称识别：" + value)
    companies = []
    for block in value.split(';'):
        print(block)
        if not block:
            continue
        company_name = re.findall(r'公司名称：(.*?),', block)[0]
        alias = re.findall(r'别称：(.*?),', block)[0]
        former_name = re.findall(r'曾用名：(.*?),', block)[0]
        credit_code = re.findall(r'统一社会信用代码：(.*)', block)[0]
        if company_name == '无':
            continue
        if alias == '无':
            alias = ''
        if former_name == '无':
            former_name = ''
        if credit_code == '无':
            credit_code = ''

        company_info = {
            '公司名称': company_name,
            '别称': alias,
            '曾用名': former_name,
            '统一社会信用代码': credit_code
        }
        companies.append(company_info)
    return companies

    # 打印结果
    # for company in companies:
    #     save_database_company(company, from_id, paper_id, input_key)



ai_list = {
    'tell_tool_list': [
        "paper_subject_tell",
    ]
}
while True:
    value = ai_parse_next(data=ai_list)
    identify_text = value['input_text']
    identify_text = re.sub(r"\n", "", identify_text)
    print(identify_text)
    queue_id = value['id']
    paper_id = value['paper_id']
    input_key = value['input_key']
    chat_text = identify_text

    try:
        # 深度求索识别人的信息
        people_companies = deepseek_identify_people(chat_text)
        # 深度求索识别公司的信息
        company_companies = gpt_identify_company(chat_text)
    except Exception as e:
        fail_data = {
                    'id': f'{queue_id}',
                    'remark': f'{e}',
        }
        ai_parse_fail(data=fail_data)
        continue

    for company in people_companies:
        save_database_people(company, queue_id, paper_id, input_key)
    for company in company_companies:
        save_database_company(company, queue_id, paper_id, input_key)

    success_data = {
                    'id': f'{queue_id}',
                    'remark': '',
                }
    ai_parse_success(data=success_data)



