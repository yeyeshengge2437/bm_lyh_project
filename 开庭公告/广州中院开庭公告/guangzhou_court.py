import base64
import hashlib
import json
import time
from datetime import datetime
from lxml import etree
import ddddocr
import mysql.connector
import os
import requests
from DrissionPage import ChromiumPage, ChromiumOptions, WebPage
import redis

# 连接到redis数据库
redis_conn = redis.Redis()

ocr = ddddocr.DdddOcr(show_ad=False)

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


co = ChromiumOptions()
co = co.set_paths(local_port=9114)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错

page = ChromiumPage(co)
page.set.auto_handle_alert()

# page = WebPage()


def get_captcha():
    yzm_img = page.ele(".el-input el-input--small").next(1)
    yzm_img.wait(2)
    yzm_img1 = yzm_img.attr('src')[22:]
    # 将base64图片转换为图片文件
    img_yzm = base64.b64decode(yzm_img1)
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


value_unique = paper_queue_next(webpage_url_list=['https://www.gzcourt.gov.cn/fygg/ktgg'])
from_queue = value_unique['id']
webpage_id = value_unique["webpage_id"]



page.get('https://www.gzcourt.gov.cn/fygg/ktgg/')
attempts = 0
flag = 1
while not page.wait.ele_displayed('.container'):
    page.refresh()
    time.sleep(3)
    attempts += 1
    if attempts > 3:
        flag = 0
        page.close()
        # 连接到redis数据库
        redis_conn = redis.Redis()

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://www.gzcourt.gov.cn/fygg/index.html",
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }

        url = "https://www.gzcourt.gov.cn/wwfx/webapp/ktgg/ktggdata.jsp"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = etree.HTML(response.text)
            # 获取全部开庭公告
            all_notice = html.xpath("//table[@class='pageTable']/tbody/tr[position()>1]")
            # 新增数据
            new_num = 0

            for notice in all_notice[:-1]:
                notice_info = notice.xpath("./td/text()")
                case_no = notice_info[4]
                cause = notice_info[5]
                court = notice_info[1]
                members = notice_info[6]
                open_time = notice_info[2].rstrip()
                # 分割日期和时间
                date_part = open_time[:8]
                time_part = open_time[8:]
                # 将日期部分格式化为 "YYYY-MM-DD"
                formatted_date = datetime.strptime(date_part, "%Y%m%d").strftime("%Y-%m-%d")
                # 将时间部分格式化为 "HH:MM"
                # formatted_time = time_part.replace(':', '')
                formatted_time = time_part
                # 合并日期和时间部分
                open_time = f"{formatted_date} {formatted_time}"
                court_room = notice_info[3]
                # 设置创建时间
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 设置创建日期
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 来源
                origin = "广东省广州市中级人民法院"
                # 来源域名
                origin_domain = "gzcourt.gov.cn"
                data_unique = case_no
                # 数据去重
                hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
                # 判断唯一的哈希值是否在集合中
                if not redis_conn.sismember("guangzhou_set", hash_value):
                    # 不重复哈希值添加到集合中
                    redis_conn.sadd("guangzhou_set", hash_value)
                    new_num += 1
                    # 连接到测试库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
                    cursor_test = conn_test.cursor()
                    # 将数据插入到表中
                    insert_sql = "INSERT INTO col_case_open (case_no, cause, court, members, open_time, court_room,  origin, origin_domain, create_time, create_date,from_queue, webpage_id) VALUES (%s,  %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor_test.execute(insert_sql, (
                        case_no, cause, court, members, open_time, court_room,
                        origin,
                        origin_domain, create_time, create_date, from_queue, webpage_id))
                    conn_test.commit()
                    cursor_test.close()
                    conn_test.close()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"时间：{now}， 新增数据数：", new_num)
            success_data = {
                'id': from_queue,
                'description': '广州中院数据获取成功',
            }
            paper_queue_success(success_data)
        else:
            fail_data = {
                "id": from_queue,
                "description": "获取广州中院数据失败",
            }
            paper_queue_fail(fail_data)
        break

if flag:
    try:

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
                            insert_sql = "INSERT INTO col_case_open (case_no, cause, court, members, open_time, court_room,  origin, origin_domain, create_time, create_date,from_queue, webpage_id) VALUES (%s,  %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor_test.execute(insert_sql, (
                                case_no, cause, court, members, open_time, court_room, release_date,
                                origin,
                                origin_domain, create_time, create_date, from_queue, webpage_id))
                            conn_test.commit()
                            cursor_test.close()
                            conn_test.close()

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
        success_data = {
            'id': from_queue,
            'description': '广州各区数据获取成功',
        }
        paper_queue_success(success_data)
    except Exception as e:
        print(f"发生异常：{e}")
        fail_data = {
            "id": from_queue,
        }
        paper_queue_fail(fail_data)
