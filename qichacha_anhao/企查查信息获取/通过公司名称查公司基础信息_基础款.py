import json
import random
import re
from datetime import datetime, timedelta

from 验证码识别 import get_captcha
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from qcc_auto_login import auto_login


def timenum_to_time(timenum):
    """
    时间戳转时间
    :param timenum: 时间戳
    :return:
    """
    return time.strftime("%Y-%m-%d", time.localtime(timenum / 1000))


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'qcc_did=0e655a36-176a-4d60-bf14-39aea82d965f; UM_distinctid=193852d2541169-0c4391aad3d138-26011851-13c680-193852d2542fad; QCCSESSID=3ee8f6f53044c4b5493f4c8359; tfstk=gKpxga4_140mt63KuKlljUmmW6nlkbxqmE-QINb01ULJAHzc1s0VWQL6zsbbnm5tXUTem1v9bRI6fFoVSmlk0nWNC20hWvx20sSA20glCct5IGpwZryv0nWa4iLBYF-4WvXW8h665T15bMW1fN_s2zsGP-s_hGaS2aS1Crwf1Yw5xMIbhF6s23_PfO_65sM_UbQaGw2991Dscq0SxRe9eiCAJRb8BRnGDsQBca3IRLH1MwtfyRgFCNZRWaJIrbKy-ITc4FHKy9OeydCCBxUFDQtdFZXIHo7BnGKH6H3LSgRXkL19Ecl22dQAOK18ARX5UGT16QuLKiBDw6pvgczWcebvOt-gvqxR9QCFV_ZTGtAHxd5BhxUFr6S9y6AxJ-LC4IpHpkca-wIgG0n8_55f4IScpFHaRuXd2wmlm5PNwbSR-0n8_55f4gQnqrVa__hP.; acw_tc=0a47318a17368169255757388e00d9f6bef18ef008bdf90c9cf4d9d46cc960; CNZZDATA1254842228=2056976077-1733106149-%7C1736818209',
    'priority': 'u=0, i',
    'referer': 'https://www.qcc.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}


def qcc_search_company_nibo(search_company_name):
    search_company_name = search_company_name
    hit_field_list = ['曾用名']  # 股东，曾用名
    random_num = random.randint(1, 6)

    co = ChromiumOptions()
    co = co.set_user_data_path(r"C:\chome_data\data_nibo")
    # co = co.set_argument('--no-sandbox')
    # co = co.headless()
    co.set_paths(local_port=9167)
    random_float = random.uniform(1, 5)
    # 连接浏览器
    page = ChromiumPage(co)
    page.set.window.max()
    tab = page.get_tab()
    # 访问网页
    tab.get('https://www.qcc.com/')

    # 判断是否有账号在
    tab.wait(4)
    try:
        tab.ele("xpath=//div[@class='qccd-modal-body']/div[@class='qcc-login']", timeout=3)
        # 登录账号
        """
        这里输入账号密码
        """
        login_outcome = auto_login(tab, '15938554242', "liyongheng10")
        if login_outcome:
            print('登录成功')
        else:
            print(f'登录失败,请手动登录')
            input()
    except:
        print('账号已存在')
    cookie_dict = {}
    value_cookies = tab.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    # page.quit()
    # input()

    params = {
        'key': search_company_name,
    }
    response = requests.get('https://www.qcc.com/web/search', params=params, cookies=cookie_dict, headers=headers)
    time.sleep(random_num)
    res_html = response.text
    res_json = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', res_html)
    if res_json:
        page.quit()
        search_company_list = []
        res_json = res_json[0]
        res_json = json.loads(res_json)
        try:
            all_company_list = res_json["search"]["searchRes"]["Result"]
        except:
            all_company_list = []
        for company in all_company_list:
            flag = False
            key_no = company.get("KeyNo")  # 公司id
            company_name = company.get('Name')  # 公司名称
            if company_name.strip("<em>").strip('</em>') == search_company_name:
                flag = True
                print("名字重合")
            legal_rep = company.get('OperName')  # 法定代表人
            reg_capital = company.get('RegistCapi')  # 注册资本
            start_date = company.get('StartDate')  # 成立时间
            address = company.get('Address')  # 地址
            uni_code = company.get('CreditCode')  # 统一社会信用代码
            phone_num_now = company.get('ContactNumber')  # 联系电话
            email = company.get('Email')  # 邮箱
            official_web = company.get('GW')  # 官网
            short_status = company.get('ShortStatus')  # 状态
            tag_list = []
            tag = company.get('Tag')  # 标签
            if tag:
                tag_list.append(tag)
            tag_info_list = company.get('TagsInfoV2')  # 标签信息
            if tag_info_list:
                for tag_info in tag_info_list:
                    tag_name = tag_info.get('Name')  # 标签名称
                    tag_list.append(tag_name)
            scale = company.get('Scale')  # 规模
            hit_reasons = company.get('HitReasons')  # 命中原因
            hit_reason_dict = {}
            for hit_reason in hit_reasons:
                hit_field = hit_reason.get('Field')  # 命中字段
                hit_value = hit_reason.get('Value')  # 命中值
                hit_reason_dict[hit_field] = hit_value
                # print(f"命中字段：{hit_field}，命中值：{hit_value}")
                if hit_value.strip("<em>").strip('</em>') == search_company_name and hit_field in hit_field_list:
                    flag = True
                    print(f"命中字段:{hit_field}")
            if start_date:  # 时间戳转为时间
                try:
                    start_date = timenum_to_time(start_date)
                except:
                    start_date = ''
            if flag:
                target_url = f'https://www.qcc.com/firm/{key_no}.html'
                response = requests.get(target_url, cookies=cookie_dict, headers=headers)
                time.sleep(random_num)
                company_html = response.text
                company_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', company_html)
                if company_data:
                    company_json = json.loads(company_data[0])
                    # print(company_json)
                    company_detail = company_json["company"][
                        "companyDetail"]  # ["company"]["companyDetail"]["TagsInfoV2"][2]["Name"]
                    print(company_detail)
                    if company_detail.get('DJInfo'):
                        company_detail_dj = company_detail.get('DJInfo')
                        company_old_name_list = company_detail.get(
                            'OriginalName')  # ["company"]["companyDetail"]["OriginalName"][0]["Name"] # 企业曾用名
                        company_old_name = []
                        if company_old_name_list:
                            for old_name in company_old_name_list:
                                company_old_name.append(old_name.get('Name'))
                        enrollment_num = None
                        check_date = None
                        no = None
                        status = company_detail_dj.get('status')  # 状态
                        header_peo = company_detail_dj.get('Oper').get('Name')  # 法人
                        header_peo_type = company_detail_dj.get('Oper').get('OperType')  # 法人类型
                        regist_capi = company_detail_dj.get('registCapi')  # 注册资本
                        credit_code = company_detail_dj.get('creditCode')  # 统一社会信用代码
                        rec_cap = None  # 实缴资本
                        org_no = None  # 组织机构代码
                        tax_no = None  # 纳税人识别号
                        econ_kind = company_detail_dj.get('econKind')  # 社会组织类型
                        period_bus = company_detail_dj.get('certificatePeriod')  # 营业期限
                        taxpayer_type = company_detail_dj.get('taxpayerType')  # 纳税人资质
                        staff_scale = company_detail_dj.get('staffScale')  # 人员规模
                        belong_org = company_detail_dj.get('belongOrg')  # 登记机关
                        national_standard_industry = company_detail_dj.get('industry')  # 行业
                        english_name = company_detail_dj.get('englishName')  # 英文名
                        reg_address = company_detail_dj.get('address')  # 注册地址
                        area_list = company_detail.get('Area')  # 所属地区
                        area = ''
                        province = area_list.get('Province')
                        if province:
                            area += province
                        city = area_list.get('City')
                        if city:
                            area += city
                        county = area_list.get('County')
                        if county:
                            area += county
                        com_address = None
                        scope = company_detail_dj.get('scope')  # 经营范围
                        phone = company_detail.get('ContactInfo')
                        if phone:
                            phone = phone.get('PhoneNumber')
                        phone_old_list = []
                        email_old_list = []
                        gw = None
                        # 将数据组织为字典
                        company_data = {
                            "company_name": company_name,
                            'search_company_name': search_company_name,
                            'key_no': key_no,
                            "company_old_name": company_old_name,
                            "enrollment_num": enrollment_num,
                            "check_date": check_date,
                            "no": no,
                            "start_date": start_date,
                            "status": status,
                            "header_peo": header_peo,
                            "header_peo_type": header_peo_type,
                            "regist_capi": regist_capi,
                            "credit_code": credit_code,
                            "rec_cap": rec_cap,
                            "org_no": org_no,
                            "tax_no": tax_no,
                            "econ_kind": econ_kind,
                            "period_bus": period_bus,
                            "taxpayer_type": taxpayer_type,
                            "staff_scale": staff_scale,
                            "belong_org": belong_org,
                            "national_standard_industry": national_standard_industry,
                            "english_name": english_name,
                            "reg_address": reg_address,
                            "area": area,
                            "com_address": com_address,
                            "scope": scope,
                            "phone": phone,
                            "phone_old_list": phone_old_list,
                            "email": email,
                            "email_old_list": email_old_list,
                            "gw": gw
                        }
                        # 转换为 JSON 格式
                        company_json = json.dumps(company_data, ensure_ascii=False, indent=4)
                        print(company_json)
                        return True, company_json
                    company_name = company_detail.get('Name')  # 公司名称
                    company_old_name = []  # 公司曾用名
                    company_tag_info_list = company_detail.get('TagsInfoV2')
                    if company_tag_info_list:
                        for company_tag_info in company_tag_info_list:
                            company_tag = company_tag_info.get('Name')
                            if company_tag == '曾用名' and company_tag_info.get('DataExtend'):
                                company_old_name.append(company_tag_info.get('DataExtend'))
                    enrollment_num = ''  # 参保人数
                    common_list = company_detail.get('CommonList')  # 通用消息
                    if common_list:
                        for common in common_list:
                            common_kd = common.get('KeyDesc')  # 通用消息key
                            if common_kd == '参保人数':
                                enrollment_num = common.get('Value')  # 参保人数
                    enrollment_year_ = ''  # 参保年份
                    annual_report_info = company_detail["company"]["companyDetail"]["CommonList"]  # 获取年报信息
                    if annual_report_info:
                        for annual_report in annual_report_info:
                            if annual_report.get('Key'):
                                if annual_report.get('Key') == 25:
                                    enrollment_year_json = annual_report.get('Value')  # 参保年份
                                    if enrollment_year_json:
                                        enrollment_year_dict = json.loads(enrollment_year_json)
                                        if enrollment_year_dict.get('s'):
                                            enrollment_year_ += str(enrollment_year_dict.get('s'))
                                            break
                    if enrollment_year_:
                        enrollment_num += f'({enrollment_year_})年报'
                    check_date = company_detail.get('CheckDate')  # 核准日期
                    if check_date:
                        check_date = (datetime.utcfromtimestamp(check_date) + timedelta(days=1)).strftime(
                            "%Y-%m-%d")  # 核准日期格式化
                    else:
                        check_date = ''
                    no = company_detail.get('No')  # 工商注册号
                    start_date = company_detail.get('StartDate')  # 成立时间
                    if start_date:
                        try:
                            start_date = (datetime.utcfromtimestamp(start_date) + timedelta(days=1)).strftime(
                                "%Y-%m-%d")  # 成立时间格式化
                        except:
                            start_date = ''
                    else:
                        start_date = ''
                    status = company_detail.get('Status')  # 登记状态
                    try:
                        header_peo = company_detail.get('Oper').get('Name')  # 法定代表人
                    except:
                        header_peo = ''
                    try:
                        header_peo_type = company_detail.get('Oper').get('OperType')  # 法人类型
                    except:
                        header_peo_type = ''
                    regist_capi = company_detail.get('RegistCapi')  # 注册资本
                    credit_code = company_detail.get('CreditCode')  # 统一社会信用代码
                    rec_cap = company_detail.get('RecCap')  # 实缴资本
                    org_no = company_detail.get('OrgNo')  # 组织机构代码
                    tax_no = company_detail.get('TaxNo')  # 纳税人识别号
                    econ_kind = company_detail.get('EconKind')  # 企业类型
                    period_bus_start = company_detail.get('TermStart')  # 经营开始日期
                    period_bus_end = company_detail.get('TeamEnd')  # 经营结束日期
                    if period_bus_start:
                        try:
                            period_bus_start = (
                                    datetime.utcfromtimestamp(period_bus_start) + timedelta(days=1)).strftime(
                                "%Y-%m-%d")
                        except:
                            period_bus_start = ''
                    if period_bus_end:
                        try:
                            period_bus_end = (datetime.utcfromtimestamp(period_bus_end) + timedelta(days=1)).strftime(
                                "%Y-%m-%d")
                        except:
                            period_bus_end = '长期'
                    try:
                        if int(period_bus_end) == 0:
                            period_bus_end = '无固定期限'
                    except:
                        pass
                    period_bus = str(period_bus_start) + ' 至 ' + str(period_bus_end)  # 经营期限
                    taxpayer_type = company_detail.get('TaxpayerType')  # 纳税人资质
                    staff_scale = company_detail.get('StaffScale')  # 人员规模
                    belong_org = company_detail.get('BelongOrg')  # 登记机关
                    national_standard_industry = ''
                    if company_detail.get('IndustryV3'):
                        national_standard_industry = company_detail.get('IndustryV3').get(
                            "Industry")
                        sub_industry = company_detail.get('IndustryV3').get("SubIndustry")  # 行业
                        if sub_industry:
                            national_standard_industry += '>' + sub_industry
                        middle_category = company_detail.get('IndustryV3').get("MiddleCategory")  # 行业
                        if middle_category:
                            national_standard_industry += '>' + middle_category
                        small_category = company_detail.get('IndustryV3').get("SmallCategory")
                        if small_category:
                            national_standard_industry += '>' + small_category
                    english_name = company_detail.get('EnglishName')  # 英文名
                    address = company_detail.get('AddressList')  # 地址
                    reg_address = ''  # 注册地址
                    com_address = ''  # 通信地址
                    if address:
                        for add in address:
                            if add.get('TypeDesc') == '注册地址':
                                reg_address = add.get('Address')
                            if add.get('TypeDesc') == '通信地址':
                                com_address = add.get('Address')
                    scope = company_detail.get('Scope')  # 经营范围
                    phone = company_detail.get('info').get('phone')  # 电话
                    his_tel_list = company_detail.get('HisTelList')  # 历史电话
                    phone_old_list = []  # 历史电话列表
                    for his_tel in his_tel_list:
                        phone_old_list.append(his_tel.get('Tel'))
                    email = company_detail.get('info').get('email')  # 邮箱
                    his_email_list = company_detail.get('MoreEmailList')  # 历史邮箱
                    email_old_list = []  # 历史邮箱列表
                    if his_email_list:
                        for his_email in his_email_list:
                            email_old_list.append(his_email.get('e'))
                    gw = company_detail.get('info').get('gw')  # 网址
                    area_list = company_detail.get('Area')  # 所属地区
                    area = ''
                    if area_list:
                        province = area_list.get('Province')
                        if province:
                            area += province
                        city = area_list.get('City')
                        if city:
                            area += city
                        county = area_list.get('County')
                        if county:
                            area += county
                    # 将数据组织为字典
                    company_data = {
                        "company_name": company_name,
                        'search_company_name': search_company_name,
                        'key_no': key_no,
                        "company_old_name": company_old_name,
                        "enrollment_num": enrollment_num,
                        "check_date": check_date,
                        "no": no,
                        "start_date": start_date,
                        "status": status,
                        "header_peo": header_peo,
                        "header_peo_type": header_peo_type,
                        "regist_capi": regist_capi,
                        "credit_code": credit_code,
                        "rec_cap": rec_cap,
                        "org_no": org_no,
                        "tax_no": tax_no,
                        "econ_kind": econ_kind,
                        "period_bus": period_bus,
                        "taxpayer_type": taxpayer_type,
                        "staff_scale": staff_scale,
                        "belong_org": belong_org,
                        "national_standard_industry": national_standard_industry,
                        "english_name": english_name,
                        "reg_address": reg_address,
                        "area": area,
                        "com_address": com_address,
                        "scope": scope,
                        "phone": phone,
                        "phone_old_list": phone_old_list,
                        "email": email,
                        "email_old_list": email_old_list,
                        "gw": gw
                    }
                    # 转换为 JSON 格式
                    company_json = json.dumps(company_data, ensure_ascii=False, indent=4)
                    print(company_json)
                    return True, company_json
                    # print(f'公司名称：{company_detail.get("Name")}\n曾用名：{company_old_name}\n统一社会信用代码：{credit_code}\n成立日期：{start_date}\n参保人数：{enrollment_num}\n注册资本：{regist_capi}\n实缴资本：{rec_cap}\n组织机构代码：{org_no}\n核准日期：{check_date}\n纳税人识别号：{tax_no}\n企业类型：{econ_kind}\n经营期限：{period_bus}\n纳税人资质：{taxpayer_type}\n人员规模：{staff_scale}\n登记状态：{status}\n登记机关：{belong_org}\n行业：{national_standard_industry}\n英文名：{english_name}\n注册地址：{reg_address}\n通信地址：{com_address}\n经营范围：{scope}\n电话：{phone}\n历史电话：{phone_old_list}\n邮箱：{email}\n历史邮箱：{email_old_list}\n网址：{gw}\n')
            else:
                company_simple_dict = {
                    'company_name': company_name,
                    'key_no': key_no,
                    'search_company_name': search_company_name,
                    'hit_reason': hit_reason_dict,
                    'legal_rep': legal_rep,
                    'reg_capital': reg_capital,
                    'start_date': start_date,
                    'address': address,
                    'uni_code': uni_code,
                    'phone_num_now': phone_num_now,
                    'email': email,
                    'official_web': official_web,
                    'short_status': short_status,
                    'tag_list': tag_list,
                    'scale': scale
                }
                search_company_list.append(company_simple_dict)
                # print(f"公司名称：{company_name}，命中原因：{hit_reason_dict}，法定代表人：{legal_rep}，注册资本：{reg_capital}，成立时间：{start_date}，地址：{address}，统一社会信用代码：{uni_code}，电话：{phone_num_now}，邮箱：{email}，官网：{official_web}，状态：{short_status}，标签：{tag_list}，规模：{scale}")
        # 将搜索页面的信息转换为 JSON 格式
        company_simple_json = json.dumps(search_company_list, ensure_ascii=False, indent=4)
        print(company_simple_json)
        return False, company_simple_json

    else:
        print("网站限制")
        # print(page.html)
        # iframe_url = page.get_frame(1).attr('src')
        # 判断是否为验证码
        try:
            get_captcha(page)
        except:
            time.sleep(3600)
        time.sleep(10)
        page.refresh()
        time.sleep(5)
        page.refresh()
        # 判断是否为扫描二维码

        page.quit()
        # input('出现错误，请查看')
        return "失败", None


def qcc_search_keyno_nibo(key_no):
    random_num = random.randint(1, 6)

    co = ChromiumOptions()
    co = co.set_user_data_path(r"C:\chome_data\data_nibo")
    # co = co.set_argument('--no-sandbox')
    # co = co.headless()
    co.set_paths(local_port=9167)
    random_float = random.uniform(1, 5)
    # 连接浏览器
    page = ChromiumPage(co)
    tab = page.get_tab()
    # 访问网页
    tab.get('https://www.qcc.com/')
    cookie_dict = {}
    value_cookies = tab.cookies()
    for key in value_cookies:
        cookie_dict[key['name']] = key['value']
    page.quit()
    # input()
    key_no_url = f'https://www.qcc.com/firm/{key_no}.html'
    print(key_no_url)
    response = requests.get(key_no_url, cookies=cookie_dict, headers=headers)
    time.sleep(random_num)
    company_html = response.text
    # print(company_html)
    # return
    company_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', company_html)
    if company_data:
        company_json = json.loads(company_data[0])
        # print(company_json)
        company_detail = company_json["company"][
            "companyDetail"]  # ["company"]["companyDetail"]["TagsInfoV2"][2]["Name"]
        company_name = company_detail.get('Name')  # 公司名称
        company_old_name = []  # 公司曾用名
        company_tag_info_list = company_detail.get('TagsInfoV2')
        if company_tag_info_list:
            for company_tag_info in company_tag_info_list:
                company_tag = company_tag_info.get('Name')
                if company_tag == '曾用名' and company_tag_info.get('DataExtend'):
                    company_old_name.append(company_tag_info.get('DataExtend'))
        enrollment_num = ''  # 参保人数
        common_list = company_detail.get('CommonList')  # 通用消息
        if common_list:
            for common in common_list:
                common_kd = common.get('KeyDesc')  # 通用消息key
                if common_kd == '参保人数':
                    enrollment_num = common.get('Value')  # 参保人数
        check_date = company_detail.get('CheckDate')  # 核准日期
        if check_date:
            check_date = (datetime.utcfromtimestamp(check_date) + timedelta(days=1)).strftime(
                "%Y-%m-%d")  # 核准日期格式化
        else:
            check_date = ''
        no = company_detail.get('No')  # 工商注册号
        start_date = company_detail.get('StartDate')  # 成立时间
        if start_date:
            start_date = (datetime.utcfromtimestamp(start_date) + timedelta(days=1)).strftime(
                "%Y-%m-%d")  # 成立时间格式化
        else:
            start_date = ''
        status = company_detail.get('Status')  # 登记状态
        header_peo = company_detail.get('Oper').get('Name')  # 法定代表人
        header_peo_type = company_detail.get('Oper').get('OperType')  # 法人类型
        regist_capi = company_detail.get('RegistCapi')  # 注册资本
        credit_code = company_detail.get('CreditCode')  # 统一社会信用代码
        rec_cap = company_detail.get('RecCap')  # 实缴资本
        org_no = company_detail.get('OrgNo')  # 组织机构代码
        tax_no = company_detail.get('TaxNo')  # 纳税人识别号
        econ_kind = company_detail.get('EconKind')  # 企业类型
        period_bus_start = company_detail.get('TermStart')  # 经营开始日期
        period_bus_end = company_detail.get('TeamEnd')  # 经营结束日期
        if period_bus_start:
            period_bus_start = (datetime.utcfromtimestamp(period_bus_start) + timedelta(days=1)).strftime(
                "%Y-%m-%d")
        if period_bus_end:
            try:
                period_bus_end = (datetime.utcfromtimestamp(period_bus_end) + timedelta(days=1)).strftime(
                    "%Y-%m-%d")
            except:
                period_bus_end = '长期'
        period_bus = str(period_bus_start) + ' 到 ' + str(period_bus_end)  # 经营期限
        taxpayer_type = company_detail.get('TaxpayerType')  # 纳税人资质
        staff_scale = company_detail.get('StaffScale')  # 人员规模
        belong_org = company_detail.get('BelongOrg')  # 登记机关
        national_standard_industry = company_detail.get('IndustryV3').get(
            "Industry") + '>' + company_detail.get('IndustryV3').get(
            "SubIndustry") + '>' + company_detail.get(
            'IndustryV3').get("MiddleCategory")  # 行业
        small_category = company_detail.get('IndustryV3').get("SmallCategory")
        if small_category:
            national_standard_industry += '>' + small_category
        english_name = company_detail.get('EnglishName')  # 英文名
        address = company_detail.get('AddressList')  # 地址
        reg_address = ''  # 注册地址
        com_address = ''  # 通信地址
        for add in address:
            if add.get('TypeDesc') == '注册地址':
                reg_address = add.get('Address')
            if add.get('TypeDesc') == '通信地址':
                com_address = add.get('Address')
        scope = company_detail.get('Scope')  # 经营范围
        phone = company_detail.get('info').get('phone')  # 电话
        his_tel_list = company_detail.get('HisTelList')  # 历史电话
        phone_old_list = []  # 历史电话列表
        for his_tel in his_tel_list:
            phone_old_list.append(his_tel.get('Tel'))
        email = company_detail.get('info').get('email')  # 邮箱
        his_email_list = company_detail.get('MoreEmailList')  # 历史邮箱
        email_old_list = []  # 历史邮箱列表
        for his_email in his_email_list:
            email_old_list.append(his_email.get('e'))
        gw = company_detail.get('info').get('gw')  # 网址
        # 将数据组织为字典
        company_data = {
            "company_name": company_name,
            'key_no': key_no,
            "company_old_name": company_old_name,
            "enrollment_num": enrollment_num,
            "check_date": check_date,
            "no": no,
            "start_date": start_date,
            "status": status,
            "header_peo": header_peo,
            "header_peo_type": header_peo_type,
            "regist_capi": regist_capi,
            "credit_code": credit_code,
            "rec_cap": rec_cap,
            "org_no": org_no,
            "tax_no": tax_no,
            "econ_kind": econ_kind,
            "period_bus": period_bus,
            "taxpayer_type": taxpayer_type,
            "staff_scale": staff_scale,
            "belong_org": belong_org,
            "national_standard_industry": national_standard_industry,
            "english_name": english_name,
            "reg_address": reg_address,
            "com_address": com_address,
            "scope": scope,
            "phone": phone,
            "phone_old_list": phone_old_list,
            "email": email,
            "email_old_list": email_old_list,
            "gw": gw
        }
        # 转换为 JSON 格式
        company_json = json.dumps(company_data, ensure_ascii=False, indent=4)
        print(company_json)
        return company_json
    else:
        print("网站限制")
        # print(page.html)
        # iframe_url = page.get_frame(1).attr('src')
        # 判断是否为验证码
        try:
            get_captcha(page)
        except:
            time.sleep(3600)
        time.sleep(10)
        page.refresh()
        time.sleep(5)
        page.refresh()
        # 判断是否为扫描二维码

        page.quit()
        # input('出现错误，请查看')
        return None


qcc_search_company_nibo('杭州百蜜网络科技有限公司')
# count = 0
# while True:
#     random_num = random.randint(3, 9)
#     try:
#         value = qcc_parse_next()
#     except Exception as e:
#         # print(f"获取队列出错:{e}")
#         time.sleep(5)
#         continue
#     time.sleep(random_num)
#     if value:
#         try:
#             id = value['value']['id']
#             count += 1
#         except:
#             time.sleep(5)
#             continue
#         search_type = value["value"]["search_type"]
#         if search_type == 'corp_qcc_list':  # 根据企业名称查询列表
#             company_name = value.get('value')
#             # # 字符串转json
#             # company_name = json.loads(company_name)
#             company_name = company_name.get('name')
#             try:
#                 search_flag, search_value = qcc_search_company(company_name)
#             except Exception as e:
#                 data = {
#                     'id': id,
#                     'description': f'{e}',
#                 }
#                 qcc_parse_fail(data)
#                 continue
#             if search_flag == True:
#                 # print('_______________________________________')
#                 data = {'corp_info': search_value}
#                 qcc_upload_detail_info(data=data)
#                 success_data = {
#                     'id': id
#                 }
#                 qcc_parse_success(success_data)
#             elif search_flag == False:
#                 data = {'corp_summary_array': search_value}
#                 qcc_upload_info_list(data)
#                 success_data = {
#                     'id': id
#                 }
#                 qcc_parse_success(success_data)
#             elif search_flag == "失败":
#                 data = {
#                     'id': id,
#                     'description': '没有json数据',
#                 }
#                 qcc_parse_fail(data)
#         elif search_type == 'corp_qcc_detail':  # 根据keyno查询列表
#             key_no = value.get('value')
#             # # 字符串转json
#             # key_no = json.loads(key_no)
#             key_no = key_no.get('out_key')
#             search_value = qcc_search_keyno(key_no)
#             if search_value:
#                 data = {'corpInfo': search_value}
#                 qcc_upload_detail_info(data)
#                 success_data = {
#                     'id': id
#                 }
#                 qcc_parse_success(success_data)
#             else:
#                 data = {
#                     'id': id,
#                     'description': '没有json数据',
#                 }
#                 qcc_parse_fail(data)
#     else:
#         time.sleep(8)
#     print(count)
