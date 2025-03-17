import re
import time
import os
import random
import re
import time
from datetime import datetime
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from api_paper import get_image, judge_bm_repeat, upload_file, judge_title_repeat, upload_file_by_url, get_now_image
import requests
from lxml import etree
from bs4 import BeautifulSoup

co = ChromiumOptions()
# co = co.set_argument('--no-sandbox')
# co = co.headless()
# co.set_paths(local_port=9209)



headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.cquae.com/Project?q=s&projectID=5&',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '__jsluid_s=35256ae16524f8aa98f136b6204311f6; Hm_lvt_626131e5d1fe8ad7532ecced20a716b5=1740042017; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_a5cf993912d876d06d4efa4e14364ecc=1740042017; ASP.NET_SessionId=11asgc0bdygjr0hjjlo1ntws; __jsl_clearance_s=1740559754.967|0|wWBg2ap7ntypEsGELmBhbMR1y%2FY%3D; Hm_lpvt_626131e5d1fe8ad7532ecced20a716b5=1740559758; Hm_lpvt_a5cf993912d876d06d4efa4e14364ecc=1740559758',
}

def remove_script_tags_safe(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup.find_all('script'):
        script.decompose()
    return str(soup)

def get_jiangsuchanquanshichangwang(queue_id, webpage_id):
    page = ChromiumPage(co)
    page.set.load_mode.none()
    page.get('https://www.jscq.com.cn/jscq/cqjy/zypt/blzcjypt/index.shtml')
    page.scroll.to_bottom()
    time.sleep(3)
    try:
        # for zq_type in ['G3', 'PG3']:
        for page_num in range(0, 133):
            if page_num != 0:
                page.ele("xpath=//a[@class='layui-laypage-next']").click(by_js=True)
                time.sleep(3)

            img_set = set()
            name = '江苏产权市场网'
            title_set = judge_title_repeat(name)

            # print(page.html)
            # return
            res_json = page.html
            html = etree.HTML(res_json)
            # print(res_json)
            data_list = html.xpath("//li[@class='pxitem']")
            for data in data_list:
                time.sleep(1)
                # page_url = ''.join(data.xpath(".//a//@href"))
                page_url = 'https://www.jscq.com.cn/' + ''.join(data.xpath(".//a[@class='cairong1']/@href"))
                title_name = ''.join(data.xpath(".//a[@class='cairong1']/text()"))
                # title_date = ''.join(data.xpath(".//td[@class='n2_wsbm']/div[1]/span//text()"))
                title_date = re.findall(r'\d{4}-\d{1,2}/\d{2}', str(page_url))
                if title_date:
                    title_date = title_date[0]
                    title_date = title_date.replace('/', '-')
                else:
                    title_date = ''
                # print(page_url, title_name, title_date)

                tab_detail = page.new_tab()
                tab_detail.get(page_url)
                tab_detail.scroll.to_bottom()
                time.sleep(3)
                res = tab_detail.html
                tab_detail.close()
                # print(res)
                res_html = etree.HTML(res)
                # title_list = res_html.xpath("//div[@class='rightListContent list-item']")
                # 使用re模块提取日期

                title_url = page_url
                if title_url not in title_set:
                # if 1:
                    title_content = "".join(res_html.xpath("//div[@class='detail_bottom']/div[@class='tab_bottom tab_bottom1']//text()"))
                    # print(title_content)
                    # return


                    annex = res_html.xpath("//div[@class='detail_bottom']/div[@class='tab_bottom tab_bottom1']//@href")
                    if annex:
                        # print(page_url, annex)
                        files = []
                        original_url = []
                        for ann in annex:
                            if "http" not in ann:
                                ann = 'https://files.cquae.com' + ann
                            file_type = ann.split('.')[-1]
                            if file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                             'png', 'jpg', 'jpeg'] and 'upload' in ann:
                                file_url = upload_file_by_url(ann, "jiangsu", file_type)
                                # file_url = 111
                                files.append(file_url)
                                original_url.append(ann)
                    else:
                        files = ''
                        original_url = ''
                    if not files:
                        files = ''
                        original_url = ''
                    files = str(files).replace("'", '"')
                    original_url = str(original_url).replace("'", '"')
                    # print(files, original_url)
                    # title_html_info = res_html.xpath("//td[@class='td_contont']/div[@class='contont_div']")
                    content_1 = res_html.xpath("//div[@class='detail_bottom']/div[@class='tab_bottom tab_bottom1']")
                    content_html = ''
                    for con in content_1:
                        content_html += etree.tostring(con, encoding='utf-8').decode()
                    content_html = re.sub(r'<div class="tab_bottom tab_bottom2 none">.*</html>', '', content_html,  flags=re.DOTALL )
                    # print(content_html)
                    # return
                    try:
                        image = get_image(page, title_url,
                                          "xpath=//div[@class='detail_bottom']/div[@class='tab_bottom tab_bottom1']")
                    except:
                        print('截取当前显示区域')
                        image = get_now_image(page, title_url)
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    # print(title_name, title_date, title_url, title_content, content_html)
                    # return
                    # 上传到测试数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col",
                    )
                    cursor_test = conn_test.cursor()
                    # print(bm_name, article_name, article_url, bm_pdf, content)
                    if image not in img_set and judge_bm_repeat(name, title_url):
                        # 将报纸url上传
                        up_img = upload_file(image, "png", "paper")
                        img_set.add(image)
                        # 上传到报纸的图片或PDF
                        insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_date, name, title_name, up_img, title_url, up_img, create_time,
                                             queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                    else:
                        if os.path.exists(f'{image}.png'):
                            os.remove(f'{image}.png')

                    if title_url not in title_set:
                        # 上传到报纸的内容
                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time,original_files, files, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (title_url, title_date, name, title_name, title_content, title_url,
                                             content_html,
                                             create_time, original_url, files, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                        title_set.add(title_url)

                    cursor_test.close()
                    conn_test.close()
        page.close()

    except Exception as e:
        try:
            page.close()
        except:
            pass
        raise Exception(e)
    try:
        page.quit()
    except:
        pass


# get_jiangsuchanquanshichangwang(111, 222)
