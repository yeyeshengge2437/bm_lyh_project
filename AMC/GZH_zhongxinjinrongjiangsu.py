import os
import re
import time
from datetime import datetime

import mysql.connector
from lxml import etree
from DrissionPage import ChromiumPage, ChromiumOptions

from AMC.api_paper import upload_file_by_url, get_image, judge_bm_repeat, upload_file, judge_title_repeat

co = ChromiumOptions()
co = co.set_argument('--no-sandbox')
co = co.headless()
co.set_paths(local_port=9237)
def zhongxinjinrongjiangsu_gzh(queue_id, webpage_id):
    img_set = set()
    name = '中国中信金融资产江苏分公司'
    title_set = judge_title_repeat(name)
    page = ChromiumPage(co)
    page.get('https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI5ODk2MTY1Mg==&action=getalbum&album_id=3421134606546747396#wechat_redirect')
    # 点击正序
    page.ele("倒序").click(by_js=True)
    time.sleep(2)
    for i in range(20):
        page.scroll.to_bottom()
        time.sleep(1)
    time.sleep(10)
    html = etree.HTML(page.html)
    data_list = html.xpath("//li[contains(@class, 'album__list-item')]")
    for data in data_list:
        title_name = ''.join(data.xpath("./@data-title"))
        title_url = ''.join(data.xpath("./@data-link"))
        page.get(title_url)
        title_date1 = page.ele("xpath=//em[@id='publish_time']").text
        # 正则匹配 2024年01月08日 10:35
        title_date = re.findall(r'\d{4}年\d{2}月\d{2}日', title_date1)[0]
        # 转换成 2024-01-08
        title_date = title_date.replace('年', '-').replace('月', '-').replace('日', '')
        title_content = page.ele("xpath=//div[@id='js_content']/section").text
        content_html = page.ele("xpath=//div[@id='js_content']").html
        html = etree.HTML(content_html)
        annex = html.xpath("//@data-src")
        # print(title_date, title_content)
        # print(annex)
        if annex:
            # print(page_url, annex)
            files = []
            original_url = []
            for ann in annex:
                file_url = upload_file_by_url(ann, "jiangsu", 'png')
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
        image = get_image(page, title_url, "xpath=//div[@id='img-content']", is_to_bottom=True)
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        create_date = datetime.now().strftime('%Y-%m-%d')
        # 上传到测试数据库
        conn_test = mysql.connector.connect(
            host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database="col",
        )
        cursor_test = conn_test.cursor()
        # print(title_name, title_date, title_url, files, image)
        if image not in img_set and judge_bm_repeat(name, title_url):
            # 将报纸url上传
            up_img = upload_file(image, "png", "paper")
            img_set.add(image)
            # 上传到报纸的图片或PDF
            insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

            cursor_test.execute(insert_sql,
                                (title_date, name, title_name, up_img, title_url, up_img, create_time, queue_id,
                                 create_date, webpage_id))
            conn_test.commit()
        else:
            if os.path.exists(f'{image}.png'):
                os.remove(f'{image}.png')

        if title_url not in title_set:
            # 上传到报纸的内容
            insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url, content_html, create_time,original_files, files, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

            cursor_test.execute(insert_sql,
                                (
                                    title_url, title_date, name, title_name, title_content, title_url,
                                    content_html,
                                    create_time, original_url, files, queue_id,
                                    create_date, webpage_id))
            conn_test.commit()
            title_set.add(title_url)

        cursor_test.close()
        conn_test.close()

    page.close()


