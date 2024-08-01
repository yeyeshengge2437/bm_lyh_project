# import time
#
# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)  # headless=False 表示非无头模式
#     page = browser.new_page()
#     page.goto('http://epaper.legaldaily.com.cn/fzrb/PDF/20240801/09.pdf')
#     time.sleep(5)
#     # page.pdf(path='example.pdf')  # 保存PDF文件
#     input()
#     page.click('cr-icon-button#download')
import os

import requests


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


upload_pdf_by_url('http://epaper.legaldaily.com.cn/fzrb/PDF/20240801/09.pdf')

