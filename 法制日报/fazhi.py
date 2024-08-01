import os

from DrissionPage import ChromiumPage, ChromiumOptions
import requests
from lxml import etree
import base64
import hashlib
import json
import time
from datetime import datetime


def upload_pdf_by_url(pdf_url, file_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    r = requests.get(pdf_url, headers=headers)
    if r.status_code != 200:
        return ""
    pdf_path = f"{file_name}.pdf"
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    fw = open(pdf_path, 'wb')
    fw.write(r.content)
    fw.close()
    # 缺少上传接口


claims_keys = [
    '债权通知书', '债权告知书', '债权通知公告', '债权登报公告', '债权补登公告', '债权补充公告', '债权拍卖公告', '债权公告', '债权通知',
    '转让通知书', '转让告知书', '转让通知公告', '转让登报公告', '转让补登公告', '转让补充公告', '转让拍卖公告', '转让公告', '转让通知',
    '受让通知书', '受让告知书', '受让通知公告', '受让登报公告', '受让补登公告', '受让补充公告', '受让拍卖公告', '受让公告', '受让通知',
    '处置通知书', '处置告知书', '处置通知公告', '处置登报公告', '处置补登公告', '处置补充公告', '处置拍卖公告', '处置公告', '处置通知',
    '招商通知书', '招商告知书', '招商通知公告', '招商登报公告', '招商补登公告', '招商补充公告', '招商拍卖公告', '招商公告', '招商通知',
    '营销通知书', '营销告知书', '营销通知公告', '营销登报公告', '营销补登公告', '营销补充公告', '营销拍卖公告', '营销公告', '营销通知',
    '信息通知书', '信息告知书', '信息通知公告', '信息登报公告', '信息补登公告', '信息补充公告', '信息拍卖公告', '信息公告', '信息通知',
    '联合通知书', '联合告知书', '联合通知公告', '联合登报公告', '联合补登公告', '联合补充公告', '联合拍卖公告', '联合公告', '联合通知',
    '催收通知书', '催收告知书', '催收通知公告', '催收登报公告', '催收补登公告', '催收补充公告', '催收拍卖公告', '催收公告', '催收通知',
    '催讨通知书', '催讨告知书', '催讨通知公告', '催讨登报公告', '催讨补登公告', '催讨补充公告', '催讨拍卖公告', '催讨公告', '催讨通知'
]

not_claims_keys = ['法院公告', '减资公告', '注销公告', '清算公告', '合并公告', '出让公告', '重组公告', '调查公告', '分立公告', '重整公告', '悬赏公告', '注销登记公告']

co = ChromiumOptions()
co.headless()
co.set_paths(local_port=9112)
# 构造实例
page = ChromiumPage(co)
# 获取当前年月日,格式为20240801
now = datetime.now()
date_str = now.strftime('%Y%m%d')
structure_url = f"http://epaper.legaldaily.com.cn/fzrb/content/{date_str}/"
des_url = structure_url + 'PageArticleIndexBT.htm'
# 打开网页
page.get(des_url)
if page.url != des_url:
    print("该天没有报纸")
else:
    html = etree.HTML(page.html)

    # 获取所有标题
    all_titles = html.xpath("//tbody/tr/td[2]/table[3]/tbody/tr/td[2]/a")
    # 遍历所有标题
    for title in all_titles:
        # 判断标题是否有公告等字样
        if '公告' in title.text:
            print(title.text)
            # 获取标题对应的链接
            link = title.xpath("./@href")[0]
            print(structure_url + link)
            ann_link = structure_url + link
            page.get(ann_link)
            ann_html = etree.HTML(page.html)

            # 获取pdf地址
            paper_pdf = ann_html.xpath("//tr[2]/td/table/tbody/tr/td[8]/a[@class='14']/@href")[0]
            paper_pdf = paper_pdf.strip('../../')
            paper_pdf_url = 'http://epaper.legaldaily.com.cn/fzrb/' + paper_pdf
            print(paper_pdf_url)
            file_name = paper_pdf.strip('.pdf').replace("/", "_")
            upload_pdf_by_url(paper_pdf_url, file_name=file_name)

            # 获取公告内容
            ann_contents = ann_html.xpath(
                "//span[2]/table[2]/tbody/tr/td/table[2]/tbody/tr/td//br/following-sibling::text()[1]")
            for content in ann_contents:
                print(content)
                if any(key in content for key in claims_keys):
                    print(content)
                if any(key in content for key in not_claims_keys):
                    print('---------其他公告', content, ann_contents.count(content)),
