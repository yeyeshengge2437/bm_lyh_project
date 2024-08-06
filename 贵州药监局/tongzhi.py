import time

import requests
from lxml import etree
import re
import redis

# 连接redis
r = redis.Redis()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://yjj.guizhou.gov.cn/xwdt/tzgg/index.html', headers=headers)
print(response.status_code)
html_1 = etree.HTML(response.content.decode())
# 获取一共有多少条数据
page = html_1.xpath("//div[3]/div/div[2]/div[2]/script/text()")[0]
page_num = re.findall(r'\d+', page)[0]
print(page_num)
if not r.llen('guizhou_yjj'):
    for i in range(1, int(page_num) + 1):
        if i == 1:
            url = "https://yjj.guizhou.gov.cn/xwdt/tzgg/index.html"
        else:
            url = "https://yjj.guizhou.gov.cn/xwdt/tzgg/index_" + str(i-1) + ".html"
        # 使用redis构造任务队列

        r.lpush('guizhou_yjj', url)

# 从任务队列中获取任务
while r.llen('guizhou_yjj'):
    url = r.rpop('guizhou_yjj').decode()
    print(url)

# # 获取该页面下的所有通知公告
# notices = html_1.xpath("//div[@class='right-list-box']/ul/li/a")
# for notice in notices:
#     title_name = "".join(notice.xpath("./text()")[0]).strip()
#     # notice_url = "https://yjj.guizhou.gov.cn" + notice.xpath("./@href")[0]
#     title_url = "".join(notice.xpath("./@href")[0])
#     if len(title_url) < 67:
#         base_title_url = title_url[:42]
#     else:
#         base_title_url = title_url[:48]
#     title_res = requests.get(title_url, headers=headers)
#     time.sleep(2)
#     if title_res.status_code == 200:
#         title_html = etree.HTML(title_res.content.decode())
#         # 文章路径
#         article_path = "".join(title_html.xpath("//div[@class='dqwz']//text()")).strip().strip('您当前所在的位置: ')
#         content = "".join(title_html.xpath("//div[@class='trs_editor_view TRS_UEDITOR trs_paper_default trs_word']//text()")).strip()
#         source = "".join(title_html.xpath("//div[@class='Article_ly']/span[@class='SourceName']//text()"))
#         if not source:
#             source = "".join(title_html.xpath("//div[@id='c']/div[@class='Article_ly']/span[2]//text()"))
#             source = re.findall(r"var wzly='(.*?)';", source)[0]
#         else:
#             source = re.findall(r"var SourceName='(.*?)';", source)[0]
#         pub_date = "".join(title_html.xpath("//div[@id='c']/div[@class='Article_ly']/span[1]//text()"))
#         pub_date = re.findall(r"var  pubdata='(.*?)';", pub_date)[0]
#         annexs = title_html.xpath("//p[@class='insertfileTag']/a")   # 获取所有附件
#         if annexs:
#             for annex in annexs:
#                 annex_name = annex.xpath("./text()")[0]
#                 annex_url = ''.join(annex.xpath("./@href")[0].strip('.'))
#                 annex_url = base_title_url + annex_url
#                 print(annex_name, annex_url)



