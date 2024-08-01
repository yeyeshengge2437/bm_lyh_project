
import log
import requests
import json

testUrl = ""
liveUrl = ""


apiUrl = liveUrl

headers = {
    'Content-Type': 'application/json;'
}

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False



def corp_queue_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/queue/next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_queue_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/queue/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_queue_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/queue/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_queue_success(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/queue/success"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_queue_fail(data=None):
    try:
        if data is None:
            data = {}
        url = apiUrl + "/corp/queue/fail"
        data_str = json.dumps(data)
        log.base.info("url:" + url + " data:" + data_str)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        log.base.info(result)
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def corp_court_queue_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/court-queue/next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_court_queue_success(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/court-queue/success"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_court_queue_fail(data=None):
    try:
        if data is None:
            data = {}
        url = apiUrl + "/corp/court-queue/fail"
        data_str = json.dumps(data)
        log.base.info("url:" + url + " data:" + data_str)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        log.base.info(result)
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def corp_court_notice_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/court-notice/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_info_get(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/info/get"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_info_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/info/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_info_quick_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/info/quick-add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_info_change_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/info-change/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_annual_report_get(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/annual-report/get"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_annual_report_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/annual-report/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_sh_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/sh/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_sh_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/sh/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_sh_his_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/sh-his/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_sh_his_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/sh-his/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_main_member_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/main-member/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_main_member_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/main-member/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_benefit_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/benefit/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_boss_info_get(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/boss-info/get"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_boss_info_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/boss-info/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_admin_permit_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/admin-permit/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_admin_punish_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/admin-punish/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_tax_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/tax/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_movables_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/movables/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_pollute_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/pollute/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_medical_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/medical/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_medical_get(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/medical/get"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_case_count(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case/count"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_case_com_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-com/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_case_com_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-com/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_case_doc_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-doc/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 裁判文书对比
def corp_case_doc_text_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-doc-text/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 裁判文书添加
def corp_case_doc_text_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-doc-text/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_case_legal_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-legal/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_case_broke_count(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-broke/count"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_case_broke_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-broke/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_case_broke_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-broke/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_action_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/action/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_action_dishonest_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/action-dishonest/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_action_dishonest_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/action-dishonest/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_action_end_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/action-end/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def corp_sumptuary_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/sumptuary/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 立案信息对比
def corp_case_register_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-register/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 立案信息添加
def corp_case_register_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-register/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 开庭公告对比
def corp_case_open_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-open/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 开庭公告添加
def corp_case_open_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-open/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 庭审信息对比
def corp_case_live_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-live/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 庭审信息添加
def corp_case_live_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-live/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 庭审信息失效
def corp_case_live_invalid(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-live/invalid"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 庭审信息更新失败
def corp_case_live_update_fail(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-live/update-fail"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 庭审信息需要更新
def corp_case_live_need_update_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-live/need-update-next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 法院公告对比
def corp_case_court_notice_compare(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-court-notice/compare"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 法院公告添加
def corp_case_court_notice_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/case-court-notice/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 土地供应添加
def corp_land_supply_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/land-supply/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 土地供应更新
def corp_land_supply_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/land-supply/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 土地供应获取
def corp_land_supply_get(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/land-supply/get"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


# 土地供应获取
def corp_land_supply_need_update_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/corp/land-supply/need-update-next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def file_upload(files, data=None, upload_type='paper'):
    if data is None:
        data = {}
    # url = apiUrl + "/file/upload/file?type=" + upload_type
    url = liveUrl + "/file/upload/file?type=" + upload_type

    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = s.post(url=url, headers=headers1, files=files)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def hl_file_upload(files, data=None, upload_type='paper'):
    if data is None:
        data = {}
    # url = apiUrl + "/file/upload/file?type=" + upload_type
    url = liveUrl + "/inner-api/file/upload/file?type=" + upload_type

    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = s.post(url=url, headers=headers1, files=files)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_notice_analyze_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/paper-notice/analyze-next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_notice_analyze_success(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/paper-notice/analyze-success"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_next_by_status_extend(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/page/next-by-status-extend"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_tell_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/tell/next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_tell_success(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/tell/success"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_analysis_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/analysis/next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_analysis_success(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/analysis/success"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_page_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/page/next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_page_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/page/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_page_img_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/page-img/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_page_img_update(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/page-img/update"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_page_img_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/page-img/next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_page_img_update_content(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/page-img/update-content"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def test_paper_notice_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/test/paper-notice/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_queue_next(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/queue/next"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_queue_success(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/paper/queue/success"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")


def paper_queue_fail(data=None):
    try:
        if data is None:
            data = {}
        url = apiUrl + "/paper/queue/fail"
        data_str = json.dumps(data)
        log.base.info("url:" + url + " data:" + data_str)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        log.base.info(result)
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def paper_page_get(data=None):
    try:
        if data is None:
            data = {}
        url = apiUrl + "/paper/page/get"
        data_str = json.dumps(data)
        log.base.info("url:" + url + " data:" + data_str)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        log.base.info(result)
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def paper_page_add(data=None):
    try:
        if data is None:
            data = {}
        url = apiUrl + "/paper/page/add"
        data_str = json.dumps(data)
        log.base.info("url:" + url + " data:" + data_str)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        log.base.info(result)
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def paper_paper_get(data=None):
    try:
        if data is None:
            data = {}
        url = apiUrl + "/paper/paper/get"
        data_str = json.dumps(data)
        log.base.info("url:" + url + " data:" + data_str)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        log.base.info(result)
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def paper_paper_add(data=None):
    try:
        if data is None:
            data = {}
        url = apiUrl + "/paper/paper/add"
        data_str = json.dumps(data)
        log.base.info("url:" + url + " data:" + data_str)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        log.base.info(result)
        return result.get("value")
    except Exception as err:
        print(err)
        return None


# 司法拍卖信息添加
def judicial_auction_add(data=None):
    if data is None:
        data = {}
    url = apiUrl + "/auction/judicial-auction/add"
    data_str = json.dumps(data)
    log.base.info("url:" + url + " data:" + data_str)
    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    log.base.info(result)
    return result.get("value")
