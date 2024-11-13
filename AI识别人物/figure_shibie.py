import json
import re
from datetime import datetime

import mysql.connector
from AI接口.deepseek import deepseek_chat, deepseek_people
from AI接口.chatgpt_4mini import gpt_freechat
from api_ai import ai_parse_next, ai_parse_success, ai_parse_fail


def get_individual_info(value):
    name = value.get("姓名")
    name_old = value.get("曾用名")
    gender = value.get("性别")
    id_num = value.get("身份证号")
    address = value.get("住址")
    role = value.get("角色")
    company = value.get("关联公司")
    office = value.get("职务")
    relationship = value.get("人物关系")
    asset = value.get("名下资产")
    is_died = value.get("是否去世")
    other = value.get("其他")
    if name and name != '无':
        fields = ["曾用名", "性别", "身份证号", "住址", "角色", "关联公司", "职务", "人物关系", "名下资产", "是否去世",
                  "其他"]
        for field in fields:
            for i in ['None', '无', []]:
                if value.get(field):
                    if value[field] == i:
                        value[field] = ''
                    else:
                        continue
                else:
                    value[field] = ''
            if not value.get(field):
                value[field] = ' '
        return [name, name_old, gender, id_num, address, role, company, office, relationship, asset, is_died, other]
    else:
        print('未找到姓名')
        return False


def save_database_people(all_info, from_id, paper_id, input_key):
    print(all_info)
    all_info = [str(item) for item in all_info]
    name, name_old, gender, id_num, address, role, company, office, relationship, asset, is_died, other = all_info
    if not gender:
        gender = None
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


def check_is_None(all_info, from_id, paper_id, input_key):
    for i in all_info:
        if i == None or i == "None":
            value_index = all_info.index(i)
            all_info[value_index] = ''
    save_database_people(all_info, from_id, paper_id, input_key)
# 深度求索识别人的信息
def deepseek_identify_people(chat_text, from_id, paper_id, input_key):
    a, b, value = deepseek_people(chat_text)
    print(value)
    value = json.loads(value)
    print(value, type(value))
    if isinstance(value, dict):
        name = value.get("姓名")
        print(456, name)
        if name is None:
            print("未找到姓名")
            for str_field in ["个人信息", "债务人", "担保人", "借款人", "债权人", "债权转让通知暨债务催收公告"]:
                value_1 = value.get(str_field)
                if value_1 is not None:
                    if isinstance(value_1, list):
                        for _value in value_1:
                            all_info = get_individual_info(_value)
                            if all_info:
                                check_is_None(all_info, from_id, paper_id, input_key)
                    elif isinstance(value_1, dict):
                        all_info = get_individual_info(value_1)
                        if all_info:
                            check_is_None(all_info, from_id, paper_id, input_key)
        else:
            print("找到了", name)
            all_info = get_individual_info(value)
            print(345, all_info)

            if all_info:
                check_is_None(all_info, from_id, paper_id, input_key)
    elif isinstance(value, list):
        for _value in value:
            all_info = get_individual_info(_value)
            print(222, all_info)
            if all_info:
                check_is_None(all_info, from_id, paper_id, input_key)
    else:
        print("error")


def gpt_identify_company(chat_text, from_id, paper_id, input_key):
    # chat_4识别公司信息
    a, b, value = gpt_freechat(
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

    # 打印结果
    for company in companies:
        save_database_company(company, from_id, paper_id, input_key)


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

    # try:
    # 深度求索识别人的信息
    deepseek_identify_people(chat_text, queue_id, paper_id, input_key)

    # gpt识别公司的信息
    gpt_identify_company(chat_text, queue_id, paper_id, input_key)

    success_data = {
                    'id': f'{queue_id}',
                    'remark': '',
                }
    ai_parse_success(data=success_data)
    # except Exception as e:
    #     fail_data = {
    #                 'id': f'{queue_id}',
    #                 'remark': f'{e}',
    #     }
    #     ai_parse_fail(data=fail_data)




