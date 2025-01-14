import json
import random
import re
from 验证码识别 import get_captcha
import requests
import time
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\data_one")
co.set_paths(local_port=9136)
random_float = random.uniform(1, 5)
# 连接浏览器
page = ChromiumPage(co)
tab = page.get_tab()
# 访问网页
tab.get('https://www.qcc.com/')
# time.sleep(3)
search_name = tab.ele("xpath=//input[@id='searchKey']")
search_name.click()
time.sleep(1)
# search_name.input('金川集团股份有限公司')
search_name.input('华为通数字科技')
# 搜索按键点击
tab.ele("xpath=//span[@class='input-group-btn']/button[@class='btn btn-primary']").click(by_js=True)
time.sleep(2)
# 获取公司列表
res_html = tab.html
print(res_html)
# 获取公司信息
input("1111")
page.quit()
