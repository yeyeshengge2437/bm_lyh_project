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
tab.get('https://www.qcc.com/firm/2a5889eb817fdc6ae9e71d0bc2252416.html')

input()
page.quit()