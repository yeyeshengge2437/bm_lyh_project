import datetime
import random
import re
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from a_ktgg_api import judge_repeat_invest

co = ChromiumOptions()
# co = co.set_argument('--no-sandbox')
# co = co.headless()
co = co.set_user_data_path(r"D:\chome_data\ali_two")
co.set_paths(local_port=9155)
origin = '中国审判流程信息公告网'
origin_domain = 'splcgk.court.gov.cn'


def get_chinacourt_info(from_queue, webpage_id):
    page = ChromiumPage()
    page.get("https://splcgk.court.gov.cn/gzfwww//ktgg")
    page.wait(10)
    for i in range(1, 500):
        random_thing = random.randint(0, 3)
        if random_thing != 0:
            next_ele = page.ele("xpath=//span[@class='pageBtnWrap']/a[last()]")
        else:
            next_ele = page.ele("xpath=//span[@class='pageBtnWrap']/a[last()-1]")

        next_ele.click()
        random_num = random.randint(4, 10)
        page.wait(random_num)
        html_page = page.html
        html = etree.HTML(html_page)
        kt_list = html.xpath("//div[@id='compoment']/div[@class='fd-tab']/table/tbody/tr")
        if len(kt_list) >= 2:
            for kt in kt_list[1:]:
                content = "".join(kt.xpath("./td[@class='fd-tab-frist']//text()"))
                url = "https://splcgk.court.gov.cn/gzfwww//" + ''.join(kt.xpath("./td[@class='fd-tab-frist']/a/@href"))
                if judge_repeat_invest(url):
                    continue
                court_name = "".join(kt.xpath("./td[@class='fd-tab-two'][2]/text()"))
                release = "".join(kt.xpath("./td[4]//text()"))
                open_time = ''.join(re.findall(r"定于(.*?) 在", content))
                court_room = ''.join(re.findall(r"在(.*?)依法公开", content))
                members = ''.join(re.findall(r"开庭审理 (.*?)的.*?一案", content))
                cause = ''.join(re.findall(r"的(.*?)一案", content))
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 设置创建日期
                create_date = datetime.datetime.now().strftime('%Y-%m-%d')
                department = ''
                # 连接到测试库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col"
                )
                cursor_test = conn_test.cursor()
                # 将数据插入到表中
                insert_sql = "INSERT INTO col_case_open (court,  open_time, court_room, department, origin, origin_domain, create_time, create_date, from_queue, webpage_id) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                cursor_test.execute(insert_sql, (
                    court_name, open_time, court_room,
                    department,
                    origin,
                    origin_domain, create_time, create_date, from_queue, webpage_id))
                # print("插入成功")
                conn_test.commit()
                cursor_test.close()
                conn_test.close()
                print(
                    f"内容：{content} 案由：{cause} 开庭时间：{open_time} 法庭：{court_room} 当事人：{members} url：{url} 法院：{court_name} 发布时间：{release}\n")

    page.quit()


# get_chinacourt_info(11, 22)
