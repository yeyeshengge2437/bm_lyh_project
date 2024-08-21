import base64
import json
import time
from datetime import datetime

from DrissionPage import ChromiumPage, ChromiumOptions

import pymongo
import ddddocr
import mysql.connector
import hashlib
import redis

# 连接redis数据库
redis_conn = redis.Redis()

destination = 1

# 引入验证码模板
# chaojiying = Chaojiying_Client('2437948121', 'liyongheng10', '961977')
ocr = ddddocr.DdddOcr(show_ad=False)

co = ChromiumOptions()
co = co.set_paths(local_port=9113)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错

page = ChromiumPage()
import os
import json
import requests
produce_url = "http://121.43.164.84:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False


def paper_queue_next(webpage_url_list=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if webpage_url_list is None:
        webpage_url_list = []

    url = test_url + "/website/queue/next"
    data = {
        "webpage_url_list": webpage_url_list
    }

    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    print(result)
    return result.get("value")


def paper_queue_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = test_url + "/website/queue/success"
    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result.get("value")


def paper_queue_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    try:
        if data is None:
            data = {}
        url = test_url + "/website/queue/fail"
        data_str = json.dumps(data)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        return result.get("value")
    except Exception as err:
        print(err)
        return None



def upload_file_by_url(file_url, file_name, file_type, type="paper"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(file_url, headers=headers)
    if r.status_code != 200:
        return "获取失败"
    pdf_path = f"{file_name}.{file_type}"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}
    url = 'http://121.43.164.84:29775' + f"/file/upload/file?type={type}"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    return result.get("value")["file_url"]


def get_captcha():
    time.sleep(3)
    # 获取验证码图片，并识别验证码
    img_yzm = page.ele(".el-image__inner").attr("src")[23:]
    # 将base64图片转换为图片文件
    img_yzm = base64.b64decode(img_yzm)


    captcha = ocr.classification(img_yzm)


    # 点击验证码输入框，输入验证码
    yzm_srk = page.ele("xpath=//div[@class='el-input el-input--mini']/input[@class='el-input__inner']", index=-1)
    # 清空输入框
    yzm_srk.clear()
    yzm_srk.click()
    yzm_srk.input(captcha)


def click_Inquire():
    """
    点击查询按钮
    :return:
    """
    value = page.ele("查询").parent()
    page.run_js("arguments[0].click();", value)


def error_dispose():
    """
    错误处理
    :return:
    """
    message = page.ele('@class:el-message')
    if message:
        # # 获取元素文本
        # print(message.text)
        # 再次获取验证码
        get_captcha()
        # 点击查询
        click_Inquire()

        return True
    else:
        return False


def jump_to_page(num):
    """
    跳转到指定页面
    :return:
    """
    jump = page.ele(".el-input__inner", index=8)
    if jump:
        jump.click()
        jump.clear()
        jump.input(num)
        # 回车
        jump.tab.actions.key_down('ENTER')
    else:
        get_captcha()
        click_Inquire()
        get_captcha()
        time.sleep(3)
        jump_to_page(num)


def run(destination_page):
    # 打开目标网页
    page.get("https://ssfw.njfy.gov.cn/#/ktggList")
    time.sleep(10)
    # 点击日期
    date = page.ele(".el-input__inner", index=5)
    date.clear()
    # 获取两个月之后的日期
    date.input(time.strftime('%Y-%m-%d', time.localtime(time.time() + 60 * 60 * 24 * 60)))
    # 点击回车
    date.tab.actions.key_down('ENTER')

    page.wait(2)

    get_captcha()

    # 点击搜索按钮
    click_Inquire()

    # 如果提示元素出现
    error_dispose()

    # 获取数据
    # 等待页面加载完成
    page.wait.ele_displayed('.el-table__row')
    elements = page.eles('.el-table__row')

    # 获取共多少页
    total_page = int(page.ele(".el-pagination__total").text.split("共")[1].split("条")[0])
    total_page = int(total_page / 10) + 1


    # # 遍历元素
    # for element in elements:
    #     # 获取到的数据
    #     # print(element.text)
    #     # 存储到数据库
    #     collection.insert_one({"data": element.text})

    if destination_page != 1:
        get_captcha()
        jump_to_page(destination_page)

    data_num = 0
    new_data_num = 0

    for page_now in range(destination_page, total_page):
        # 等待页面加载完成
        page.wait.ele_displayed('.el-table__row')
        elements = page.eles('.el-table__row')
        # 遍历元素
        for element in elements:
            data_num += 1
            # 获取到的数据
            element = element.text
            value = element.split('\n\t')
            # 设置创建时间
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 设置创建日期
            create_date = datetime.now().strftime('%Y-%m-%d')
            # 来源
            origin = "南京中级人民法院开庭公告"
            # 来源域名
            origin_domain = "ssfw.njfy.gov.cn"
            if len(value) == 10:
                # 案号
                case_no = value[0]
                # 案由
                cause = value[1]
                # 当事人
                members = value[2]
                # 审理法院
                trial_court = value[3]
                # 承办人
                room_leader = value[4]
                # 承办部门
                department = value[5]
                # 是否公开开庭
                is_public = value[6].split('\t')[-1]
                # 开庭法院
                court_room = value[7]
                # 开庭日期
                open_date = value[8] + " " + value[9]

                # 确定唯一值
                unique = case_no
                # 数据去重
                hash_value = hashlib.md5(json.dumps(unique).encode('utf-8')).hexdigest()
                if not redis_conn.sismember("nanjing_set", hash_value):
                    # 不重复哈希值添加到集合中
                    redis_conn.sadd("nanjing_set", hash_value)

                    new_data_num += 1

                    # 连接到测试库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
                    cursor_test = conn_test.cursor()
                    # 将数据插入到表中
                    insert_sql = "INSERT INTO col_case_open (case_no, cause, court, members, open_time, court_room, room_leader, department,  origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,  %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql, (
                        case_no, cause, trial_court, members, open_date, court_room, room_leader, department,
                        origin,
                        origin_domain, create_time, create_date,from_queue, webpage_id))
                    # print("插入成功")
                    conn_test.commit()
                    cursor_test.close()
                    conn_test.close()


            else:
                # 案号
                case_no = value[0]
                # 案由
                cause = value[1]
                # 当事人
                members = value[2]
                # 审理法院
                trial_court = value[3]
                # 承办人
                room_leader = value[4]
                # 承办部门
                department = value[5]
                # 书记员
                clerk = value[6]
                # 是否公开开庭
                is_public = value[7]
                # 开庭法院
                court_room = value[8]
                # 开庭日期
                open_date = value[9] + " " + value[10]

                # 确定唯一值
                unique = case_no
                # 数据去重
                hash_value = hashlib.md5(json.dumps(unique).encode('utf-8')).hexdigest()
                if not redis_conn.sismember("nanjing_set", hash_value):
                    # 不重复哈希值添加到集合中
                    redis_conn.sadd("nanjing_set", hash_value)


                    # 连接到测试库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
                    cursor_test = conn_test.cursor()
                    # 将数据插入到case_open_copy1表中
                    insert_sql = "INSERT INTO col_case_open (case_no, cause, court, members, open_time, court_room, room_leader, department,  origin, origin_domain, create_time, create_date,from_queue, webpage_id) VALUES (%s,  %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql, (
                        case_no, cause, trial_court, members, open_date, court_room, room_leader, department,
                        origin,
                        origin_domain, create_time, create_date, from_queue, webpage_id))

                    conn_test.commit()
                    cursor_test.close()
                    conn_test.close()

            # 存储到数据库
            # collection.insert_one({"data": element.text})

        destination = page_now

        # try:
        #     # 获取下一页的状态
        #     next_page_state = page.ele(".el-icon el-icon-arrow-right").parent().attr("disabled")
        #     # 获取当前页数
        #     # page_now = int(page.ele(".number active").text)
        # except Exception as e:
        #     print(f"获取下一页状态发生错误：{e}")
        #     # 再次获取验证码
        #     get_captcha()
        #     click_Inquire()
        #     get_captcha()
        #     jump_to_page(page_now)

        # 再次获取验证码
        get_captcha()
        try:
            # 点击下一页
            page.ele(".el-icon el-icon-arrow-right").click(by_js=True)
        except Exception as e:

            get_captcha()
            click_Inquire()
            get_captcha()
            time.sleep(3)
            jump_to_page(page_now)

        # 错误处理
        value_error = error_dispose()
        # 跳转到当前爬取界面
        if value_error:
            jump_to_page(page_now)

    # 获取当前时间
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{now_time}:本次爬取{data_num}条数据, 新增数据{new_data_num}条")

    # 关闭浏览器
    page.quit()


max_attempts = 5  # 设置最大尝试次数
attempts = 0

while attempts < max_attempts:
    value = paper_queue_next(webpage_url_list=['https://ssfw.njfy.gov.cn/#/ktggList'])
    from_queue = value['id']
    webpage_id = value["webpage_id"]
    try:
        run(destination)
        success_data = {
            'id': from_queue,
        }
        paper_queue_success(success_data)
        break  # 如果函数执行成功，退出循环
    except Exception as e:
        print(f"发生错误：{e}")
        attempts += 1  # 增加尝试次数
        print(f"尝试再次爬取，尝试{attempts}/{max_attempts}")
        time.sleep(3600)  # 等待一小时后再次尝试


        if attempts == max_attempts:
            print("已达到最大尝试次数。退出。")
            fail_data = {
                "id": from_queue,
            }
            paper_queue_fail(fail_data)
