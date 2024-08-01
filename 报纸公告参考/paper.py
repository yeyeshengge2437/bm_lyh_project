import json
import os
import re
import traceback
import cv2

import requests
from playwright.sync_api import sync_playwright
import time
import api
import log
import pytesseract
import paper_util
import settings
import xml.etree.ElementTree as ET
import datetime
import fitz
import numpy as np
from PIL import Image

# p = sync_playwright().start()
# browser = p.chromium.launch(channel="chrome", headless=False)  # 关闭无头模式，方便看到页面加载情况
p = None
browser = None

js = """
Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
"""
context = None
page = None


# 上传pdf
def upload_pdf_by_url(pdf_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    r = requests.get(pdf_url, headers=headers)
    if r.status_code != 200:
        return ""
    pdf_path = "file/paper_page.pdf"
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    fw = open(pdf_path, 'wb')
    fw.write(r.content)
    fw.close()
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}
    res = api.file_upload(upload_type='paper', files=file_data)
    fr.close()
    return res.get("file_url")


# 上传img
def upload_img_by_url(img_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    r = requests.get(img_url, headers=headers)
    if r.status_code != 200:
        return ""
    img_path = "file/paper_page.png"
    if os.path.exists(img_path):
        os.remove(img_path)
    fw = open(img_path, 'wb')
    fw.write(r.content)
    fw.close()
    fr = open(img_path, 'rb')
    file_data = {"file": fr}
    res = api.file_upload(upload_type='paper', files=file_data)
    fr.close()
    return res.get("file_url")


# 上传img
def upload_img_by_local_path(img_path):
    fr = open(img_path, 'rb')
    file_data = {"file": fr}
    res = api.file_upload(upload_type='paper', files=file_data)
    fr.close()
    os.remove(img_path)
    return res.get("file_url")


def get_url_by_xml(xml_url, day):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    r = requests.get(xml_url, headers=headers)
    if r.status_code != 200:
        return ""
    root = ET.fromstring(r.content)
    _front_page = ""
    _period_date = ""
    for child in root:
        for child1 in child:
            if child1.tag == "period_date":
                _period_date = child1.text
            elif child1.tag == "front_page":
                _front_page = child1.text
        if _period_date == day:
            break
        else:
            _front_page = ""
    return _front_page


def get_url_by_xml_2(xml_url, day):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    r = requests.get(xml_url, headers=headers)
    if r.status_code != 200:
        return ""
    root = ET.fromstring(r.content)
    _front_page = ""
    _period_date = ""
    for child in root:
        for child1 in child:
            if child1.tag == "date":
                _period_date = child1.text
            elif child1.tag == "url":
                _front_page = child1.text
        if _period_date == day:
            break
        else:
            _front_page = ""
    return _front_page


def deal_paper_list(paper_list, paper_page, page_img_list=None, queue=None):
    if paper_list is None or paper_page is None:
        return
    _res = api.paper_page_get(paper_page)
    queue_id = 0
    if queue is not None:
        queue_id = queue.get("id")
    if _res is None or _res.get("status") == "to_collect":
        paper_page["queue_id"] = queue_id
        if paper_page.get("original_pdf") is not None and paper_page.get("original_pdf") != "":
            paper_page["pdf_url"] = upload_pdf_by_url(paper_page.get("original_pdf"))
            _res = api.paper_page_add(paper_page)
        elif paper_page.get("img_url") is not None and paper_page.get("img_url") != "":
            if paper_page.get("img_url").find(".debtop.com") == -1:
                paper_page["img_url"] = upload_img_by_url(paper_page.get("img_url"))
            _res = api.paper_page_add(paper_page)
        else:
            return
    for i1 in range(len(paper_list)):
        _paper = paper_list[i1]
        _paper["queue_id"] = queue_id
        _paper["page_id"] = _res.get("id")
        _paper["paper"] = _res.get("paper")
        _paper["day"] = _res.get("day")
        api.paper_paper_add(_paper)
    if page_img_list is not None:
        for i1 in range(len(page_img_list)):
            _page_img = page_img_list[i1]
            _page_img["page_id"] = _res.get("id")
            _page_img["paper"] = _res.get("paper")
            _page_img["day"] = _res.get("day")
            api.paper_page_img_add(_page_img)


def check_page_pdf(pdf_url):
    if settings.path_tesseract is not None and settings.path_tesseract != "":
        pytesseract.pytesseract.tesseract_cmd = settings.path_tesseract
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    pdf_path = "file/paper_" + time_str + ".pdf"
    img_path = "file/paper_" + time_str + ".png"
    r = requests.get(pdf_url, headers=headers)
    f = open(pdf_path, 'wb')
    f.write(r.content)
    f.close()
    time.sleep(1)
    pdf_doc = fitz.open(pdf_path)
    pdf_page = pdf_doc[0]
    mat = fitz.Matrix(4, 4)  # 1.5表示放大1.5倍
    pix = pdf_page.get_pixmap(matrix=mat, alpha=False)
    pix.save(img_path)
    pdf_doc.close()
    os.remove(pdf_path)
    text = pytesseract.image_to_string(Image.open(img_path), lang="chi_sim", config='--psm 6')
    os.remove(img_path)
    return paper_util.check_notice2(text)


# 浙江-标题索引
def paper_zhejiang_index(current_page):
    current_page.locator("li#titlenav > a").click()
    _title_node_list = current_page.locator("body > div.main > div.title-nav-wrapper > div > div > div > ul > li > a")
    for i in range(_title_node_list.count()):
        if paper_util.title_check_notice(_title_node_list.nth(i).inner_text()):
            return True
    return False


# 浙江
def paper_zhejiang(queue, base_url, only_title=False):
    _url = None
    _year = queue.get("day")[0:4]
    _month = queue.get("day")[5:7]
    if _month.startswith("0"):
        _month = _month.replace("0", "")
    _url_1 = queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(base_url)
    time.sleep(2)
    page.locator("select#SM").select_option(_month)
    time.sleep(1)
    page.locator("select#SY").select_option(_year)
    time.sleep(1)
    _day_list = page.locator("div.main-tools-calendar").locator("form[name=\"CLD\"]").locator("tr.dataTr > td > a")
    for i in range(_day_list.count()):
        _day_href = _day_list.nth(i).get_attribute("href")
        if _day_href.find(_url_1) > 0:
            _url = paper_util.generate_url(url=page.url, href=_day_href)
            break
    if _url is None:
        return "not exist"
    page.goto(_url)
    time.sleep(1)
    if only_title:
        if paper_zhejiang_index(current_page=page):
            page.goto(_url)
            time.sleep(1)
        else:
            return None
    _page_node_list = page.locator("div.main-ednav-nav > dl")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("dt > a")
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        original_pdf = ""
        _pdfs = _page_node_list.nth(i).locator("dd").locator("img")
        for i1 in range(_pdfs.count()):
            _pdf_url = _pdfs.nth(i1).get_attribute("filepath")
            if _pdf_url.endswith("pdf"):
                original_pdf = paper_util.generate_url(url=page.url, href=_pdf_url)
                break
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("ul.main-ed-articlenav-list > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("body > div.main > div.main-ed > div.main-ed-map-weapper > div > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)
        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 浙江-浙江法治报
def paper_zhejiang_zjfzb(queue):
    _base_url = "http://zjfzb.zjol.com.cn/"
    return paper_zhejiang(queue=queue, base_url=_base_url)


# 浙江-浙江日报
def paper_zhejiang_zjrb(queue):
    _base_url = "http://zjrb.zjol.com.cn/"
    return paper_zhejiang(queue=queue, base_url=_base_url, only_title=True)


# 浙江-江南游报
def paper_zhejiang_jnyb(queue):
    _base_url = "http://jnyb.zjol.com.cn/"
    return paper_zhejiang(queue=queue, base_url=_base_url, only_title=True)


# 江苏-20年9月前
def paper_jiangsu_old(queue, base_url):
    return None


# 江苏-20年9月后
def paper_jiangsu_202009(queue, base_url, only_title=False):
    _url = None
    _year = queue.get("day")[0:4]
    _month = queue.get("day")[5:7]
    # if _month.startswith("0"):
    #     _month = _month.replace("0", "")
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)

    _page_node_list = page.locator("body > div.Newslistbox > div.Newsmain > div.newscon.clearfix > div.newsside > ul > li.oneclick1 > div > div > p")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_a_list.nth(0).get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_a_list.nth(1).get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#ScroLeft > div.newslist > ul > li > h3 > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator(
                "body > div.Newslistbox > div.Newsmain > div.newscon.clearfix > div.\\+div "
                "> div.newsconimg > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": "公告",
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 江苏-江苏经济报
def paper_jiangsu_jsjjb(queue):
    _base_url = "http://jsjjb.xhby.net/"
    if queue.get("day") >= "2020-09-01":
        return paper_jiangsu_202009(queue=queue, base_url=_base_url)
    else:
        return None


# 江苏-江南时报
def paper_jiangsu_jnsb(queue):
    _base_url = "http://jnsb.xhby.net/"
    if queue.get("day") >= "2020-09-01":
        return paper_jiangsu_202009(queue=queue, base_url=_base_url)
    else:
        return None


# 江苏-江苏法治报
def paper_jiangsu_jsfzb(queue):
    _base_url = "http://jsfzb.xhby.net/"
    if queue.get("day") >= "2020-09-01":
        return paper_jiangsu_202009(queue=queue, base_url=_base_url)
    else:
        return None


# 江苏-新华日报
def paper_jiangsu_xhrb(queue):
    _base_url = "http://xh.xhby.net/"
    if queue.get("day") >= "2020-09-01":
        return paper_jiangsu_202009(queue=queue, base_url=_base_url)
    else:
        return None


# 江苏-江苏商报
def paper_jiangsu_jssb(queue):
    base_url = "http://jssb.njdaily.cn/"
    _url = None
    only_title = False
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("#catalog > ul > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = ""
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(
            url=page.url, href=page.locator("#downpdfLink > li > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#listBox > ul> li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("#MapLeave > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#articleContent").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 上海-文汇报
def paper_shanghai_whb(queue):
    base_url = "http://dzb.whb.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + queue.get("day") + "/1/index.html"
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("#spaceBox > div")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        _page_node = _a_list.nth(0)
        _pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_a_list.nth(0).get_attribute("data-href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_a_list.nth(1).get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > div > div > div.centerBox > div.center_right > div.navigation_title "
                                   "> div.title_box.list > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map#newspaper > span")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("data-href"))
                _title = _node.get_attribute("data-title")
                if _title is None or _title == "":
                    _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#newsContent").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 上海-青年报
def paper_shanghai_qnb(queue):
    base_url = "http://www.why.com.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "epaper/webpc/qnb/html/" + queue.get("day")[0:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "epaper/webpc/qnb/html/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("#table64 > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _page_pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_page_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#table61 > tbody > tr > td > table > tbody > tr > td > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("#bmt > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 北京-劳动午报
def paper_beijing_ldwb(queue):
    base_url = "http://ldwb.workerbj.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "content/" + queue.get("day")[0:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "content/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("body > table > tbody > tr:nth-child(1) > td:nth-child(2) > table:nth-child(2) "
                                   "> tbody > tr > td:nth-child(1) > table:nth-child(4) > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _page_pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_page_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > table > tbody > tr:nth-child(1) > td:nth-child(1) > table > tbody "
                                   "> tr > td > table:nth-child(3) > tbody > tr > td:nth-child(2) > table "
                                   "> tbody > tr > td > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"pagepicmap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 天津-天津日报
def paper_tianjin_tjrb(queue):
    base_url = "http://epaper.tianjinwe.com/tjrb/"
    _url = None
    only_title = True
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("body > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2) "
                                   "> table:nth-child(2) > tbody > tr > td:nth-child(1) > table:nth-child(2) "
                                   "> tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > table "
                                   "> tbody > tr.bmdh_tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _page_pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_page_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main-ed-articlenav-list > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("#main-ed-map > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            if paper_util.may_notice_by_title(_title):
                good_page = True
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or good_page or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 重庆-重庆日报
def paper_chongqing_cqrb(queue):
    base_url = "https://epaper.cqrb.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/"
    _url = base_url + "cqrb/" + queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/001/node.htm"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > table > tbody > tr:nth-child(1) > td:nth-child(2) > table:nth-child(2) "
                                   "> tbody > tr > td:nth-child(1) > table:nth-child(3) > tbody > tr > td > div "
                                   "> table > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _page_pdf_node = _a_list.nth(1)
        if _page_node.is_hidden():
            continue
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_page_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > table > tbody > tr:nth-child(1) > td:nth-child(1) > table > tbody "
                                   "> tr:nth-child(2) > td > table > tbody > tr > td > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 重庆-重庆商报
def paper_chongqing_cqsb(queue):
    base_url = "https://e.chinacqsb.com/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "html/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "html/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#allBody > div.Newslistbox > div.Newsmain > div.newscon.clearfix "
                                   "> div.newsside > ul > li.oneclick1 > div > div > p")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _page_pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_page_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#ScroLeft > div.newslist > ul > li > h3 > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            if paper_util.may_notice_by_title(_title):
                good_page = True
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("#ScroLeft > div.newsdetatext > founder-content").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or good_page or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 重庆-重庆法治报
def paper_chongqing_cqfzb(queue):
    base_url = "https://szb.cqfzb.net/"
    _url = None
    only_title = False
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#bmdhTable > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _page_pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_page_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main-ed-articlenav-list > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("#main-ed-map > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            if paper_util.may_notice_by_title(_title):
                good_page = True
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or good_page or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 安徽-安徽商报
def paper_anhui_ahsb(queue):
    base_url = "https://ahsbszb.ahnews.com.cn/"
    first_url = "https://ahsbszb.ahnews.com.cn/pc/layout/index.html"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#layoutlist > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = ""
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(url=page.url, href=page.locator("p#pdfUrl").inner_text())
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#articlelist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            if paper_util.may_notice_by_title(_title):
                good_page = True
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or good_page or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 安徽-安徽法治报
def paper_anhui_ahfzb(queue):
    base_url = "https://szb.ahnews.com.cn/fzb/"
    first_url = "https://szb.ahnews.com.cn/fzb/pc/layout/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > div.Newslistbox > div.Newsmain > div.newscon.clearfix "
                                   "> div.newsside > ul > li.oneclick1 > div > div > p")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _page_pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_page_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#ScroLeft > div.newslist > ul > li> h3 > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("#ScroLeft > div.newsdetatext > div > founder-content").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 福建-福建
def paper_fujian(queue, base_url, all_page=False):
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/col/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/col/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#bmdhTable > tbody > tr > td > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = ""
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(
            url=page.url, href=page.locator("#mainBox > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(2) "
                                            "> td > table > tbody > tr > td:nth-child(1) > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main-ed-articlenav-list > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("#main-ed-map > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or all_page or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 福建-福建日报
def paper_fujian_fjrb(queue):
    base_url = "https://fjrb.fjdaily.com/"
    return paper_fujian(queue=queue, base_url=base_url)


# 福建-海峡都市报
def paper_fujian_hxdsb(queue):
    base_url = "https://hxdsb.fjdaily.com/"
    return paper_fujian(queue=queue, base_url=base_url, all_page=True)


# 广东-南方日报-1
def paper_guangdong_nfrb(queue):
    base_url = "https://epaper.southcn.com/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "nfdaily/html/" + _url_1 + "node_A01.html"
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#mCSB_4 > div.mCSB_container > h3 > a")
    if _page_node_list.count() < 1:
        return "not exist"
    _title_list_list = page.locator("#mCSB_4 > div.mCSB_container > ul")

    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _title_list = _title_list_list.nth(i).locator("a")
        _paper_list = []
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            _paper_list.append({
                "title": _title,
                "content_url": _content_url,
            })
        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content_node = page1.locator("#content")
            _content = ""
            if _content_node.count() > 0:
                _content = _content_node.nth(0).inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)
        if len(_paper_list_1) < 1:
            continue
        page1.goto(_page_href)
        time.sleep(1)
        _paper_page["img_url"] = paper_util.generate_url(url=page1.url, href=page1.locator("#picMap > img")
                                                         .get_attribute("src").replace(".jpg.1", ".jpg"))
        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 广东-南方日报-2
def paper_guangdong_nfrb2(queue):
    _url = "https://epaper.southcn.com/app_if/getPaperLayouts?id=1&date=" \
           + queue.get("day")[0:4] + queue.get("day")[5:7] + queue.get("day")[8:10]
    r = requests.get(_url)
    if r.status_code != 200:
        return "not exist"
    result = r.json()
    _page_list = result["layouts"]
    if _page_list is None or len(_page_list) < 1:
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    for i in range(len(_page_list)):
        _page_item = _page_list[i]
        _notice_list = _page_item.get("list")
        if _notice_list is None or len(_notice_list) < 1:
            continue
        _paper_list_1 = []
        for i1 in range(len(_notice_list)):
            _notice_item = _notice_list[i1]
            _title = paper_util.remove_empty(_notice_item.get("title").replace("<p>", "").replace("</p>", ""))
            if _title == "":
                _title = "公告"
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            _content_url = _notice_item.get("shareUrl").replace("/m/ipaper/nfrb", "/nfdaily")
            page.goto(_content_url)
            time.sleep(1)
            _content_node = page.locator("#content")
            _content = ""
            if _content_node.count() > 0:
                _content = _content_node.nth(0).inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper = {
                "title": _title,
                "content_url": _content_url,
                "content": _content
            }
            _paper_list_1.append(_paper)

        _paper_page = {
            "name": paper_util.remove_empty(_page_item.get("name")),
            "page_url": _page_item.get("url"),
            "original_pdf": _page_item.get("pdfUrl").replace("/m/ipaper/nfrb", "/nfdaily"),
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page.close()
    return None


# 广东-羊城晚报、羊晚区域版
def paper_guangdong_yc(queue, base_url):
    _url = None
    only_title = False
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > div > div > div.shortcutbox > ul > li > div > ul > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = ""
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(
            url=page.url, href=page.locator("#downpdfLink > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#list > div.main-list > ul > li > h2 > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"newbook\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            if paper_util.may_notice_by_title(_title):
                good_page = True
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("#list > div > div.text").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or good_page or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 广东-羊城晚报
def paper_guangdong_ycwb(queue):
    base_url = "http://ep.ycwb.com/epaper/ycwb/"
    return paper_guangdong_yc(queue=queue, base_url=base_url)


# 广东-羊晚区域版
def paper_guangdong_ywqy(queue):
    base_url = "http://ep.ycwb.com/epaper/ywdf/"
    return paper_guangdong_yc(queue=queue, base_url=base_url)


# 广西-广西日报
def paper_guangxi_gxrb(queue):
    base_url = "https://gxrb.gxrb.com.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:10]
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "?name=gxrb&date=" + _url_1
    page.goto(_url)
    time.sleep(5)
    _page_node_list = page.locator("#banmian > ul > li > a")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = base_url + "?name=gxrb&date=" + _url_1 + "&code=" + re.search("第(\\d+)版", _page_name).group(1)
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(5)
        _paper_list = []
        _content_url_list = []
        _paper_page["original_pdf"] = paper_util.generate_url(
            url=page.url, href=page.locator("a#pptf").get_attribute("href"))
        _title_list = page.locator("#right_news1 > table > tbody > tr")
        if _title_list.count() < 1:
            return "no title"
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _title_num = _node.get_attribute("data-xuhao")
            if _title_num is None:
                continue
            _content_url = _page_href + "&xuhao=" + _title_num
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _page_num = re.search("第(\\d+)版", _paper_page.get("name")).group(1)
            _content_list = page.locator("map#map-" + _page_num).locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _title_num = _node.get_attribute("data-xuhao")
                if _title_num is None:
                    continue
                _content_url = _page_href + "&xuhao=" + _title_num
                _title = _node.get_attribute("title")
                if _title is None:
                    _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(5)
            _content = page1.locator("#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 云南-云南经济日报
def paper_yunnan_ynjjrb(queue):
    base_url = "https://jjrbpaper.yunnan.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#bmdhTable > tbody > tr > td > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(url=page.url, href=page.locator(
            "#mainBox > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(2) > td > table "
            "> tbody > tr > td:nth-child(1) > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main-ed-articlenav-list > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 四川-四川日报
def paper_sichuan_scrb(queue):
    base_url = "https://epaper.scdaily.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "shtml/scrb/" + _url_1 + "index.shtml"
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#main > div.main_r > ul:nth-child(2) > li > p > a")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["img_url"] = paper_util.generate_url(
            url=page.url,
            href=page.locator("#main > div.main_l > ul > li:nth-child(1) > map "
                              "> area:nth-child(1)").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main > div.main_r > ul:nth-child(3) > li:nth-child(2) > p > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("#main > div.main_l > ul > li:nth-child(2) > a.selectBox")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content_node = page1.locator("#main2 > div.main2_r > ul > li:nth-child(2) > p:nth-child(3) > font")
            _content = ""
            if _content_node.count() > 0:
                _content = _content_node.nth(0).inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 四川-四川法治报
def paper_sichuan_scfzb(queue):
    base_url = "https://dzb.scfzbs.com/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "shtml/scfzb/" + _url_1 + "index.shtml"
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#scrollDiv > ul > li > a")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["img_url"] = paper_util.generate_url(
            url=page.url,
            href=page.locator("img#imgPage").get_attribute("src").replace("b_", "", 1))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("dl.Rcon > dd > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("div.border-grey.content > div.lefta_left > div.lefta_left > a")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content_node = page1.locator("#DivDisplay > div.f-14.height-25 > p")
            _content = ""
            if _content_node.count() > 0:
                _content = _content_node.nth(0).inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 湖南
def paper_hunan(queue, base_url):
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "html/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > table > tbody > tr:nth-child(1) > td:nth-child(2) > table:nth-child(2) "
                                   "> tbody > tr > td:nth-child(1) > table:nth-child(2) > tbody > tr > td > table "
                                   "> tbody > tr:nth-child(2) > td > div > table > tbody > tr")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > table > tbody > tr:nth-child(1) > td:nth-child(1) > table > tbody "
                                   "> tr:nth-child(1) > td > table:nth-child(3) > tbody > tr > td:nth-child(2) "
                                   "> table > tbody > tr:nth-child(4) > td > div > ul > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 湖南-湖南日报
def paper_hunan_hnrb(queue):
    base_url = "https://epaper.voc.com.cn/hnrb/"
    return paper_hunan(queue=queue, base_url=base_url)


# 湖南-三湘都市报
def paper_hunan_sxdsb(queue):
    base_url = "https://epaper.voc.com.cn/sxdsb/"
    return paper_hunan(queue=queue, base_url=base_url)


# 湖北
def paper_hubei(queue, base_url):
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/column/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/column/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > div.container > div.center.clearfix > div:nth-child(4) > div.row.mt40 "
                                   "> div.col-md-5 > div > ul > li > a")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(url=page.url, href=page.locator("p#pdfUrl").inner_text())
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > div.container > div.center.clearfix > div:nth-child(4) > div.row.mt40 "
                                   "> div.col-md-7 > div > div.news-list > ul > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            if paper_util.may_notice_by_title(_title):
                good_page = True
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or good_page or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 湖北-楚天都市报
def paper_hubei_ctdsb(queue):
    base_url = "https://ctdsbepaper.hubeidaily.net/"
    return paper_hubei(queue=queue, base_url=base_url)


# 湖北-湖北日报
def paper_hubei_hbrb(queue):
    base_url = "https://epaper.hubeidaily.net/"
    return paper_hubei(queue=queue, base_url=base_url)


# 湖北-三峡晚报
def paper_hubei_sxwb(queue):
    base_url = "https://sxwbepaper.hubeidaily.net/"
    return paper_hubei(queue=queue, base_url=base_url)


# 江西-江西日报
def paper_jiangxi_jxrb(queue):
    base_url = "http://epaper.jxxw.com.cn/"
    _url = None
    only_title = False
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("#bmdhTable > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _node_list = _page_node_list.nth(i).locator("a")
        _page_node = _node_list.nth(0)
        _pdf_node = _node_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main-ed-articlenav-list > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"pagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 江西-新法治报
def paper_jiangxi_xfzb(queue):
    base_url = "https://epaper.jxnews.com.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + "/" + queue.get("day")[5:7] + "/" + queue.get("day")[5:10] + "/"
    _url = base_url + "szpt/" + _url_1 + "xfz/1.jpg"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    r = requests.get(_url, headers=headers)
    if r.status_code != 200 or r.url != _url:
        return "not exist"
    for i in range(50):
        time.sleep(0.5)
        _img_url = base_url + "szpt/" + _url_1 + "xfz/" + str(i + 1) + ".jpg"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        r = requests.get(_img_url, headers=headers)
        if r.status_code != 200 or r.url != _img_url:
            break
        _paper_page = {
            "name": str(i + 1) + "版",
            "img_url": _img_url,
            "page_url": _img_url,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }

        deal_paper_list(paper_list=[], paper_page=_paper_page, queue=queue)

    return None


# 海南-海南日报
def paper_hainan_hnrb(queue):
    base_url = "http://hnrb.hinews.cn/"
    _url = None
    only_title = False
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("#bmdhTable > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _node_list = _page_node_list.nth(i).locator("a")
        _page_node = _node_list.nth(0)
        _pdf_node = _node_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main-ed-articlenav-list > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"pagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 河北-河北法制报
def paper_hebei_hbfzb(queue):
    base_url = "https://szbz.hbfzb.com/hbfzbpaper/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("ul#layoutlist > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node_list.nth(i).get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        # _paper_page["original_pdf"] = paper_util.generate_url(
        #     url=page.url, href=page.locator("body > div.wrap > div.content.clearfix > div.newspaper-pic.pull-left "
        #                                     "> div > div:nth-child(1) > a").get_attribute("href"))
        _paper_page["original_pdf"] = paper_util.generate_url(url=page.url, href=page.locator("p#pdfUrl").inner_text())

        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("ul#articlelist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"pagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 河北-河北经济日报
def paper_hebei_hbjjrb(queue):
    base_url = "http://epaper.hbjjrb.com/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("ul#layoutlist > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node_list.nth(i).get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        # _paper_page["original_pdf"] = paper_util.generate_url(
        #     url=page.url, href=page.locator("body > div.wrap > div.content.clearfix > div.newspaper-pic.pull-left "
        #                                     "> div > div:nth-child(1) > a").get_attribute("href"))
        _paper_page["original_pdf"] = paper_util.generate_url(url=page.url, href=page.locator("p#pdfUrl").inner_text())
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("ul#articlelist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"pagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 山东-山东法制报
def paper_shandong_sdfzb(queue):
    base_url = "https://paper.dzwww.com/sdfzb/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    xml_url = base_url + "data/" + _url_1 + "xml/list.xml"
    r = requests.get(xml_url)
    if r.status_code != 200:
        return "not exist"
    root = ET.fromstring(r.content)
    _front_page = ""
    _period_date = ""
    _page_pdf_map = {}
    for child in root:
        _page_num = ""
        _page_pdf = ""
        for child1 in child:
            if child1.tag == "PAGENUMBER":
                _page_num = child1.text
            elif child1.tag == "PDF":
                _page_pdf = child1.text
        if _page_num != "" and _page_pdf != "":
            _page_pdf_map[_page_num] = base_url + "data/" + _page_pdf.replace("./", "")
    _url = base_url + "data/" + _url_1 + "html/1/partindex.html"
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#banlist > li")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        original_pdf = _page_pdf_map.get(_page_node.get_attribute("href")
                                         .replace("/partindex.html", "").replace("../", ""))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        # _paper_page["original_pdf"] = "https://paper.dzwww.com/pdf.html?name=" + page.locator("#pdfimage > img")\
        #     .get_attribute("onclick").replace("javascript:viewpdf('", "")\
        #     .replace("');", "").replace("','", "&issue=", 1).replace("','", "&num=", 1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#newslist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"pagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#content").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 山东-齐鲁晚报
def paper_shandong_qlwb(queue):
    base_url = "https://epaper.qlwb.com.cn/qlwb/content/"
    _url = None
    # only_title = False
    # _year = queue.get("day")[0:4] + "年"
    # _month = queue.get("day")[5:7] + "月"
    # if _month.startswith("0"):
    #     _month = _month.replace("0", "", 1)
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    # page.goto(base_url)
    # time.sleep(2)
    # page.locator("select#sMonth").select_option(label=_month)
    # time.sleep(1)
    # page.locator("select#sYear").select_option(label=_year)
    # time.sleep(1)
    # _day_list = page.locator("#calendar > table > tbody > tr > td > a")
    # for i in range(_day_list.count()):
    #     _day_href = _day_list.nth(i).get_attribute("href")
    #     if _day_href.find(_url_1) > 0:
    #         _url = paper_util.generate_url(url=page.url, href=_day_href)
    #         break
    # if _url is None:
    #     return "not exist"
    _url = base_url + _url_1 + "PageArticleIndexLB.htm"
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("body > div.listdaohang > div")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.locator("h4").inner_text())
        original_pdf = paper_util.generate_url(url=page.url,
                                               href=_page_node.locator("h4").locator("a.pdf").get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": original_pdf,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
    #     _paper_page_list.append(_paper_page)
    #
    # for i in range(len(_paper_page_list)):
    #     _paper_page = _paper_page_list[i]
    #     _page_href = _paper_page.get("page_url")
    #     page.goto(_page_href)
    #     time.sleep(1)
        # _paper_page["name"] = page.locator("#table5 > tbody > tr > td:nth-child(1)").inner_text()
        # _paper_page["original_pdf"] = paper_util.generate_url(
        #     url=page.url, href=page.locator("#table5 > tbody > tr > td:nth-child(3) > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = _page_node.locator("ul").locator("li").locator("a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = base_url + _url_1 + _node.get_attribute("daoxiang")
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#contenttext").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 山东-经济导报
def paper_shandong_jjdb(queue):
    base_url = "http://jjdb.sdenews.com/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "jjdb/jjdb/content/" + _url_1 + "Page01NU.htm"
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#banlist > li")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(
            url=page.url,
            href=page.locator("#pdfimage > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#newslist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("div#mylink > a")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#content").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 山西-山西经济日报
def paper_shanxi_sxjjrb(queue):
    base_url = "http://www.sxjjb.cn/"
    _url = None
    only_title = True
    _url_1 = queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "szb/html/" + queue.get("day")[0:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "szb/html/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2) "
                                   "> table:nth-child(2) > tbody > tr > td:nth-child(1) > table:nth-child(2) "
                                   "> tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > table > tbody "
                                   "> tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "original_pdf": _original_pdf,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2) "
                                   "> table:nth-child(2) > tbody > tr > td:nth-child(1) > table:nth-child(2) "
                                   "> tbody > tr > td > table > tbody > tr:nth-child(3) > td > table "
                                   "> tbody > tr:nth-child(4) > td > div > table > tbody > tr > td > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        _good_page = _paper_page.get("name").find("公告") >= 0
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if _good_page or len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 陕西-陕西日报(待完善)
def paper_shaanxi_sxrb(queue):
    base_url = "https://esb.sxdaily.com.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("body > div.main > div.wrap > div.right > div:nth-child(3) > div.bmml "
                                   "> div.bmml_con > div.bmml_con_div > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["img_url"] = paper_util.generate_url(
            url=page.url, href=page.locator("img#bantu_img").get_attribute("src").replace("jpg.2","jpg"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > div.main > div.wrap > div.right > div:nth-child(3) "
                                   "> div.bmdh > div.bmdh_con > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            good_page = True
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#zoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if good_page or len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 陕西-西部法制报
def paper_shaanxi_xbfzb(queue):
    base_url = "http://esb.xbfzb.com/"
    _url = None
    only_title = False
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("#breakNewsList1 > div")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "original_pdf": _original_pdf,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#breakNewsList > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"Map\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#zoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 甘肃
def paper_gansu(queue, base_url, only_title=False):
    _url = None
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)

    _page_node_list = page.locator("body > div.Newslistbox > div.Newsmain > div.newscon.clearfix > div.newsside > ul > li.oneclick1 > div > div > p")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_a_list.nth(0).get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_a_list.nth(1).get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#ScroLeft > div.newslist > ul > li > h3 > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator(
                "body > div.Newslistbox > div.Newsmain > div.newscon.clearfix > div.\\+div "
                "> div.newsconimg > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": "公告",
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 青海-青海日报
def paper_qinghai_qhrb(queue):
    base_url = "https://epaper.tibet3.com/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "qhrb/html/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "qhrb/html/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > div > div.main-body > div.epaper > div > div.epaper-content.fr "
                                   "> div.content.cf > div.w4.fr > nav > ul > li.nav-item > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _pdf_url = ""
        _pdf_node_list = page.locator("body > div > div.main-body > div.epaper > div > div.epaper-body.fl "
                     "> div.epaper-map > div.epaper-meta > a")
        for i1 in range(_pdf_node_list.count()):
            _pdf_url_1 = _pdf_node_list.nth(i1).get_attribute("href")
            if _pdf_url_1 is not None and _pdf_url_1.endswith(".pdf"):
                _pdf_url = _pdf_url_1
                break
        if _pdf_url != "":
            _paper_page["original_pdf"] = paper_util.generate_url(
                url=page.url, href=_pdf_url)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > div > div.main-body > div.epaper > div > div.epaper-content.fr "
                                   "> div.content.cf > div.w8.fl > div > ul > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("body > div > div.main-body > div.epaper > div > div.epaper-content.fr "
                                     "> div.content.cf > article > div").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 辽宁-辽宁日报
def paper_liaoning_lnrb(queue):
    base_url = "https://epaper.lnd.com.cn/lnrbepaper/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#allBody > div > div.Newsmain > div.newscon.clearfix > div.newsside > ul "
                                   "> li.oneclick1 > div > div > p")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))

        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "original_pdf": _original_pdf,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#ScroLeft > div.newslist > ul > li > h3 > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            if _title == "公告" or _title == "分类信息专栏":
                good_page = True
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("#ScroLeft > div.newsdetatext > founder-content").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if good_page or len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 吉林-吉林日报
def paper_jilin_jlrb(queue):
    base_url = "http://jlrbszb.dajilin.com/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/paper/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/paper/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#layoutlist > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(url=page.url, href=page.locator(
            "body > div.wrap > div.content.clearfix > div.newspaper-pic.pull-left > div > div.pull-right > a"
        ).get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#articlelist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 吉林-城市晚报
def paper_jilin_cswb(queue):
    base_url = "http://www.cswbszb.com/cswb/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/paper/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/paper/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#layoutlist > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(url=page.url, href=page.locator(
            "body > div.wrap > div.content.clearfix > div.newspaper-pic.pull-left > div > div.pull-right > a"
        ).get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#articlelist > li > a")
        print(_title_list.count())
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        good_page = False
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if paper_util.may_notice_by_title(_title):
                good_page = True
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if good_page or len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 黑龙江-黑龙江日报
def paper_heilongjiang_hljrb(queue):
    base_url = "http://epaper.hljnews.cn/hljrb/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#allBody > div > div.Newsmain > div.newscon.clearfix > div.newsside > ul "
                                   "> li.oneclick1 > div > div > p")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))

        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "original_pdf": _original_pdf,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#ScroLeft > div.newslist > ul > li > h3 > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("#ScroLeft > div.newsdetatext > founder-content").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 内蒙古-内蒙古日报
def paper_neimenggu_nmgrb(queue):
    base_url = "http://szb.northnews.cn/nmgrb/"
    _url = None
    only_title = False
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#bmdhTable > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "original_pdf": _original_pdf,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main-ed-articlenav-list > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 内蒙古-内蒙古晨报
def paper_neimenggu_nmgcb(queue):
    base_url = "http://szb.nmgcb.com.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/"
    _url = base_url + "html/" + _url_1 + "node_2.htm"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator(
        "body > table > tbody > tr:nth-child(1) > td:nth-child(2) > table:nth-child(2) > tbody > tr > td:nth-child(1) "
        "> table:nth-child(2) > tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > table > tbody > tr")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        if _page_node_list.nth(i).locator("a").count() < 2:
            continue
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        if _page_name.find("财富") < 0:
            continue
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "original_pdf": _original_pdf,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator(
            "body > table > tbody > tr:nth-child(1) > td:nth-child(1) > table > tbody > tr > td > table:nth-child(3) "
            "> tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td > div > table > tbody > tr > td > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 内蒙古-内蒙古法制报
def paper_neimenggu_nmgfzb(queue):
    base_url = "http://www.nmgfzb.cn/xpaper/"
    _url = None
    only_title = False
    _year = queue.get("day")[0:4]
    _month = queue.get("day")[5:7]
    if _month.startswith("0"):
        _month = _month.replace("0", "", 1)
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(base_url)
    time.sleep(2)
    page.locator("select#SM").select_option(label=_month)
    time.sleep(1)
    page.locator("select#SY").select_option(label=_year)
    time.sleep(1)
    _day_list = page.locator("#rili > table > tbody > tr > td > a")
    _day = queue.get("day")[8:10]
    if _day.startswith("0"):
        _day = _day.replace("0", "", 1)
    for i in range(_day_list.count()):
        _day_href = _day_list.nth(i).get_attribute("href")
        if _day_list.nth(i).inner_text() == _day:
            _url = paper_util.generate_url(url=page.url, href=_day_href)
            break
    if _url is None:
        return "not exist"
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator(
        "body > center > table:nth-child(1) > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(2) "
        "> table > tbody > tr:nth-child(3) > td > table > tbody > tr > td:nth-child(1) > table:nth-child(1) "
        "> tbody > tr > td > table:nth-child(2) > tbody > tr > td > div > table > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": _original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > center > table:nth-child(1) > tbody > tr > td > table:nth-child(2) "
                                   "> tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(3) > td "
                                   "> table > tbody > tr > td:nth-child(1) > table:nth-child(2) > tbody > tr "
                                   "> td > div > table > tbody > tr > td > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _check_title = _title.endswith("…")
            _notice = paper_util.title_check_notice(_title)
            if (not _check_title) and (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue

            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            if _check_title:
                _title = paper_util.remove_empty(page1.locator(
                    "body > center > table:nth-child(1) > tbody > tr > td > table:nth-child(2) > tbody > tr "
                    "> td:nth-child(2) > table > tbody > tr:nth-child(4) > td > table:nth-child(1) > tbody > tr "
                    "> td > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(2) > td > h2"
                ).inner_text())
                _paper["title"] = _title
                _notice = paper_util.title_check_notice(_title)
                if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                    continue
            _content = page1.locator("body > center > table:nth-child(1) > tbody > tr > td > table:nth-child(2) "
                                     "> tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(4) > td "
                                     "> table:nth-child(1) > tbody > tr > td > table > tbody > tr:nth-child(4) "
                                     "> td > table > tbody > tr > td > div > table > tbody > tr > td > table > tbody "
                                     "> tr:nth-child(1) > td > div").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 内蒙古-北方新报
def paper_neimenggu_bfxb(queue):
    base_url = "http://szb.northnews.cn/bfxb/"
    _url = None
    only_title = False
    _xml_url = base_url + "html/" + queue.get("day")[0:7] + "/navi.xml"
    _front_page = get_url_by_xml_2(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    _url = base_url + "html/" + queue.get("day")[0:7] + "/" + _front_page.replace("../", "")
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("#bmdhTable > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _pdf_node = _page_node_list.nth(i).locator("a").nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_pdf_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "original_pdf": _original_pdf,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#main-ed-articlenav-list > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 宁夏
def paper_ningxia(queue, base_url):
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > div.container > div.center.clearfix > div:nth-child(4) > div.row.mt40 "
                                   "> div.col-md-5 > div > ul > li")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i).locator("a").nth(0)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(url=page.url, href=page.locator("#pdfUrl").inner_text())
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > div.container > div.center.clearfix > div:nth-child(4) > div.row.mt40 "
                                   "> div.col-md-7 > div > div.news-list > ul > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 宁夏-宁夏日报
def paper_ningxia_nxrb(queue):
    base_url = "https://szb.nxrb.cn/nxrb/"
    return paper_ningxia(queue=queue, base_url=base_url)


# 宁夏-宁夏法治报
def paper_ningxia_nxfzb(queue):
    base_url = "https://szb.nxrb.cn/nxfzb/"
    return paper_ningxia(queue=queue, base_url=base_url)


# 全国-经济日报
def paper_china_jjrb(queue):
    base_url = "http://paper.ce.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("ul#layoutlist > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node_list.nth(i).get_attribute("href"))
        _original_pdf = paper_util.generate_url(url=page.url, href=_page_node_list.nth(i).locator("a")
                                               .get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": _original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("ul#articlelist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("body > div.content > div.wrap > div.clearfix "
                                         "> div.newspaper-pic.pull-left > map > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 全国-法治日报
def paper_china_fzrb(queue):
    base_url = "http://epaper.legaldaily.com.cn/fzrb/content/PaperIndex.htm"
    first_url = "http://epaper.legaldaily.com.cn/fzrb/content/PaperIndex.htm"
    _url = None
    only_title = False
    _year = queue.get("day")[0:4] + "年"
    _month = queue.get("day")[5:7] + "月"
    if _month.startswith("0"):
        _month = _month.replace("0", "", 1)
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(first_url)
    time.sleep(2)
    page.locator("select#sMonth").select_option(label=_month)
    time.sleep(1)
    page.locator("select#sYear").select_option(label=_year)
    time.sleep(1)
    _day_list = page.locator("#calendar > table > tbody > tr > td > a")
    for i in range(_day_list.count()):
        _day_href = _day_list.nth(i).get_attribute("href")
        if _day_href.find(_url_1) > 0:
            _url = paper_util.generate_url(url=page.url, href=_day_href)
            break
    if _url is None:
        return "not exist"
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("body > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) "
                                   "> table:nth-child(3) > tbody > tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        _page_node = _a_list.nth(0)
        _pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_a_list.nth(0).get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_a_list.nth(1).get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        # _paper_page["name"] = page.locator("#table5 > tbody > tr > td:nth-child(1)").inner_text()
        # _paper_page["original_pdf"] = paper_util.generate_url(
        #     url=page.url, href=page.locator("#table5 > tbody > tr > td:nth-child(3) > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) "
                                   "> table:nth-child(5) > tbody > tr > td > a.atitle")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("#mylink > a")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("span#oldcontenttext").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        if len(_paper_list_1) > 0 or _paper_page.get("page_url") == queue.get("page_url"):
            deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 全国-中国商报
def paper_china_zgsb(queue):
    base_url = "https://timg.zgswcn.com/zgsb/html/"
    first_url = "https://timg.zgswcn.com/zgsb/html/2023-01/03/node_2.htm"
    _url = None
    only_title = False
    _year = queue.get("day")[0:4]
    _month = queue.get("day")[5:7]
    _url_1 = queue.get("day")[0:7] + "/" + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(first_url)
    time.sleep(2)

    _xml_url = base_url + queue.get("day")[0:7] + "/period.xml"
    r = requests.get(_xml_url)
    if r.status_code != 200:
        return "not exist"
    root = ET.fromstring(r.content)
    _front_page = ""
    _period_date = ""
    for child in root:
        for child1 in child:
            if child1.tag == "period_date":
                _period_date = child1.text
            # elif child1.tag == "front_page":
            #     _front_page = child1.text
        if _period_date == queue.get("day"):
            _url = base_url + _url_1 + "node_2.htm"
            break
    if _url is None:
        return "not exist"
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("body > table > tbody > tr:nth-child(1) > td:nth-child(3) > table > tbody "
                                   "> tr:nth-child(4) > td > table > tbody > tr:nth-child(2) > td:nth-child(1) "
                                   "> table > tbody > tr > td > table:nth-child(2) > tbody > tr > td > table > tbody "
                                   "> tr")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _a_list = _page_node_list.nth(i).locator("a")
        if _a_list.count() < 2:
            continue
        _page_node = _a_list.nth(0)
        _pdf_node = _a_list.nth(1)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_a_list.nth(0).get_attribute("href"))
        original_pdf = paper_util.generate_url(url=page.url, href=_a_list.nth(1).get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("body > table > tbody > tr:nth-child(1) > td:nth-child(2) > table:nth-child(2) "
                                   "> tbody > tr:nth-child(5) > td > table > tbody > tr:nth-child(2) > td > table "
                                   "> tbody > tr > td > table > tbody > tr > td:nth-child(2) > a.blue1")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"pagepicmap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 全国-中华工商时报
def paper_china_zhgssb(queue):
    base_url = "http://epaper.cbt.com.cn/"
    _url = None
    only_title = False
    _url_1 = queue.get("day")[0:4] + "/" + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "epaper/uniflows/html/" + _url_1 + "boardurl.htm"
    page.goto(_url)
    time.sleep(2)
    _page_node_list = page.locator("body > table > tbody > tr > td > table > tbody > tr > td > a")
    if _page_node_list.count() < 1:
        return "not exist"
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node.get_attribute("href"))
        _paper_page = {
            "name": _page_name,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["img_url"] = _page_href.replace("default.htm", "images/back.jpg")
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#mybody > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(3) > td "
                                   "> table > tbody > tr:nth-child(2) > td.a_link.titles > table > tbody "
                                   "> tr > td > table > tbody > tr > td > div > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if _title == "":
                _title = "公告"
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map#pagepicmap > area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content_node = page1.locator("#pgcontent")
            _content = ""
            if _content_node.count() > 0:
                _content = _content_node.nth(0).inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 全国-国际商报
def paper_china_gjsb(queue):
    base_url = "https://epa.comnews.cn/"
    _url = None
    only_title = False
    _year = queue.get("day")[0:4]
    _month = queue.get("day")[5:7]
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("#layoutlist > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node_list.nth(i).get_attribute("href"))
        original_pdf = ""
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(
            url=page.url, href=page.locator("#layoutlist > li > a > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#articlelist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 全国-中国县域经济报
def paper_china_zgxyjjb(queue):
    base_url = "https://www.xyshjj.cn/newspaper/"
    _url = None
    only_title = False
    _year = queue.get("day")[0:4]
    _month = queue.get("day")[5:7]
    _url_1 = queue.get("day")[0:4] + queue.get("day")[5:7] + "/" + queue.get("day")[8:10] + "/"
    _xml_url = base_url + "pc/layout/" + queue.get("day")[0:4] + queue.get("day")[5:7] + "/period.xml"
    _front_page = get_url_by_xml(xml_url=_xml_url, day=queue.get("day"))
    if _front_page == "":
        return "not exist"
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    _url = base_url + "pc/layout/" + _url_1 + _front_page
    page.goto(_url)
    time.sleep(1)
    _page_node_list = page.locator("#layoutlist > li > a")
    _page_url_list = []
    _paper_page_list = []
    page1 = context.new_page()
    for i in range(_page_node_list.count()):
        _page_node = _page_node_list.nth(i)
        _page_name = paper_util.remove_empty(_page_node.inner_text())
        _page_href = paper_util.generate_url(url=page.url, href=_page_node_list.nth(i).get_attribute("href"))
        original_pdf = ""
        _paper_page = {
            "name": _page_name,
            "original_pdf": original_pdf,
            "page_url": _page_href,
            "day": queue.get("day"),
            "paper": queue.get("name"),
        }
        _paper_page_list.append(_paper_page)

    for i in range(len(_paper_page_list)):
        _paper_page = _paper_page_list[i]
        _page_href = _paper_page.get("page_url")
        page.goto(_page_href)
        time.sleep(1)
        _paper_page["original_pdf"] = paper_util.generate_url(
            url=page.url, href=page.locator("#layoutlist > li > a > a").get_attribute("href"))
        _paper_list = []
        _content_url_list = []
        _title_list = page.locator("#articlelist > li > a")
        for i1 in range(_title_list.count()):
            _node = _title_list.nth(i1)
            _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
            _title = paper_util.remove_empty(_node.inner_text())
            if not _content_url_list.__contains__(_content_url):
                _content_url_list.append(_content_url)
                _paper_list.append({
                    "title": _title,
                    "content_url": _content_url,
                })

        if not only_title:
            _content_list = page.locator("map[name=\"PagePicMap\"]").locator("area")
            for i1 in range(_content_list.count()):
                _node = _content_list.nth(i1)
                _content_url = paper_util.generate_url(url=page.url, href=_node.get_attribute("href"))
                _title = "公告"
                if not _content_url_list.__contains__(_content_url):
                    _content_url_list.append(_content_url)
                    _paper_list.append({
                        "title": _title,
                        "content_url": _content_url,
                    })

        _paper_list_1 = []
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            _notice = paper_util.title_check_notice(_title)
            if (not _notice) and (not paper_util.may_notice_by_title(_title)):
                continue
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _content = page1.locator("div#ozoom").inner_text()
            if (not _notice) and (not paper_util.check_notice2(_content)):
                continue
            _paper["content"] = _content
            _paper_list_1.append(_paper)

        deal_paper_list(paper_list=_paper_list_1, paper_page=_paper_page, queue=queue)

    page1.close()
    return None


# 银登网
def paper_yindeng(queue):
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page1 = context.new_page()
    for i in range(100):
        time.sleep(5)
        _url = "https://www.yindeng.com.cn/Home/cn/zczrxx/xxpl/zrgg/InfoList_" + str(i+1) + ".shtml"
        page.goto(_url)
        time.sleep(2)
        _paper_node_list = page.locator(
            "body > div.tow_main > div.left_menu_main > div.left_menu_main_box > div.newlist > ul > li")
        _paper_list = []
        page1 = context.new_page()
        for i1 in range(_paper_node_list.count()):
            _paper_node = _paper_node_list.nth(i1)
            _paper_href = _paper_node.locator("a")
            _day = ""
            for i2 in range(_paper_node.locator("span").count()):
                _text = paper_util.remove_empty(_paper_node.locator("span").nth(i2).inner_text())
                if paper_util.check_day(_text):
                    _day = _text
                    break
            if _day != "" and _day < queue.get("day"):
                page1.close()
                return None
            _title = paper_util.remove_empty(_paper_href.inner_text())
            _paper_url = paper_util.generate_url(url=page.url, href=_paper_href.get_attribute("href"))
            _paper = {
                "title": _title,
                "content_url": _paper_url,
                "day": _day,
                "paper": queue.get("name"),
            }
            _res = api.paper_paper_get(_paper)
            if _res is not None:
                continue
            _paper_list.append(_paper)
        for i1 in range(len(_paper_list)):
            _paper = _paper_list[i1]
            _title = _paper.get("title")
            page1.goto(_paper.get("content_url"))
            time.sleep(1)
            _pdf_node = page1.locator("body > div.news_info_box > div.zw_main4 > ul > li > span > a")
            if _pdf_node.count() > 0:
                _paper["pdf_original"] = _pdf_node.nth(0).get_attribute("href")
                _paper["pdf_url"] = upload_pdf_by_url(_paper.get("pdf_original"))
            api.paper_paper_add(_paper)

    page1.close()
    return None


# AMC-中信金融，华融
def paper_amc_zhongxin(queue):
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page1 = context.new_page()
    # _url = "https://www.chamc.com.cn/ywjs/ywdt/zcczxx/index.shtml"
    # page.goto(_url)
    # time.sleep(3)
    day = queue.get("day")
    total_page = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    for ii in range(10):
        if ii + 1 > total_page:
            break
        _ts = str(time.time() * 1000)
        _jsoncallback = "jQuery36106790844690994846_" + _ts
        _url = "https://www.chamc.com.cn/search/search.shtml" \
               "?jsoncallback=" + _jsoncallback + \
               "&kw=&startdate=" + day + \
               "&enddate=" + day + \
               "&pnum=" + str(ii+1) + \
               "&columnid=355&_=" + _ts
        r = requests.get(url=_url, headers=headers)
        _r_text = r.text.replace(_jsoncallback+"(", "")
        _r_text = re.sub("\\)\\s*$", "", _r_text)
        _res = json.loads(_r_text)
        total_page = _res.get("pages")
        _list = _res.get("list")
        if len(_list) < 1:
            break
        _paper_page_list = []
        for i in range(len(_list)):
            _item = _list[i]
            _page_url = "https://www.chamc.com.cn" + _item.get("url")
            _paper_page = {
                "name": str(_item.get("id")),
                "page_url": _page_url,
                "day": _item.get("pubdate").replace("/", "-"),
                "paper": queue.get("name"),
            }
            _paper_page_list.append(_paper_page)
        for i in range(len(_paper_page_list)):
            _paper_page = _paper_page_list[i]
            _res = api.paper_page_get(_paper_page)
            if _res is not None:
                continue
            _page_url = _paper_page.get("page_url")
            page1.goto(_page_url)
            time.sleep(3)
            _paper = {
                "content_url": _page_url,
            }
            _paper["title"] = re.sub("\\d{4}-\\d{2}-\\d{2}", "", paper_util.remove_empty(page1.locator(
                "body > div.container.inner_content > div.inner_right > div.inner_txt > div.blzcwz_title2").inner_text()))
            _content_div = page1.locator(
                "body > div.container.inner_content > div.inner_right > div.inner_txt > div.blzcwz_text")
            _content = _content_div.inner_text()
            _paper["content"] = _content
            _page_img = {
                "content": _content,
                "has_content": "true",
                "has_table": "false",
                "create_type": "cut",
            }
            _obj = tell_tables(content_div=_content_div)
            if len(_obj.get("tables")) > 0:
                _page_img["has_table"] = "true"
            _page_img["table_text_html"] = json.dumps(_obj, ensure_ascii=False)
            time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            img_path = "file/paper_img_" + time_str + ".png"
            page1.locator("body > div.container.inner_content > div.inner_right > div.inner_txt")\
                .screenshot(path=img_path, timeout=60000)
            img_url = upload_img_by_local_path(img_path=img_path)
            _page_img["img_url"] = img_url
            _paper_page["img_url"] = img_url
            _paper_list = [_paper]
            _page_img_list = [_page_img]
            deal_paper_list(paper_list=_paper_list, paper_page=_paper_page, page_img_list=_page_img_list, queue=queue)

        if ii + 1 >= total_page:
            break

    page1.close()
    return None


# AMC-信达
def paper_amc_xinda(queue):
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page1 = context.new_page()
    _url = "https://www.cinda.com.cn/home/pc/cn/xdjt/qykhfw/blzcjy/zcczggjk/index.shtml"
    page.goto(_url)
    day = queue.get("day")
    for ii in range(100):
        time.sleep(3)
        _page_node_list = page.locator("#jr_box > div > div.bu_follow > ul > li")
        _page_url_list = []
        _paper_page_list = []
        for i in range(_page_node_list.count()):
            _page_node = _page_node_list.nth(i)
            _day = _page_node.locator("p.times").inner_text().strip()
            if _day < day:
                break
            _page_href = _page_node.locator("a")
            _page_url = paper_util.generate_url(url=page.url, href=_page_href.get_attribute("href"))
            _search = re.search("=(\\d+)$", _page_url)
            _page_name = ""
            if _search is not None:
                _page_name = _search.group(1)
            _paper_page = {
                "name": _page_name,
                "page_url": _page_url,
                "day": _day,
                "paper": queue.get("name"),
            }
            _paper_page_list.append(_paper_page)

        for i in range(len(_paper_page_list)):
            _paper_page = _paper_page_list[i]
            _res = api.paper_page_get(_paper_page)
            if _res is not None:
                continue
            _page_url = _paper_page.get("page_url")
            page1.goto(_page_url)
            time.sleep(3)
            _paper = {
                "content_url": _page_url,
            }
            _paper["title"] = paper_util.remove_empty(page1.locator("#jr_box > div > div.bu_text > div.bu_tits").inner_text())
            _content_div = page1.locator("#jr_box > div > div.bu_text")
            _content = _content_div.inner_text()
            _paper["content"] = _content
            _page_img = {
                "content": _content,
                "has_content": "true",
                "has_table": "true",
                "create_type": "cut",
            }
            time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            pdf_path = "file/paper_img_" + time_str + ".pdf"
            img_path = "file/paper_img_" + time_str + ".png"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            }
            _pdf_url = ""
            r = requests.get(_pdf_url, headers=headers)
            f = open(pdf_path, 'wb')
            f.write(r.content)
            f.close()
            pdfDoc = fitz.open(pdf_path)
            text = ""
            for i1 in range(len(pdfDoc)):
                page = pdfDoc[i]
                text += page.get_text() + "\n"
                mat = fitz.Matrix(2, 2)  # 1.5表示放大1.5倍
                pix = page.get_pixmap(matrix=mat, alpha=False)
                pix.save("file/pdf2img" + str(i + 1) + ".png")

            img_url = upload_img_by_local_path(img_path=img_path)
            _page_img["img_url"] = img_url
            _paper_page["img_url"] = img_url
            _paper_list = [_paper]
            _page_img_list = [_page_img]
            deal_paper_list(paper_list=_paper_list, paper_page=_paper_page, page_img_list=_page_img_list, queue=queue)

    page1.close()
    return None


# AMC-东方
def paper_amc_dongfang(queue, notice_cate=1):
    if notice_cate == 1:
        _url = "https://sales.coamc.com.cn/coamc/notice/notice"
    elif notice_cate == 2:
        _url = "https://sales.coamc.com.cn/coamc/notice/attract"
    else:
        return None
    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto(_url)
    time.sleep(3)
    page1 = context.new_page()
    day = queue.get("day")
    _start_page_num = queue.get("start_page_num")
    if _start_page_num is None or _start_page_num < 1:
        _start_page_num = 1
    _api_url = "https://sales.coamc.com.cn/coamc/api/getNoticePage"
    finished = False
    for ii in range(100):
        if finished:
            break
        _ts = str(time.time() * 1000)
        _form_data = {
            "title": "",
            "type": "",
            "branchId": "",
            "condition": "0",
            "pageSize": "10",
            "page": str(ii + _start_page_num),
            "noticeCate": str(notice_cate),
        }
        time.sleep(2)
        response = page.request.post(url=_api_url+"?" + _ts + "&" + _ts, form=_form_data)
        result = response.json()
        _list = result.get("data").get("data").get("content")
        if len(_list) < 1:
            break
        _paper_page_list = []
        for i in range(len(_list)):
            _item = _list[i]
            _day = _item.get("auditTime")
            if _day < day:
                finished = True
                break
            _page_url = "https://sales.coamc.com.cn/" + _item.get("url")
            _paper_page = {
                "name": str(_item.get("id")),
                "page_url": _page_url,
                "day": _day,
                "paper": queue.get("name"),
            }
            _paper_page_list.append(_paper_page)
        for i in range(len(_paper_page_list)):
            _paper_page = _paper_page_list[i]
            _res = api.paper_page_get(_paper_page)
            if _res is not None:
                continue
            _page_url = _paper_page.get("page_url")
            page1.goto(_page_url)
            time.sleep(3)
            _paper = {
                "content_url": _page_url,
            }
            _paper["title"] = paper_util.remove_empty(re.sub("^[^<>]*<br>", "", page1.locator(
                "body > div.notice-con > div.notice-inner > div.notice-detail.clear > h3").nth(0).inner_html()))
            _content_div = page1.locator("body > div.notice-con > div.notice-inner > div.notice-detail.clear")
            _content = _content_div.inner_text()
            _paper["content"] = _content
            _page_img = {
                "content": _content,
                "has_content": "true",
                "has_table": "false",
                "create_type": "cut",
            }
            _obj = tell_tables(content_div=_content_div)
            if len(_obj.get("tables")) > 0:
                _page_img["has_table"] = "true"
            _page_img["table_text_html"] = json.dumps(_obj, ensure_ascii=False)
            time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            img_path = "file/paper_img_" + time_str + ".png"
            page1.locator("body > div.notice-con > div.notice-inner").screenshot(path=img_path)
            img_url = upload_img_by_local_path(img_path=img_path)
            _page_img["img_url"] = img_url
            _paper_page["img_url"] = img_url
            _paper_list = [_paper]
            _page_img_list = [_page_img]
            deal_paper_list(paper_list=_paper_list, paper_page=_paper_page, page_img_list=_page_img_list, queue=queue)

    page1.close()
    return None


# AMC-长城
def paper_amc_changcheng(queue):

    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page.goto("https://www.gwamcc.com/Hiring.aspx?liName=64")
    time.sleep(3)
    page1 = context.new_page()
    day = queue.get("day")
    _start_page_num = queue.get("start_page_num")
    if _start_page_num is None or _start_page_num < 1:
        _start_page_num = 1
    _api_url = "https://www.gwamcc.com/Ajax/GetArticleList.ashx"
    finished = False
    for ii in range(100):
        if finished:
            break
        _ts = str(time.time() * 1000)
        _param = {
            "t": _ts,
            "pIndex": str(ii + _start_page_num),
            "pSize": "15",
            "liName": "64",
            "titleLength": "50",
        }
        response = page.request.get(url=_api_url, params=_param)
        result = response.json()
        _list = result.get("ds")
        if len(_list) < 1:
            break
        _paper_page_list = []
        for i in range(len(_list)):
            _item = _list[i]
            _day = _item.get("ActionDate")
            if _day < day:
                finished = True
                break
            _page_url = "https://www.gwamcc.com/HiringDetail.aspx?liName=64&ID=" + _item.get("ID")
            _paper_page = {
                "name": str(_item.get("ID")),
                "page_url": _page_url,
                "day": _day,
                "paper": queue.get("name"),
            }
            _paper_page_list.append(_paper_page)
        for i in range(len(_paper_page_list)):
            _paper_page = _paper_page_list[i]
            _res = api.paper_page_get(_paper_page)
            if _res is not None:
                continue
            _page_url = _paper_page.get("page_url")
            page1.goto(_page_url)
            time.sleep(3)
            _paper = {
                "content_url": _page_url,
            }
            _paper["title"] = paper_util.remove_empty(page1.locator("div.pagestyle_title > h1").nth(0).inner_text())
            _content_div = page1.locator("div.pagestyle_box").nth(0)
            _content = _content_div.inner_text()
            _paper["content"] = _content
            _page_img = {
                "content": _content,
                "has_content": "true",
                "has_table": "false",
                "create_type": "cut",
            }
            _obj = tell_tables(content_div=_content_div)
            if len(_obj.get("tables")) > 0:
                _page_img["has_table"] = "true"
            _page_img["table_text_html"] = json.dumps(_obj, ensure_ascii=False)
            time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            img_path = "file/paper_img_" + time_str + ".png"
            page1.locator("#ctl00 > div.news.container.clearfix > div.inner_con.float_r > div.inner_main")\
                .screenshot(path=img_path, timeout=60000)
            img_url = upload_img_by_local_path(img_path=img_path)
            _page_img["img_url"] = img_url
            _paper_page["img_url"] = img_url
            _paper_list = [_paper]
            _page_img_list = [_page_img]
            deal_paper_list(paper_list=_paper_list, paper_page=_paper_page, page_img_list=_page_img_list, queue=queue)

    page1.close()
    return None


# AMC-银河
def paper_amc_yinhe(queue):

    global context
    context = browser.new_context()
    global page
    page = context.new_page()
    page1 = context.new_page()
    day = queue.get("day")
    finished = False
    for ii in range(100):
        if finished:
            break
        _url = "https://www.galaxyamc.com.cn/czgg_" + str(ii + 1) + ".htm"
        page.goto(_url)
        time.sleep(3)
        _page_node_list = page.locator("div.right > ul.item > li")
        _ts = str(time.time() * 1000)
        _paper_page_list = []
        if _page_node_list.count() < 1:
            break
        for i in range(_page_node_list.count()):
            _page_node = _page_node_list.nth(i)
            _day = _page_node.locator("div.time").inner_text().strip().replace("/", "-")
            if _day < day:
                finished = True
                break
            _page_url = None
            _search = re.search("(\\d+)\\.htm", _page_node.get_attribute("onclick"))
            _name = ""
            if _search is not None:
                _name = _search.group(1)
                _page_url = "https://www.galaxyamc.com.cn/czgg/" + _name + ".htm"
            if _page_url is None:
                continue
            _paper_page = {
                "name": _name,
                "page_url": _page_url,
                "day": _day,
                "paper": queue.get("name"),
            }
            _paper_page_list.append(_paper_page)
        for i in range(len(_paper_page_list)):
            _paper_page = _paper_page_list[i]
            _res = api.paper_page_get(_paper_page)
            if _res is not None:
                continue
            _page_url = _paper_page.get("page_url")
            page1.goto(_page_url)
            time.sleep(3)
            _paper = {
                "content_url": _page_url,
            }
            _paper["title"] = paper_util.remove_empty(page1.locator("h2.article-title").nth(0).inner_text())
            _content_div = page1.locator("div.article-content").nth(0)
            _content = _content_div.inner_text()
            _paper["content"] = _content
            _page_img = {
                "content": _content,
                "has_content": "true",
                "has_table": "false",
                "create_type": "cut",
            }
            _obj = tell_tables(content_div=_content_div)
            if len(_obj.get("tables")) > 0:
                _page_img["has_table"] = "true"
            _page_img["table_text_html"] = json.dumps(_obj, ensure_ascii=False)
            time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            img_path = "file/paper_img_" + time_str + ".png"
            page1.locator("div.article").nth(0).screenshot(path=img_path, timeout=60000)
            img_url = upload_img_by_local_path(img_path=img_path)
            _page_img["img_url"] = img_url
            _paper_page["img_url"] = img_url
            _paper_list = [_paper]
            _page_img_list = [_page_img]
            deal_paper_list(paper_list=_paper_list, paper_page=_paper_page, page_img_list=_page_img_list, queue=queue)

    page1.close()
    return None


def tell_tables(content_div):
    _obj = {
        "tables": [],
    }
    _table_div = content_div.locator("table")
    if _table_div.count() > 0:
        for i1 in range(_table_div.count()):
            _table = _table_div.nth(i1)
            _tr_list = _table.locator("tr")
            _row_num = _tr_list.count()
            matrix = np.zeros((_row_num, 50))
            _table_obj = []
            for i2 in range(_tr_list.count()):
                _row_index = i2
                _tr = _tr_list.nth(i2)
                _td_list = _tr.locator("td")
                if _td_list.count() < 1:
                    _td_list = _tr.locator("th")
                _col_index = 0
                _tr_obj = []
                for i3 in range(_td_list.count()):
                    _td = _td_list.nth(i3)
                    _td_content = _td.inner_text().strip()
                    _col_span = 1
                    _row_span = 1
                    colspan = _td.get_attribute("colspan")
                    rowspan = _td.get_attribute("rowspan")
                    if colspan is not None:
                        _col_span = int(colspan)
                    if rowspan is not None:
                        _row_span = int(rowspan)
                    for i4 in range(_col_index, 50):
                        if matrix[_row_index, i4] == 0:
                            _col_index = i4
                            break
                    for row1 in range(_row_index, _row_index + _row_span):
                        for col1 in range(_col_index, _col_index + _col_span):
                            matrix[row1, col1] = 1
                    _td_obj = {
                        "sx": _col_index,
                        "ex": _col_index + _col_span,
                        "sy": _row_index,
                        "ey": _row_index + _row_span,
                        "text": [_td_content],
                    }
                    _tr_obj.append(_td_obj)
                    _col_index = _col_index + 1

                _table_obj.append(_tr_obj)
            _obj["tables"].append(_table_obj)
    return _obj


def deal_queue(queue):
    global p
    global browser
    try:
        p = sync_playwright().start()
        browser = p.chromium.launch(channel="chrome", headless=True)  # 关闭无头模式，方便看到页面加载情况
        _name = queue.get("name")
        if _name == "浙江法治报":
            return paper_zhejiang_zjfzb(queue=queue)
        elif _name == "浙江日报":
            return paper_zhejiang_zjrb(queue=queue)
        elif _name == "江南游报":
            return paper_zhejiang_jnyb(queue=queue)
        elif _name == "江苏经济报":
            return paper_jiangsu_jsjjb(queue=queue)
        elif _name == "江苏法治报":
            return paper_jiangsu_jsfzb(queue=queue)
        elif _name == "新华日报":
            return paper_jiangsu_xhrb(queue=queue)
        elif _name == "江南时报":
            return paper_jiangsu_jnsb(queue=queue)
        elif _name == "江苏商报":
            return paper_jiangsu_jssb(queue=queue)
        elif _name == "文汇报":
            return paper_shanghai_whb(queue=queue)
        elif _name == "青年报":
            return paper_shanghai_qnb(queue=queue)
        elif _name == "劳动午报":
            return paper_beijing_ldwb(queue=queue)
        elif _name == "天津日报":
            return paper_tianjin_tjrb(queue=queue)
        elif _name == "重庆日报":
            return paper_chongqing_cqrb(queue=queue)
        elif _name == "重庆商报":
            return paper_chongqing_cqsb(queue=queue)
        elif _name == "重庆法治报":
            return paper_chongqing_cqfzb(queue=queue)
        elif _name == "安徽商报":
            return paper_anhui_ahsb(queue=queue)
        elif _name == "安徽法治报":
            return paper_anhui_ahfzb(queue=queue)
        elif _name == "福建日报":
            return paper_fujian_fjrb(queue=queue)
        elif _name == "海峡都市报":
            return paper_fujian_hxdsb(queue=queue)
        elif _name == "南方日报":
            return paper_guangdong_nfrb2(queue=queue)
        elif _name == "羊城晚报":
            return paper_guangdong_ycwb(queue=queue)
        elif _name == "羊晚区域版":
            return paper_guangdong_ywqy(queue=queue)
        elif _name == "广西日报":
            return paper_guangxi_gxrb(queue=queue)
        elif _name == "云南经济日报":
            return paper_yunnan_ynjjrb(queue=queue)
        elif _name == "四川日报":
            return paper_sichuan_scrb(queue=queue)
        elif _name == "四川法治报":
            return paper_sichuan_scfzb(queue=queue)
        elif _name == "湖南日报":
            return paper_hunan_hnrb(queue=queue)
        elif _name == "三湘都市报":
            return paper_hunan_sxdsb(queue=queue)
        elif _name == "楚天都市报":
            return paper_hubei_ctdsb(queue=queue)
        elif _name == "湖北日报":
            return paper_hubei_hbrb(queue=queue)
        elif _name == "三峡晚报":
            return paper_hubei_sxwb(queue=queue)
        elif _name == "江西日报":
            return paper_jiangxi_jxrb(queue=queue)
        elif _name == "新法治报":
            return paper_jiangxi_xfzb(queue=queue)
        elif _name == "海南日报":
            return paper_hainan_hnrb(queue=queue)
        elif _name == "河北法制报":
            return paper_hebei_hbfzb(queue=queue)
        elif _name == "河北经济日报":
            return paper_hebei_hbjjrb(queue=queue)
        elif _name == "山东法制报":
            return paper_shandong_sdfzb(queue=queue)
        elif _name == "齐鲁晚报":
            return paper_shandong_qlwb(queue=queue)
        elif _name == "经济导报":
            return paper_shandong_jjdb(queue=queue)
        elif _name == "山西经济日报":
            return paper_shanxi_sxjjrb(queue=queue)
        elif _name == "陕西日报":
            return paper_shaanxi_sxrb(queue=queue)
        elif _name == "西部法制报":
            return paper_shaanxi_xbfzb(queue=queue)
        elif _name == "青海日报":
            return paper_qinghai_qhrb(queue=queue)
        elif _name == "辽宁日报":
            return paper_liaoning_lnrb(queue=queue)
        elif _name == "吉林日报":
            return paper_jilin_jlrb(queue=queue)
        elif _name == "城市晚报":
            return paper_jilin_cswb(queue=queue)
        elif _name == "黑龙江日报":
            return paper_heilongjiang_hljrb(queue=queue)
        elif _name == "内蒙古日报":
            return paper_neimenggu_nmgrb(queue=queue)
        elif _name == "内蒙古晨报":
            return paper_neimenggu_nmgcb(queue=queue)
        elif _name == "内蒙古法制报":
            return paper_neimenggu_nmgfzb(queue=queue)
        elif _name == "北方新报":
            return paper_neimenggu_bfxb(queue=queue)
        elif _name == "宁夏日报":
            return paper_ningxia_nxrb(queue=queue)
        elif _name == "宁夏法治报":
            return paper_ningxia_nxfzb(queue=queue)
        elif _name == "经济日报":
            return paper_china_jjrb(queue=queue)
        elif _name == "法治日报":
            return paper_china_fzrb(queue=queue)
        elif _name == "中国商报":
            return paper_china_zgsb(queue=queue)
        elif _name == "中华工商时报":
            return paper_china_zhgssb(queue=queue)
        elif _name == "国际商报":
            return paper_china_gjsb(queue=queue)
        elif _name == "中信金融":
            return paper_amc_zhongxin(queue=queue)
        elif _name == "东方资产":
            paper_amc_dongfang(queue=queue, notice_cate=1)
            paper_amc_dongfang(queue=queue, notice_cate=2)
            return None
        elif _name == "长城资产":
            return paper_amc_changcheng(queue=queue)
        elif _name == "银河资产":
            return paper_amc_yinhe(queue=queue)
        else:
            return "未定义的报纸类型"
    except Exception as err:
        log.base.error(str(err))
        traceback.print_exc()
        return str(err)
    finally:
        time.sleep(1)
        if browser is not None:
            try:
                browser.close()
            except Exception as err:
                log.base.error(str(err))
        if p is not None:
            try:
                p.stop()
            except Exception as err:
                log.base.error(str(err))
        # if page is not None:
        #     try:
        #         page.close()
        #     except Exception as err:
        #         log.base.error(str(err))
        # if context is not None:
        #     try:
        #         context.close()
        #     except Exception as err:
        #         log.base.error(str(err))
