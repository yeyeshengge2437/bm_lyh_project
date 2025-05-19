"""
获取企查查的查询详细页的基础信息
存在翻页的需要再次请求一下
"""
import hashlib
# 注意：数据放在测试库中
import json
import math
import random
import re
import time
import traceback
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
from dingdingbot import dd_program_abnormal
from a_mysql_connection_pool import up_qcc_data, up_qcc_res_data, get_ban_data, del_ban_data, up_part_qcc_data
from api_paper import paper_queue_next, paper_queue_success, paper_queue_fail, paper_queue_step_finish
from qcc_api_res import get_response, post_response
from qcc_auto_login import auto_login
from 验证码识别 import get_captcha

file_path = r'D:\chome_data\qcc_xia'
iphone_num = '18157172586'
password = "Renliang1221"


def generate_md5(data):
    """
    生成输入数据的 MD5 哈希值

    参数:
        data: 可以是字符串、字典、列表等

    返回:
        返回数据的 MD5 哈希值（32位十六进制字符串）
    """
    # 如果是字典或列表，先转成 JSON 字符串
    if isinstance(data, (dict, list)):
        data = json.dumps(data, sort_keys=True, ensure_ascii=False)

    # 如果是字符串，编码成字节
    if isinstance(data, str):
        data = data.encode('utf-8')

    # 计算 MD5
    md5_hash = hashlib.md5(data)
    return md5_hash.hexdigest()


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


def encounter_captcha(value_json, page):
    if value_json.get('message'):
        if value_json.get('message') in ['未满足前提条件', '被立即暂停服务']:
            print("未满足前提条件, 网站限制")
            page.refresh()
            time.sleep(8)
            try:
                get_captcha(page)
                time.sleep(10)
                page.refresh()
                time.sleep(10)
                if '验证后再操作' in str(page.html):
                    return False
                else:
                    print("验证码识别成功")
                    return "验证码识别成功"
            except Exception as e:
                print(e)
                print("不是验证码")
                time.sleep(3600)
                # input_value = input('是否等待3600秒, 0=等')
                # if input_value == '0':
                #     time.sleep(3600)
                return False
    else:
        return "没有遇到验证码"


def dispose_success_data(success_data, data_key, data_type, key_no, from_queue, webpage_id):
    if success_data:
        up_part_qcc_data(success_data, data_key, key_no, from_queue, webpage_id)
    part_data = {
        'data_type': data_type,
        'id': from_queue,
    }
    paper_queue_step_finish(part_data)


def qcc_search_company(search_company_name, from_queue, webpage_id):
    search_company_name = search_company_name
    hit_field_list = ['曾用名']  # 股东，曾用名
    random_num = random.randint(1, 6)

    co = ChromiumOptions()
    co = co.set_user_data_path(file_path)
    co.set_paths(local_port=9232)
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
        login_outcome = auto_login(tab, iphone_num, password)
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

    params = {
        'key': search_company_name,
    }
    response = requests.get('https://www.qcc.com/web/search', params=params, cookies=cookie_dict, headers=headers)
    time.sleep(10)
    res_html = response.text
    res_json = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', res_html)
    if res_json:
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
            else:
                flag = False
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
            else:
                pass
            tag_info_list = company.get('TagsInfoV2')  # 标签信息
            if tag_info_list:
                for tag_info in tag_info_list:
                    tag_name = tag_info.get('Name')  # 标签名称
                    tag_list.append(tag_name)
            else:
                pass
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
            else:
                pass
            if flag:
                print('成功命中该公司')
                # return True
                # continue
                target_url = f'https://www.qcc.com/firm/{key_no}.html'
                response = requests.get(target_url, cookies=cookie_dict, headers=headers)
                time.sleep(12)
                company_html = response.text
                pid_list = re.findall(r"<script>window\.pid='(.*?)'; window\.tid", company_html)
                tid_list = re.findall(r"window\.tid='(.*?)'</script>", company_html)
                if not pid_list or not tid_list:
                    print("网站限制")
                    print("获取数据失败")
                    try:
                        get_captcha(page)
                        time.sleep(random.uniform(7, 17))
                        page.refresh()
                        time.sleep(random.uniform(2, 4))
                    except:
                        time.sleep(3600)
                    # 直接调取失败接口
                    fail_data = {
                        'id': from_queue,
                        'description': f'数据获取失败, 网站限制',
                    }
                    paper_queue_fail(data=fail_data)
                else:
                    pid = pid_list[0]
                    tid = tid_list[0]
                    company_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', company_html)
                    susong_url = f'https://www.qcc.com/csusong/{key_no}.html'
                    susong_response = requests.get(susong_url, cookies=cookie_dict, headers=headers)
                    time.sleep(9)

                    # 刚开始获取json数据
                    if company_data:
                        company_json = json.loads(company_data[0])
                        """
                        获取一定存在的信息，比如工商信息
                        获取每个小表所占数据的多少
                        再根据数量判断该不该需要再次请求下一页
                        """
                        inquire_dict = {}
                        company_nav_list = company_json["company"]["companyNav"]
                        for company_nav in company_nav_list:
                            company_nav_name = company_nav.get('name')
                            print(f"公司导航首层：{company_nav_name}")
                            company_nav_children_list = company_nav.get('children')
                            for company_nav_children in company_nav_children_list:
                                company_nav_children_name = company_nav_children.get('name')
                                company_nav_children_count = company_nav_children.get('count')
                                print(f'公司导航次层：{company_nav_children_name}，数据条数：{company_nav_children_count}')
                                if type(company_nav_children_count) == int:
                                    inquire_dict[company_nav_children_name] = company_nav_children_count
                        print(inquire_dict)
                        # return

                        # 企业年报
                        try:
                            company_reportyear = company_json["datalist"]["reportyear"]["data"]
                        except:
                            company_reportyear = []
                        # dispose_success_data(company_reportyear, 'annual_report', 'annual_report:current', key_no,
                        #                      from_queue, webpage_id)
                        '''
                        企业年报获取到年报的详细信息，待完善
                        '''
                        annual_report_info_list = []
                        nianbao_shareholder_list = []
                        nianbao_modify_record_list = []
                        for reportyear_data in company_reportyear:
                            # 获取年报的基本详情
                            reportyear_id = reportyear_data.get('Id')
                            year_str = reportyear_data.get('Year')
                            year_num = re.findall(r'\d+', year_str)[0]
                            if reportyear_id:
                                reportyear_url = f'https://www.qcc.com/webReportYearDetail/{key_no}_{year_num}.html'
                                reportyear_value = requests.get(reportyear_url, headers=headers, cookies=cookie_dict)
                                time.sleep(12)
                                reportyear_html = reportyear_value.text
                                nianbao_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', reportyear_html)

                                nianbao_json = json.loads(nianbao_data[0])
                                print(nianbao_json)
                                annual_report_info = nianbao_json["detail"]["reportYearEntity"]["reportInfo"]
                                annual_report_info_list.append(annual_report_info)

                                # # 年报股东信息
                                # nianbao_shareholder_num = int(nianbao_json["detail"]["reportYearEntity"]["reportInfo"]["NodesCount"]["PartnersCount"])
                                # if 0 < nianbao_shareholder_num <= 10:
                                #     nianbao_shareholder = nianbao_json["detail"]["reportYearEntity"]["partnersList"]["Result"]
                                #     for nianbao_shareholder_data in nianbao_shareholder:
                                #         nianbao_shareholder_data['year'] = year_num
                                #         nianbao_shareholder_list.append(nianbao_shareholder_data)
                                # elif nianbao_shareholder_num > 10:
                                #     nianbao_shareholder_page = math.ceil(nianbao_shareholder_num / 10)
                                #     for page_ in range(1, nianbao_shareholder_page + 1):
                                #         nianbao_shareholder_url = f'https://www.qcc.com/api/datalist/annualReportPartnerList'
                                #         json_data = {
                                #             'pageIndex': page_,
                                #             'keyNo': f'{key_no}',
                                #             'year': f'{year_str}',
                                #         }
                                #         nianbao_shareholder_value = post_response(nianbao_shareholder_url, key_no, pid, tid, cookie_dict, json_data)
                                #         captcha_value = encounter_captcha(nianbao_shareholder_value, page)
                                #         if captcha_value in ['没有遇到验证码']:
                                #             nianbao_shareholder = nianbao_shareholder_value['data']
                                #             for nianbao_shareholder_data in nianbao_shareholder:
                                #                 nianbao_shareholder_data['year'] = year_num
                                #                 nianbao_shareholder_list.append(nianbao_shareholder_data)
                                #             time.sleep(13)
                                #         else:
                                #             # 先将请求数据上传到数据库中，后续处理
                                #             json_data = json.dumps(json_data, ensure_ascii=False)
                                #             up_qcc_res_data(nianbao_shareholder_url, 'annual_report_shareholder', 'post', json_data, key_no,
                                #                             webpage_id)

                                # 年报修改记录
                                nianbao_modify_record_num = int(nianbao_json["detail"]["reportYearEntity"]["reportInfo"]["NodesCount"]["ChangeCount"])
                                if 0 < nianbao_modify_record_num <= 10:
                                    nianbao_modify_record = nianbao_json["detail"]["reportYearEntity"]["reportInfo"]["ChangeList"]
                                    for nianbao_modify_record_data in nianbao_modify_record:
                                        nianbao_modify_record_data['year'] = year_num
                                        nianbao_modify_record_list.append(nianbao_modify_record_data)
                                elif nianbao_modify_record_num > 10:
                                    nianbao_modify_record_page = math.ceil(nianbao_modify_record_num / 10)
                                    for page_ in range(1, nianbao_modify_record_page + 1):
                                        nianbao_modify_record_url = f'https://www.qcc.com/api/datalist/annualReportChangeList'
                                        json_data = {
                                            'pageIndex': page_,
                                            'keyNo': f'{key_no}',
                                            'year': f'{year_str}',
                                        }
                                        nianbao_modify_record_value = post_response(nianbao_modify_record_url, key_no, pid, tid, cookie_dict, json_data)
                                        captcha_value = encounter_captcha(nianbao_modify_record_value, page)
                                        if captcha_value in ['没有遇到验证码']:
                                            nianbao_modify_record = nianbao_modify_record_value['data']
                                            for nianbao_modify_record_data in nianbao_modify_record:
                                                nianbao_modify_record_data['year'] = year_num
                                                nianbao_modify_record_list.append(nianbao_modify_record_data)
                                            time.sleep(13)
                                        else:
                                            # 先将请求数据上传到数据库中，后续处理
                                            json_data = json.dumps(json_data, ensure_ascii=False)
                                            up_qcc_res_data(nianbao_modify_record_url, 'annual_report_change', 'post', json_data, key_no,
                                                            webpage_id)

                        # print(annual_report_info_list)
                        # print(nianbao_shareholder_list)
                        # input('数据获取完成')
                        # dispose_success_data(annual_report_info_list, 'annual_report_info',
                        #                      'annual_report_info:current', key_no,
                        #                      from_queue,
                        #                      webpage_id)
                        # dispose_success_data(nianbao_shareholder_list, 'annual_report_shareholder',
                        #                      'annual_report_shareholder:current', key_no,
                        #                      from_queue,
                        #                      webpage_id)
                        dispose_success_data(nianbao_modify_record_list, 'annual_report_change',
                                             'annual_report_change:current', key_no,
                                             from_queue,
                                             webpage_id)
                        # 对于封禁的数据，需要单独处理（从数据库中获取信息）
                        sql_data = get_ban_data(webpage_id)
                        for ban_id, url, data_key, res_type, json_data, key_no, from_queue, webpage_id in sql_data:
                            # print(ban_id, url, data_key, res_type, json_data, key_no, webpage_id)
                            if res_type == 'post':
                                # 转为json数据
                                json_data = json.loads(json_data)
                                value_ban = post_response(url, key_no, pid, tid, cookie_dict, json_data=json_data)
                                if value_ban:
                                    for data_value in value_ban['data']:
                                        if data_key in ['business_info', 'credit_eval', 'trade_credit']:
                                            data_md5 = generate_md5(str(data_value))
                                            data_status = "current"
                                            data_json = json.dumps(data_value, ensure_ascii=False)
                                            up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue,
                                                        webpage_id)
                                        elif data_key in ['annual_report_shareholder', 'annual_report_change']:
                                            year_str = json_data['year']
                                            year_num = re.findall(r'\d+', year_str)[0]
                                            data_status = 'current'
                                            data_value['year'] = year_num
                                            data_md5 = generate_md5(str(data_value))
                                            data_json = json.dumps(data_value, ensure_ascii=False)
                                            up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue,
                                                        webpage_id)


                                        else:
                                            if 'his_' in data_key:
                                                # 历史信息，增加标识
                                                data_status = 'history'
                                                # for up_data in data_value:
                                                if data_value:
                                                    data_key = data_key.replace('his_', '')
                                                    data_json = json.dumps(data_value, ensure_ascii=False)
                                                    data_md5 = generate_md5(str(data_value))
                                                    up_qcc_data(key_no, data_key, data_status, data_md5, data_json,
                                                                from_queue,
                                                                webpage_id)
                                            else:
                                                # for up_data in data_value:
                                                if data_value:
                                                    data_status = "current"
                                                    data_json = json.dumps(data_value, ensure_ascii=False)
                                                    data_md5 = generate_md5(str(data_value))
                                                    up_qcc_data(key_no, data_key, data_status, data_md5, data_json,
                                                                from_queue,
                                                                webpage_id)
                                    del_ban_data(ban_id)
                            elif res_type == 'get':
                                value_ban = get_response(url, key_no, pid, tid, cookie_dict)
                                if value_ban:
                                    for data_value in value_ban['data']:
                                        if data_key in ['business_info', 'credit_eval', 'trade_credit']:
                                            data_md5 = generate_md5(str(data_value))
                                            data_status = "current"
                                            data_json = json.dumps(data_value, ensure_ascii=False)
                                            up_qcc_data(key_no, data_key, data_status, data_md5, data_json, from_queue,
                                                        webpage_id)

                                        else:
                                            if 'his_' in data_key:
                                                # 历史信息，增加标识
                                                data_status = 'history'
                                                # for up_data in data_value:
                                                if data_value:
                                                    data_key = data_key.replace('his_', '')
                                                    data_json = json.dumps(data_value, ensure_ascii=False)
                                                    data_md5 = generate_md5(str(data_value))
                                                    up_qcc_data(key_no, data_key, data_status, data_md5, data_json,
                                                                from_queue,
                                                                webpage_id)
                                            else:
                                                data_status = "current"
                                                if data_key == 'bid':
                                                    data_json = json.dumps(data_value, ensure_ascii=False)
                                                    data_md5 = generate_md5(str(data_value))
                                                    up_qcc_data(key_no, data_key, data_status, data_md5, data_json,
                                                                from_queue,
                                                                webpage_id)
                                                else:
                                                    # for up_data in data_value:
                                                    if data_value:
                                                        data_json = json.dumps(data_value, ensure_ascii=False)
                                                        data_md5 = generate_md5(str(data_value))
                                                        up_qcc_data(key_no, data_key, data_status, data_md5,
                                                                    data_json,
                                                                    from_queue,
                                                                    webpage_id)
                                    del_ban_data(ban_id)

                        return True
            else:
                pass

    else:
        print("网站限制")
        print("获取数据失败")
        # 直接调取失败接口
        fail_data = {
            'id': from_queue,
            'description': f'数据获取失败, 网站限制',
        }
        paper_queue_fail(data=fail_data)

        try:
            get_captcha(page)
        except:
            time.sleep(3600)
        time.sleep(10)
        page.refresh()
        time.sleep(5)
        page.refresh()
        # 判断是否为扫描二维码
        # page.quit()
        return False

company_list = [
    # "常州市兰新建筑工程有限公司",
    # "印力商用置业有限公司",
    # "杭州电鲸网络科技有限公司",
    # "江苏瑞恒新材料科技有限公司",
    # "丹阳市华琪汽车内饰件厂",
    # "江苏天和汽配有限公司",
    # "丹阳市浩源车业有限公司",
    "江苏长丰耐火材料有限公司",
    "江苏锐光车业有限公司",
    "江苏华鹏电缆股份有限公司",
    "丹阳市明珠工具有限公司",
    "江苏德泰电子科技有限公司",
    "江苏泰德机械制造有限公司"
]
for company in company_list:
    print(company)
    qcc_search_company(company, 1999837, 17417)
    time.sleep(10)
# qcc_search_company('萨驰智能装备股份有限公司', 123, 345)
