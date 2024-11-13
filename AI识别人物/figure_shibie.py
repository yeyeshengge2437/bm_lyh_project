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


def test_data(chat_text, queue_id, paper_id, input_key):
    deepseek_identify_people(chat_text, queue_id, paper_id, input_key)

    # gpt识别公司的信息
    gpt_identify_company(chat_text, queue_id, paper_id, input_key)


# ai_list = {
#     'tell_tool_list': [
#         "paper_subject_tell",
#     ]
# }
# while True:
#     value = ai_parse_next(data=ai_list)
#     identify_text = value['input_text']
#     identify_text = re.sub(r"\n", "", identify_text)
#     print(identify_text)
#     queue_id = value['id']
#     paper_id = value['paper_id']
#     input_key = value['input_key']
#     chat_text = identify_text
#
#     # try:
#     # 深度求索识别人的信息
#     deepseek_identify_people(chat_text, queue_id, paper_id, input_key)
#
#     # gpt识别公司的信息
#     gpt_identify_company(chat_text, queue_id, paper_id, input_key)
#
#     success_data = {
#                     'id': f'{queue_id}',
#                     'remark': '',
#                 }
#     ai_parse_success(data=success_data)
#     # except Exception as e:
#     #     fail_data = {
#     #                 'id': f'{queue_id}',
#     #                 'remark': f'{e}',
#     #     }
#     #     ai_parse_fail(data=fail_data)


chat_test = """二、债权资产情况

（一）湖北金茨泉酒业有限公司

1.债务企业基本情况

该公司成立于1999年11月28日，公司类型为有限责任公司（自然人投资或控股），法定代表人为赵世文，注册资本为5000万元人民币，住所地为湖北省恩施市金龙大道酿酒工业园（龙凤镇三河村）。公司经营范围：“金茨泉”系列酒生产、销售；副食、饮料、啤酒、白酒、百货、销售；粮食购销。（涉及许可经营项目，应取得相关部门许可后方可经营）

2.债权担保及诉讼执行情况

（1）保证担保情况

恩施州农发信用担保股份有限公司、赵世文、向远兰。

（2）诉讼及执行情况

2018年8月27日恩施市人民法院出具（2017）鄂2801民初3444号《民事判决书》，2020年11月20日，恩施市人民法院出具（2020）鄂2801民初608号《民事判决书》，目前该案已终本。

3.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

（二）湖北宜恒茶油产业科技有限责任公司

1.债务企业基本情况

该公司成立于2007年4月3日，公司类型为其他有限责任公司，法定代表人为吴楚银，注册资本为1200万元人民币，住所地为恩施市龙鳞宫200号。公司经营范围：生产、加工、销售食用植物油（全精炼）；农副产品收购；粮食收购；对外贸易进出口业务；预包装食品、散装食品的批发兼零售；化妆品的销售。（依法须经批准的项目，经相关部门批准后方可展开经营活动）

2.债权担保及诉讼执行情况

（1）保证担保情况

恩施州农发信用担保股份有限公司、恩施市大有日化有限公司、吴楚银。

（2）诉讼及执行情况

2021年9月14日，恩施市人民法院裁定变更中国长城资产管理股份有限公司湖北省分公司为本案申请执行人，目前该案已终本。

3.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

（三）湖北巨源油业有限公司

1.债务企业基本情况 

该公司成立于2004年4月16日，公司类型为有限责任公司（法人独资），法定代表人庄传标，注册资本为3000万元人民币，住所地为潜江经济开发区广泽大道北侧。公司经营范围：食用植物油（全精炼、半精炼）自产自销；单一饲料（棉籽粕、菜籽粕）加工、批发。（全国工业生产许可证有效期至2015年5月29日）一般经营项目：油料作物收购、销售；文具用品、日用百货、电子器材（不含安全技术防范产品）销售；门店出租。

债权1担保及诉讼执行情况 

（1）抵押担保情况

储油罐。

质押担保情况

    4000吨菜籽油，已经灭失。

（3）保证担保情况

保证人：庄传标；

（4）诉讼及执行情况

2021年4月25日，武汉市硚口区人民法院下达（2020）鄂0104民初624号《民事判决书》，目前该案件处于终本阶段。

债权2担保及诉讼执行情况

（1）抵押担保情况

该债权抵押物为湖北巨源油业有限公司名下位于潜江泽口开发区广泽大道北侧巨源油业内厂房及土地，建筑面积合计16427.35平方米，土地面积53460.36平方米。

（2）质押担保情况

11485吨菜籽油，已经灭失。

（3）保证担保情况

保证人：庄传标。

（4）诉讼及执行情况

2018年9月10日，汉江中级人民法院下达（2018）鄂96民初9号《民事判决书》，目前该案处于终本阶段。

4.资产亮点

该抵押物位于潜江工业园区核心区域，地理位置较好，交通方便，抵押物整体性较好，配套设施完善。

5.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

 

（四）潜江市源鑫纺织实业有限公司

1.债务企业基本情况 

该公司成立于2004年4月11日，公司类型为有限责任公司（自然人独资），法定代表人为雷元涛，注册资本为2600万元人民币，住所地为潜江市园林办事处章华北路39号。公司经营范围：许可经营项目：棉纱加工；棉花加工（限有棉花加工资格认定证书的分支机构经营）。一般经营项目：棉花、纺织辅助材料收购、销售；棉纱、织布销售；进出口业务（不含法律、行政法规或国务院决定设定前置行政审批的种类）。

2.债权担保及诉讼执行情况 

（1）抵押担保情况

该债权抵押物为潜江市源鑫纺织实业有限公司名下位于湖北省潜江市杨市刘岭街88号、潜江市杨市办事处菜科所的12746.11㎡厂房和52842.15㎡土地。

质押担保情况

    质押537套/台设备。

（3）保证担保情况

保证人1：雷元涛；

保证人2：林琼；

（4）诉讼及执行情况

2016年7月27日，汉江市中级人民法院下达（2016）鄂96号民初5号《民事判决书》，2017年4月28日汉江市中级人民法院作出（2016）鄂96执122-1号之一民事裁定书，裁定终结本次执行。

3.资产亮点

该抵押物位于潜江市主干道核心区域，地理位置较好，离G50沪渝高速路出入不到1公里，交通方便，抵押物整体性较好，配套设施完善。

4.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

（五）武汉枫国工业集团有限公司 

1.债务企业基本情况

该公司成立于2006年6月2日，公司类型为有限责任公司(自然人投资或控股)，法定代表人为李吉文，注册资本为3,000万元人民币，住所地为武汉市青山区119街25门6号。公司经营范围：金属结构、金属加工机械、通用零部件、采矿、冶金、建筑专用设备、电子元件制造；金属及金属矿、建材及化工产品（不含危险化学品）、电子产品、纺织、服装及家庭用品、文具用品、体育用品及器材批零兼营；百货零售；技术推广服务（国家有专项规定的项目经审批后或凭许可证在核定的期限内方可经营）。该公司目前已停止经营。

2.债权担保及诉讼执行情况

（1）抵押担保情况

抵押物：王珏以其名下位于上海市长宁区虹梅路3721号626室商业房产提供最高额抵押担保，建筑面积46.47平方米，担保金额为116万元。

（2）保证担保情况

保证人：上海秋广实业有限公司、上海优虎紧固件有限公司、张旭、顾云高、王珏。

（3）诉讼及执行情况

该债权未进入诉讼程序。

3.资产亮点

该债权抵押物位于上海市长宁区程家桥街道，周边有较多商业房产，有一定的商业聚集度。抵押物附近有多条公交线路通行，距地铁10号线龙溪路站较近，公共交通便捷，道路通达度较高。

4.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

（六）武汉长信锦华商贸有限公司 

1.债务企业基本情况

该公司成立于2005年9月15日，公司类型为有限责任公司(自然人投资或控股)，法定代表人为余婷婷，注册资本为500万元人民币，住所地为东西湖区东西湖大道特1号农贸市场交易19区12栋4号（8）。公司经营范围：通讯器材（不含无线电发射）、电子元器件、机电产品、洗涤设备、制冷设备、五金交电、家用电器、服装饰品、建筑材料、装饰材料、农产品、日用百货销售（国家有专项规定的项目须取得有效审批文件或许可证后方可经营）。

2.债权担保及诉讼执行情况

（1）保证担保情况

保证人：武汉市农业融资担保有限公司（曾用名：武汉市农业担保有限公司）、余婷婷、黄睿。

（2）诉讼及执行情况

该债权未进入诉讼程序。

3.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

（七）襄阳德尔驰机电工程有限公司

1.债务企业基本情况

该公司成立于2008年1月30日，公司类型为有限责任公司(自然人投资或控股)，法定代表人陈肯，注册资本为3160万元人民币，住所地为襄阳市樊城区大庆西路50号盛世唐朝1幢1单元。公司经营范围：汽车线束、电控盒制作、监控系统工程、网络工程设计、安装；电力器材、电线电缆、电子电器、计算机办公自动化设备、机械零部件销售；房屋出租；建筑设备租赁。

2.债权担保及诉讼执行情况

（1）抵押担保情况

襄阳德尔驰机电工程有限公司名下位于襄阳市樊城区丹江路93号5幢，6幢、7幢共计2152.23平方米房产及1808.19平方米土地使用权。

（2）保证担保情况

保证人：樊金红、陈少兵、陈肯、襄阳陈少兵建筑装饰工程有限公司。

（3）诉讼及执行情况

2020年11月3日，襄阳市襄城区人民法院出具（2018）鄂0602民初2676号《民事判决书》，抵押物二拍流拍，目前该案已终本。

3.资产亮点

该抵押物位于襄阳市樊城区丹江路93号5幢，6幢、7幢共3栋独立建筑，位于樊城区核心区域，地理位置较好，周边配套齐全，人流量较大，抵押物整体性较好。

4.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

 

（八）襄阳市东方绿园植保器械有限公司

1.债务企业基本情况 

该公司成立于2006年9月29日，公司类型为有限责任公司（自然人投资或控股），法定代表人张波，注册资本为600万元人民币，住所地为襄阳市襄州区双沟镇九号路（双沟工业园吴河村）。公司经营范围：植保器械组装、零配件批发、零售；普通机械设备销售、安装、维修（涉及前置许可的项目除外）；货物及技术进出口（不含国家禁止或限制进出口的货物或技术）。

2.债权担保及诉讼执行情况 

（1）抵押担保情况

债务人名下位于襄州双沟工业园区内的3幢房屋建筑物及土地使用权，房屋建筑物面积共4089.8平方米、土地使用权面积为6665.42平方米。

（2）保证担保情况

保证人：张波、张玉兄、杨腊香、张礼兵。

（3）诉讼及执行情况

2019年3月8日，襄阳市襄州区人民法院下达（2018）鄂0607民初5760号《民事判决书》，目前该案件处于终本阶段。

3.资产亮点

该抵押物位于襄州双沟工业园区内，地理位置较好，周边配套齐全，交通便利，抵押物整体性较好。

4.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

（九）黄冈市宝诚商贸有限公司

1.债务企业基本情况 

该公司成立于2010年3月10日，公司类型为有限责任公司（自然人独资或控股），法定代表人为余新年，注册资本为1500万元人民币，住所地为黄冈市赤壁大道。公司经营范围：日用百货、酒、纺织品、服装、鞋帽、五金、交电、建筑材料、家俱、电子器材销售（涉及许可经营项目，应取得相关部门许可后方可经营）。

2.债权担保及诉讼执行情况 

（1）抵押担保情况

该债权抵押物为黄冈市黄州蓝星商贸有限公司名下黄州区赤壁大道95号房产及土地使用权，房产位于该综合楼的第一、二、三、九层(共九层)，建筑总面积合计为3348.39平方米，土地使用权面积为4108.1平方米。

（2）保证担保情况

余新年、兰淑英。

（3）诉讼及执行情况

2016年4月29日，黄冈市黄州区人民法院下达（2016）鄂1102号民初897号《民事调解书》，抵押物二拍流拍，目前该案已终本。

3.资产亮点

该抵押物位于黄冈市主干道核心区域，地理位置较好，紧邻黄冈万达，周边人流量较大、交通方便，抵押物整体性较好，配套设施完善。

4.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

（十）湖北好美佳丰彩色包装印务有限公司

1.债务企业基本情况 

该公司成立于2012年11月29日，公司类型为有限责任公司（自然人独资或控股），法定代表人为南又国，注册资本为500万元人民币，住所地为浠水经济开发区散花工业园。公司经营范围：出版物印刷、包装装潢印制品印刷、其他印制品印刷。（涉及许可经营项目，应取得相关部门许可后方可经营）

2.债权担保及诉讼执行情况 

（1）抵押担保情况

该债权抵押物为湖北好美佳丰彩色包装印务有限公司名下黄冈浠水县散花工业园内的工业用地，土地使用权面积为31297平方米。

（2）保证担保情况

武汉美益经贸发展有限公司、南又国、南军、胡飞、林曙光。

（3）诉讼及执行情况

2018年12月11日，浠水县人民法院下达（2018）鄂1125号民初3038号《民事判决书》，抵押物二拍流拍，目前该案已终本。

3.资产亮点

该抵押物位于黄冈市浠水工业园核心区域，地理位置较好，交通方便，抵押物整体性较好，配套设施完善。

4.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

（十一）湖北喳西泰旅游开发投资有限公司

1.债务企业基本情况 

该公司成立于2011年7月13日，公司类型为有限责任公司（自然人独资或控股），法定代表人为刘仕龙，注册资本为10000万元人民币，住所地为来凤县翔凤镇凤南路喳西泰水城。公司经营范围：旅游项目投资开发与建设经营；旅游商品、民族工艺品开发与经营；宾馆、酒店投资；城乡基础设施建设项目投资；房地产投资开发与营销；旅游景区（点）经营管理（依法须经批准的项目，经相关部门批准后方可开展经营活动）

2.债权诉讼执行情况 

该案已进入破产重整程序，具体分配方案详见破产分配方案。

3.其他情况说明

以上信息仅供参考，具体债权情况最终以借据、合同、催收通知书、法院判决书、调解书、裁定书、相关部门产权登记、工商管理部门登记等有关法律资料为准，请投资者自行调查判断并自行承担购买债权后可能存在的风险。

 

 

 三、交易对象

具有完全民事行为能力、支付能力的法人、组织或自然人。但以下主体不得购买：

（1）国家公务员、金融监管机构工作人员、政法干警、资产公司工作人员、原债务人管理人员、参与资产处置工作的律师、会计师、评估师、拍卖人等中介机构人员等关联人或者上述关联人参与的非金融机构法人；（2）参与不良债权转让的资产公司工作人员、原债务人管理人员或者受托资产评估机构负责人员等有近亲属关系的人员；（3）债权资产项下的债务人及关联企业等利益相关方；（4）失信被执行人或失信被执行人的法定代表人、主要负责人、影响债务履行的直接责任人员、实际控制人；（5）债权资产所涉及的债务人、相关担保人、其关联方及债务人、相关担保人委托的主体；（6）列入反洗钱、反恐怖黑名单的人员；（7）其他依据法律法规、司法解释或监管机构的规定不得收购、受让标的债权的主体。

四、交易条件：一次性付款。

五、处置方式：组包公开竞价转让、单户公开竞价转让或协议转让。

六、公告有效期：自本公告发布之日起20个工作日。

七、合作意向：中国长城资产管理股份有限公司湖北省分公司面对国际和国内两个投资人市场，欢迎广大有识之士参与购买债权。 

上述债权自本公告发布之日起至公告有效期届满日受理对上述债权资产相关处置的征询和异议，以及有关排斥、阻挠征询或异议以及其他干扰资产处置公告活动的举报。

受理公示事项

联系人：夏先生、谭先生      

联系电话：027-86771092、027-86771020

联系地址：湖北省武汉市武昌区东湖路155号

分公司纪检审计部联系人：任女士

联系电话：027-86790607

 

中国长城资产管理股份有限公司湖北省分公司

                              2024年11月6日"""

# chat_test = re.sub(r' ', '', chat_test)
test_data(chat_test, "123", "123", "123")




