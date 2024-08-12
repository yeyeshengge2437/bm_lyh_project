import hashlib
import time

import mysql.connector
from lxml import etree
import re
import redis
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
    return result.get("value")['id']


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


def upload_file_by_url(file_url, file_name, file_type, type="paper"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    r = requests.get(file_url, headers=headers)
    if r.status_code != 200:
        return "获取失败"
    pdf_path = f"{file_name}.{file_type}"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}
    url = 'http://121.43.164.84:29775' + f"/file/upload/file?type={type}"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    if "file_url" in result.get("value"):
        return result.get("value")["file_url"]
    else:
        return "链接失效"


# from_queue = paper_queue_next(webpage_url_list=['https://szb.gansudaily.com.cn/gsjjrb'])
#
# success_data = {
#         'id': from_queue,
#         'description': '成功',
#     }
# paper_queue_success(success_data)
#
# fail_data = {
#         "id": from_queue,
#         "description": "该天没有报纸",
#     }
# paper_queue_fail(fail_data)
# 连接redis
r = redis.Redis()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get('https://yjj.guizhou.gov.cn/gsgg/ypscxkgs/', headers=headers)
print(response.status_code)
# 获取所有首要的URL
html_1 = etree.HTML(response.content.decode())
main_urls = html_1.xpath("//ul[@id='Left_Nav']/li/a/@href")
main_urls.append('https://yjj.guizhou.gov.cn/xwdt/tzgg/')
if not r.llen('guizhou_yjj'):
    for main in main_urls:
        if any(s in main for s in ['wtgysxzspsxgs', 'xzcf', 'sfgs']):  # 去除三项不要的数据
            pass
        else:
            res_target = requests.get(main, headers=headers)
            if res_target.status_code == 200:
                html_2 = etree.HTML(res_target.content.decode())
                time.sleep(2)
                # 获取一共有多少条数据
                page = html_2.xpath("//div[3]/div/div[2]/div[2]/script/text()")[0]
                page_num = re.findall(r'\d+', page)[0]

                for i in range(1, int(page_num) + 1):
                    if i == 1:
                        url = main + "index.html"
                    else:
                        url = main + "index_" + str(i - 1) + ".html"

                    res_notices = requests.get(url, headers=headers)
                    time.sleep(2)
                    html_3 = etree.HTML(res_notices.content.decode())
                    notices = html_3.xpath("//div[@class='right-list-box']/ul/li/a")
                    for notice in notices:
                        title_url = "".join(notice.xpath("./@href")[0])

                        r.lpush('guizhou_yjj', title_url)

while r.llen('guizhou_yjj'):
    url = r.rpop('guizhou_yjj').decode()
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
                content_html = ''
                if not contents:
                    contents = title_html.xpath("//div[@class='Article_zw']")
                for cont in contents:
                    content_html += etree.tostring(cont, method='html', encoding='unicode')
                source = "".join(title_html.xpath("//div[@class='Article_ly']/span[@class='SourceName']//text()"))
                if not source:
                    source = "".join(title_html.xpath("//div[@id='c']/div[@class='Article_ly']/span[2]//text()"))
                    source = re.findall(r"var wzly='(.*?)';", source)[0]
                    if not re.search(r'[\u4e00-\u9fff]+', source):
                        source = "贵州省药品监督管理局"

                elif re.search(r'[A-Za-z]', source):
                    source = re.findall(r"var SourceName='(.*?)';", source)[0]
                    if not re.search(r'[\u4e00-\u9fff]+', source):
                        source = "贵州省药品监督管理局"
                else:
                    source = source
                pub_date = "".join(title_html.xpath("//div[@id='c']/div[@class='Article_ly']/span[1]//text()"))
                pub_date = re.findall(r"var  pubdata='(.*?)';", pub_date)[0]
                annexs = title_html.xpath("//p[@class='insertfileTag']/a")  # 获取所有附件
                if not annexs:
                    annexs = title_html.xpath("//div[contains(@class, 'trs_paper_default')]/p/a")
                if not annexs:
                    annexs = title_html.xpath("//font[@id='Zoom']/p//a")

                if url_key == 'xwdt/tzgg':
                    base_title_url = url[:42]
                elif url_key == 'gsgg':
                    cleaned_url = re.sub(r'/t\d+_\d+\.html', '', url)
                    base_title_url = cleaned_url
                # elif url_key == 'zwgk/jdhy':
                else:
                    base_title_url = url[:45]
                annex_url_list = []
                if annexs:
                    for annex in annexs:
                        if not annex.xpath("./@href") or not annex.xpath("./text()"):
                            continue
                        annex_name = annex.xpath("./text()")[0]
                        annex_url = ''.join(annex.xpath("./@href")[0].strip('.'))
                        if "http" not in annex_url:
                            annex_url = base_title_url + annex_url
                        annex_url_list.append(annex_url)
                origin_annex_data = ''
                new_annex_data = ''
                if annex_url_list:
                    for annex_url in annex_url_list:
                        try:
                            annex_url_type = annex_url.split('.')[-1]
                            if annex_url_type == 'html':
                                continue
                            origin_annex_data += annex_url + ','
                            new_annex_url = upload_file_by_url(file_url=annex_url, file_name='1', file_type=annex_url_type,
                                                               type='other')
                            new_annex_data += new_annex_url + ','
                        except Exception as e:
                            continue
                origin = "贵州药品监督管理局"
                origin_domain = 'http://yjj.guizhou.gov.cn/'
                create_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                # 进行数据的去重
                data_unique = f"文章标题：{title_name}, 文章内容：{content_html}, 来源：{source}, 发布时间：{pub_date}"
                # 数据去重
                hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
                if not r.sismember("guizhou_yjj_set", hash_value):
                    # 不重复哈希值添加到集合中
                    r.sadd("guizhou_yjj_set", hash_value)
                    # 连接到测试库
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database="col_test"
                    )
                    cursor_test = conn_test.cursor()
                    # 将数据插入到指定表中
                    insert_sql = "INSERT INTO col_chief_public (title,title_url, content_html, path, summary, annex, origin_annex, source,pub_date, origin, origin_domain, create_date) VALUES (%s,%s,  %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"
                    cursor_test.execute(insert_sql, (
                        title_name,url, content_html, article_path, summary_str, new_annex_data, origin_annex_data, source, pub_date,
                        origin, origin_domain, create_date))
                    conn_test.commit()
                    cursor_test.close()
                    conn_test.close()
                    print(f"标题：{title_name}入库成功")
