import os
from datetime import datetime

import mysql.connector
import requests
from PIL import Image
from lxml import etree

import os
import json
import requests

produce_url = "http://121.43.164.84:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False


def paper_queue_next(webpage_url_list=None):
    headers = {
        'Content-Type': 'application/json'
    }
    if webpage_url_list is None:
        webpage_url_list = []

    url = test_url + "/website/queue/next"
    data = {
        "webpage_url_list": webpage_url_list
    }

    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()
    print(result)
    return result.get("value")


def paper_queue_success(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    if data is None:
        data = {}
    url = test_url + "/website/queue/success"
    data_str = json.dumps(data)

    res = s.post(url=url, headers=headers, data=data_str)
    result = res.json()

    return result.get("value")


def paper_queue_fail(data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json'
    }
    try:
        if data is None:
            data = {}
        url = test_url + "/website/queue/fail"
        data_str = json.dumps(data)
        res = s.post(url=url, headers=headers, data=data_str)
        result = res.json()
        return result.get("value")
    except Exception as err:
        print(err)
        return None


def upload_img_by_url(img_url, file_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(img_url, headers=headers)
    if r.status_code != 200:
        return "获取失败"
    pdf_path = f"{file_name}.jpg"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}

    url = 'http://121.43.164.84:29775' + "/file/upload/file?type=paper"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    return result.get("value")["file_url"]


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

create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
create_date = datetime.now().strftime('%Y-%m-%d')
paper = "农业科技报"
# 获取任务id

value = paper_queue_next(webpage_url_list=['http://eb.nkb.com.cn/nykjb'])
queue_id = value['id']
webpage_id = value["webpage_id"]

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
now_day = datetime.now().strftime('%Y%m%d')
# now_day = '20230821'
# now_day = '20230928'
day = now_day[:4] + '-' + now_day[4:6] + '-' + now_day[6:]
try:
    base_url = 'http://eb.nkb.com.cn/nykjb/' + now_day + '/mhtml/'
    url = base_url + 'index.htm'
    response = requests.get(url, headers=headers, verify=False)
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
                # 打印栏目信息
                title_info = "".join(title.xpath("./a/text()"))
                title_link = title.xpath("./a/@href")[0]

                # 判断是否包含债权关键字
                if any(key in title_info for key in claims_keys):
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
                    key_html = etree.HTML(key_res.text)
                    # 获取文章文章字数
                    article_content = "".join(key_html.xpath("//div[@class='cont']/div[@id='memo']/div[@id='numb']/text()"))
                    # 上传到数据库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
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

                    img_url = upload_img_by_url(bm_img, "1")
                    bm_url = base_url + f"index.htm#page{page_num}"
                    # 存储当前版次图片
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_img, page_url, img_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_info, bm_img, bm_url, img_url, create_time, queue_id, create_date, webpage_id))
                    conn_test.commit()
                    cursor_test.close()
                    conn_test.close()
        success_data = {
            'id': queue_id,
            'description': '成功',
        }
        paper_queue_success(success_data)


    else:
        print("今天暂无报纸", url)
        success_data = {
            'id': queue_id,
            'description': '今天暂无报纸',
        }
        paper_queue_success(success_data)
except Exception as e:
    print(f"失败原因: {e}")
    fail_data = {
        'id': queue_id,
        'description': '程序问题',
    }
    paper_queue_fail(data=fail_data)
