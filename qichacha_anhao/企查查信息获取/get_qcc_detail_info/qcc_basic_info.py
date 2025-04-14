"""
获取企查查的查询详细页的基础信息
存在翻页的需要再次请求一下
"""
import json
import math
import random
import re
from datetime import datetime, timedelta

from 验证码识别 import get_captcha
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from qcc_auto_login import auto_login
from qcc_api_res import get_response, post_response


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

def encounter_captcha(value_json):
    if value_json.get('message'):
        if value_json.get('message') == '未满足前提条件':
            input('遇到验证码')

def qcc_search_company(search_company_name):
    search_company_name = search_company_name
    hit_field_list = ['曾用名']  # 股东，曾用名
    random_num = random.randint(1, 6)

    co = ChromiumOptions()
    # co = co.set_user_data_path(r"C:\chome_data\data_nibo")
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

    params = {
        'key': search_company_name,
    }
    response = requests.get('https://www.qcc.com/web/search', params=params, cookies=cookie_dict, headers=headers)
    time.sleep(random_num)
    res_html = response.text
    res_json = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', res_html)
    if res_json:
        # page.quit()
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
            else:
                pass
            if flag:
                target_url = f'https://www.qcc.com/firm/{key_no}.html'
                response = requests.get(target_url, cookies=cookie_dict, headers=headers)
                time.sleep(random_num)
                company_html = response.text
                pid_list = re.findall(r"<script>window\.pid='(.*?)'; window\.tid", company_html)
                tid_list = re.findall(r"window\.tid='(.*?)'</script>", company_html)
                pid = pid_list[0]
                tid = tid_list[0]
                company_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', company_html)
                susong_url = f'https://www.qcc.com/csusong/{key_no}.html'
                susong_response = requests.get(susong_url, cookies=cookie_dict, headers=headers)
                time.sleep(random_num)
                susong_html = susong_response.text
                susong_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', susong_html)
                cfengxian_url = f'https://www.qcc.com/cfengxian/{key_no}.html'
                cfengxian_response = requests.get(cfengxian_url, cookies=cookie_dict, headers=headers)
                time.sleep(random_num)
                cfengxian_html = cfengxian_response.text
                cfengxian_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', cfengxian_html)
                crun_url = f'https://www.qcc.com/crun/{key_no}.html'
                crun_response = requests.get(crun_url, cookies=cookie_dict, headers=headers)
                time.sleep(random_num)
                crun_html = crun_response.text
                crun_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', crun_html)
                cassets_url = f'https://www.qcc.com/cassets/{key_no}.html'
                cassets_response = requests.get(cassets_url, cookies=cookie_dict, headers=headers)
                time.sleep(random_num)
                cassets_html = cassets_response.text
                cassets_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', cassets_html)
                chistory_url = f'https://www.qcc.com/chistory/{key_no}.html'
                chistory_response = requests.get(chistory_url, cookies=cookie_dict, headers=headers)
                time.sleep(random_num)
                chistory_html = chistory_response.text
                chistory_data = re.findall(r'window\.__INITIAL_STATE__=(.*?);\(function', chistory_html)
                # print(company_data[0])
                # return
                # 刚开始获取json数据
                if company_data and susong_data and cfengxian_data and crun_data and cassets_data and chistory_data:
                    company_json = json.loads(company_data[0])
                    susong_json = json.loads(susong_data[0])
                    cfengxian_json = json.loads(cfengxian_data[0])
                    crun_json = json.loads(crun_data[0])
                    cassets_json = json.loads(cassets_data[0])
                    chistory_json = json.loads(chistory_data[0])
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
                    """
                    获取每个表的json信息
                    """
                    """
                    基本信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    """
                    # 工商信息
                    company_detail = company_json["company"][
                        "companyDetail"]
                    # 股东信息
                    partner_num = inquire_dict.get('股东信息')
                    # 少于50个的情况下
                    if 0 < partner_num <= 50:
                        company_partners = company_json["datalist"]["partner"]
                    # 多于50个的情况下
                    elif partner_num > 50:    # 股东信息可以显示超过十个
                        company_partners = []
                        partner_page = math.ceil(partner_num / 50)
                        for page in range(1, partner_page + 1):
                            partner_url = f'https://www.qcc.com/api/datalist/partner?keyNo={key_no}&pageIndex={page}&pageSize=50&type=IpoPartners'
                            partner_value = get_response(partner_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(partner_value)
                            company_partners.append(partner_value)
                            time.sleep(7)
                    else:
                        company_partners = []
                    # 主要人员
                    employees_num = inquire_dict.get('主要人员')
                    # 少于10个的情况下
                    if 0 < employees_num <= 10:
                        company_employees = company_json["company"]["companyDetail"]["Employees"]
                    # 多于10个的情况下
                    elif employees_num > 10:
                        company_employees = []
                        employees_page = math.ceil(employees_num / 10)
                        for page in range(1, employees_page + 1):
                            employees_url = f'https://www.qcc.com/api/datalist/mainmember?isNewAgg=true&keyNo={key_no}&nodeName=Employees&pageIndex={page}'
                            employees_value = get_response(employees_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(employees_value)
                            company_employees.append(employees_value)
                            time.sleep(7)
                    else:
                        company_employees = []
                    # 对外投资
                    touzilist_num = inquire_dict.get('对外投资')
                    # 少于10个的情况下
                    if 0 < touzilist_num <= 10:
                        company_touzilist = company_json["datalist"]["touzilist"]["data"]
                    # 多于10个的情况下
                    elif touzilist_num > 10:
                        company_touzilist = []
                        touzilist_page = math.ceil(touzilist_num / 10)
                        for page in range(1, touzilist_page + 1):
                            touzilist_url = f'https://www.qcc.com/api/datalist/touzilist?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                            touzilist_value = get_response(touzilist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(touzilist_value)
                            touzilist_value_data = touzilist_value["data"]
                            for touzilist_data in touzilist_value_data:
                                company_touzilist.append(touzilist_data)
                            time.sleep(7)
                    else:
                        company_touzilist = []
                    # # 间接对外投资
                    # # 少于10个的情况下
                    # if 0 < touzilist_num <= 10:
                    #     company_holdcolist = company_json["datalist"]["holdcolist"]["data"]
                    # # 多于10个的情况下
                    # elif touzilist_num > 10:
                    #     company_holdcolist = []
                    #     holdcolist_page = math.ceil(touzilist_num / 10)
                    #     for page in range(1, holdcolist_page + 1):
                    #         holdcolist_url = f'https://www.qcc.com/api/datalist/indirecttouzilist?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                    #         holdcolist_value = get_response(holdcolist_url, key_no, pid, tid, cookie_dict)
                    #         encounter_captcha(holdcolist_value)
                    #
                    #         company_holdcolist.append(holdcolist_value)
                    #         time.sleep(7)
                    # else:
                    #     company_holdcolist = []
                    # 历史对外投资
                    histouzilist_num = inquire_dict.get('历史对外投资')
                    # 少于10个的情况下
                    if 0 < histouzilist_num <= 10:
                        chistory_histouzilist = chistory_json["datalist"]["histouzilist"]["data"]
                    # 多于10个的情况下
                    elif histouzilist_num > 10:
                        chistory_histouzilist = []
                        histouzilist_page = math.ceil(histouzilist_num / 10)
                        for page in range(1, histouzilist_page + 1):
                            histouzilist_url = f'https://www.qcc.com/api/datalist/touzilist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}'
                            histouzilist_value = get_response(histouzilist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(histouzilist_value)
                            histouzilist_value_data = histouzilist_value['data']
                            for histouzilist_data in histouzilist_value_data:
                                chistory_histouzilist.append(histouzilist_data)
                            time.sleep(7)
                    else:
                        chistory_histouzilist = []
                    # 变更记录
                    changelist_num = inquire_dict.get('变更记录')
                    # 少于10个的情况下
                    if 0 < changelist_num <= 10:
                        company_changelist = company_json["datalist"]["changelist"]["data"]
                    # 多于10个的情况下
                    elif changelist_num > 10:
                        company_changelist = []
                        changelist_page = math.ceil(changelist_num / 10)
                        for page in range(1, changelist_page + 1):
                            changelist_url = f'https://www.qcc.com/api/datalist/changelist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                                'isAggs': True,
                            }
                            changelist_value = post_response(changelist_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(changelist_value)
                            changelist_value_data = changelist_value['data']
                            for changelist_data in changelist_value_data:
                                company_changelist.append(changelist_data)
                            time.sleep(7)
                    else:
                        company_changelist = []
                    # 企业年报
                    company_reportyear = company_json["datalist"]["reportyear"]["data"]
                    '''
                    企业年报获取到年报的详细信息，待完善
                    '''
                    # 疑似关系
                    suspectlist_num = inquire_dict.get('疑似关系')
                    if not suspectlist_num:
                        suspectlist_num = 0
                    # 少于10个的情况下
                    if 0 < suspectlist_num <= 10:
                        company_suspectlist = company_json["datalist"]["suspectlist"]["data"]
                    # 多于10个的情况下
                    elif suspectlist_num > 10:
                        company_suspectlist = []
                        suspectlist_page = math.ceil(suspectlist_num / 10)
                        for page in range(1, suspectlist_page + 1):
                            suspectlist_url = f'https://www.qcc.com/api/datalist/suspectlist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                            }
                            suspectlist_value = post_response(suspectlist_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(suspectlist_value)
                            suspectlist_value_data = suspectlist_value['data']
                            for suspectlist_data in suspectlist_value_data:
                                company_suspectlist.append(suspectlist_data)
                            time.sleep(7)
                    else:
                        company_suspectlist = []

                    """
                    法律诉讼!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    """
                    # 司法案件
                    susong_caselist_num = inquire_dict.get('司法案件')
                    # 少于10个的情况下
                    if 0 < susong_caselist_num <= 10:
                        susong_caselist = susong_json["datalist"]["caselist"]["data"]
                    # 多于10个的情况下
                    elif susong_caselist_num > 10:
                        susong_caselist = []
                        caselist_page = math.ceil(susong_caselist_num / 10)
                        for page in range(1, caselist_page + 1):
                            caselist_url = f"https://www.qcc.com/api/datalist/caselist?isCombine=true&isNewAgg=true&keyNo={key_no}&pageIndex={page}&province=&round=&tag=&videoFlag=&year="
                            caselist_value = get_response(caselist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(caselist_value)
                            caselist_value_data = caselist_value["data"]
                            for caselist_data in caselist_value_data:
                                susong_caselist.append(caselist_data)
                            time.sleep(7)
                    else:
                        susong_caselist = []
                    # 裁判文书
                    susong_wenshulist_num = inquire_dict.get('裁判文书')
                    # 少于10个的情况下
                    if 0 < susong_wenshulist_num <= 10:
                        susong_wenshulist = susong_json["datalist"]["wenshulist"]["data"]
                    # 多于10个的情况下
                    elif susong_wenshulist_num > 10:
                        susong_wenshulist = []
                        wenshulist_page = math.ceil(susong_wenshulist_num / 10)
                        for page in range(1, wenshulist_page + 1):
                            wenshulist_url = f"https://www.qcc.com/api/datalist/wenshulist?isNewAgg=true&keyNo={key_no}&pageIndex={page}&searchKey={key_no}"
                            wenshulist_value = get_response(wenshulist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(wenshulist_value)
                            wenshulist_value_data = wenshulist_value["data"]
                            for wenshulist_data in wenshulist_value_data:
                                susong_wenshulist.append(wenshulist_data)
                            time.sleep(7)
                    else:
                        susong_wenshulist = []
                    # 立案信息
                    susong_lawcaselist_num = inquire_dict.get('立案信息')
                    # 少于10个的情况下
                    if 0 < susong_lawcaselist_num <= 10:
                        susong_lianliast = susong_json["datalist"]["lianlist"]["data"]
                    # 多于10个的情况下
                    elif susong_lawcaselist_num > 10:
                        susong_lianliast = []
                        lianlist_page = math.ceil(susong_lawcaselist_num / 10)
                        for page in range(1, lianlist_page + 1):
                            lianlist_url = f"https://www.qcc.com/api/datalist/lianlist?isNewAgg=true&keyNo={key_no}&pageIndex={page}"
                            lianlist_value = get_response(lianlist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(lianlist_value)
                            lianlist_value_data = lianlist_value["data"]
                            for lianlist_data in lianlist_value_data:
                                susong_lianliast.append(lianlist_data)
                            time.sleep(7)
                    else:
                        susong_lianliast = []
                    # 开庭公告
                    susong_ktgglist_num = inquire_dict.get('开庭公告')
                    # 少于10个的情况下
                    if 0 < susong_ktgglist_num <= 10:
                        susong_noticelist = susong_json["datalist"]["noticelist"]["data"]
                    # 多于10个的情况下
                    elif susong_ktgglist_num > 10:
                        susong_noticelist = []
                        ktgglist_page = math.ceil(susong_ktgglist_num / 10)
                        for page in range(1, ktgglist_page + 1):
                            ktgglist_url = f"https://www.qcc.com/api/datalist/noticelist?isNewAgg=true&keyNo={key_no}&KeyNo={key_no}&pageIndex={page}"
                            ktgglist_value = get_response(ktgglist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(ktgglist_value)
                            ktgglist_value_data = ktgglist_value["data"]
                            for ktgglist_data in ktgglist_value_data:
                                susong_noticelist.append(ktgglist_data)
                            time.sleep(7)
                    else:
                        susong_noticelist = []
                    # 法院公告
                    susong_courtlist_num = inquire_dict.get('法院公告')
                    # 少于10个的情况下
                    if 0 < susong_courtlist_num <= 10:
                        susong_gonggaolist = susong_json["datalist"]["gonggaolist"]["data"]
                    # 多于10个的情况下
                    elif susong_courtlist_num > 10:
                        susong_gonggaolist = []
                        courtlist_page = math.ceil(susong_courtlist_num / 10)
                        for page in range(1, courtlist_page + 1):
                            courtlist_url = f"https://www.qcc.com/api/datalist/gonggaolist?isNewAgg=true&keyNo={key_no}&pageIndex={page}&searchKey={key_no}&sortField=PublishDate"
                            courtlist_value = get_response(courtlist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(courtlist_value)
                            courtlist_value_data = courtlist_value["data"]
                            for courtlist_data in courtlist_value_data:
                                susong_gonggaolist.append(courtlist_data)
                            time.sleep(7)
                    else:
                        susong_gonggaolist = []
                    # 送达公告
                    susong_sentlist_num = inquire_dict.get('送达公告')
                    # 少于10个的情况下
                    if 0 < susong_sentlist_num <= 10:
                        susong_dnoticelist = susong_json["datalist"]["dnoticelist"]["data"]
                    # 多于10个的情况下
                    elif susong_sentlist_num > 10:
                        susong_dnoticelist = []
                        sentlist_page = math.ceil(susong_sentlist_num / 10)
                        for page in range(1, sentlist_page + 1):
                            sentlist_url = f"https://www.qcc.com/api/datalist/dnoticelist?isNewAgg=true&keyNo={key_no}&pageIndex={page}"
                            sentlist_value = get_response(sentlist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(sentlist_value)
                            sentlist_value_data = sentlist_value["data"]
                            for sentlist_data in sentlist_value_data:
                                susong_dnoticelist.append(sentlist_data)
                            time.sleep(7)
                    else:
                        susong_dnoticelist = []
                    # 诉前调解
                    susong_pretrialmediationlist_num = inquire_dict.get('诉前调解')
                    # 少于10个的情况下
                    if 0 < susong_pretrialmediationlist_num <= 10:
                        susong_pretrialmediationlist = susong_json["datalist"]["pretrialmediationlist"]["data"]
                    # 多于10个的情况下
                    elif susong_pretrialmediationlist_num > 10:
                        susong_pretrialmediationlist = []
                        pretrialmediationlist_page = math.ceil(susong_pretrialmediationlist_num / 10)
                        for page in range(1, pretrialmediationlist_page + 1):
                            pretrialmediationlist_url = f"https://www.qcc.com/api/datalist/pretrialmediationlist?caseType=2&isNewAgg=true&keyNo={key_no}&pageIndex={page}"
                            pretrialmediationlist_value = get_response(pretrialmediationlist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(pretrialmediationlist_value)
                            pretrialmediationlist_value_data = pretrialmediationlist_value["data"]
                            for pretrialmediationlist_data in pretrialmediationlist_value_data:
                                susong_pretrialmediationlist.append(pretrialmediationlist_data)
                            time.sleep(7)
                    else:
                        susong_pretrialmediationlist = []
                    # 司法拍卖
                    susong_judicialsalelist_num = inquire_dict.get('司法拍卖')
                    # 少于10个的情况下
                    if 0 < susong_judicialsalelist_num <= 10:
                        susong_judicialsalelist = susong_json["datalist"]["judicialsalelist"]["data"]
                    # 多于10个的情况下
                    elif susong_judicialsalelist_num > 10:
                        susong_judicialsalelist = []
                        judicialsalelist_page = math.ceil(susong_judicialsalelist_num / 10)
                        for page in range(1, judicialsalelist_page + 1):
                            judicialsalelist_url = f"https://www.qcc.com/api/datalist/judicialsalelist?isNewAgg=true&keyNo={key_no}&KeyNo={key_no}&pageIndex={page}"
                            judicialsalelist_value = get_response(judicialsalelist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(judicialsalelist_value)
                            judicialsalelist_value_data = judicialsalelist_value["data"]
                            for judicialsalelist_data in judicialsalelist_value_data:
                                susong_judicialsalelist.append(judicialsalelist_data)
                            time.sleep(7)
                    else:
                        susong_judicialsalelist = []
                    # 失信被执行人
                    susong_shixinlist_num = inquire_dict.get('失信被执行人')
                    # 少于10个的情况下
                    if 0 < susong_shixinlist_num <= 10:
                        susong_shixinlist = susong_json["datalist"]["shixinlist"]["data"]
                    # 多于10个的情况下
                    elif susong_shixinlist_num > 10:
                        susong_shixinlist = []
                        input('失信被执行人超过十个，建议处理')
                        shixinlist_page = math.ceil(susong_shixinlist_num / 10)
                        for page in range(1, shixinlist_page + 1):
                            shixinlist_url = f"https://www.qcc.com/api/datalist/shixinlist?isNewAgg=true&keyNo={key_no}&pageIndex={page}"
                            pass
                    else:
                        susong_shixinlist = []
                    # 终本案件
                    susong_endexecutioncaselist_num = inquire_dict.get('终本案件')
                    # 少于10个的情况下
                    if 0 < susong_endexecutioncaselist_num <= 10:
                        susong_endexecutioncaselist = susong_json["datalist"]["endexecutioncaselist"]["data"]
                    # 多于10个的情况下
                    elif susong_endexecutioncaselist_num > 10:
                        susong_endexecutioncaselist = []
                        endexecutioncaselist_page = math.ceil(susong_endexecutioncaselist_num / 10)
                        for page in range(1, endexecutioncaselist_page + 1):
                            endexecutioncaselist_url = f"https://www.qcc.com/api/datalist/endexecutioncaselist?isNewAgg=true&keyNo={key_no}&pageIndex={page}"
                            endexecutioncaselist_value = get_response(endexecutioncaselist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(endexecutioncaselist_value)
                            endexecutioncaselist_value_data = endexecutioncaselist_value["data"]
                            for endexecutioncaselist_data in endexecutioncaselist_value_data:
                                susong_endexecutioncaselist.append(endexecutioncaselist_data)
                            time.sleep(7)
                    else:
                        susong_endexecutioncaselist = []


                    """
                    经营风险!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    """
                    # 严重违法
                    cfengxian_serious_illegal_num = inquire_dict.get('严重违法')
                    # 少于10个的情况下
                    if 0 < cfengxian_serious_illegal_num <= 10:
                        cfengxian_svlist = cfengxian_json["datalist"]["svlist"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_serious_illegal_num > 10:
                        cfengxian_svlist = []
                        input("严重违法超过十个，请获取")
                    else:
                        cfengxian_svlist = []
                    # 股权出质
                    cfengxian_pledgelist_num = inquire_dict.get('股权出质')
                    # 少于10个的情况下
                    if 0 < cfengxian_pledgelist_num <= 10:
                        cfengxian_pledgelist = cfengxian_json["datalist"]["pledgelist"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_pledgelist_num > 10:
                        cfengxian_pledgelist = []
                        pledgelist_page = math.ceil(cfengxian_pledgelist_num / 10)
                        for page in range(1, pledgelist_page + 1):
                            pass  # 暂未找到超过十个的
                    else:
                        cfengxian_pledgelist = []
                    # 经营异常
                    cfengxian_exceptions_num = inquire_dict.get('经营异常')
                    # 少于10个的情况下
                    if 0 < cfengxian_exceptions_num <= 10:
                        cfengxian_exceptions = cfengxian_json["datalist"]["exceptions"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_exceptions_num > 10:
                        cfengxian_exceptions = []
                        exceptions_page = math.ceil(cfengxian_exceptions_num / 10)
                        for page in range(1, exceptions_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        cfengxian_exceptions = []
                    # 动产抵押
                    cfengxian_mpledgelist_num = inquire_dict.get('动产抵押')
                    # 少于10个的情况下
                    if 0 < cfengxian_mpledgelist_num <= 10:
                        cfengxian_mpledgelist = cfengxian_json["datalist"]["mpledgelist"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_mpledgelist_num > 10:
                        cfengxian_mpledgelist = []
                        mpledgelist_page = math.ceil(cfengxian_mpledgelist_num / 10)
                        for page in range(1, mpledgelist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        cfengxian_mpledgelist = []
                    # 注销备案
                    cfengxian_cancelrecordlist_num = inquire_dict.get('注销备案')
                    # 少于10个的情况下
                    if 0 < cfengxian_cancelrecordlist_num <= 10:
                        cfengxian_enliqinfo = cfengxian_json["datalist"]["enliqinfo"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_cancelrecordlist_num > 10:
                        cfengxian_enliqinfo = []
                        enliqinfo_page = math.ceil(cfengxian_cancelrecordlist_num / 10)
                        for page in range(1, enliqinfo_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        cfengxian_enliqinfo = []
                    # 行政处罚
                    cfengxian_adminpenaltylist_num = inquire_dict.get('行政处罚')
                    # 少于10个的情况下
                    if 0 < cfengxian_adminpenaltylist_num <= 10:
                        cfengxian_adminpenaltylist = cfengxian_json["datalist"]["adminpenaltylist"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_adminpenaltylist_num > 10:
                        cfengxian_adminpenaltylist = []
                        adminpenaltylist_page = math.ceil(cfengxian_adminpenaltylist_num / 10)
                        for page in range(1, adminpenaltylist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        cfengxian_adminpenaltylist = []
                    # 环保处罚
                    cfengxian_envpenaltylist_num = inquire_dict.get('环保处罚')
                    # 少于10个的情况下
                    if 0 < cfengxian_envpenaltylist_num <= 10:
                        cfengxian_envlist = cfengxian_json["datalist"]["envlist"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_envpenaltylist_num > 10:
                        cfengxian_envlist = []
                        envlist_page = math.ceil(cfengxian_envpenaltylist_num / 10)
                        for page in range(1, envlist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        cfengxian_envlist = []
                    # 税务非正常户
                    cfengxian_taxabnormallist_num = inquire_dict.get('税务非正常户')
                    # 少于10个的情况下
                    if 0 < cfengxian_taxabnormallist_num <= 10:
                        cfengxian_taxabnormallist = cfengxian_json["datalist"]["taxabnormallist"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_taxabnormallist_num > 10:
                        cfengxian_taxabnormallist = []
                        taxabnormallist_page = math.ceil(cfengxian_taxabnormallist_num / 10)
                        for page in range(1, taxabnormallist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        cfengxian_taxabnormallist = []
                    # 欠税公告(通过里面的id再次请求查看详情)
                    cfengxian_taxillegallist_num = inquire_dict.get('欠税公告')
                    # 少于10个的情况下
                    if 0 < cfengxian_taxillegallist_num <= 10:
                        cfengxian_owenoticelist = cfengxian_json["datalist"]["owenoticelist"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_taxillegallist_num > 10:
                        cfengxian_owenoticelist = []
                        owenoticelist_page = math.ceil(cfengxian_taxillegallist_num / 10)
                        for page in range(1, owenoticelist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        cfengxian_owenoticelist = []
                    # 税收违法
                    cfengxian_taxillegallist_num = inquire_dict.get('税收违法')
                    # 少于10个的情况下
                    if 0 < cfengxian_taxillegallist_num <= 10:
                        cfengxian_taxillegallist = cfengxian_json["datalist"]["taxillegallist"]["data"]
                    # 多于10个的情况下
                    elif cfengxian_taxillegallist_num > 10:
                        cfengxian_taxillegallist = []
                        taxillegallist_page = math.ceil(cfengxian_taxillegallist_num / 10)
                        for page in range(1, taxillegallist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        cfengxian_taxillegallist = []

                    """
                    经营信息
                    """
                    # 招投标
                    crun_tenderlist_num = inquire_dict.get('招投标')
                    # 少于10个的情况下
                    if 0 < crun_tenderlist_num <= 10:
                        crun_tenderlist = crun_json["datalist"]["tenderlist"]["data"]
                    # 多于10个的情况下
                    elif crun_tenderlist_num > 10:
                        crun_tenderlist = []
                        tenderlist_page = math.ceil(crun_tenderlist_num / 10)
                        for page in range(1, tenderlist_page + 1):
                            pass    # 暂未找到超过十个的, 招投标暂未解决
                    else:
                        crun_tenderlist = []
                    # 资质证书
                    crun_certificationsummary_num = inquire_dict.get('资质证书')
                    if crun_certificationsummary_num != 0:
                        crun_certificationsummary = []
                        certificationsummary_page = math.ceil(crun_certificationsummary_num / 10)
                        for page in range(1, certificationsummary_page + 1):
                            certificationsummary_url = f'https://www.qcc.com/api/datalist/certificationlist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'isNew': True,
                                'pageIndex': page,
                                'isNewAgg': True,
                            }
                            certificationsummary_value = post_response(certificationsummary_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(certificationsummary_value)
                            certificationsummary_value_data = certificationsummary_value["data"]
                            for certificationsummary_data in certificationsummary_value_data:
                                crun_certificationsummary.append(certificationsummary_data)
                            time.sleep(7)
                    else:
                        crun_certificationsummary = []
                    # 信用评价
                    crun_creditrating_num = inquire_dict.get('信用评价')
                    # 少于10个的情况下
                    if 0 < crun_creditrating_num <= 10:
                        crun_creditrate = crun_json["datalist"]["creditrate"]
                    # 多于10个的情况下
                    elif crun_creditrating_num > 10:
                        crun_creditrate = []
                        input('信用评价列表超过十个, 建议处理')
                        creditrate_page = math.ceil(crun_creditrating_num / 10)
                        for page in range(1, creditrate_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        crun_creditrate = []
                    # 招聘
                    crun_joblist_num = inquire_dict.get('招聘')
                    # 少于10个的情况下
                    if 0 < crun_joblist_num <= 10:
                        crun_joblist = crun_json["datalist"]["joblist"]["data"]
                    # 多于10个的情况下
                    elif crun_joblist_num > 10:
                        crun_joblist = []
                        joblist_page = math.ceil(crun_joblist_num / 10)
                        for page in range(1, joblist_page + 1):
                            joblist_url = f'https://www.qcc.com/api/datalist/joblist?isNewAgg=true&keyNo={key_no}&pageIndex={page}&sortField=publishtime'
                            joblist_value = requests.get(url=joblist_url, headers=headers).json()
                            encounter_captcha(joblist_value)
                            joblist_value_data = joblist_value["data"]
                            for joblist_data in joblist_value_data:
                                crun_joblist.append(joblist_data)
                            time.sleep(7)
                    else:
                        crun_joblist = []
                    # 进出口信用
                    try:
                        crun_ciaxlist = crun_json["datalist"]["ciaxlist"]["data"]
                    except:
                        crun_ciaxlist = []
                    # 土地信息
                    crun_landlist_num = inquire_dict.get('土地信息')
                    # 少于10个的情况下
                    if 0 < crun_landlist_num <= 10:
                        crun_landlist = crun_json["datalist"]["landlist"]["data"]
                    # 多于10个的情况下
                    elif crun_landlist_num > 10:
                        crun_landlist = []
                        input('土地信息列表超过十个, 建议处理')
                        landlist_page = math.ceil(crun_landlist_num / 10)
                        for page in range(1, landlist_page + 1):
                            landlist_url = f'https://www.qcc.com/api/datalist/landlist?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                            pass    # 暂未找到超过十个的
                    else:
                        crun_landlist = []
                    # 行政许可
                    crun_licenselist_num = inquire_dict.get('行政许可')
                    # 少于10个的情况下
                    if 0 < crun_licenselist_num <= 10:
                        crun_acolist = crun_json["datalist"]["acolist"]["data"]
                    # 多于10个的情况下
                    elif crun_licenselist_num > 10:
                        crun_acolist = []
                        aco_page = math.ceil(crun_licenselist_num / 10)
                        for page in range(1, aco_page + 1):
                            aco_url = f'https://www.qcc.com/api/datalist/acolist?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                            aco_value = get_response(aco_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(aco_value)
                            aco_value_data = aco_value["data"]
                            for aco_data in aco_value_data:
                                crun_acolist.append(aco_data)
                            time.sleep(7)
                    else:
                        crun_acolist = []
                    # 抽查检查
                    crun_spotchecklist_num = inquire_dict.get('抽查检查')
                    # 少于10个的情况下
                    if 0 < crun_spotchecklist_num <= 10:
                        crun_spotchecklist = crun_json["datalist"]["spotchecklist"]["data"]
                    # 多于10个的情况下
                    elif crun_spotchecklist_num > 10:
                        crun_spotchecklist = []
                        input('抽查检查列表超过十个, 建议处理')
                        spotchecklist_page = math.ceil(crun_spotchecklist_num / 10)
                        for page in range(1, spotchecklist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        crun_spotchecklist = []
                    # 食品安全
                    crun_foodsafetylist_num = inquire_dict.get('食品安全')
                    # 少于10个的情况下
                    if 0 < crun_foodsafetylist_num <= 10:
                        crun_foodsafetylist = crun_json["datalist"]["foodsafetylist"]["data"]
                    # 多于10个的情况下
                    elif crun_foodsafetylist_num > 10:
                        crun_foodsafetylist = []
                        foodsafetylist_page = math.ceil(crun_foodsafetylist_num / 10)
                        for page in range(1, foodsafetylist_page + 1):
                            foodsafetylist_url = f'https://www.qcc.com/api/datalist/foodsafetylist?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                            foodsafetylist_value = get_response(foodsafetylist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(foodsafetylist_value)
                            foodsafetylist_value_data = foodsafetylist_value["data"]
                            for foodsafetylist_data in foodsafetylist_value_data:
                                crun_foodsafetylist.append(foodsafetylist_data)
                            time.sleep(7)
                    else:
                        crun_foodsafetylist = []
                    # 双随机抽查
                    crun_randomlist_num = inquire_dict.get('双随机抽查')
                    # 少于10个的情况下
                    if 0 < crun_randomlist_num <= 10:
                        crun_drclist = crun_json["datalist"]["drclist"]["data"]
                    # 多于10个的情况下
                    elif crun_randomlist_num > 10:
                        crun_drclist = []
                        drclist_url = f'https://www.qcc.com/api/datalist/drclist?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                        drclist_value = get_response(drclist_url, key_no, pid, tid, cookie_dict)
                        encounter_captcha(drclist_value)
                        drclist_value_data = drclist_value["data"]
                        for drclist_data in drclist_value_data:
                            crun_drclist.append(drclist_data)
                        time.sleep(7)
                    else:
                        crun_drclist = []
                    # 纳税人资质
                    crun_taxpayerlist_num = inquire_dict.get('纳税人资质')
                    # 少于10个的情况下
                    if 0 < crun_taxpayerlist_num <= 10:
                        crun_taxpayerlist = crun_json["datalist"]["taxpayerlist"]["data"]
                    # 多于10个的情况下
                    elif crun_taxpayerlist_num > 10:
                        crun_taxpayerlist = []
                        input('纳税人资质列表超过十个, 建议处理')
                        taxpayerlist_page = math.ceil(crun_taxpayerlist_num / 10)
                        for page in range(1, taxpayerlist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        crun_taxpayerlist = []
                    # 产权交易
                    crun_transactionlist_num = inquire_dict.get('产权交易')
                    # 少于10人的情况下
                    if 0 < crun_transactionlist_num <= 10:
                        crun_transactionlist = crun_json["datalist"]["transactionlist"]["data"]
                    # 多于10人的情况下
                    elif crun_transactionlist_num > 10:
                        crun_transactionlist = []
                        input('产权交易列表超过十个, 建议处理')
                        transactionlist_page = math.ceil(crun_transactionlist_num / 10)
                        for page in range(1, transactionlist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        crun_transactionlist = []
                    # 资产拍卖
                    assetsalelist_num = inquire_dict.get('资产拍卖')
                    # 少于10人的情况下
                    if 0 < assetsalelist_num <= 10:
                        crun_assetsalelist = crun_json["datalist"]["assetsalelist"]["data"]
                    # 多于10人的情况下
                    elif assetsalelist_num > 10:
                        crun_assetsalelist = []
                        input('资产拍卖列表超过十个, 建议处理')
                        assetsalelist_page = math.ceil(assetsalelist_num / 10)
                        for page in range(1, assetsalelist_page + 1):
                            pass    # 暂未找到超过十个的
                    else:
                        crun_assetsalelist = []
                    # 电信许可
                    crun_telecomlist_num = inquire_dict.get('电信许可')
                    # 少于10个的情况下
                    if 0 < crun_telecomlist_num <= 10:
                        crun_telecomlist = crun_json["datalist"]["telecomlist"]["data"]
                    # 多于10个的情况下
                    elif crun_telecomlist_num > 10:
                        crun_telecomlist = []
                        input('电信许可列表超过十个, 建议处理')
                        telecomlist_page = math.ceil(crun_telecomlist_num / 10)
                        for page in range(1, telecomlist_page + 1):
                            pass
                    else:
                        crun_telecomlist = []

                    """
                    知识产权!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    """
                    # 商标信息
                    cassets_shangbiaolist_num = inquire_dict.get('商标信息')
                    # 少于10个的情况下
                    if 0 < cassets_shangbiaolist_num <= 10:
                        cassets_shangbiaolist = cassets_json["datalist"]["shangbiaolist"]["data"]
                    # 多于10个的情况下
                    elif cassets_shangbiaolist_num > 10:
                        cassets_shangbiaolist = []
                        shangbiaolist_page = math.ceil(cassets_shangbiaolist_num / 10)
                        for page in range(1, shangbiaolist_page + 1):
                            shangbiaolist_url = 'https://www.qcc.com/api/datalist/shangbiaolist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                            }
                            shangbiaolist_value = post_response(shangbiaolist_url,key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(shangbiaolist_value)
                            shangbiaolist_value_data = shangbiaolist_value["data"]
                            for shangbiaolist_data in shangbiaolist_value_data:

                                cassets_shangbiaolist.append(shangbiaolist_data)
                            time.sleep(6)
                    else:
                        cassets_shangbiaolist = []
                    # 商标文书
                    cassets_sbwslist_num = inquire_dict.get('商标文书')
                    # 少于10个的情况下
                    if 0 < cassets_sbwslist_num <= 10:
                        cassets_tmcdslist = cassets_json["datalist"]["tmcdslist"]["data"]
                    # 多于10个的情况下
                    elif cassets_sbwslist_num > 10:
                        cassets_tmcdslist = []
                        sbwslist_page = math.ceil(cassets_sbwslist_num / 10)
                        for page in range(1, sbwslist_page + 1):
                            sbwslist_url = f'https://www.qcc.com/api/datalist/tmcdslist?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                            sbwslist_value = get_response(sbwslist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(sbwslist_value)
                            sbwslist_value_data = sbwslist_value["data"]
                            for sbwslist_data in sbwslist_value_data:

                                cassets_tmcdslist.append(sbwslist_data)
                            time.sleep(6)
                    else:
                        cassets_tmcdslist = []
                    # 专利信息
                    cassets_zhuanlilist_num = inquire_dict.get('专利信息')
                    # 少于10个的情况下
                    if 0 < cassets_zhuanlilist_num <= 10:
                        cassets_zhuanlilist = cassets_json["datalist"]["zhuanlilist"]["data"]
                    # 多于10个的情况下
                    elif cassets_zhuanlilist_num > 10:
                        cassets_zhuanlilist = []
                        zhuanlilist_page = math.ceil(cassets_zhuanlilist_num / 10)
                        for page in range(1, zhuanlilist_page + 1):
                            zhuanlilist_url = f'https://www.qcc.com/api/datalist/zhuanlilist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                            }
                            zhuanlilist_value = post_response(zhuanlilist_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(zhuanlilist_value)
                            zhuanlilist_value_data = zhuanlilist_value["data"]
                            for zhuanlilist_data in zhuanlilist_value_data:
                                cassets_zhuanlilist.append(zhuanlilist_data)
                            time.sleep(6)
                    else:
                        cassets_zhuanlilist = []
                    # 作品著作权
                    cassets_zzqlist_num = inquire_dict.get('作品著作权')
                    # 少于10个的情况下
                    if 0 < cassets_zzqlist_num <= 10:
                        cassets_zzqlist = cassets_json["datalist"]["zzqlist"]["data"]
                    # 多于10个的情况下
                    elif cassets_zzqlist_num > 10:
                        cassets_zzqlist = []
                        zzqlist_page = math.ceil(cassets_zzqlist_num / 10)
                        for page in range(1, zzqlist_page + 1):
                            zzqlist_url = f'https://www.qcc.com/api/datalist/zzqlist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                            }
                            zzqlist_value = post_response(zzqlist_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(zzqlist_value)
                            zzqlist_value_data = zzqlist_value["data"]
                            for zzqlist_data in zzqlist_value_data:

                                cassets_zzqlist.append(zzqlist_data)
                            time.sleep(6)
                    else:
                        cassets_zzqlist = []
                    # 软件著作权
                    cassets_rjzzqlist_num = inquire_dict.get('软件著作权')
                    # 少于10个的情况下
                    if 0 < cassets_rjzzqlist_num <= 10:
                        cassets_rjzzqlist = cassets_json["datalist"]["rjzzqlist"]["data"]
                    # 多于10个的情况下
                    elif cassets_rjzzqlist_num > 10:
                        cassets_rjzzqlist = []
                        rjzzqlist_page = math.ceil(cassets_rjzzqlist_num / 10)
                        for page in range(1, rjzzqlist_page + 1):
                            rjzzqlist_url = f'https://www.qcc.com/api/datalist/rjzzqlist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                            }
                            rjzzqlist_value = post_response(rjzzqlist_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(rjzzqlist_value)
                            rjzzqlist_value_data = rjzzqlist_value["data"]
                            for rjzzqlist_data in rjzzqlist_value_data:
                                cassets_rjzzqlist.append(rjzzqlist_data)
                            time.sleep(6)
                    else:
                        cassets_rjzzqlist = []
                    # 备案网站
                    cassets_webitelist_num = inquire_dict.get('备案网站')
                    # 少于10个的情况下
                    if 0 < cassets_webitelist_num <= 10:
                        cassets_webitelist = cassets_json["datalist"]["websitelist"]["data"]
                    # 多于10个的情况下
                    elif cassets_webitelist_num > 10:
                        cassets_webitelist = []
                        webitelist_page = math.ceil(cassets_webitelist_num / 10)
                        for page in range(1, webitelist_page + 1):
                            webitelist_url = f'https://www.qcc.com/api/datalist/websitelist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                            }
                            webitelist_value = post_response(webitelist_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(webitelist_value)
                            webitelist_value_data = webitelist_value["data"]
                            for webitelist_data in webitelist_value_data:
                                cassets_webitelist.append(webitelist_data)
                            time.sleep(6)
                    else:
                        cassets_webitelist = []
                    # APP
                    cassets_applist_num = inquire_dict.get('APP')
                    # 少于10个的情况下
                    if 0 < cassets_applist_num <= 10:
                        cassets_applist = cassets_json["datalist"]["applist"]["data"]
                    # 多于10个的情况下
                    elif cassets_applist_num > 10:
                        cassets_applist = []
                        applist_page = math.ceil(cassets_applist_num / 10)
                        for page in range(1, applist_page + 1):
                            applist_url = f'https://www.qcc.com/api/datalist/applist?keyNo={key_no}&pageIndex={page}'
                            applist_value = get_response(applist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(applist_value)
                            applist_value_data = applist_value["data"]
                            for applist_data in applist_value_data:
                                cassets_applist.append(applist_data)
                            time.sleep(6)
                    else:
                        cassets_applist = []
                    # 微信公众号
                    cassets_wechatlist_num = inquire_dict.get('微信公众号')
                    # 少于10个的情况下
                    if 0 < cassets_wechatlist_num <= 10:
                        cassets_wechatlist = cassets_json["datalist"]["wechatlist"]["data"]
                    # 多于10个的情况下
                    elif cassets_wechatlist_num > 10:
                        cassets_wechatlist = []
                        wechatlist_page = math.ceil(cassets_wechatlist_num / 10)
                        for page in range(1, wechatlist_page + 1):
                            wechatlist_url = f'https://www.qcc.com/api/datalist/wechatlist?keyNo={key_no}&pageIndex={page}'
                            wechatlist_value = get_response(wechatlist_url, key_no, pid, tid, cookie_dict)
                            encounter_captcha(wechatlist_value)

                            cassets_wechatlist.append(wechatlist_value)
                            time.sleep(6)
                    else:
                        cassets_wechatlist = []
                    # 集成电路布图
                    cassets_jcdllist_num = inquire_dict.get('集成电路布图')
                    # 少于10个的情况下
                    if 0 < cassets_jcdllist_num <= 10:
                        cassets_jcdllist = cassets_json["datalist"]["jcdllist"]["data"]
                    # 多于10个的情况下
                    elif cassets_jcdllist_num > 10:
                        cassets_jcdllist = []
                        input('集成电路布图列表超过十个, 建议处理')
                        jcdllist_page = math.ceil(cassets_jcdllist_num / 10)
                        for page in range(1, jcdllist_page + 1):
                            pass
                    else:
                        cassets_jcdllist = []
                    # 标准信息
                    cassets_standarlist_num = inquire_dict.get('标准信息')
                    # 少于10个的情况下
                    if 0 < cassets_standarlist_num <= 10:
                        cassets_standarlist = cassets_json["datalist"]["standardlist"]["data"]
                    # 多于10个的情况下
                    elif cassets_standarlist_num > 10:
                        cassets_standarlist = []
                        input('标准信息列表超过十个, 建议处理')
                        standarlist_page = math.ceil(cassets_standarlist_num / 10)
                        for page in range(1, standarlist_page + 1):
                            standarlist_url = f'https://www.qcc.com/api/datalist/standardlist?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                            standarlist_value = get_response(standarlist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(standarlist_value)

                            cassets_standarlist.append(standarlist_value)
                            time.sleep(6)
                    else:
                        cassets_standarlist = []
                    # 微博
                    cassets_weibolist_num = inquire_dict.get('微博')
                    # 少于10个的情况下
                    if 0 < cassets_weibolist_num <= 10:
                        cassets_weibolist = cassets_json["datalist"]["weibolist"]["data"]
                    # 多于10个的情况下
                    elif cassets_weibolist_num > 10:
                        cassets_weibolist = []
                        weibolist_page = math.ceil(cassets_weibolist_num / 10)
                        for page in range(1, weibolist_page + 1):
                            weibolist_url = f'https://www.qcc.com/api/datalist/weibolist?keyNo={key_no}&pageIndex={page}'
                            weibolist_value = get_response(weibolist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(weibolist_value)

                            cassets_weibolist.append(weibolist_value)
                            time.sleep(6)
                    else:
                        cassets_weibolist = []
                    # 抖音/快手
                    cassets_shortvideolist_num = inquire_dict.get('抖音/快手')
                    # 少于10个的情况下
                    if 0 < cassets_shortvideolist_num <= 10:
                        cassets_shortvideolist = cassets_json["datalist"]["shortvideolist"]["data"]
                    # 多于10个的情况下
                    elif cassets_shortvideolist_num > 10:
                        cassets_shortvideolist = []
                        input('抖音/快手列表超过10条数据，建议处理')
                        shortvideolist_page = math.ceil(cassets_shortvideolist_num / 10)
                        for page in range(1, shortvideolist_page + 1):
                            shortvideolist_url = f'https://www.qcc.com/api/datalist/shortvideolist?keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        cassets_shortvideolist = []
                    # 小程序
                    cassets_miniprogramlist_num = inquire_dict.get('小程序')
                    # 少于10个的情况下
                    if 0 < cassets_miniprogramlist_num <= 10:
                        cassets_wplist = cassets_json["datalist"]["wplist"]["data"]
                    # 多于10个的情况下
                    elif cassets_miniprogramlist_num > 10:
                        cassets_wplist = []
                        wplist_page = math.ceil(cassets_miniprogramlist_num / 10)
                        for page in range(1, wplist_page + 1):
                            wplist_url = f'https://www.qcc.com/api/datalist/wplist?keyNo={key_no}&pageIndex={page}'
                            wplist_value = get_response(wplist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(wplist_value)

                            cassets_wplist.append(wplist_value)
                            time.sleep(6)
                    else:
                        cassets_wplist = []
                    # 线上店铺
                    cassets_shopslist_num = inquire_dict.get('线上店铺')
                    # 少于10个的情况下
                    if 0 < cassets_shopslist_num <= 10:
                        cassets_shopslist = cassets_json["datalist"]["shopslist"]["data"]
                    # 多于10个的情况下
                    elif cassets_shopslist_num > 10:
                        cassets_shopslist = []
                        input('线上店铺列表超过10条数据，建议处理')
                        shopslist_page = math.ceil(cassets_shopslist_num / 10)
                        for page in range(1, shopslist_page + 1):
                            shopslist_url = f'https://www.qcc.com/api/datalist/shopslist?keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        cassets_shopslist = []
                    # 商业特许经营
                    cassets_sytxjylist_num = inquire_dict.get('商业特许经营')
                    # 少于10个的情况下
                    if 0 < cassets_sytxjylist_num <= 10:
                        cassets_sytxjylist = cassets_json["datalist"]["sytxjylist"]["data"]
                    # 多于10个的情况下
                    elif cassets_sytxjylist_num > 10:
                        cassets_sytxjylist = []
                        input('商业特许经营列表超过10条数据，建议处理')
                        sytxjylist_page = math.ceil(cassets_sytxjylist_num / 10)
                        for page in range(1, sytxjylist_page + 1):
                            sytxjylist_url = f'https://www.qcc.com/api/datalist/sytxjylist?keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        cassets_sytxjylist = []
                    # 知产出质
                    cassets_patentpledgelist_num = inquire_dict.get('知产出质')
                    # 少于10个的情况下
                    if 0 < cassets_patentpledgelist_num <= 10:
                        cassets_patentpledgelist = cassets_json["datalist"]["patentpledgelist"]["data"]
                    # 多于10个的情况下
                    elif cassets_patentpledgelist_num > 10:
                        cassets_patentpledgelist = []
                        input('知产出质列表超过10条数据，建议处理')
                        patentpledgelist_page = math.ceil(cassets_patentpledgelist_num / 10)
                        for page in range(1, patentpledgelist_page + 1):
                            patentpledgelist_url = f'https://www.qcc.com/api/datalist/patentpledgelist?keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        cassets_patentpledgelist = []

                    """
                    历史信息!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    """

                    # 历史法人代表
                    chistory_faren_num = inquire_dict.get('历史法定代表人')
                    # 少于10个的情况下
                    if 0 < chistory_faren_num <= 10:
                        chistory_operlist = chistory_json["datalist"]["hisinfo"]["data"]["OperList"]
                    # 多于10个的情况下
                    elif chistory_faren_num > 10:
                        chistory_operlist = []
                        input('历史法定代表人列表超过10条数据，建议处理')
                        operlist_page = math.ceil(chistory_faren_num / 10)
                        for page in range(1, operlist_page + 1):
                            operlist_url = f'https://www.qcc.com/api/datalist/operlist?keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        chistory_operlist = []
                    # 历史主要人员
                    chistory_mainmember_num = inquire_dict.get('历史主要人员')
                    # 少于10个的情况下
                    if 0 < chistory_mainmember_num <= 10:
                        chistory_hismainmember = chistory_json["datalist"]["hismainmember"]["data"]
                    # 多于10个的情况下
                    elif chistory_mainmember_num > 10:
                        chistory_hismainmember = []
                        input('历史主要人员列表超过10条数据，建议处理')
                        hismainmember_page = math.ceil(chistory_mainmember_num / 10)
                        for page in range(1, hismainmember_page + 1):
                            hismainmember_url = f'https://www.qcc.com/api/datalist/hismainmember?isNewAgg=true&keyNo={key_no}&pageIndex={page}'
                            hismainmember_value = get_response(hismainmember_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hismainmember_value)
                            chistory_hismainmember.append(hismainmember_value)
                            time.sleep(7)
                    else:
                        chistory_hismainmember = []
                    # 历史被执行人
                    chistory_hiszhixinglist_num = inquire_dict.get('历史被执行人')
                    # 少于10个的情况下
                    if 0 < chistory_hiszhixinglist_num <= 10:
                        chistory_hiszhixinglist = chistory_json["datalist"]["hiszhixinglist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hiszhixinglist_num > 10:
                        chistory_hiszhixinglist = []
                        hiszhixinglist_page = math.ceil(chistory_hiszhixinglist_num / 10)
                        for page in range(1, hiszhixinglist_page + 1):
                            hiszhixinglist_url = f'https://www.qcc.com/api/datalist/zhixinglist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}&searchKey={key_no}'
                            hiszhixinglist_value = get_response(hiszhixinglist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hiszhixinglist_value)
                            chistory_hiszhixinglist.append(hiszhixinglist_value)
                            time.sleep(7)
                    else:
                        chistory_hiszhixinglist = []
                    # 历史立案信息
                    chistory_hisliainfo_num = inquire_dict.get('历史立案信息')
                    # 少于10个的情况下
                    if 0 < chistory_hisliainfo_num <= 10:
                        chistory_hislianlist = chistory_json["datalist"]["hislianlist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisliainfo_num > 10:
                        chistory_hislianlist = []
                        hislianlist_page = math.ceil(chistory_hisliainfo_num / 10)
                        for page in range(1, hislianlist_page + 1):
                            hislianlist_url = f'https://www.qcc.com/api/datalist/lianlist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}'
                            hislianlist_value = get_response(hislianlist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hislianlist_value)
                            chistory_hislianlist.append(hislianlist_value)
                            time.sleep(7)
                    else:
                        chistory_hislianlist = []
                    # 历史裁判文书
                    chistory_hiswenshulist_num = inquire_dict.get('历史裁判文书')
                    # 少于10个的情况下
                    if 0 < chistory_hiswenshulist_num <= 10:
                        chistory_hiswenshulist = chistory_json["datalist"]["hiswenshulist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hiswenshulist_num > 10:
                        chistory_hiswenshulist = []
                        hiswenshulist_page = math.ceil(chistory_hiswenshulist_num / 10)
                        for page in range(1, hiswenshulist_page + 1):
                            hiswenshulist_url = f'https://www.qcc.com/api/datalist/wenshulist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}&searchKey={key_no}'
                            hiswenshulist_value = get_response(hiswenshulist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hiswenshulist_value)
                            chistory_hiswenshulist.append(hiswenshulist_value)
                            time.sleep(7)
                    else:
                        chistory_hiswenshulist = []
                    # 历史开庭公告
                    chistory_hisktgglist_num = inquire_dict.get('历史开庭公告')
                    # 少于10个的情况下
                    if 0 < chistory_hisktgglist_num <= 10:
                        chistory_hisnoticelist = chistory_json["datalist"]["hisnoticelist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisktgglist_num > 10:
                        chistory_hisnoticelist = []
                        hisnoticelist_page = math.ceil(chistory_hisktgglist_num / 10)
                        for page in range(1, hisnoticelist_page + 1):
                            hisnoticelist_url = f'https://www.qcc.com/api/datalist/noticelist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}'
                            hisnoticelist_value = get_response(hisnoticelist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hisnoticelist_value)
                            chistory_hisnoticelist.append(hisnoticelist_value)
                            time.sleep(7)
                    else:
                        chistory_hisnoticelist = []
                    # 历史行政许可
                    chistory_hisacolist_num = inquire_dict.get('历史行政许可')
                    # 少于10个的情况下
                    if 0 < chistory_hisacolist_num <= 10:
                        chistory_hisacolist = chistory_json["datalist"]["hisacolist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisacolist_num > 10:
                        chistory_hisacolist = []
                        hisacolist_page = math.ceil(chistory_hisacolist_num / 10)
                        for page in range(1, hisacolist_page + 1):
                            hisacolist_url = f'https://www.qcc.com/api/datalist/acolist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}'
                            hisacolist_value = get_response(hisacolist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hisacolist_value)
                            chistory_hisacolist.append(hisacolist_value)
                            time.sleep(7)
                    else:
                        chistory_hisacolist = []
                    # 历史行政处罚
                    chistory_hisadminpenaltylist_num = inquire_dict.get('历史行政处罚')
                    # 少于10个的情况下
                    if 0 < chistory_hisadminpenaltylist_num <= 10:
                        chistory_hisadminpenaltylist = chistory_json["datalist"]["hisadminpenaltylist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisadminpenaltylist_num > 10:
                        chistory_hisadminpenaltylist = []
                        hisadminpenaltylist_page = math.ceil(chistory_hisadminpenaltylist_num / 10)
                        for page in range(1, hisadminpenaltylist_page + 1):
                            hisadminpenaltylist_url = f'https://www.qcc.com/api/datalist/adminpenaltylist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}'
                            hisadminpenaltylist_value = get_response(hisadminpenaltylist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hisadminpenaltylist_value)
                            chistory_hisadminpenaltylist.append(hisadminpenaltylist_value)
                            time.sleep(7)
                    else:
                        chistory_hisadminpenaltylist = []
                    # 历史股权出质
                    chistory_hispledgelist_num = inquire_dict.get('历史股权出质')
                    # 少于10个的情况下
                    if 0 < chistory_hispledgelist_num <= 10:
                        chistory_hispledgelist = chistory_json["datalist"]["hispledgelist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hispledgelist_num > 10:
                        chistory_hispledgelist = []
                        input('股权出质列表超过十个，建议处理')
                        hispledgelist_page = math.ceil(chistory_hispledgelist_num / 10)
                        for page in range(1, hispledgelist_page + 1):
                            hispledgelist_url = f'https://www.qcc.com/api/datalist/pledgelist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        chistory_hispledgelist = []
                    # 历史商标信息
                    chistory_hisshangbiaolist_num = inquire_dict.get('历史商标信息')
                    # 少于10个的情况下
                    if 0 < chistory_hisshangbiaolist_num <= 10:
                        chistory_hisshangbiaolist = chistory_json["datalist"]["hisshangbiaolist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisshangbiaolist_num > 10:
                        chistory_hisshangbiaolist = []
                        hisshangbiaolist_page = math.ceil(chistory_hisshangbiaolist_num / 10)
                        for page in range(1, hisshangbiaolist_page + 1):
                            hisshangbiaolist_url = f'https://www.qcc.com/api/datalist/shangbiaolist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                                'isValid': '0',
                            }
                            hisshangbiaolist_value = post_response(hisshangbiaolist_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(hisshangbiaolist_value)
                            chistory_hisshangbiaolist.append(hisshangbiaolist_value)
                            time.sleep(7)
                    else:
                        chistory_hisshangbiaolist = []
                    # 历史专利信息
                    chistory_hiszhuanlilist_num = inquire_dict.get('历史专利信息')
                    # 少于10个的情况下
                    if 0 < chistory_hiszhuanlilist_num <= 10:
                        chistory_hiszhuanlilist = chistory_json["datalist"]["hiszhuanlilist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hiszhuanlilist_num > 10:
                        chistory_hiszhuanlilist = []
                        input('专利信息列表超过十个，建议处理')
                        hiszhuanlilist_page = math.ceil(chistory_hiszhuanlilist_num / 10)
                        for page in range(1, hiszhuanlilist_page + 1):
                            hiszhuanlilist_url = f'https://www.qcc.com/api/datalist/zhuanlilist'
                            json_data = {
                                'keyNo': f'{key_no}',
                                'pageIndex': page,
                                'isNewAgg': True,
                                'isValid': '0',
                            }
                            hiszhuanlilist_value = post_response(hiszhuanlilist_url, key_no, pid, tid, cookie_dict, json_data)
                            encounter_captcha(hiszhuanlilist_value)
                            chistory_hiszhuanlilist.append(hiszhuanlilist_value)
                            time.sleep(7)
                    else:
                        chistory_hiszhuanlilist = []
                    # 历史备案网站
                    chistory_hiswebsitelist_num = inquire_dict.get('历史备案网站')
                    # 少于10个的情况下
                    if 0 < chistory_hiswebsitelist_num <= 10:
                        chistory_hiswebsitelist = chistory_json["datalist"]["hiswebsitelist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hiswebsitelist_num > 10:
                        chistory_hiswebsitelist = []
                        input('历史备案网站列表超过十个，建议处理')
                        hiswebsitelist_page = math.ceil(chistory_hiswebsitelist_num / 10)
                        for page in range(1, hiswebsitelist_page + 1):
                            hiswebsitelist_url = f'https://www.qcc.com/api/datalist/websitelist'
                            pass
                    else:
                        chistory_hiswebsitelist = []
                    # 历史股东信息
                    chistory_hispartnerlist_num = inquire_dict.get('历史股东信息')
                    # 少于10个的情况下
                    if 0 < chistory_hispartnerlist_num <= 10:
                        chistory_hispartner = chistory_json["datalist"]["hispartner"]["data"]
                    # 多于10个的情况下
                    elif chistory_hispartnerlist_num > 10:
                        chistory_hispartner = []
                        input('历史股东信息列表超过十个，建议处理')
                        hispartnerlist_page = math.ceil(chistory_hispartnerlist_num / 10)
                        for page in range(1, hispartnerlist_page + 1):
                            hispartnerlist_url = f'https://www.qcc.com/api/datalist/partnerlist'
                            pass
                    else:
                        chistory_hispartner = []
                    # 历史欠税公告
                    chistory_hisqianshitax_num = inquire_dict.get('历史欠税公告')
                    # 少于10个的情况下
                    if 0 < chistory_hisqianshitax_num <= 10:
                        chistory_hisowenoticelist = chistory_json["datalist"]["hisowenoticelist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisqianshitax_num > 10:
                        chistory_hisowenoticelist = []
                        input('历史欠税公告列表超过十个，建议处理')
                        hisowenoticelist_page = math.ceil(chistory_hisqianshitax_num / 10)
                        for page in range(1, hisowenoticelist_page + 1):
                            hisowenoticelist_url = f'https://www.qcc.com/api/datalist/owenoticelist'
                            pass
                    else:
                        chistory_hisowenoticelist = []
                    # 历史法院公告
                    chistory_hiscourtlist_num = inquire_dict.get('历史法院公告')
                    # 少于10个的情况下
                    if 0 < chistory_hiscourtlist_num <= 10:
                        chistory_hisgonggaolist = chistory_json["datalist"]["hisgonggaolist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hiscourtlist_num > 10:
                        chistory_hisgonggaolist = []
                        input('历史法院公告列表超过十个，建议处理')
                        hisgonggaolist_page = math.ceil(chistory_hiscourtlist_num / 10)
                        for page in range(1, hisgonggaolist_page + 1):
                            hisgonggaolist_url = f'https://www.qcc.com/api/datalist/gonggaolist'
                            pass
                    else:
                        chistory_hisgonggaolist = []
                    # 历史环保处罚
                    chistory_hisenvlist_num = inquire_dict.get('历史环保处罚')
                    # 少于10个的情况下
                    if 0 < chistory_hisenvlist_num <= 10:
                        chistory_hisenvlist = chistory_json["datalist"]["hisenvlist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisenvlist_num > 10:
                        chistory_hisenvlist = []
                        input('历史环保处罚列表超过十个，建议处理')
                        hisenvlist_page = math.ceil(chistory_hisenvlist_num / 10)
                        for page in range(1, hisenvlist_page + 1):
                            hisenvlist_url = f'https://www.qcc.com/api/datalist/envlist'
                            pass
                    else:
                        chistory_hisenvlist = []
                    # 历史终本案件
                    chistory_hisendexecutioncaselist_num = inquire_dict.get('历史终本案件')
                    # 少于10个的情况下
                    if 0 < chistory_hisendexecutioncaselist_num <= 10:
                        chistory_hisendexecutioncaselist = chistory_json["datalist"]["hisendexecutioncaselist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisendexecutioncaselist_num > 10:
                        chistory_hisendexecutioncaselist = []
                        hisendexecutioncaselist_page = math.ceil(chistory_hisendexecutioncaselist_num / 10)
                        for page in range(1, hisendexecutioncaselist_page + 1):
                            hisendexecutioncaselist_url = f'https://www.qcc.com/api/datalist/endexecutioncaselist?isValid=0&keyNo={key_no}&pageIndex={page}'
                            hisendexecutioncaselist_value = get_response(hisendexecutioncaselist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hisendexecutioncaselist_value)
                            chistory_hisendexecutioncaselist.append(hisendexecutioncaselist_value)
                            time.sleep(8)
                    else:
                        chistory_hisendexecutioncaselist = []
                    # 历史限制高消费
                    chistory_hisconsumptionlist_num = inquire_dict.get('历史限制高消费')
                    # 少于10个的情况下
                    if 0 < chistory_hisconsumptionlist_num <= 10:
                        chistory_hissumptuarylist = chistory_json["datalist"]["hissumptuarylist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisconsumptionlist_num > 10:
                        chistory_hissumptuarylist = []
                        input('历史限制高消费列表超过十个，建议处理')
                        hisconsumptionlist_page = math.ceil(chistory_hisconsumptionlist_num / 10)
                        for page in range(1, hisconsumptionlist_page + 1):
                            hisconsumptionlist_url = f'https://www.qcc.com/api/datalist/sumptuarylist?id={key_no}&isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}'
                            hisconsumptionlist_value = get_response(hisconsumptionlist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hisconsumptionlist_value)
                            chistory_hissumptuarylist.append(hisconsumptionlist_value)
                            time.sleep(8)
                    else:
                        chistory_hissumptuarylist = []
                    # 历史失信被执行人
                    chistory_hisshixinlist_num = inquire_dict.get('历史失信被执行人')
                    # 少于10个的情况下
                    if 0 < chistory_hisshixinlist_num <= 10:
                        chistory_hisshixinlist = chistory_json["datalist"]["hisshixinlist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisshixinlist_num > 10:
                        chistory_hisshixinlist = []
                        hisshixinlist_page = math.ceil(chistory_hisshixinlist_num / 10)
                        for page in range(1, hisshixinlist_page + 1):
                            hisshixinlist_url = f'https://www.qcc.com/api/datalist/shixinlist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}&searchKey={key_no}&sortField=pubdate'
                            hisshixinlist_value = get_response(hisshixinlist_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hisshixinlist_value)
                            chistory_hisshixinlist.extend(hisshixinlist_value)
                            time.sleep(8)
                    else:
                        chistory_hisshixinlist = []
                    # 历史经营异常
                    chistory_hisexceptions_num = inquire_dict.get('历史经营异常')
                    # 少于10个的情况下
                    if 0 < chistory_hisexceptions_num <= 10:
                        chistory_hisexceptions = chistory_json["datalist"]["hisexceptions"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisexceptions_num > 10:
                        chistory_hisexceptions = []
                        input('历史经营异常列表超过十个，建议处理')
                        hisexceptions_page = math.ceil(chistory_hisexceptions_num / 10)
                        for page in range(1, hisexceptions_page + 1):
                            hisexceptions_url = f'https://www.qcc.com/api/datalist/exceptions?isValid=0&keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        chistory_hisexceptions = []
                    # 历史股权冻结
                    chistory_hisfreeze_num = inquire_dict.get('历史股权冻结')
                    # 少于10个的情况下
                    if 0 < chistory_hisfreeze_num <= 10:
                        chistory_hisassistancelist = chistory_json["datalist"]["hisassistancelist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisfreeze_num > 10:
                        chistory_hisassistancelist = []
                        hisfreeze_page = math.ceil(chistory_hisfreeze_num / 10)
                        for page in range(1, hisfreeze_page + 1):
                            hisfreeze_url = f'https://www.qcc.com/api/datalist/assistancelist?isNewAgg=true&isValid=0&keyNo={key_no}&pageIndex={page}'
                            hisfreeze_value = get_response(hisfreeze_url, key_no, pid, tid, cookie_dict).json()
                            encounter_captcha(hisfreeze_value)
                            chistory_hisassistancelist.append(hisfreeze_value)
                            time.sleep(8)
                    else:
                        chistory_hisassistancelist = []
                    # 历史双随机抽查
                    chistory_hisdrclist_num = inquire_dict.get('历史双随机抽查')
                    # 少于10个的情况下
                    if 0 < chistory_hisdrclist_num <= 10:
                        chistory_hisdrclist = chistory_json["datalist"]["hisdrclist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hisdrclist_num > 10:
                        chistory_hisdrclist = []
                        input('历史双随机抽查列表超过十个，建议处理')
                        hisdrclist_page = math.ceil(chistory_hisdrclist_num / 10)
                        for page in range(1, hisdrclist_page + 1):
                            hisdrclist_url = f'https://www.qcc.com/api/datalist/drclist?isValid=0&keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        chistory_hisdrclist = []
                    # 历史知产出质
                    chistory_hispledgelist_num = inquire_dict.get('历史知产出质')
                    # 少于10个的情况下
                    if 0 < chistory_hispledgelist_num <= 10:
                        chistory_hispatentpledgelist = chistory_json["datalist"]["hispatentpledgelist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hispledgelist_num > 10:
                        chistory_hispatentpledgelist = []
                        input('历史知产出质列表超过十个，建议处理')
                        hispledgelist_page = math.ceil(chistory_hispledgelist_num / 10)
                        for page in range(1, hispledgelist_page + 1):
                            hispledgelist_url = f'https://www.qcc.com/api/datalist/patentpledgelist?isValid=0&keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        chistory_hispatentpledgelist = []
                    # 历史动产抵押
                    chistory_hismpledgelist_num = inquire_dict.get('历史动产抵押')
                    # 少于10个的情况下
                    if 0 < chistory_hismpledgelist_num <= 10:
                        chistory_hismpledgelist = chistory_json["datalist"]["hismpledgelist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hismpledgelist_num > 10:
                        chistory_hismpledgelist = []
                        input('历史动产抵押列表超过十个，建议处理')
                        hismpledgelist_page = math.ceil(chistory_hismpledgelist_num / 10)
                        for page in range(1, hismpledgelist_page + 1):
                            hismpledgelist_url = f'https://www.qcc.com/api/datalist/mpledgelist?isValid=0&keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        chistory_hismpledgelist = []
                    # 历史诉前调解
                    chistory_hispretrialmediationlist_num = inquire_dict.get('历史诉前调解')
                    # 少于10个的情况下
                    if 0 < chistory_hispretrialmediationlist_num <= 10:
                        chistory_hispretrialmediationlist = chistory_json["datalist"]["hispretrialmediationlist"]["data"]
                    # 多于10个的情况下
                    elif chistory_hispretrialmediationlist_num > 10:
                        chistory_hispretrialmediationlist = []
                        input('历史诉前调解列表超过十个，建议处理')
                        hispretrialmediationlist_page = math.ceil(chistory_hispretrialmediationlist_num / 10)
                        for page in range(1, hispretrialmediationlist_page + 1):
                            hispretrialmediationlist_url = f'https://www.qcc.com/api/datalist/pretrialmediationlist?isValid=0&keyNo={key_no}&pageIndex={page}'
                            pass
                    else:
                        chistory_hispretrialmediationlist = []


                    value_dict = {
                        '工商信息': company_detail,
                        '股东信息': company_partners,
                        '主要人员': company_employees,
                        '对外投资': company_touzilist,
                        '变更记录': company_changelist,
                        '企业年报': company_reportyear,
                        '疑似关系': company_suspectlist,
                        '司法案件': susong_caselist,
                        '裁判文书': susong_wenshulist,
                        '立案信息': susong_lianliast,
                        '开庭公告': susong_noticelist,
                        '法院公告': susong_gonggaolist,
                        '送达公告': susong_dnoticelist,
                        '诉前调解': susong_pretrialmediationlist,
                        '司法拍卖': susong_judicialsalelist,
                        '失信被执行人': susong_shixinlist,
                        '终本案件': susong_endexecutioncaselist,
                        '严重违法': cfengxian_svlist,
                        '股权出质': cfengxian_pledgelist,
                        '经营异常': cfengxian_exceptions,
                        '动产抵押': cfengxian_mpledgelist,
                        '注销备案': cfengxian_enliqinfo,
                        '行政处罚': cfengxian_adminpenaltylist,
                        '环保处罚': cfengxian_envlist,
                        '税务非正常户': cfengxian_taxabnormallist,
                        '欠税公告': cfengxian_owenoticelist,
                        '税收违法': cfengxian_taxillegallist,
                        '招投标': cfengxian_taxillegallist,
                        '资质证书': crun_certificationsummary,
                        '信用评价': crun_creditrate,
                        '招聘': crun_joblist,
                        '进出口信用': crun_ciaxlist,
                        '土地信息': crun_landlist,
                        '行政许可': crun_acolist,
                        '抽查检查': crun_spotchecklist,
                        '食品安全': crun_foodsafetylist,
                        '双随机抽查': crun_drclist,
                        '纳税人资质': crun_taxpayerlist,
                        '产权交易': crun_transactionlist,
                        '资产拍卖': crun_assetsalelist,
                        '电信许可': crun_telecomlist,
                        '商标信息': cassets_shangbiaolist,
                        '商标文书': cassets_tmcdslist,
                        '专利信息': cassets_zhuanlilist,
                        '作品著作权': cassets_zzqlist,
                        '软件著作权': cassets_rjzzqlist,
                        '备案网站': cassets_webitelist,
                        'APP': cassets_applist,
                        '微信公众号': cassets_wechatlist,
                        '集成电路布图': cassets_jcdllist,
                        '标准信息': cassets_standarlist,
                        '微博': cassets_weibolist,
                        '抖音/快手': cassets_shortvideolist,
                        '小程序': cassets_wplist,
                        '线上店铺': cassets_shopslist,
                        '商业特许经营': cassets_sytxjylist,
                        '知产出质': cassets_patentpledgelist,
                        '历史法定代表人': chistory_operlist,
                        '历史主要人员': chistory_hismainmember,
                        '历史被执行人': chistory_hiszhixinglist,
                        '历史立案信息': chistory_hislianlist,
                        '历史裁判文书': chistory_hiswenshulist,
                        '历史开庭公告': chistory_hisnoticelist,
                        '历史行政许可': chistory_hisacolist,
                        '历史行政处罚': chistory_hisadminpenaltylist,
                        '历史股权出质': chistory_hispledgelist,
                        '历史商标信息': chistory_hisshangbiaolist,
                    }
                    print(value_dict)
                    # 转为json数据
                    value_json = json.dumps(value_dict, ensure_ascii=False, indent=4)
                    # 将数据保存为json文件
                    with open(f"江苏徽海能源发展有限公司.json", "w", encoding="utf-8") as f:
                        f.write(value_json)



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
                # 没有匹配到公司，获取到的公司列表
                # print("没有匹配到精确公司，获取到的多个公司列表")
                # print(company_simple_json)

    else:
        print("网站限制")
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
        print("获取数据失败")
        return "失败", None


# qcc_search_company("杭州泽荣财务咨询有限公司")
# qcc_search_company("福建金闽再造烟叶发展有限公司")
# qcc_search_company("广东瑞生科技集团有限公司")
# qcc_search_company("泸州丹山建筑建材有限责任公司")
# qcc_search_company("江苏太平洋印刷有限公司")
# qcc_search_company("江阴市国马呢绒染整有限公司")
# qcc_search_company("中国华润有限公司")
# qcc_search_company("常州市兰新建筑工程有限公司")
qcc_search_company("江苏徽海能源发展有限公司")
