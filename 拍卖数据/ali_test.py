import json
import os
import random
import re
import time
from datetime import datetime, timedelta
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from urllib.parse import urlencode, urljoin
from typing import Dict


def save_to_json(data: Dict, filename: str = "data.json") -> None:
    """
    将数据追加到 JSON 文件，每次保存完整数据
    :param data: 要保存的字典数据，需包含 url, url_name, state
    :param filename: JSON 文件名 (默认: data.json)
    """
    # 如果文件不存在则初始化空列表
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)

    # 读取现有数据
    with open(filename, 'r') as f:
        existing_data = json.load(f)

    # 检查重复（根据 url 去重）
    urls = {item['url'] for item in existing_data}
    if data['url'] not in urls:
        existing_data.append(data)
    else:
        # 如果已存在，可以选择更新状态（可选）
        for item in existing_data:
            if item['url'] == data['url']:
                item.update(data)
                break

    # 写入更新后的数据
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=True)


co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\ali_two")
# co = co.set_argument('--no-sandbox')
# co = co.headless()
co.set_paths(local_port=9153)

codes = ["321100", "320200", "320600", "320700", "320800", "320900", "321000", "320300",
         "320400", "321200", "321300", "330600", "330100", "330200", "330800", "330700", "330400", "330300",
         "330500", "331000", "330900", "331100", "110100", "410900", "410200", "410100", "410600", "410300",
         "411200", "410800", "410500", "411000", "411100", "410400", "411300", "411400", "410700", "411600",
         "411700", "411500", "410881", "441900", "440500", "440100", "440400", "442000", "440300", "440700",
         "440600", "440800", "440200", "441800", "441300", "441600", "440900", "441700", "445100", "441400",
         "445200", "441200", "445300", "442101", "441500", "510700", "510100", "512000", "511300", "511700",
         "513300", "511100", "511400", "511000", "510900", "511600", "511500", "510600", "513200", "511900",
         "511800", "510500", "513400", "510800", "510400", "510300", "371400", "371000", "370700", "371100",
         "371500", "370500", "371700", "370800", "370300", "370100", "370900", "370200", "371300", "371600",
         "370600", "370400", "371200", "450500", "450800", "450300", "450900", "450100", "450400", "450200",
         "451300", "451400", "451100", "450700", "450600", "451000", "451200", "530100", "530400", "532500",
         "530300", "532300", "532900", "532600", "533100", "530900", "530700", "530800", "533300", "533400",
         "532800", "530500", "530600", "520300", "522600", "522400", "520100", "520200", "522700", "522200",
         "522300", "520400", "500100", "430100", "431000", "431200", "430600", "430700", "430400", "433100",
         "430500", "430900", "430300", "431100", "431300", "430200", "430800", "350700", "350200", "350500",
         "350300", "350100", "350600", "350800", "350400", "350900", "210700", "210600", "210200", "210100",
         "211400", "210300", "210900", "211300", "210500", "211000", "210800", "211200", "210400", "211100",
         "340100", "341100", "340800", "340300", "341700", "341000", "340200", "340500", "340400", "341300",
         "341200", "340700", "341500", "340600", "341800", "341600", "310100", "360800", "360300", "360100",
         "360400", "361100", "360600", "360700", "360900", "360200", "361000", "360500", "150100", "150600",
         "150200", "152500", "150500", "150400", "150700", "152900", "150800", "150300", "152200", "150900",
         "230100", "231100", "231200", "231000", "230400", "232700", "230600", "230700", "230500", "230300",
         "230200", "230900", "230800", "420100", "421100", "420800", "420900", "421300", "420300", "420500",
         "421000", "420600", "420200", "429005", "421200", "429021", "429006", "429004", "422800", "420700",
         "610100", "610400", "610800", "610500", "610300", "610700", "610600", "610900", "610200", "611000",
         "130100", "130300", "130700", "130600", "131000", "130800", "130900", "130400", "130500", "131100",
         "130200", "621200", "620400", "620900", "620700", "620100", "620500", "620300", "620800", "622900",
         "620600", "621100", "620200", "623000", "621000", "222400", "220100", "220300", "220200", "220800",
         "220400", "220700", "220600", "220500", "460100", "460200", "469028", "469027", "469026", "469025",
         "469039", "469038", "469037", "469036", "469035", "469034", "469033", "469031", "469030", "460300",
         "469006", "469005", "469003", "469002", "469001", "469007", "140100", "141000", "141100", "140400",
         "140500", "140600", "140800", "140700", "140900", "140300", "140200", "120100", "640300", "640100",
         "640200", "640500", "640400", "650100", "652900", "652300", "653000", "652200", "652100", "654300",
         "653200", "652800", "652700", "659011", "659010", "659005", "659004", "659003", "659002", "659009",
         "659008", "659007", "659006", "659001", "650200", "654200", "653100", "654000", "632100", "632800",
         "632700", "632600", "632500", "630100", "632300", "632200", "542200", "542300", "542100", "542600",
         "540100", "542400", "542500", "810200", "810300", "810100", "820200", "820100", "711100", "710300",
         "710500", "710400", "712800", "711700", "711500", "712700", "710700", "711900", "710600", "711200",
         "710100", "712400", "711400", "712600", "711300", "712500", "710200", "712100", "710900", "710800",
         "990100", "320100", "320500"]
page = ChromiumPage(co)
# search_value = '（2024）苏1081执恢412号'
for code in codes:
    for status_orders in [2, 1, 0, 6]:
    # for status_orders in [6]:
        page_num = 0
        while True:
            tab_1 = page.new_tab()
            page_num += 1
            print(f"第{page_num}页")
            url = "https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch"
            params = {
                "disableNav": "YES",
                "page": f"{page_num}",
                "pmid": "2175852518_1653962822378",
                "pmtk": "20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879",
                "path": "27181431,27076131,25287064,27064540",
                "spm": "a2129.27064540.puimod-zc-focus-2021_2860107850.category-4-5",
                "fcatV4Ids": "[\"206067301\"]",
                "statusOrders": f"[\"{status_orders}\"]",
                "locationCodes": f"[\"{code}\"]"
            }
            # 将参数字典转换为URL编码的字符串
            query_string = urlencode(params)
            # 将查询字符串附加到基础URL后面
            full_url = urljoin(url, '?' + query_string)
            # print(full_url)
            # input()
            tab_1.get(full_url)
            tab_1.wait(2)
            tab_1.scroll.to_bottom()
            time.sleep(2)
            info_list = tab_1.eles("xpath=//div[@id='guid-2004318340']//div/a")
            if not info_list:
                tab_1.close()
                break
            for info in info_list:
                url = info.attr("href")
                url_name = info.ele("xpath=/div[2]/div[1]/span[@class='text']/text()")
                if status_orders == 2:
                    start = '已结束'
                elif status_orders == 1:
                    start = '即将开始'
                elif status_orders == 0:
                    start = '正在进行'
                else:
                    start = '招商中'
                if start == '已结束' and 'zc/mn_detail.htm' in url:
                    continue
                value_data = {
                    "url": url,
                    "url_name": url_name,
                    "start": start
                }
                save_to_json(value_data, 'tb_all_url_data.json')
                print(value_data)
            tab_1.close()
