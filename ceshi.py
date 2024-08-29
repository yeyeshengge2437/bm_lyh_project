
import json
import re
import time
from datetime import datetime

import mysql.connector
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import redis
from lxml import etree

# 连接redis数据库
redis_conn = redis.Redis()

co = ChromiumOptions()
co = co.set_paths(local_port=9121)
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错

page = ChromiumPage()
page.set.load_mode.none()
url = 'https://dkjgfw.mnr.gov.cn/#/detail/dwxxxq/2/1/f22f42eba55741b988c800b62f9b985b/91230110585139891Y/ycml'

page.get(url)
print(page.html)
