import json
import time
from datetime import datetime

import mysql.connector
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import redis
from lxml import etree

# 连接redis数据库
redis_conn = redis.Redis()

co = ChromiumOptions()

co = co.set_paths().auto_port()
# co = co.set_argument('--no-sandbox')  # 关闭沙箱模式, 解决`$DISPLAY`报错
co = co.headless()  # 无头模式
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
page = ChromiumPage()
page.set.load_mode.none()


def get_quanguoyichangminglu_data():
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
        for data in all_datas["result"]:
            target_url = f'https://dkjgfw.mnr.gov.cn/#/detail/dwxxxq/2/1/{data["dwGuid"]}/{data["dwUnifiedCode"]}/ycml'
            tab = page.new_tab()
            tab.get(target_url)
            time.sleep(6)
            content_html = etree.HTML(tab.html)
            path = "".join(content_html.xpath("//div[@class='DwxxXq_link__1E0YW']//text()")).strip()
            title = "异常名录记录主体：" + data['dwUnitName']
            title_url = str(target_url)
            summary = "".join(content_html.xpath("//div[@class='ant-col ant-col-20']/div[@class='DwxxXq_form__UIGQf']//text()")).strip()
            content = {
                '企业名称': data['dwUnitName'],
                '异常名录认定依据': data['abnormalReason'],
                '认定部门': data['abnormalRecDept'],
                '列入异常名录日期': data['abnormalDate'],
                '移出异常名录日期': data['unAbnormalDate'],
                '统一社会信用代码': data['dwUnifiedCode']
            }
            content = json.dumps(content, ensure_ascii=False)
            con_html = content_html.xpath("//div[@class='ant-col']")
            cont_html = ''
            for con in con_html:
                cont_html += etree.tostring(con, encoding='utf-8').decode()
            source = ''.join(content_html.xpath("//div[@class='DwxxJdXq_come-from__PBaRd']//text()")).strip()
            source = source.replace("信息来源：", "")
            pub_date = "".join(content_html.xpath("//div[@class='DwxxJdXq_pub-date__2F6iC']//text()")).strip()
            pub_date = pub_date.replace("时间：", "")
            origin = "全国地质勘察行业监管服务平台"
            origin_domain = "https://dkjgfw.mnr.gov.cn/"
            print(title, path, title_url, summary, content, source, pub_date, origin, origin_domain)
            create_date = datetime.now().strftime('%Y-%m-%d')
            conn_test = mysql.connector.connect(
                host="rm-bp1u9285s2m2p42t08o.mysql.rds.aliyuncs.com",
                user="col2024",
                password="Bm_a12a06",
                database='col_test',
            )
            cursor_test = conn_test.cursor()
            # if judge_url_repeat(url):
            insert_sql = "INSERT INTO col_chief_public (title,title_url,summary, content,content_html, path,  source,pub_date, origin, origin_domain,create_date) VALUES (%s,%s, %s,%s,%s, %s, %s, %s, %s,%s,%s)"
            cursor_test.execute(insert_sql, (
                title, title_url, summary, content, cont_html, path,
                source, pub_date,
                origin, origin_domain, create_date))
            conn_test.commit()
            cursor_test.close()
            conn_test.close()


get_quanguoyichangminglu_data()
page.quit()
