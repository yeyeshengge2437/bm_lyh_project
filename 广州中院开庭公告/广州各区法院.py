import base64
import hashlib
import json
import time
from datetime import datetime

import ddddocr
import mysql.connector

import requests
from DrissionPage import ChromiumPage, ChromiumOptions, WebPage
import redis

# 连接到redis数据库
redis_conn = redis.Redis()

ocr = ddddocr.DdddOcr()

court_names = [
    '广东自由贸易区南沙片区人民法院',
    '广州市荔湾区人民法院',
    '广州市越秀区人民法院',
    '广州市海珠区人民法院',
    '广州市黄埔区人民法院',
    '广州市白云区人民法院',
    '广州市花都区人民法院',
    '广州市增城区人民法院',
    '广州市番禺区人民法院',
    '广州市南沙区人民法院',
    '广州市天河区人民法院',
    '广州市从化区人民法院',
    '广州互联网法院'
]
# court_names = [
#     '广州市天河区人民法院',
#     '广州市从化区人民法院',
#     '广州互联网法院'
# ]
# 隧道域名:端口号
tunnel = "x170.kdltps.com:15818"

co = ChromiumOptions()
co.set_proxy("http://" + tunnel)

# page = WebPage(chromium_options=co)
page = ChromiumPage(9113)
page.set.auto_handle_alert()

# page = WebPage()


def get_captcha():
    yzm_img = page.ele(".el-input el-input--small").next(1)
    yzm_img.wait(2)
    yzm_img1 = yzm_img.attr('src')[22:]
    # 将base64图片转换为图片文件
    img_yzm = base64.b64decode(yzm_img1)
    with open("yzm.png", "wb") as f:
        f.write(img_yzm)
    captcha = ocr.classification(img_yzm)
    yzm_input = page.ele('@placeholder=请输入验证码')
    yzm_input.input(captcha, clear=True)


def warning_message_processing():
    """
    处理警告信息
    :return:
    """
    warning_flag = 0
    while page.ele('@class^el-message'):
        time.sleep(10)
        get_captcha()
        page.ele('.el-button red-query-button el-button--danger el-button--small').click()
        warning_flag = 1
    return warning_flag


page.set.window.max()
page.get('https://www.gzcourt.gov.cn/fygg/ktgg/')
attempts = 0
flag = 1
while not page.wait.ele_displayed('.container'):
    page.refresh()
    time.sleep(3)
    attempts += 1
    if attempts > 5:
        flag = 0
        print("该页面内容无法显示")
        page.close()
        break

if flag:

    # 记录当前爬取页数——————————————————————
    page_num = 1

    # while page.ele('暂无数据'):
    #     page.refresh()
    for court_name in court_names:
        page.wait.ele_displayed('.el-input__icon el-icon-arrow-down')
        court_ele = page.ele('.el-input__icon el-icon-arrow-down')
        court_ele.click()
        time.sleep(4)
        if court_ele.text == '暂无数据':
            court_ele.click()
            time.sleep(4)
            court_ele.click()
        page.wait.ele_displayed(court_name)
        page.ele(court_name).click()

        # 验证码部分——————————————————————————

        get_captcha()

        # 下滑到底部
        page.scroll.to_bottom()
        page.ele('@placeholder=请选择', index=-1).click()
        time.sleep(2)
        page.ele('.el-scrollbar__view el-select-dropdown__list').child(index=-1).click(by_js=True)
        time.sleep(10)
        get_captcha()
        page.ele('.el-button red-query-button el-button--danger el-button--small').click()

        warning_message_processing()

        page.wait.ele_displayed('.el-table__row')
        page.wait.ele_displayed('.btn-next')
        next_btn = page.ele('.btn-next')

        while not next_btn.attr('disabled'):

            court_infos = page.eles('.el-table__row')
            # 获取目前爬取页数
            page_num = page.ele('.number active').text

            for court_info in court_infos:
                trial_info = court_info.text.split('\n\t')
                if len(trial_info) == 7:
                    case_no = trial_info[0]
                    cause = trial_info[1]
                    members = trial_info[2]
                    court = trial_info[3]
                    open_time = trial_info[4]
                    court_room = trial_info[5]
                    release_date = trial_info[6]
                    # 设置创建时间
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # 设置创建日期
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # 来源
                    origin = "广州中院公告公示中心开庭公告"
                    # 来源域名
                    origin_domain = "gzcourt.gov.cn"

                    data_unique = case_no
                    # 数据去重
                    hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
                    # 判断唯一的哈希值是否在集合中
                    if not redis_conn.sismember("guangdong_region_set", hash_value):
                        # 不重复哈希值添加到集合中
                        redis_conn.sadd("guangdong_region_set", hash_value)
                        print("新数据：", data_unique)
                        # 连接到测试库
                        conn_test = mysql.connector.connect(
                            host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                            user="col2024",
                            password="Bm_a12a06",
                            database="col_test"
                        )
                        cursor_test = conn_test.cursor()
                        # 将数据插入到case_open_copy1表中
                        insert_sql = "INSERT INTO case_open_copy1 (case_no, cause, court, members, open_time, court_room, release_date, origin, origin_domain, create_time, create_date) VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql, (
                            case_no, cause, court, members, open_time, court_room, release_date,
                            origin,
                            origin_domain, create_time, create_date))
                        print("插入成功")
                        conn_test.commit()
                        cursor_test.close()
                        conn_test.close()
                    else:
                        print("重复数据：", data_unique)

            time.sleep(15)
            # 点击下一页——————————————————————————————
            page.ele(".btn-next").click()
            warning_value = warning_message_processing()
            if warning_value:
                time.sleep(4)
                get_captcha()
                jump_page = page.ele('.el-input__inner', index=-1)
                jump_page.input(page_num, clear=True)
                jump_page.tab.actions.key_down('ENTER')
            page.wait.ele_hidden('.el-loading-text')
            # warning_message_processing()


    page.close()
