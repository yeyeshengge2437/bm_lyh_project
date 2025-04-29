# 目的：为多账号服务一个队列进行进行处理，遇到网站限制时可以快速切换到另一个账号进行数据的采集。
"""
1,获取到多个qcc的cookies账号，并判断该cookies是否有效。
2，如果有效，将cookies存放在cookies池中，cookies池用queue存放
3，需要用到时能拿出一个cookies并判断是否有效。
4，无效后需要对cookies进行处理，但不耽误其他cookies被使用（可以用两个线程进行处理）
"""
import json
import math
import random
import re
from datetime import datetime, timedelta
import hashlib
from 验证码识别 import get_captcha
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from qcc_auto_login import auto_login
from qcc_api_res import get_response, post_response
from a_mysql_connection_pool import in_qcc_cookies, search_qcc_cookies_one, up_qcc_cookies, lapse_qcc_cookies, get_lapse_qcc_cookies
from api_paper import paper_queue_next, paper_queue_success, paper_queue_fail, paper_queue_step_finish

co_one = ChromiumOptions()
co_one = co_one.set_user_data_path(r"D:\chome_data\qcc_one")
co_one.set_paths(local_port=9254)

co_two = ChromiumOptions()
co_two = co_two.set_user_data_path(r"D:\chome_data\qcc_two")
co_two.set_paths(local_port=9255)


def get_qcc_cookies(co, phone_num, password, co_name):
    page = ChromiumPage(co)
    page.set.window.max()
    tab = page.get_tab()
    # 访问网页
    tab.get('https://www.qcc.com/')
    input()


    # 判断是否有账号在
    tab.wait(4)
    try:
        tab.ele("xpath=//div[@class='qccd-modal-body']/div[@class='qcc-login']", timeout=3)
        # 登录账号
        """
        这里输入账号密码
        """
        login_outcome = auto_login(tab, phone_num, password)
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
    page.quit()
    cookie_str = json.dumps(cookie_dict, sort_keys=True, ensure_ascii=False)
    in_qcc_cookies(cookie_str, 1, co_name)
    return True


# get_qcc_cookies(co_one, '18812345678', '123456', 'co_one')
# get_qcc_cookies(co_two, '18812345678', '123456', 'co_two')


# 处理已经失效的cookies
def lapse_cookies_up_qcc():
    cookies_id, cookies_tag = get_lapse_qcc_cookies()
    if cookies_id:
        # 存在失效的cookies，则进行处理
        if cookies_tag == 'co_one':
            page = ChromiumPage(co_one)
            page.get('https://www.qcc.com/')
            page.refresh()
            time.sleep(8)
            try:
                get_captcha(page)
                page.refresh()
                time.sleep(6)
                if '账号使用异常，已限制继续访问' not in page.html:
                    if page.ele("xpath=//input[@id='searchKey']"):
                        cookie_dict = {}
                        value_cookies = page.cookies()
                        for key in value_cookies:
                            cookie_dict[key['name']] = key['value']
                        cookies_str = json.dumps(cookie_dict, sort_keys=True, ensure_ascii=False)
                        up_qcc_cookies(cookies_str, 1, cookies_id)
                        page.quit()
                        print('已更新cookies')
                        return True
                    else:
                        lapse_qcc_cookies(cookies_id)
                        page.quit()
                        return False
                else:
                    print("账号使用异常，已限制继续访问。一小时后重试")
                    time.sleep(3600)
            except Exception as e:
                print(e)
                print("不是验证码")
                page.quit()
                lapse_qcc_cookies(cookies_id)
                time.sleep(3600)
                return False
        elif cookies_tag == 'co_two':
            page = ChromiumPage(co_one)
            page.get('https://www.qcc.com/')
            page.refresh()
            time.sleep(8)
            try:
                get_captcha(page)
                page.refresh()
                time.sleep(5)
                if '账号使用异常，已限制继续访问' not in page.html:
                    if page.ele("xpath=//input[@id='searchKey']"):
                        cookie_dict = {}
                        value_cookies = page.cookies()
                        for key in value_cookies:
                            cookie_dict[key['name']] = key['value']
                        cookies_str = json.dumps(cookie_dict, sort_keys=True, ensure_ascii=False)
                        up_qcc_cookies(cookies_str, 1, cookies_id)
                        page.quit()
                        print('已更新cookies')
                        return True
                    else:
                        lapse_qcc_cookies(cookies_id)
                        page.quit()
                        return False
                else:
                    print("账号使用异常，已限制继续访问。一小时后重试")
                    time.sleep(3600)
            except Exception as e:
                print(e)
                print("不是验证码")
                page.quit()
                lapse_qcc_cookies(cookies_id)
                time.sleep(3600)
                return False

    else:
        print('没有已失效的cookies,五分钟后重新查询')
        time.sleep(300)


while True:
    lapse_cookies_up_qcc()
