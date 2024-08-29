import hashlib
import json
import re
import time
from datetime import datetime
from api_chief import judge_url_repeat
import mysql.connector
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import redis
from lxml import etree

# 连接redis数据库
redis_conn = redis.Redis()

co = ChromiumOptions()

co = co.set_paths().auto_port()
co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless(True)  # 开启无头模式, 解决`浏览器无法连接`报错
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://dkjgfw.mnr.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://dkjgfw.mnr.gov.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_quanguoyichangminglu_data(queue_id, webpage_id):
    page = ChromiumPage()
    page.set.load_mode.none()
    try:
        json_data = {
            'dwGuid': None,
        }

        abnormal_response = requests.post(
            'https://dkjgfw.mnr.gov.cn/dks-webapi/site/DzkcAbnormalList/listNoLand',
            headers=headers,
            json=json_data,
        )
        all_datas = abnormal_response.json()
        if all_datas["succeed"] == "yes":
            origin = "全国地质勘察行业监管服务平台"
            uni_set = judge_url_repeat(origin)
            for data in all_datas["result"]:
                target_url = f'https://dkjgfw.mnr.gov.cn/#/detail/dwxxxq/2/1/{data["dwGuid"]}/{data["dwUnifiedCode"]}/ycml'
                if target_url not in uni_set:
                    uni_set.add(target_url)
                    tab = page.new_tab()
                    tab.get(target_url)
                    time.sleep(6)
                    content_html = etree.HTML(tab.html)
                    tab.close()
                    path = "".join(content_html.xpath("//div[@class='DwxxXq_link__1E0YW']//text()")).strip()
                    title = "异常名录记录主体：" + data['dwUnitName']
                    title_url = str(target_url)
                    summary = "".join(content_html.xpath(
                        "//div[@class='ant-col ant-col-20']/div[@class='DwxxXq_form__UIGQf']//text()")).strip()
                    content = {
                        '企业名称': data['dwUnitName'],
                        '异常名录认定依据': data['abnormalReason'],
                        '认定部门': data['abnormalRecDept'],
                        '列入异常名录日期': data['abnormalDate'],
                        '移出异常名录日期': data['unAbnormalDate'],
                        '统一社会信用代码': data['dwUnifiedCode'],
                        '地质勘查单位基本信息': {
                            '企业名称': data['dwUnitName'],
                            '法定代表人': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[1]/td[4]/text()")).strip(),
                            '机构类型': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[2]/td[2]/text()")).strip(),
                            '上级主管单位': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[2]/td[4]/text()")).strip(),
                            '公示联系人': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[3]/td[2]/text()")).strip(),
                            '联系电话': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[3]/td[4]/text()")).strip(),
                            '单位所在省': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[4]/td[2]/text()")).strip(),
                            '单位所在地详细地址': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[4]/td[4]/text()")).strip(),
                            '主要业务活动': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[5]/td[2]/text()")).strip(),
                            '高级地质技术人员(人)': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[6]/td[4=2]/text()")).strip(),
                            '中级地质技术人员(人)': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[6]/td[4]/text()")).strip(),
                            '单位简介': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[7]/td[2]//text()")).strip(),
                        },
                    }
                    content = json.dumps(content, ensure_ascii=False)
                    con_html = content_html.xpath("//div[@class='ant-col']")
                    cont_html = ''
                    for con in con_html:
                        cont_html += etree.tostring(con, encoding='utf-8').decode()
                    style_pattern = r'style="[^"]*"'
                    cont_html = re.sub(style_pattern, '', cont_html)
                    source = ''.join(content_html.xpath("//div[@class='DwxxJdXq_come-from__PBaRd']//text()")).strip()
                    source = source.replace("信息来源：", "")
                    pub_date = "".join(content_html.xpath("//div[@class='DwxxJdXq_pub-date__2F6iC']//text()")).strip()
                    pub_date = re.findall(r'\d{4}-\d{2}-\d{2}', pub_date)
                    if not pub_date:
                        pub_date = ''.join(content_html.xpath(
                            "//div[@class='ant-col']/div[@class='DwxxXq_push-time__kuJ4_']/div[@class='DwxxXq_pub-date__Ig2qZ']//text()")).strip()
                    try:
                        pub_date = re.findall(r'\d{4}-\d{2}-\d{2}', pub_date)[0]
                    except:
                        pub_date = None

                    origin_domain = "https://dkjgfw.mnr.gov.cn/"
                    uni_data = f'{str(title), str(content), str(origin_domain)}'
                    md5_key = hashlib.md5(json.dumps(uni_data).encode('utf-8')).hexdigest()
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    conn_test = mysql.connector.connect(
                        host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                        user="col2024",
                        password="Bm_a12a06",
                        database='col',
                    )
                    cursor_test = conn_test.cursor()
                    # if judge_url_repeat(url):
                    insert_sql = "INSERT INTO col_chief_public (title,title_url,summary, content,content_html, path,  source,pub_date, origin, origin_domain,create_date, md5_key, from_queue, webpage_id) VALUES (%s,%s, %s,%s,%s, %s,%s,%s,%s, %s, %s, %s,%s,%s)"
                    cursor_test.execute(insert_sql, (
                        title, title_url, summary, content, cont_html, path,
                        source, pub_date,
                        origin, origin_domain, create_date, md5_key, queue_id, webpage_id))
                    conn_test.commit()
                    # print(title, title_url, summary, content, cont_html, path)
                    cursor_test.close()
                    conn_test.close()
        page.quit()
    except Exception as e:
        page.quit()
        raise e


def get_quanguodizhikanchadanwei_data(queue_id, webpage_id):
    json_data = {
        'dwRegionCode': '',
        'searchValue': '',
        'dwBodytypeCodes': [],
        'dwOperstateCodes': [],
        'manageTypes': [],
        'moneyTypes': [],
        'projectTypes': [],
    }

    response = requests.post('https://dkjgfw.mnr.gov.cn/dks-webapi/site/listBasicInforPub', headers=headers,
                             json=json_data)
    all_datas = response.json()
    if all_datas["succeed"] == "yes":
        page = ChromiumPage()
        try:
            page.set.load_mode.none()
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database='col',
            )

            repeat = -9999
            origin = "全国地质勘察行业监管服务平台"
            uni_set = judge_url_repeat(origin)
            for data in all_datas["result"]:
                target_url = f'https://dkjgfw.mnr.gov.cn/#/detail/dwxxxq/3/1/{data["dwGuid"]}/{data["dwUnifiedCode"]}/zc'
                if target_url not in uni_set:
                    uni_set.add(target_url)
                    tab = page.new_tab()
                    tab.get(target_url)
                    tab.wait.doc_loaded()
                    time.sleep(5)
                    content_html = etree.HTML(tab.html)
                    tab.close()
                    path = "".join(content_html.xpath("//div[@class='DwxxXq_link__1E0YW']//text()")).strip()
                    title = "全国地质勘查单位:" + data['dwUnitName']
                    title_url = str(target_url)
                    summary = "".join(content_html.xpath(
                        "//div[@class='ant-col ant-col-20']/div[@class='DwxxXq_form__UIGQf']//text()")).strip()
                    content = {
                        '企业名称': data['dwUnitName'],
                        '法定代表人': data['dwResponsiblePerson'],
                        '统一社会信用代码': data['dwUnifiedCode'],
                        '机构类型': ''.join(content_html.xpath(
                            "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[2]/td[2]/text()")).strip(),
                        '主要业务活动': ''.join(content_html.xpath(
                            "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[5]/td[2]/text()")).strip(),
                        '地质勘查单位基本信息': {
                            '企业名称': data['dwUnitName'],
                            '法定代表人': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[1]/td[4]/text()")).strip(),
                            '机构类型': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[2]/td[2]/text()")).strip(),
                            '上级主管单位': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[2]/td[4]/text()")).strip(),
                            '公示联系人': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[3]/td[2]/text()")).strip(),
                            '联系电话': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[3]/td[4]/text()")).strip(),
                            '单位所在省': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[4]/td[2]/text()")).strip(),
                            '单位所在地详细地址': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[4]/td[4]/text()")).strip(),
                            '主要业务活动': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[5]/td[2]/text()")).strip(),
                            '高级地质技术人员(人)': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[6]/td[4=2]/text()")).strip(),
                            '中级地质技术人员(人)': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[6]/td[4]/text()")).strip(),
                            '单位简介': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[7]/td[2]//text()")).strip().strip(
                                '... 更多'),
                        },
                    }
                    content = json.dumps(content, ensure_ascii=False)
                    con_html = content_html.xpath("//div[@class='ant-col']")
                    cont_html = ''
                    for con in con_html:
                        cont_html += etree.tostring(con, encoding='utf-8').decode()
                    style_pattern = r'style="[^"]*"'
                    cont_html = re.sub(style_pattern, '', cont_html)
                    source = ''.join(content_html.xpath("//div[@class='DwxxJdXq_come-from__PBaRd']//text()")).strip()
                    source = source.replace("信息来源：", "")
                    pub_date = "".join(content_html.xpath("//div[@class='DwxxJdXq_pub-date__2F6iC']//text()")).strip()
                    pub_date = re.findall(r'\d{4}-\d{2}-\d{2}', pub_date)
                    if not pub_date:
                        pub_date = ''.join(content_html.xpath(
                            "//div[@class='ant-col']/div[@class='DwxxXq_push-time__kuJ4_']/div[@class='DwxxXq_pub-date__Ig2qZ']//text()")).strip()
                    try:
                        pub_date = re.findall(r'\d{4}-\d{2}-\d{2}', pub_date)[0]
                    except:
                        pub_date = None
                    origin = "全国地质勘察行业监管服务平台"
                    origin_domain = "https://dkjgfw.mnr.gov.cn/"
                    uni_data = f'{str(title), str(content), str(origin_domain)}'
                    md5_key = hashlib.md5(json.dumps(uni_data).encode('utf-8')).hexdigest()
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    cursor_test = conn_test.cursor()
                    insert_sql = "INSERT INTO col_chief_public (title,title_url,summary, content,content_html, path,  source,pub_date, origin, origin_domain,create_date, md5_key, from_queue, webpage_id) VALUES (%s,%s, %s,%s,%s, %s,%s,%s,%s, %s, %s, %s,%s,%s)"
                    cursor_test.execute(insert_sql, (
                        title, title_url, summary, content, cont_html, path,
                        source, pub_date,
                        origin, origin_domain, create_date, md5_key, queue_id, webpage_id))
                    conn_test.commit()
                    cursor_test.close()

                else:
                    repeat += 1
                    if repeat == 100:
                        break

            conn_test.close()
            page.quit()
        except Exception as e:
            page.quit()
            raise e


def get_yanzhongshixinmingdan_data(queue_id, webpage_id):
    json_data = {
        'dwGuid': None,
    }

    response = requests.post('https://dkjgfw.mnr.gov.cn/dks-webapi/site/DzkcBlackList/listNoLand', headers=headers,
                             json=json_data)
    all_datas = response.json()
    if all_datas["succeed"] == "yes":
        page = ChromiumPage()
        try:
            page.set.load_mode.none()
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database='col',
            )

            repeat = -9999
            origin = "全国地质勘察行业监管服务平台"
            uni_set = judge_url_repeat(origin)
            for data in all_datas["result"]:
                target_url = f'https://dkjgfw.mnr.gov.cn/#/detail/dwxxxq/1/1/{data["dwGuid"]}/{data["dwUnifiedCode"]}/hmd'

                if target_url not in uni_set:
                    uni_set.add(target_url)
                    tab = page.new_tab()
                    tab.get(target_url)
                    tab.wait.doc_loaded()
                    time.sleep(5)
                    content_html = etree.HTML(tab.html)
                    tab.close()
                    path = "".join(content_html.xpath("//div[@class='DwxxXq_link__1E0YW']//text()")).strip()
                    title = "全国严重失信主体:" + data['dwUnitName']
                    title_url = str(target_url)
                    summary = "".join(content_html.xpath(
                        "//div[@class='ant-col ant-col-20']/div[@class='DwxxXq_form__UIGQf']//text()")).strip()
                    content = {
                        '企业名称': data['dwUnitName'],
                        '严重失信主体名单认定依据': data['abnormalReason'],
                        '认定部门': data['abnormalRecDept'],
                        '列入严重失信主体名单日期': data['abnormalDate'],
                        '移出严重失信主体名单日期': data['unAbnormalDate'],
                        '地质勘查单位基本信息': {
                            '企业名称': data['dwUnitName'],
                            '法定代表人': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[1]/td[4]/text()")).strip(),
                            '机构类型': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[2]/td[2]/text()")).strip(),
                            '上级主管单位': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[2]/td[4]/text()")).strip(),
                            '公示联系人': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[3]/td[2]/text()")).strip(),
                            '联系电话': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[3]/td[4]/text()")).strip(),
                            '单位所在省': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[4]/td[2]/text()")).strip(),
                            '单位所在地详细地址': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[4]/td[4]/text()")).strip(),
                            '主要业务活动': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[5]/td[2]/text()")).strip(),
                            '高级地质技术人员(人)': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[6]/td[4=2]/text()")).strip(),
                            '中级地质技术人员(人)': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[6]/td[4]/text()")).strip(),
                            '单位简介': ''.join(content_html.xpath(
                                "//div/table[@class='DwxxXq_DkxxTable__a8Fgo']/tbody/tr[7]/td[2]//text()")).strip().strip(
                                '... 更多'),
                        },
                    }
                    content = json.dumps(content, ensure_ascii=False)
                    con_html = content_html.xpath("//div[@class='ant-col']")
                    cont_html = ''
                    for con in con_html:
                        cont_html += etree.tostring(con, encoding='utf-8').decode()
                    style_pattern = r'style="[^"]*"'
                    cont_html = re.sub(style_pattern, '', cont_html)
                    source = ''.join(content_html.xpath("//div[@class='DwxxJdXq_come-from__PBaRd']//text()")).strip()
                    source = source.replace("信息来源：", "")
                    pub_date = "".join(content_html.xpath("//div[@class='DwxxJdXq_pub-date__2F6iC']//text()")).strip()
                    pub_date = re.findall(r'\d{4}-\d{2}-\d{2}', pub_date)
                    if not pub_date:
                        pub_date = ''.join(content_html.xpath(
                            "//div[@class='ant-col']/div[@class='DwxxXq_push-time__kuJ4_']/div[@class='DwxxXq_pub-date__Ig2qZ']//text()")).strip()
                    try:
                        pub_date = re.findall(r'\d{4}-\d{2}-\d{2}', pub_date)[0]
                    except:
                        pub_date = None

                    origin_domain = "https://dkjgfw.mnr.gov.cn/"
                    uni_data = f'{str(title), str(content), str(origin_domain)}'
                    md5_key = hashlib.md5(json.dumps(uni_data).encode('utf-8')).hexdigest()
                    create_date = datetime.now().strftime('%Y-%m-%d')
                    cursor_test = conn_test.cursor()
                    insert_sql = "INSERT INTO col_chief_public (title,title_url,summary, content,content_html, path,  source,pub_date, origin, origin_domain,create_date, md5_key, from_queue, webpage_id) VALUES (%s,%s, %s,%s,%s, %s,%s,%s,%s, %s, %s, %s,%s,%s)"
                    cursor_test.execute(insert_sql, (
                        title, title_url, summary, content, cont_html, path,
                        source, pub_date,
                        origin, origin_domain, create_date, md5_key, queue_id, webpage_id))
                    conn_test.commit()
                    cursor_test.close()

                else:
                    repeat += 1
                    if repeat == 20:
                        break

            conn_test.close()
            page.quit()
        except Exception as e:
            page.quit()
            raise e

