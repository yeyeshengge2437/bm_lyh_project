import json
import re
import time
from datetime import datetime
from api_paimai import judge_repeat, judge_repeat_attracting
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Settings
from fake_useragent import UserAgent
import tempfile
import random
from lxml import etree
from jingdongpaimai import JingDongPaiMai
# import datetime
import re


def parse_opentime(s):
    # 处理绝对时间格式
    if s.startswith("开拍时间："):
        try:
            dt = datetime.strptime(s, "开拍时间：%Y年%m月%d日 %H:%M:%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

    # 处理剩余时间格式
    elif "距离开拍仅剩：" in s:
        # 正则匹配时、分、秒
        match = re.match(
            r"距离开拍仅剩：(?:(\d+)时)?(\d+)分(\d+)秒",
            s
        )
        if not match:
            return None

        # 提取时间部分（缺失的部分默认为0）
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2))
        seconds = int(match.group(3))

        # 计算开拍时间（当前时间 + 时间差）
        delta = datetime.timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )
        open_time = datetime.now() + delta

        return open_time.strftime("%Y-%m-%d %H:%M:%S")

    else:
        return None


def remove_styles(tree):
    # 删除 <style> 标签
    for tag in tree.xpath('//style | //link[@rel="stylesheet"]'):
        parent = tag.getparent()
        if parent is not None:
            parent.remove(tag)
    # 删除 <style> 标签
    for tag in tree.xpath('//script'):
        parent = tag.getparent()
        if parent is not None:
            parent.remove(tag)
    # 删除内联样式属性
    for element in tree.xpath('//@style'):
        parent = element.getparent()
        del parent.attrib['style']
    return tree


def get_jingdongpaimai_detail(url, url_name, state, from_queue, state_now=''):
    # 禁用全局自动化特征
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True

    # 配置浏览器参数
    options = ChromiumOptions()
    # options.set_argument('--disable-blink-features=AutomationControlled')
    options.set_argument('--incognito')
    options.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')

    # # 随机化UA
    # ua = UserAgent()
    # options.set_argument(f'--user-agent={ua.random}')
    url = url
    title = url_name
    state_sql, id = judge_repeat(url)
    if state_sql:
        # page.quit()
        return
    # 启动浏览器
    page = ChromiumPage(options)

    # 设置随机窗口尺寸
    page.set.window.size(1366 + random.randint(-100, 100), 768 + random.randint(-50, 50))
    # 访问目标网站
    page.get(url)
    page.scroll.to_bottom()
    time.sleep(4)

    tree = etree.HTML(page.html)

    # 执行清理并输出, 测试阶段展示html
    cleaned_tree = remove_styles(tree)
    # cleaned_html = etree.tostring(cleaned_tree, encoding='unicode', pretty_print=True)
    # print(cleaned_html)
    # return

    state = state
    stage = ''
    address = ''.join(tree.xpath("//div[contains(@class, 'pm-location')]/em/text()"))
    start_bid = ''.join(tree.xpath(
        "//li[2]/div[@class='index_label__Nie1n ']/div[@id='right-content']//span[contains(@class, 'index_value__YfM3M ')]/text()"))
    sold_price = ''.join(tree.xpath("//div[@class='priceInfoItemPriceWrap']//text()"))
    sold_price = ''.join(re.findall(r'¥(.*)', sold_price))
    outcome = ''.join(tree.xpath("//div[@class='index_auctionstatusbanner__statustext__RxEYN']/span//text()"))
    end_time = ''
    start_time = ''
    if state_now == '已结束' or state_now == '进行中':
        end_time = ''.join(tree.xpath("//div[@class='index_auctionstatusbanner__endtime__7-dda']/text()"))
        end_time = ''.join(re.findall(r'(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2})', end_time))  # 结束时间
        end_time = end_time.replace('年', '-').replace('月', '-').replace('日', '')
    elif state_now == '预告中':
        distance_end = ''.join(tree.xpath("//div[@class='index_countdown__remainTime__O7MNa']/div//text()"))
        if not distance_end:
            distance_end = ''.join(tree.xpath("//div[@class='index_countdown__time__ArsTv']//text()"))
        start_time = parse_opentime(distance_end)
        print(distance_end)
        print(start_time)
        return
    procedure_str = ''  # 拍卖程序
    disposal_unit = ''.join(tree.xpath("//a[@id='disposalUnitTag']/text()"))  # 处置单位
    bidding_status = ''.join(tree.xpath("//table[@class='index_bidList__i8yA2']/tbody/tr[1]/td[1]/div/text()"))  # 竞买状态
    bidding_code = ''.join(tree.xpath("//table[@class='index_bidList__i8yA2']/tbody/tr[1]/td[2]/div/text()"))  # 竞买代码
    bidding_price = ''.join(tree.xpath("//table[@class='index_bidList__i8yA2']/tbody/tr[1]/td[3]/div/text()"))  # 竞买价格
    bidding_time = ''.join(tree.xpath("//table[@class='index_bidList__i8yA2']/tbody/tr[1]/td[4]/div/text()"))  # 竞买时间
    auction_history = f'竞买状态:{bidding_status} 竞买代码:{bidding_code} 竞买价格:{bidding_price} 竞买时间:{bidding_time}'
    people_num = ''.join(tree.xpath("//div[@class='index_auctionstatusbanner__statistics__-mtfv']//text()"))  # 竞买人数
    people_num = ''.join(re.findall(r'(\d+)人报名', people_num))
    # subject_info_etree = tree.xpath("//div[@class='paimaiDetailContainer']/div[@class='pm-content']/ul[@class='floors']/li[3]")  # 标的物信息_html
    subject_info_etree = tree.xpath(
        "//div[@class='paimaiDetailContainer']/div[@class='pm-content']/ul[@class='floors']/li[3]")  # 标的物信息_html
    subject_info = ''
    for con in subject_info_etree:
        subject_info += etree.tostring(con, encoding='utf-8').decode()
    subject_annex_up_list = tree.xpath("//ul[@class='floors']//@href")  # 标的物信息附件上传
    subject_annex_up = ''
    for annex in subject_annex_up_list:
        if annex == 'http://zichan.jd.com/':
            continue
        else:
            subject_annex_up += annex + ','
    subject_annex_up = subject_annex_up[:-1]
    auction_html_etree = tree.xpath("//div[@class='pm-content']//li[@class='floor index_floor__1u9-C'][1]")  # 拍卖公告_html
    auction_html = ''
    for con in auction_html_etree:
        auction_html += etree.tostring(con, encoding='utf-8').decode()

    value = {
        'url': url,
        'title': title,
        'state': state,
        'stage': stage,
        'address': address,
        'start_bid': start_bid,
        'sold_price': sold_price,
        'outcome': outcome,
        'end_time': end_time,
        'procedure_str': procedure_str,
        'disposal_unit': disposal_unit,
        'auction_history': auction_history,
        'people_num': people_num,
        'subject_info': subject_info,
        'subject_annex_up': subject_annex_up,
        'auction_html': auction_html
    }
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    create_date = datetime.now().strftime('%Y-%m-%d')
    # 上传到测试数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 上传文件
    insert_sql = "INSERT INTO col_judicial_auctions (url, title, state, stage, address, start_bid, sold_price, outcome, end_time, procedure_str, auction_html, subject_annex_up, subject_info, disposal_unit, auction_history, people_num, subject_annex, create_time, create_date, from_queue) VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s, %s, %s,%s,%s)"

    cursor_test.execute(insert_sql,
                        (url, title, state, stage, address, start_bid, sold_price,
                         outcome,
                         end_time, procedure_str, auction_html, subject_annex_up,
                         subject_info,
                         disposal_unit, auction_history, people_num, subject_annex_up,
                         create_time,
                         create_date, from_queue))
    conn_test.commit()

    cursor_test.close()
    conn_test.close()
    print(value)


def get_jd_attracting_data(url, url_name, state, from_queue):
    # 禁用全局自动化特征
    Settings.smart_launch = False
    Settings.ignore_certificate_errors = True

    # 配置浏览器参数
    options = ChromiumOptions()
    # options.set_argument('--disable-blink-features=AutomationControlled')
    options.set_argument('--incognito')
    options.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')

    # # 随机化UA
    # ua = UserAgent()
    # options.set_argument(f'--user-agent={ua.random}')
    url = url
    title = url_name
    id_value = judge_repeat_attracting(url)
    if id_value:
        # page.quit()
        return
    # 启动浏览器
    page = ChromiumPage(options)

    # 设置随机窗口尺寸
    page.set.window.size(1366 + random.randint(-100, 100), 768 + random.randint(-50, 50))
    # 访问目标网站
    page.get(url)
    page.scroll.to_bottom()
    time.sleep(4)

    tree = etree.HTML(page.html)
    # 执行清理并输出, 测试阶段展示html
    tree = remove_styles(tree)
    cleaned_html = etree.tostring(tree, encoding='unicode', pretty_print=True)
    # print(cleaned_html)
    # return
    disposition_subject = ''.join(
        tree.xpath("//dl[@class='sc-fBuWsC GdrRc']/dd[@class='sc-jhAzac bHuVwS']//text()"))  # 资产处置主体
    reference_value = ''  # 参考价值
    recruitment_time = ''.join(tree.xpath(
        "//div[@class='sc-Rmtcm jTBHht'][1]/dl[@class='sc-fBuWsC GdrRc'][4]/dd[@class='sc-hzDkRC kHJBpV']/text()"))  # 招募时间
    recruitment_time = ''.join(re.findall(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', recruitment_time))  # 招募时间
    type = ''.join(tree.xpath("//dl[@class='sc-fBuWsC GdrRc'][1]/dd[@class='sc-hzDkRC kHJBpV']/text()"))  # 类型
    guarantee_method = ''.join(tree.xpath(
        "//div[@class='sc-Rmtcm jTBHht'][1]/dl[@class='sc-fBuWsC GdrRc'][3]/dd[@class='sc-hzDkRC kHJBpV']/text()"))  # 担保方式
    total = ''.join(tree.xpath("//dl[@class='sc-fBuWsC kHwFGn']//text()")) + ',其中：' + ''.join(
        tree.xpath("//dl[@class='sc-fBuWsC GdrRc'][2]/dd[@class='sc-hzDkRC kHJBpV']//text()"))  # 债权总金额
    situation = ''.join(tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][2]/p//text()"))  # 债务人情况
    guarantor = ''.join(tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][3]/p//text()"))  # 担保人情况
    collateral_list = tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][4]")  # 抵押物情况
    collateral = ''
    for con in collateral_list:
        collateral += etree.tostring(con, encoding='utf-8').decode()
    detail_list = tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][1]")  # 公告详情
    detail_html = ''
    for con in detail_list:
        detail_html += etree.tostring(con, encoding='utf-8').decode()
    detail = ''.join(tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][1]//text()"))  # 公告详情
    supple_mater = ''.join(tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][5]/a[@class='sc-kvZOFW gOWYUa']//text()"))  # 附件
    # original_annexs = tree.xpath("//div[@class='sc-frDJqD cDnLeJ'][5]/a[@class='sc-kvZOFW gOWYUa']")   # 附件链接
    # print(len(original_annexs))
    annex_urls = ''
    # if len(original_annexs) > 0:
    #     for original_annex in original_annexs:
    #         page.ele("xpath=//div[@class='sc-frDJqD cDnLeJ'][5]/a[@class='sc-kvZOFW gOWYUa']").click(by_js=True)
    #         time.sleep(4)
    #         annex_urls += page.url + ','
    #         page.back()
    data_dict = {
        "disposition_subject": disposition_subject,
        "reference_value": reference_value,
        "recruitment_time": recruitment_time,
        "type": type,
        "guarantee_method": guarantee_method,
        "total": total,
        "situation": situation,
        "guarantor": guarantor,
        "collateral": collateral,
        "detail": detail,
        "more_info": detail_html,
        "supple_mater": supple_mater,
        "annex_urls": annex_urls,
    }

    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    create_date = datetime.now().strftime('%Y-%m-%d')

    from_queue = "4567"
    try:
        conn_test = mysql.connector.connect(
            host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database="col",
        )
        cursor_test = conn_test.cursor()
        # 上传文件
        insert_sql = "INSERT INTO col_judicial_auctions_investing (url, title, disposition_subject, reference_value, recruitment_time, type,  guarantee_method, total, situation, guarantor, collateral, detail, more_info, supple_mater, create_time, create_date, from_queue) VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s)"

        cursor_test.execute(insert_sql, (
            url, title, disposition_subject, reference_value, recruitment_time, type, guarantee_method, total,
            situation, guarantor, collateral, detail, detail_html, supple_mater, create_time,
            create_date, from_queue))
        conn_test.commit()
        print(data_dict)
        cursor_test.close()
        conn_test.close()
    except Exception as e:
        print(f"Error: {e}")
        pass


# 有附件  https://auction.jd.com/zichan/tuijie/item/109544, https://auction.jd.com/zichan/tuijie/item/109552


# 处理京东拍卖招商中的数据入库
with open("jd_attracting.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)  # 直接解析为 Python 字典或列表

count = 0
for data in data_list:
    count += 1
    url = data['url']
    url_name = data['url_name']
    state = data['state']
    print(url, url_name, state)
    get_jd_attracting_data(url, url_name, state, "4567")

# 处理京东已结束的数据入库
# jd = JingDongPaiMai()
# jd.main_func_jingdong_data()
#
# with open("jingdongpaimai.json", "r", encoding="utf-8") as f:
#     data_list = json.load(f)  # 直接解析为 Python 字典或列表
#
# count = 0
# for data in data_list:
#     count += 1
#     url = data['url']
#     url_name = data['url_name']
#     state = data['state']
#     if state == '已结束':
#         # continue
#         get_jingdongpaimai_detail(url, url_name, state, "4567", state_now='已结束')
#     elif state == '进行中':
#         continue
#         # get_jingdongpaimai_detail(url, url_name, state, "4567", state_now='进行中')
#     elif state == '预告中':
#         continue
#         # get_jingdongpaimai_detail(url, url_name, state, "4567", state_now='预告中')
#     if count == 100:
#         break
