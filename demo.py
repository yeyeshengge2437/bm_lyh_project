import hashlib
import time

import mysql.connector
import requests
from lxml import etree
import re
import redis
import os
import json
import requests
url = 'https://yjj.guizhou.gov.cn/xwdt/tzgg/202407/t20240718_85130642.html'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-platform': '"Windows"',
}
for url_key in ['xwdt/tzgg', 'gsgg', 'zwgk/jdhy']:
    if url_key in url:
        title_res = requests.get(url, headers=headers)
        time.sleep(2)
        if title_res.status_code == 200:
            title_html = etree.HTML(title_res.content.decode())
            # 文章路径
            article_path = "".join(title_html.xpath("//div[@class='dqwz']//text()")).strip()
            # 概要
            summary = title_html.xpath("//div[1]/table[@class='layui-table']/tbody/tr/td//text()")
            summary_str = ""
            if summary:
                for i in summary:
                    if "var" in i:
                        chinese_chars = re.findall(r'[\u4e00-\u9fa5]+', i)[0]
                    else:
                        chinese_chars = i
                    summary_str.join(chinese_chars)
            # 标题
            title_name = "".join(title_html.xpath("//div[@id='c']/div[@class='Article_bt']//text()")).strip()
            contents = title_html.xpath("//div[contains(@class, 'trs_paper_default')]")
            if contents:
                for cont in contents:
                    content_html = ''.join(etree.tostring(cont, method='html',encoding='unicode'))
            else:
                contents = title_html.xpath("//div[@class='Article_zw']")
                if contents:
                    for cont in contents:
                        content_html = ''.join(etree.tostring(cont, method='html', encoding='unicode'))



            # content = "".join(
            #     etree.tostring(title_html.xpath("//div[contains(@class, 'trs_paper_default')]//node()"), method='html', encoding='unicode'))
            # if not content:
            #     content = "".join(title_html.xpath("//div[@class='Article_zw']//node()")).strip()
            # print(content)
