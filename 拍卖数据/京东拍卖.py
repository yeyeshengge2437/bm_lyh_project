import datetime

import requests
import json

cookies = {
    '__jdu': '17219744346561554622123',
    'mba_muid': '17219744346561554622123',
    'shshshfpa': '90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570',
    'shshshfpx': '90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570',
    'shshshfpb': 'BApXS0y5T4vdAOjIe0u_EfeI01o8m0OKABnJ0cl9o9xJ1Mv8SPoG2',
    '__jdv': '96383255|www.google.com|-|referral|-|1733361547620',
    '3AB9D23F7A4B3CSS': 'jdd03V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPIAAAAMTSRTDRPQAAAAADP2HHBHMZLCSP4X',
    '_gia_d': '1',
    '__jda': '128418189.17219744346561554622123.1721974435.1730357564.1733361548.7',
    '__jdc': '128418189',
    '__jdb': '128418189.3.17219744346561554622123|7.1733361548',
    '3AB9D23F7A4B3C9B': 'V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPI',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': '__jdu=17219744346561554622123; mba_muid=17219744346561554622123; shshshfpa=90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570; shshshfpx=90cc9c0e-20a8-2ac9-50fd-bff89d16535a-1730357570; shshshfpb=BApXS0y5T4vdAOjIe0u_EfeI01o8m0OKABnJ0cl9o9xJ1Mv8SPoG2; __jdv=96383255|www.google.com|-|referral|-|1733361547620; 3AB9D23F7A4B3CSS=jdd03V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPIAAAAMTSRTDRPQAAAAADP2HHBHMZLCSP4X; _gia_d=1; __jda=128418189.17219744346561554622123.1721974435.1730357564.1733361548.7; __jdc=128418189; __jdb=128418189.3.17219744346561554622123|7.1733361548; 3AB9D23F7A4B3C9B=V3DLUVLJW2IICXAD4LLG6KN7CQ4TZNK2CDPASEMPLOCOQYGFABFDL6ZPIPBUIKE6TGAR75QPRHHJPNT7EXCERYTGPI',
    'pragma': 'no-cache',
    'referer': 'https://pmsearch.jd.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

params = {
    "appid": "paimai",
    "functionId": "paimai_searchMerchantsProduct",
    "body": {
        "investmentType": "",
        "apiType": 12,  # api类型
        "page": 1,  # 页码
        "pageSize": 200,  # 每页数量
        "keyword": "",
        "provinceId": "",
        "cityId": "",
        "countyId": "",
        "multiPaimaiStatus": "",
        "multiDisplayStatus": "",
        "multiPaimaiTimes": "",
        "childrenCateId": "",
        "currentPriceRangeStart": "",
        "currentPriceRangeEnd": "",
        "timeRangeTime": "endTime",
        "timeRangeStart": "",
        "timeRangeEnd": "",
        "loan": "",
        "purchaseRestriction": "",  # 购买限制
        "orgId": "",
        "orgType": "",
        "sortField": 9,  # 排序字段
        "projectType": 2,  # 项目类型
        "reqSource": 0,  # 请求来源
        "labelSet": "1033",  # 标签集
        "publishSource": "",  # 发布源
        "defaultLabelSet": ""  # 默认标签集
    }
}

# 将 body 转换为 JSON 字符串
params["body"] = json.dumps(params["body"])

# 打印最终的 params
print(params)
response = requests.get(
    "https://api.m.jd.com/api",
    params=params,
    # cookies=cookies,
    headers=headers,
)
res_datas = json.loads(response.text)
res_datas = res_datas["datas"]

for res_data in res_datas:
    address = res_data.get("address")  # 住址
    if address:
        pass
        # print(address)
    # print(res_data)
    pub_date = res_data.get("announcementPubDate")  # 发布时间
    if pub_date:
        # 将毫秒转换为秒
        timestamp_s = pub_date / 1000.0
        # 转换为datetime对象
        dt_object = datetime.datetime.fromtimestamp(timestamp_s)
        standard_time = dt_object
    else:
        standard_time = ""
    asset_type = res_data.get("assetType")  # 资产类型
    if asset_type:
        pass
    asset_disposal = res_data.get("assetsDisposal")  # 资产处置方
    if asset_disposal:
        pass
    assetssell_attachment_list = res_data.get("assetssellAttachmentList")  # 附件
    assetssell_guarantees_list = res_data.get("assetssellGuaranteesList")  # 保障措施
    auction_type = res_data.get("auctionType")  # 拍卖类型
    base_date = res_data.get("baseDate")  # 基准日期
    category_id = res_data.get("categoryId")  # 分类id
    category_name = res_data.get("categoryName")  # 分类名称
    consult_tel = res_data.get("consultTel")  # 咨询电话
    credit_capital = res_data.get("creditCapital")  # 资本金
    credit_capital_and_terest = res_data.get("creditCapitalAndTerest")  # 资本金及利息
    credit_terest = res_data.get("creditTerest")  # 利息
    credit_total_charges = res_data.get("creditTotalCharges")  # 费用总额
    guaranty_style_type = res_data.get("guarantyStyleType")  # 保障措施类型
    id = res_data.get("id")  # 拍卖id
    intended_person_num = res_data.get("intendedPersonNum")  # 报名人数
    investment_type = res_data.get("investmentType")  # 投资类型
    label_type = res_data.get("labelType")  # 标签类型
    merchants_status = res_data.get("merchantsStatus")  # 状态
    name = res_data.get("name")  # 拍卖名称
    onlookers_num = res_data.get("onlookersNum")  # 查看人数
    pawn_category_name = res_data.get("pawnCategoryName")  # 拍卖分类名称
    pawn_location = res_data.get("pawmLocation")  # 拍卖地点
    publish_time = res_data.get("publishTime")  # 发布时间
    vendor_id = res_data.get("vendorId")  # 拍卖方id
    vendor_name = res_data.get("vendorName")  # 拍卖方名称
    print(f"住址：{address}, 发布时间：{standard_time}, 资产类型：{asset_type}, 资产处置方：{asset_disposal}, 附件：{assetssell_attachment_list}, 保障措施：{assetssell_guarantees_list}, 拍卖类型：{auction_type}, 基准日期：{base_date}, 分类id：{category_id}, 分类名称：{category_name}, 咨询电话：{consult_tel}, 资本金：{credit_capital}, 资本金及利息：{credit_capital_and_terest}, 利息：{credit_terest}, 费用总额：{credit_total_charges}, 保障措施类型：{guaranty_style_type}, 拍卖id：{id}, 拍卖人数：{intended_person_num}, 投资类型：{investment_type}, 标签类型：{label_type}, 状态：{merchants_status}, 拍卖名称：{name}, 查看人数：{onlookers_num}, 拍卖分类名称：{pawn_category_name}, 拍卖地点：{pawn_location}, 拍卖方id：{vendor_id}, 拍卖方名称：{vendor_name}")

