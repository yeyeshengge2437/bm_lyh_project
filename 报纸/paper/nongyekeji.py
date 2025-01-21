import os
import time
from datetime import datetime

import mysql.connector
import requests
from PIL import Image
from lxml import etree
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat
import os
import json
import requests



paper = "农业科技报"
# 获取任务id

# value = paper_queue_next(webpage_url_list=['http://eb.nkb.com.cn/nykjb'])
# queue_id = value['id']
# webpage_id = value["webpage_id"]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    # 'Cookie': 'JSESSIONID=846F41FC2DC72F6F5734D69F24341992; Hm_lvt_eba88703966124241edc99e81a221bf2=1722820434; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_eba88703966124241edc99e81a221bf2=1722820455; Hm_lvt_be17d121a971d124a94aba36598b9295=1722820472; Hm_lpvt_be17d121a971d124a94aba36598b9295=1722820497',
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}
today = datetime.now().strftime('%Y-%m-%d')


def get_nongyekeji_paper(paper_time, queue_id, webpage_id, bm_url_in=None):
    day = paper_time
    paper_time = datetime.strptime(paper_time, '%Y-%m-%d').strftime('%Y%m%d')
    base_url = f'http://eb.nkb.com.cn/nykjb/{paper_time}/mhtml/'
    url = base_url + 'index.htm'
    response = requests.get(url, headers=headers, verify=False)
    time.sleep(2)
    status_code = response.status_code
    if status_code == 200:
        html = etree.HTML(response.text)
        # 获取所有版面
        banmian = html.xpath("//div[@class='nav-panel-primary']/div[@class='nav-items']")
        for bm in banmian:
            # 打印版面信息
            bm_info = "".join(bm.xpath("./div[@class='nav-panel-heading']/text()"))
            # 获取版面下的所有栏目
            for title in bm.xpath("./ul[@class='nav-list-group']/li"):
                img_set = set()
                # 打印栏目信息
                title_info = "".join(title.xpath("./a/text()"))
                title_link = title.xpath("./a/@href")[0]
                # 获取栏目下的所有文章
                title_link = title.xpath("./a/@href")[0]
                # 获取当前版次的img
                page_num = title_link[-1:]
                if page_num == '0':
                    bm_img = base_url + 'index_h.jpg'
                else:
                    if int(page_num) < 10:
                        page_num = '0' + page_num
                    bm_img = base_url + 'page_' + page_num + '_h.jpg'

                key_url = base_url + title_link
                key_res = requests.get(key_url, headers=headers, verify=False)
                time.sleep(2)
                key_html = etree.HTML(key_res.text)
                # 获取文章文章字数
                article_content = "".join(
                    key_html.xpath("//div[@class='cont']/div[@id='memo']/div[@id='numb']/text()"))

                # 判断是否包含债权关键字
                if judging_criteria(title_info, article_content):

                    # 上传到数据库
                    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    conn_test = mysql.connector.connect(
                        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col"
                    )
                    cursor_test = conn_test.cursor()
                    if article_content:
                        # 存储到数据库
                        page_url = url + title_link[-6:]
                        title = title_info
                        content = article_content
                        content_url = key_url
                        # 将数据插入到表中

                        insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (page_url, day, paper, title, content, content_url, create_time, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()

                    bm_url = base_url + f"index.htm#page{page_num}"
                    if bm_url not in img_set and judge_bm_repeat(paper, bm_url):
                        img_set.add(bm_url)
                        img_url = upload_file_by_url(bm_img, paper, 'img')
                        # 存储当前版次图片
                        insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                        cursor_test.execute(insert_sql,
                                            (day, paper, bm_info, bm_img, bm_url, img_url, create_time, queue_id,
                                             create_date, webpage_id))
                        conn_test.commit()
                    cursor_test.close()
                    conn_test.close()
        success_data = {
            'id': queue_id,
            'description': '成功',
        }
        paper_queue_success(success_data)
    else:
        raise Exception(f'该日期没有报纸')
