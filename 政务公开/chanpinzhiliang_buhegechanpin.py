# 国家市场监督管理总局产品质量安全监督管理局----监督抽查不合格产品发布
# 按照时间顺序进行排列，连续检测到十条为数据库中拥有的数据，则完成该天的数据更新 (未实现)
# webid 在indexhtml中定义
# tplSetId 在index.html中定义
# pageId 在index.html中定义
# 改变页码以上三个不会变
import hashlib
import json
import time
import mysql.connector
import requests
import re
from lxml import etree
from api_chief import upload_file_by_url, judge_url_repeat, paper_queue_next, paper_queue_success, paper_queue_fail

cookies = {
    '__jsluid_s': '1a5c60a35858f73b7f26c40f617df13c',
    'Hm_lvt_54db9897e5a65f7a7b00359d86015d8d': '1724919146,1725346994',
    'HMACCOUNT': 'FDD970C8B3C27398',
    'Hm_lpvt_54db9897e5a65f7a7b00359d86015d8d': '1725355091',
}

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': '__jsluid_s=1a5c60a35858f73b7f26c40f617df13c; Hm_lvt_54db9897e5a65f7a7b00359d86015d8d=1724919146,1725346994; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_54db9897e5a65f7a7b00359d86015d8d=1725355091',
    'Pragma': 'no-cache',
    'Referer': 'https://www.samr.gov.cn/zljds/jdcc/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_buhegechanpin_data(queue_id, webpage_id):
    response = requests.get('https://www.samr.gov.cn/zljds/jdcc/index.html', headers=headers)
    origin = '国家市场监督管理总局产品质量安全监督管理司'
    url_set = judge_url_repeat(origin)
    if response.status_code == 200:
        page_num = 1
        re_data = response.text
        webId = re.findall(r"'webId':'(.*?)'", re_data)[0]
        tplSetId = re.findall(r"'tplSetId':'(.*?)'", re_data)[0]
        pageId = re.findall(r"'pageId':'(.*?)'", re_data)[0]
        while True:
            paramjson = {"pageNo": page_num, "pageSize": 50}
            paramjson = str(paramjson)

            params = {
                'webId': webId,
                'pageId': pageId,
                'parseType': 'bulidstatic',
                'pageType': 'column',
                'tagId': 'ajax分页',
                'tplSetId': tplSetId,
                'paramJson': paramjson,
            }

            response = requests.get(
                'https://www.samr.gov.cn/api-gateway/jpaas-publish-server/front/page/build/unit',
                params=params,
                headers=headers,
            )
            if response.status_code == 200:
                html = response.json()["data"]["html"]
                html = etree.HTML(html)
                data_list = html.xpath("//li[@class='content-3-left-text imgContent01new']")
                count_num = len(data_list)
                if count_num == 0:
                    break
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database='col'
                )
                cursor_test = conn_test.cursor()
                for data in data_list:

                    origin_domain = 'https://www.samr.gov.cn/zljds'
                    title = ''.join(data.xpath("./a/text()"))
                    title_url = 'https://www.samr.gov.cn' + ''.join(data.xpath("./a/@href"))
                    if title_url not in url_set:
                        pub_time = ''.join(data.xpath("./div[@class='contentRight01time']/text()"))
                        if pub_time == "2023-04-28":
                            conn_test.close()
                            return True
                        title_res = requests.get(title_url, headers=headers)
                        if title_res.status_code == 200:
                            time.sleep(1)
                            title_html = etree.HTML(title_res.text)
                            path = ''.join(
                                title_html.xpath("//div[@class='wrapper']/div[@class='Second_banner']/ul/li//text()"))
                            content = ''.join(title_html.xpath("//div[@class='zt_xilan_07']//text()")).strip()
                            content = re.sub(r'(.TRS_Editor\s*[^{]*\{.*?})', '', content, flags=re.MULTILINE)
                            content_ht = title_html.xpath("//div[@class='zt_xilan_07']")
                            content_html = ''
                            for cont in content_ht:
                                content_html += etree.tostring(cont, method='html', encoding='unicode')
                            annex_list = ''
                            up_annex_list = ''
                            # 附件的处理
                            annexs = title_html.xpath("//div[@class='TRS_Editor']//a/@href")
                            if not annexs:
                                annexs = title_html.xpath("//p[@class='MsoNormal']//a/@href")
                            annexs_num = len(annexs)
                            if annexs_num > 0:
                                if annexs_num == 1:
                                    annex = 'https://www.samr.gov.cn' + annexs[0]
                                    annex_url_type = annex.split('.')[-1]
                                    annex_value = upload_file_by_url(annex, "bhgcp", annex_url_type, type="other")
                                    annex_list += annex
                                    up_annex_list += annex_value
                                else:
                                    for annex in annexs:
                                        annex = 'https://www.samr.gov.cn' + annex
                                        annex_url_type = annex.split('.')[-1]
                                        annex_value = upload_file_by_url(annex, "bhgcp", annex_url_type, type="other")
                                        annex_list += annex + ','
                                        up_annex_list += annex_value + ','
                            else:
                                annex_list = ''
                            annex_list = str(annex_list)
                            source = ''.join(title_html.xpath(
                                "//div[@class='zt_xilan_02']/ul[1]/li[@class='zt_xilan_04']/text()")).strip()
                            try:
                                source = re.findall(r'信息来源：(.*?)$', source)[0]
                            except:
                                source = '质检总局'
                            create_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                            # 进行数据的去重
                            data_unique = f"文章标题：{title}, 文章内容：{content_html}, 来源：{source}, 发布时间：{pub_time}"
                            # 数据去重
                            hash_value = hashlib.md5(json.dumps(data_unique).encode('utf-8')).hexdigest()
                            insert_sql = "INSERT INTO col_chief_public (title,title_url, content,content_html, path,  origin_annex, annex, source,pub_date, origin, origin_domain, create_date,from_queue, webpage_id,md5_key) VALUES (%s,%s, %s, %s,%s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"

                            cursor_test.execute(insert_sql, (
                                title, title_url, content, content_html, path,
                                annex_list, up_annex_list,
                                source, pub_time,
                                origin, origin_domain, create_date, queue_id, webpage_id, hash_value))

                            conn_test.commit()
                            # print(title, title_url, content, content_html, path)
                        url_set.add(title_url)
                cursor_test.close()
                conn_test.close()
            else:
                print("响应失败")
                return response.status_code
            page_num += 1

# get_buhegechanpin_data(111,222)

# paper_queue = paper_queue_next(webpage_url_list=["https://www.samr.gov.cn/zljds/jdcc/index.html"])
# if paper_queue is None or len(paper_queue) == 0:
#     time.sleep(180)
#     pass
# else:
#     queue_id = paper_queue['id']
#     webpage_id = paper_queue["webpage_id"]
#     webpage_url = paper_queue["webpage_url"]
#     try:
#         get_buhegechanpin_data(queue_id, webpage_id)
#         data = {
#             "id": queue_id,
#             'description': f'数据获取成功',
#         }
#         paper_queue_success(data=data)
#     except Exception as e:
#         print(e)
#         data = {
#             "id": queue_id,
#             'description': f'程序异常:{e}',
#         }
#         paper_queue_fail(data=data)
