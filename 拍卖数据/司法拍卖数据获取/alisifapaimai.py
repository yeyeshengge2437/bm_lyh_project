import random
import re
import time
from datetime import datetime, timedelta
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from urllib.parse import urlencode, urljoin
import redis

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\ali_two")
# co = co.set_argument('--no-sandbox')
# co = co.headless()
co.set_paths(local_port=9153)


page = ChromiumPage(co)
search_value = '（2024）苏1081执恢412号'
page.get(f'https://sf.taobao.com/?spm=a213w.3064813.sfhead2014.2.59e43fe757iUv7')
page.wait.doc_loaded()
time.sleep(4)
page.ele("xpath=//input[@id='J_SearchTxt']").input(search_value)
time.sleep(1)
page.ele("xpath=//form[@class='paimai-search-form']/button").click()
time.sleep(4)
new_tab = page.latest_tab
page.close()
new_tab.wait.doc_loaded()
time.sleep(4)
# new_tab.html
target = etree.HTML(new_tab.html)
target_html = target.xpath("//div[@class='sf-item-list']/ul[@class='sf-pai-item-list'][1]/li")
for target_ in target_html:
    url = 'https:' + ''.join(target_.xpath("./a//@href")[0])
    url_name = ''.join(target_.xpath("./a//p[@class='title']/text()")).strip()
    state_time = ''.join(target_.xpath(".//div[@class='info-section']/p[contains(@class, 'time')]//text()"))
    state_time = re.sub(' ', '', state_time)
    print(url, url_name, state_time)
    new_tab.get(url)
    new_tab.scroll.to_bottom()
    new_tab.wait.doc_loaded()
    time.sleep(4)
    html_detail = new_tab.html
    print(html_detail)
    break

# page.quit()



