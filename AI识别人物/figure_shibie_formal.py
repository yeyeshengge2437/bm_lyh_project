import json
import re
import time
from datetime import datetime
from multiprocessing import Process
import mysql.connector
from deepseek import deepseek_chat
from api_ai import ai_parse_next, ai_parse_success, ai_parse_fail


def save_database_people(all_info, from_id, paper_id, input_key, paper_item_id):
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
    insert_sql = "INSERT INTO col_paper_people (name, former_name, gender, id_num, address, role, company, office, relationship, asset, is_died, other, create_time, from_id, paper_id, input_key, paper_item_id) VALUES (%s,%s, %s, %s,%s, %s, %s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

    cursor_test.execute(insert_sql,
                        (name, name_old, gender, id_num, address, role, company, office, relationship, asset, is_died,
                         other, create_time, from_id, paper_id, input_key, paper_item_id))
    conn_test.commit()


def save_database_company(all_info, from_id, paper_id, input_key, paper_item_id):
    company_name = all_info.get("公司名称")
    role = all_info.get("角色")
    nickname = all_info.get("别称")
    former_name = all_info.get("曾用名")
    asset = all_info.get("公司名下资产")
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
    insert_sql = "INSERT INTO col_paper_company (company_name, nickname,role,asset, former_name, uscc, create_time, from_id, paper_id, input_key, paper_item_id) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s,%s,%s)"

    cursor_test.execute(insert_sql,
                        (company_name, nickname,role, asset, former_name, uscc, create_time, from_id, paper_id, input_key, paper_item_id))
    conn_test.commit()


# 深度求索识别人的信息
def deepseek_identify_people(chat_text):
    a, b, value = deepseek_chat(
        chat_text + "提取文中所有个人的关键字包含：姓名（不重复），曾用名，性别（没有填：无），身份证号，住址，角色（此人在此公告中的角色），关联公司（与该人有关联的公司，不得为空），职务，人物关系，名下资产，是否去世，其他（与该人有关的信息）。缺失值用'无'表示。不要遗漏个人信息（不要文末联系人信息），不要总结和前置语。格式为：姓名:潘静如,曾用名:潘静,性别: 女,身份证号: 440106197908020026,住址: 广州市天河区珠江新城华夏路,角色: 担保人,关联公司: 揭阳市榕城区合润化工经营部,职务: 法人,人物关系: 系潘婷之女,名下资产: 2000万,是否去世: 否,其他:无;",
        beta=True)
    value = re.sub(r'\n', '', value)
    value = re.sub(r' ', '', value)
    print("个人信息识别：" + value)
    companies = []
    success_num = 0
    fail_num = 0
    for block in value.split(';'):
        print(block)
        if not block:
            continue
        try:
            try:
                name = re.findall(r'姓名:(.*?),', block)[0]
            except:
                name = re.findall(r'(.*?):(.*?),', block)
                if name[0][0] == name[0][1]:
                    name = name[0][0]
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
            if name == '无':
                continue
            if name == "潘静如":
                continue
            if len(name) > 4:
                continue
            if former_name == '无':
                former_name = ''
            if gender == '无':
                gender = ''
            if id_num == '无':
                id_num = ''
            if address == '无':
                address = ''
            if role == '无':
                role = ''
            if company_name == '无':
                company_name = ''
            if office == '无':
                office = ''
            if relationship == '无':
                relationship = ''
            if asset == '无':
                asset = ''
            if is_dead == '无':
                is_dead = ''
            if other == '无':
                other = ''

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
            print(company_info)
            companies.append(company_info)
            success_num += 1
        except:
            fail_num += 1

    return companies, value, success_num, fail_num

    # 打印结果
    # for company in companies:
    #     save_database_people(company, from_id, paper_id, input_key)


def gpt_identify_company(chat_text):
    # chat_4识别公司信息
    a, b, value = deepseek_chat(
        chat_text + "\n提取文中所有公司的关键字包含：名称（人名不要提取），角色（公司在公告中的角色），别称（简称），以及曾用名（原名），公司名下资产，和统一社会信用代码，没有的字段放回无。不要遗漏公司，不要总结和前置语。格式为：公司名称：某某有限公司,角色：债务人,别称：无,曾用名：无,公司名下资产：无,统一社会信用代码：无;")
    # value = '公司名称：中国长城资产管理股份有限公司上海市分公司,别称：无,曾用名：无,统一社会信用代码：无'
    # 分割数据
    value = re.sub(r'\n', '', value)
    value = re.sub(r' ', '', value)
    print("公司名称识别：" + value)
    companies = []
    success_num = 0
    fail_num = 0
    for block in value.split(';'):
        print(block)
        if not block:
            continue
        try:
            company_name = re.findall(r'公司名称：(.*?),', block)[0]
            role = re.findall(r'角色：(.*?),', block)[0]
            alias = re.findall(r'别称：(.*?),', block)[0]
            former_name = re.findall(r'曾用名：(.*?),', block)[0]
            asset = re.findall(r'公司名下资产：(.*?),', block)[0]
            credit_code = re.findall(r'统一社会信用代码：(.*)', block)[0]
            if company_name == '无':
                continue
            if role == '无':
                role = ''
            if alias == '无':
                alias = ''
            if former_name == '无':
                former_name = ''
            if credit_code == '无':
                credit_code = ''
            if asset == '无':
                asset = ''

            company_info = {
                '公司名称': company_name,
                '角色': role,
                '别称': alias,
                '曾用名': former_name,
                '公司名下资产': asset,
                '统一社会信用代码': credit_code
            }
            companies.append(company_info)
            success_num += 1
        except:
            fail_num += 1
    return companies, value, success_num, fail_num

    # 打印结果
    # for company in companies:
    #     save_database_company(company, from_id, paper_id, input_key)

# ai_list = {
#         'tell_tool_list': [
#             "paper_subject_tell",
#         ]
#     }
# while True:
#
#     try:
#         value = ai_parse_next(data=ai_list)
#     except:
#         time.sleep(30)
#         continue
#     if value is None:
#         time.sleep(30)
#         continue
#     print(value)
#     identify_text = value['input_text']
#     # identify_text = re.sub(r"\n", "", identify_text)
#     print(identify_text)
#     queue_id = value['id']
#     paper_id = value['paper_id']
#     input_key = value['input_key']
#     paper_item_id = value['paper_item_id']
#     chat_text = identify_text
#
#     try:
#         # 深度求索识别人的信息
#         people_companies = deepseek_identify_people(chat_text)
#         # 深度求索识别公司的信息
#         company_companies = gpt_identify_company(chat_text)
#     except Exception as e:
#         fail_data = {
#             'id': f'{queue_id}',
#             'remark': f'{e}',
#         }
#         ai_parse_fail(data=fail_data)
#         continue
#
#     for company in people_companies:
#         save_database_people(company, queue_id, paper_id, input_key, paper_item_id)
#     for company in company_companies:
#         save_database_company(company, queue_id, paper_id, input_key, paper_item_id)
#
#     success_data = {
#         'id': f'{queue_id}',
#         'remark': '',
#     }
#     ai_parse_success(data=success_data)



def get_figure_shibie_formal():
    ai_list = {
        'tell_tool_list': [
            "paper_subject_tell",
        ]
    }
    while True:
        try:
            try:
                value = ai_parse_next(data=ai_list)
            except:
                time.sleep(30)
                continue
            if value is None:
                time.sleep(30)
                continue
            print(value)
            identify_text = value['input_text']
            # identify_text = re.sub(r"\n", "", identify_text)
            print(identify_text)
            queue_id = value['id']
            paper_id = value['paper_id']
            input_key = value['input_key']
            paper_item_id = value['paper_item_id']
            chat_text = identify_text

            try:
                # 深度求索识别人的信息
                people_companies,  reply_info, success_people_num, fail_people_num = deepseek_identify_people(chat_text)
                # 深度求索识别公司的信息
                company_companies, reply_info, success_company_num, fail_company_num = gpt_identify_company(chat_text)
            except Exception as e:
                fail_data = {
                    'id': f'{queue_id}',
                    'remark': f'{e}',
                }
                ai_parse_fail(data=fail_data)
                continue

            for company in people_companies:
                save_database_people(company, queue_id, paper_id, input_key, paper_item_id)
            for company in company_companies:
                save_database_company(company, queue_id, paper_id, input_key, paper_item_id)
            if fail_company_num == 0 and fail_people_num == 0:
                success_data = {
                    'id': f'{queue_id}',
                    # 'remark': f'成功',
                    'output_text': reply_info,
                }
                ai_parse_success(data=success_data)
            else:

                success_data = {
                    'id': f'{queue_id}',
                    'remark': f'成功个人{success_people_num}个， 失败个人{fail_people_num}个；成功公司{success_company_num}个，失败公司{fail_company_num}个',
                    'output_text': reply_info,
                }
                ai_parse_success(data=success_data)
        except:
            continue

if __name__ == '__main__':
    """
    多进程5个
    """
    process_list = []
    for i in range(5):
        process = Process(target=get_figure_shibie_formal, args=())
        process_list.append(process)

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()

