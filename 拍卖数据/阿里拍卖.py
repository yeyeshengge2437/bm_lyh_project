import random
import re
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from urllib.parse import urlencode, urljoin
import redis
from DrissionPage.common import Settings
import tempfile

co = ChromiumOptions()
# 禁用全局自动化特征
Settings.smart_launch = False
Settings.ignore_certificate_errors = True
# options.set_argument('--disable-blink-features=AutomationControlled')
co.set_argument('--incognito')
co.set_argument(f'--user-data-dir={tempfile.mkdtemp()}')
co = co.set_user_data_path(r"D:\chome_data\ali_two")
# co = co.set_argument('--no-sandbox')
# co = co.headless()
# co.set_paths(local_port=9153)

r = redis.Redis(host='localhost', port=6379, db=0)
zip_code = ["321100", "320200", "320600", "320700", "320800", "320900", "321000", "320300",
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


def judge_redis_is_value(r, db_row_name):
    """
    判断redis的目标表中是否有值
    :return:
    """
    list_length = r.llen(db_row_name)
    if list_length > 0:
        return
    else:
        # 将值写入
        zip_code = ["320100", "320500", "321100", "320200", "320600", "320700", "320800", "320900", "321000", "320300",
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
                    "990100", ]
        for value in zip_code:
            r.lpush(db_row_name, value)


def judge_repeat(url_href):
    """
    判断链接是否重复
    :return:
    """
    # 创建版面链接集合
    bm_url_set = set()
    # 连接数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    # cursor_test.execute(f"SELECT id, url, state FROM col_judicial_auctions")
    cursor_test.execute(f"SELECT id, state FROM col_judicial_auctions WHERE url = '{url_href}' LIMIT 1;")
    rows = cursor_test.fetchall()
    cursor_test.close()
    conn_test.close()
    if rows:
        id = rows[0][0]
        state = rows[0][1]
        return state, id
    else:
        return False, 0


# print(judge_repeat("https://susong-item.taobao.com/auction/859496335177.htm"))

# def encounter_verify(tab):
#     # 随机0.15到1之间的数
#     num = random.uniform(0.15, 1)
#     if "亲，请拖动下方滑块完成验证" in tab.html:
#         tab.wait(2)
#         slider_loc = tab.ele("xpath=//span[@id='nc_1_n1z']")
#         print(slider_loc.rect.location)
#         tab.actions.hold(slider_loc).move_to((1000, 504), duration=num).release()
#         tab.wait(2)
#         if "验证失败" in tab.html:
#             tab.ele("验证失败").click(by_js=None)
#             if "验证失败" in tab.html:
#                 tab.ele("验证失败").click(by_js=None)
#             if "请按住滑块" in tab.html:
#                 tab.refresh()
#                 encounter_verify(tab)
#     return tab
def split_length(total_length):
    total_length = int(total_length) + 1
    # 生成三个随机分割点
    splits = sorted(random.sample(range(1, total_length), 3))

    # 计算每段的长度
    lengths = [splits[0], splits[1] - splits[0], splits[2] - splits[1], total_length - splits[2]]

    # 返回每段的长度区间
    return lengths


def split_number_into_n_parts(total, n):
    # 确保total大于0且可以被分成n个非负数
    if total <= 0 or n <= 0:
        raise ValueError("Total must be positive and n must be a positive integer.")

    # 生成n-1个随机数并将它们累加
    parts = [random.uniform(0, total) for _ in range(n - 1)]
    sum_of_generated_parts = sum(parts)

    # 为了避免浮点运算误差，确保最后一部分直接计算以保证总和准确
    remaining = total - sum_of_generated_parts
    parts.append(remaining)

    # 如果需要确保都是正数且总和完全精确等于total，可以考虑调整生成策略或后续处理
    return parts


def valley_sort(nums):
    nums = sorted(nums)
    mid = len(nums) // 2
    # 如果列表长度是奇数，包含中间值两次；如果是偶数，则正常处理
    valley_list = nums[mid::-1] + nums[mid + 1:] + nums[mid:mid + 1] if len(nums) % 2 == 1 else nums[mid::-1] + nums[
                                                                                                                mid:]
    return valley_list


def pass_slider(page):
    slider_btn = page.ele('#nc_1_n1z')
    slider_btn_width = slider_btn.rect.size[0]
    slider_width = page.ele('.nc-lang-cnt').rect.size[0]

    # ac = Actions(page)
    ac = page.actions
    ac.hold(slider_btn)
    steps = valley_sort(split_number_into_n_parts(slider_width - slider_btn_width, 5))
    for step in steps:
        print(step)
        ac.move(step, offset_y=random.randint(-12, 12), duration=random.uniform(0.2, 0.5))
        # ac.wait(random.uniform(0.9, 1.1))
    page.wait(2)


def encounter_verify(tab):
    tab.wait(3)
    # 随机0.15到1之间的数
    num = random.uniform(0.1, 0.2)
    if "亲，请拖动下方滑块完成验证" in tab.html:
        # 获取结束位置
        end_loc = tab.ele("xpath=//div[@id='nc_1__scale_text']")
        loc_value = end_loc.rect.corners
        print(f"滑动区域的方位：{loc_value}")
        right_up = loc_value[1]
        right_down = loc_value[3]
        tager_x = right_up[0]
        tager_y = (right_up[1] + right_down[1] // 2) + random.randint(-50, 50)
        # input()
        tab.wait(2)
        slider_loc = tab.ele("xpath=//span[@id='nc_1_n1z']")
        loc_slider = slider_loc.rect.location
        print(f"滑块位置大小：{loc_slider}")
        print(f"滑动的长度：{tager_x}")
        # 原始滑动方式
        tab.actions.hold(slider_loc).move_to((tager_x, tager_y), duration=num).release()
        ran_value = random.randint(0, 1)
        # if ran_value == 0:
        #     pass_slider(tab)
        # else:
        #     tab.actions.hold(slider_loc).move_to((tager_x, tager_y), duration=0.2).release()


        # slider_loc.run_js(f"""
        #     var slider = this;
        #     var targetX = arguments[0];
        #     var duration = 1000; // 动画持续时间，单位毫秒
        #     var startTime = performance.now();
        #     var vibrationAmplitude = 5; // 抖动幅度
        #     var vibrationFrequency = 4; // 抖动频率
        #
        #     // 变加速到变减速的公式
        #     function easing(t) {{
        #         return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        #     }}
        #
        #     var move = function(to, duration) {{
        #         var start = slider.offsetLeft,
        #             change = to - start,
        #             startTime = performance.now();
        #         var animate = function() {{
        #             var timeElapsed = performance.now() - startTime;
        #             var run = Math.min(timeElapsed / duration, 1);
        #             var progress = easing(run);
        #
        #             var currentX = start + change * progress;
        #
        #             // y轴抖动效果
        #             var vibrationPhase = (timeElapsed / 1000) * vibrationFrequency;
        #             var yVibration = Math.sin(vibrationPhase) * vibrationAmplitude;
        #
        #             // 设置元素的新位置
        #             slider.style.transform = 'translate3d(' + currentX + 'px, ' + slider.offsetTop + 'px, 0)';
        #
        #             if (run < 1) {{
        #                 requestAnimationFrame(animate);
        #             }} else {{
        #                 // 到达目标位置后，模拟鼠标释放事件
        #                 slider.dispatchEvent(new MouseEvent('mouseup', {{
        #                     view: window,
        #                     bubbles: true,
        #                     cancelable: true,
        #                     clientX: slider.getBoundingClientRect().right,
        #                     clientY: slider.getBoundingClientRect().top + slider.offsetHeight / 2
        #                 }}));
        #                 slider.style.transform = 'translate3d(' + to + 'px, ' + slider.offsetTop + 'px, 0)';
        #             }}
        #         }};
        #         requestAnimationFrame(animate);
        #
        #         // 模拟鼠标按下事件，开始拖动
        #         slider.dispatchEvent(new MouseEvent('mousedown', {{
        #             view: window,
        #             bubbles: true,
        #             cancelable: true,
        #             clientX: slider.getBoundingClientRect().left,
        #             clientY: slider.getBoundingClientRect().top + slider.offsetHeight / 2
        #         }}));
        #     }};
        #     move(targetX, duration); // 1000毫秒内完成拖动
        # """, tager_x)
        tab.wait(2)
        if "验证失败" in tab.html:
            tab.ele("验证失败").click(by_js=None)
            if "验证失败" in tab.html:
                tab.ele("验证失败").click(by_js=None)
            if "请按住滑块" in tab.html:
                tab.refresh()
                encounter_verify(tab)
    return tab


def judge_repeat_invest(url_href):
    """
    判断链接是否重复
    :return:
    """
    # 创建版面链接集合
    bm_url_set = set()
    # 连接数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col",
    )
    cursor_test = conn_test.cursor()
    # 获取版面来源的版面链接
    # cursor_test.execute(f"SELECT id, url, state FROM col_judicial_auctions")
    cursor_test.execute(f"SELECT id FROM col_judicial_auctions_investing WHERE url = '{url_href}' LIMIT 1;")
    rows = cursor_test.fetchall()
    if rows:
        return True
    else:
        return False


def time_str_to_date(time_str, add=True):
    # 分割字符串并提取天数、小时、分钟和秒
    days = int(time_str.split('天')[0])
    hours = int(time_str.split('天')[1].split('时')[0])
    minutes = int(time_str.split('时')[1].split('分')[0])
    seconds = float(time_str.split('分')[1].split('秒')[0])

    # 将天数转换为小时，并与小时数相加
    total_hours = days * 24 + hours
    base_time = datetime.now()
    # 将总小时数、分钟数和秒数转换为timedelta对象并加到基础时间点上
    time_delta = timedelta(hours=total_hours, minutes=minutes, seconds=seconds)
    if add:
        result_time = base_time + time_delta
    else:
        result_time = base_time - time_delta

    return str(result_time)


def ali_paimai(from_queue):
    page = ChromiumPage(co)
    judge_redis_is_value(r, "paimai_raw_list")
    if r.llen('paimai_list') == 0:
        # 复制值到目标表上
        elements = r.lrange("paimai_raw_list", 0, -1)
        # 反转元素顺序
        elements = elements[::-1]
        # 将元素添加到目标列表
        for element in elements:
            r.rpush("paimai_list", element)
    while r.llen('paimai_list') > 0:
        code = r.lindex('paimai_list', 0)
        code = code.decode('utf-8')
        # print(code, "开始")
        for status_orders in [2, 1, 0, 6]:
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
                tab_1.get(full_url)
                tab_1.wait(2)
                info_list = tab_1.eles("xpath=//div[@id='guid-2004318340']//div/a")
                if not info_list:
                    tab_1.close()
                    break
                if status_orders == 6:
                    for info in info_list:
                        data_dict = {}
                        href_text = info.text
                        if "同类商品" not in href_text:
                            title = info.ele("xpath=/div/div/span[@class='text']")
                            if title:
                                data_dict["标题"] = title.text
                            href_url = info.attr("href")
                            url_text = re.sub(r"&.*", "", href_url)
                            if judge_repeat_invest(url_text):
                                continue
                            tab_2 = page.new_tab()
                            tab_2.get(href_url)
                            # tab_2.get("https://zc-paimai.taobao.com/zc/mn_detail.htm?id=180386&spm=a2129.27076131.puimod-pc-search-list_2004318340.25&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431%2C27076131&track_id=f36ba7d9-e768-4e22-9342-0ee897b09fd4")
                            data_dict["链接"] = url_text
                            tab_2.wait(2)
                            tab_2 = encounter_verify(tab_2)
                            tab_2.wait(2)
                            info_html = tab_2.html
                            info_etree = etree.HTML(info_html)
                            for num in range(1, 16 + 1):
                                key = info_etree.xpath(
                                    f"//div[@class='notice-detail']/table/tbody/tr[{num}]/td[@class='odd']")
                                if key:
                                    key_str = "".join(key[0].xpath(".//text()")).strip()
                                    value = info_etree.xpath(
                                        f"//div[@class='notice-detail']/table/tbody/tr[{num}]/td[2]")
                                    value_str = "".join(value[0].xpath(".//text()")).strip()
                                    if key_str == "抵押物":
                                        value_html = ""
                                        for i in value:
                                            value_html += ''.join(etree.tostring(i, method='html', encoding='unicode'))
                                        data_dict[key_str] = value_html
                                    else:
                                        data_dict[key_str] = value_str
                            # 获取附件信息
                            annexs = info_etree.xpath(
                                "//div[@class='notice-detail']//@src | //div[@class='notice-detail']//@href")
                            if annexs:
                                annex_info = ""
                                for annex in annexs:
                                    if "https" not in annex[0:5]:
                                        annex_url = "https:" + annex + ","
                                    else:
                                        annex_url = annex + ","
                                    annex_info += annex_url
                                annex_info = annex_info[:-1]
                                data_dict["附件"] = annex_info

                            # 上传数据库
                            url = data_dict.get("链接")
                            title = data_dict.get("标题")
                            disposition_subject = data_dict.get("资产处置主体")
                            phone = data_dict.get("咨询电话")
                            reference_value = data_dict.get("参考价值")
                            recruitment_time = data_dict.get("招募时间")
                            type = data_dict.get("资产类型")
                            process = data_dict.get("流程")
                            guarantee_method = data_dict.get("担保方式")
                            total = data_dict.get("债权总额")
                            situation = data_dict.get("债务人情况")
                            guarantor = data_dict.get("保证人")
                            collateral = data_dict.get("抵押物")
                            detail = data_dict.get("公告详情")
                            more_info = data_dict.get("更多信息")
                            supple_mater = data_dict.get("补充材料")
                            original_annex = data_dict.get("附件")
                            up_annex = original_annex
                            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            create_date = datetime.now().strftime('%Y-%m-%d')

                            conn_test = mysql.connector.connect(
                                host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                                user="col2024",
                                password="Bm_a12a06",
                                database="col",
                            )
                            cursor_test = conn_test.cursor()
                            # 上传文件
                            insert_sql = "INSERT INTO col_judicial_auctions_investing (url, title, disposition_subject, phone, reference_value, recruitment_time, type, process, guarantee_method, total, situation, guarantor, collateral, detail, more_info, supple_mater, original_annex, up_annex,create_time, create_date, from_queue) VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s)"

                            cursor_test.execute(insert_sql, (
                                url, title, disposition_subject, phone, reference_value, recruitment_time, type,
                                process,
                                guarantee_method, total, situation, guarantor, collateral, detail, more_info,
                                supple_mater,
                                original_annex, up_annex, create_time, create_date, from_queue))
                            conn_test.commit()

                            cursor_test.close()
                            conn_test.close()
                            print(data_dict)
                            tab_2.close()
                else:
                    flag = False
                    for info in info_list:
                        data_dict = {}
                        href_text = info.text
                        if "同类商品" not in href_text:
                            href_url = info.attr("href")
                            url_text = re.sub(r"\?.*", "", href_url)
                            now_state, old_id = judge_repeat(url_text)
                            if now_state and now_state == "已结束":
                                continue
                            if now_state and (
                                    now_state == "正在进行中" or now_state == "即将拍卖") and status_orders == 2:
                                flag = True
                            tab_2 = page.new_tab()
                            tab_2.get(href_url)

                            data_dict["链接"] = url_text
                            # tab_2.get("https://zc-item.taobao.com/auction/858628010713.htm?spm=a2129.27076131.puimod-pc-search-list_2004318340.11&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431%2C27076131&track_id=7c0d2dea-2697-4448-bca9-474a89c6a04f")
                            tab_2.wait(2)
                            tab_2 = encounter_verify(tab_2)
                            tab_2.wait(2)
                            title = tab_2.ele("xpath=//div[@id='page']//h1")  # 标题
                            if title:
                                title = title.text  # 标题
                                data_dict["标题"] = title
                            else:
                                tab_2.close()
                                continue  # 跳过没有标题的 ---------------------------------------------------------

                            if status_orders == 2:
                                data_dict["状态"] = "已结束"
                            if status_orders == 0:
                                data_dict["状态"] = "正在进行中"
                            if status_orders == 1:
                                data_dict["状态"] = "即将拍卖"
                            if status_orders == 6:
                                data_dict["状态"] = "招商中"
                            state = tab_2.ele("xpath=//div[@id='page']//h1/span[@class='item-status']")  # 状态
                            if state:
                                state = state.text  # 状态
                                if state == "招商":
                                    tab_2.close()
                                    continue  # 跳过招商--------------------------------------------------
                                data_dict["阶段"] = state

                            location = tab_2.ele("xpath=//div[@id='itemAddress']")  # 所在地
                            if location:
                                location = location.text  # 所在地
                                data_dict["所在地"] = location
                            sf_price = tab_2.ele("xpath=//span[@class='family-tahoma']", index=2)  # 起拍价
                            if sf_price:
                                sf_price = sf_price.text  # 起拍价
                                data_dict["起拍价"] = sf_price + "元"
                            if status_orders == 2:
                                auction_results = tab_2.ele(
                                    "xpath=//h1[@class='bid-fail'] | //h1[@class='bid-fail']/following-sibling::p")  # 拍卖结果
                                if auction_results:
                                    auction_results = auction_results.text  # 拍卖结果
                                    data_dict["拍卖结果"] = auction_results
                                    print("拍卖结果:", auction_results)
                            about_time = tab_2.ele("xpath=//li[@id='sf-countdown']")  # 关于时间
                            if about_time:
                                about_time = about_time.text  # 关于时间
                                if "距结束" in about_time:
                                    about_time = about_time.replace("距结束", "")
                                    time_data = ''.join(re.findall(r'(.*?)\d+次延时', about_time))
                                    data_dict["结束时间"] = time_str_to_date(time_data, add=True)
                                if "距开始" in about_time:
                                    about_time = about_time.replace("距开始", "")
                                    data_dict["开始时间"] = time_str_to_date(about_time, add=False)
                            end_time = tab_2.ele("xpath=//ul[@class='pm-bid-eyebrow']/li[1]")  # 结束时间
                            if end_time:
                                end_time = end_time.text  # 结束时间
                                if "结束时间" in end_time:
                                    data_dict["结束时间"] = \
                                        re.findall(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})', end_time)[
                                            0]
                            procedure = tab_2.ele("xpath=//div[@id='J_COMPONENT_MAIN_BOTTOM']")  # 获取程序
                            if procedure:
                                procedure = procedure.text  # 获取程序
                                procedure = re.sub(r'\n', '', procedure)
                                procedure = re.sub(r'\t', '', procedure)
                                # print(procedure)
                                procedure = ''.join(re.findall(r"程序(.*?)延时", procedure))  # 获取程序
                                procedure = procedure.replace(":", "")
                                if procedure:
                                    data_dict["程序"] = procedure
                            about_price = tab_2.ele("xpath=//li[@id='sf-price']")  # 关于价格
                            if about_price:
                                about_price = about_price.text  # 关于价格
                                if "当前价" in about_price:
                                    about_price = about_price.replace("当前价", "")
                                    now_price = "".join(re.findall(r"\d+", about_price))
                                    now_price = str(now_price) + about_price[-1]
                                    data_dict["当前价"] = now_price
                                if "拍下价" in about_price:
                                    about_price = about_price.replace("拍下价", "")
                                    now_price = "".join(re.findall(r"\d+", about_price))
                                    now_price = str(now_price) + about_price[-1]
                                    data_dict["成交价"] = now_price
                                # data_dict["关于价格"] = about_price
                            disposal_unit = tab_2.ele("xpath=//p[@class='org-name']")  # 处置单位
                            if disposal_unit:
                                disposal_unit = disposal_unit.text  # 处置单位
                                data_dict["处置单位"] = disposal_unit
                            bidding_num = tab_2.ele("xpath=//ul[@id='J_DetailTabMenu']/li[4]")  # 竞买次数
                            if bidding_num:
                                if "竞买记录" not in bidding_num.text:
                                    if "应买记录" not in bidding_num.text:
                                        bidding_num = tab_2.ele("xpath=//ul[@id='J_DetailTabMenu']/li[5]")  # 竞买次数
                            if bidding_num:
                                bidding_num = bidding_num.text  # 竞买次数
                                bidding_num = re.sub(r'\n', '', bidding_num)
                                bidd_num = ''.join(re.findall(r'\d+', bidding_num))
                                bidding_html = ""
                                if bidd_num:
                                    bidd_click_num = int(bidd_num) / 20
                                    bidding_records = tab_2.ele("xpath=//div[@id='J_RecordContent']")  # 获取竞价记录
                                    if bidding_records:
                                        bidding_records = bidding_records.html  # 竞价记录,html信息
                                        bidding_html += bidding_records
                                    for _ in range(int(bidd_click_num)):
                                        next_page = tab_2.ele(
                                            "xpath=//ul[@id='J_PageContent']/li[2]/a[@class='pagebutton']")
                                        next_page.click(by_js=True)
                                        tab_2.wait(2)
                                        tab_2 = encounter_verify(tab_2)
                                        tab_2.wait(2)
                                        bidding_records = tab_2.ele("xpath=//div[@id='J_RecordContent']")  # 获取竞价记录
                                        if bidding_records:
                                            bidding_records = bidding_records.html  # 竞价记录,html信息
                                            bidding_html += bidding_records
                                etree_html = etree.HTML(bidding_html)
                                if etree_html:
                                    bidding_records = etree_html.xpath(
                                        "//table[@id='J_RecordList']//div[@class='nickname']")
                                    bidd_set = set()
                                    for value in bidding_records:
                                        bidd_set.add(value.text)
                                    bidding_stat = ''.join(etree_html.xpath(
                                        "//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[1]//text()"))
                                    bidding_number = ''.join(etree_html.xpath(
                                        "//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[2]//text()"))
                                    bidding_price = ''.join(etree_html.xpath(
                                        "//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[3]//text()")) + "元"
                                    bidding_time = ''.join(etree_html.xpath(
                                        "//div[@id='J_RecordContent'][1]/table[@id='J_RecordList']//tr[@class='get']/td[4]//text()"))
                                    str_bidding = "竞买状态:" + bidding_stat + " 竞买号:" + bidding_number + " 竞买价:" + bidding_price + " 竞买时间:" + bidding_time + " 竞买人数:" + str(
                                        len(bidd_set))
                                    data_dict["竞价记录"] = str_bidding
                            else:
                                str_bidding = "竞买次数:0"
                                data_dict["竞价记录"] = str_bidding
                            number_applicants = tab_2.ele("xpath=//div[@id='J_COMPONENT_MAIN_BOTTOM']/div[2]")
                            if number_applicants:
                                number_applicants = number_applicants.text  # 竞买人数
                                number_applicants = re.sub(r'\n', '', number_applicants)
                                number_applicants = ''.join(re.findall(r'(\d+)人报名', number_applicants))
                                data_dict["报名人数"] = number_applicants
                                # print("报名人数:" + number_applicants)

                            target_info = tab_2.ele("xpath=//div[@id='J_ItemDetailContent']")  # 标的信息
                            if target_info:
                                target_annex = ''
                                target_html = target_info.html  # 标的信息,html信息
                                data_dict["标的信息"] = target_html
                                # print(target_html)
                                target_ann = etree.HTML(target_html)
                                target_info = target_ann.xpath("//@src | //@href")
                                for value in target_info:
                                    if "https" not in value[0:5]:
                                        annex_url = "https:" + value + ","
                                    else:
                                        annex_url = value + ","
                                    target_annex += annex_url
                                data_dict["标的信息附件"] = target_annex
                            target_ann = tab_2.ele("xpath=//div[@id='page']//a[@class='unit-txt view-ano']")
                            if target_ann:  # 拍卖公告
                                target_ann_href = target_ann.attr("href")
                                tab_3 = page.new_tab()
                                tab_3.get(target_ann_href)
                                tab_3.wait(2)
                                tab_3 = encounter_verify(tab_3)
                                tab_3.wait(2)
                                target_ann = tab_3.ele("xpath=//div[@class='notice-detail']/table")  # 拍卖公告
                                if target_ann:
                                    target_ann = target_ann.html  # 拍卖公告,html信息
                                    target_ann = str(target_ann)
                                    target_ann = re.sub(r"\n", '', target_ann)
                                    target_ann = re.sub(r" ", '', target_ann)
                                    data_dict["拍卖公告"] = target_ann
                                tab_3.close()
                            tab_2.close()
                            if data_dict:
                                url = data_dict.get("链接")
                                title = data_dict.get("标题")
                                state = data_dict.get("状态")
                                stage = data_dict.get("阶段")
                                address = data_dict.get("所在地")
                                start_bid = data_dict.get("起拍价")
                                sold_price = data_dict.get("成交价")
                                outcome = data_dict.get("拍卖结果")
                                end_time = data_dict.get("结束时间")
                                procedure_str = data_dict.get("程序")
                                disposal_unit = data_dict.get("处置单位")
                                auction_history = data_dict.get("竞价记录")
                                people_num = data_dict.get("报名人数")
                                subject_info = data_dict.get("标的信息")
                                subject_annex = data_dict.get("标的信息附件")
                                subject_annex_up = subject_annex
                                auction_html = data_dict.get("拍卖公告")
                                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                create_date = datetime.now().strftime('%Y-%m-%d')
                                print(procedure_str)
                                # 上传到测试数据库
                                conn_test = mysql.connector.connect(
                                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                                    user="col2024",
                                    password="Bm_a12a06",
                                    database="col",
                                )
                                if not flag:
                                    cursor_test = conn_test.cursor()
                                    # 上传文件
                                    insert_sql = "INSERT INTO col_judicial_auctions (url, title, state, stage, address, start_bid, sold_price, outcome, end_time, procedure_str, auction_html, subject_annex_up, subject_info, disposal_unit, auction_history, people_num, subject_annex, create_time, create_date, from_queue) VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s, %s, %s,%s,%s)"

                                    cursor_test.execute(insert_sql,
                                                        (url, title, state, stage, address, start_bid, sold_price,
                                                         outcome,
                                                         end_time, procedure_str, auction_html, subject_annex_up,
                                                         subject_info,
                                                         disposal_unit, auction_history, people_num, subject_annex,
                                                         create_time,
                                                         create_date, from_queue))
                                    conn_test.commit()
                                else:
                                    cursor_test = conn_test.cursor()
                                    # 上传文件
                                    update_sql = "UPDATE col_judicial_auctions SET url = %s, title = %s, state = %s, stage = %s, address = %s, start_bid = %s, sold_price = %s, outcome = %s, end_time = %s, procedure_str = %s, auction_html = %s, subject_annex_up = %s, subject_info = %s, disposal_unit = %s, auction_history = %s, people_num = %s, subject_annex = %s, update_time = %s, from_queue = %s WHERE id = %s;"
                                    cursor_test.execute(update_sql,
                                                        (url, title, state, stage, address, start_bid, sold_price,
                                                         outcome,
                                                         end_time,
                                                         procedure_str, auction_html, subject_annex_up, subject_info,
                                                         disposal_unit,
                                                         auction_history, people_num, subject_annex, update_time,
                                                         from_queue,
                                                         old_id))
                                    conn_test.commit()

                                cursor_test.close()
                                conn_test.close()
                                print(data_dict)
                            else:  # 可能为招商已结束
                                title = info.ele("xpath=/div/div/span[@class='text']")
                                if title:
                                    data_dict["标题"] = title.text
                                href_url = info.attr("href")
                                url_text = re.sub(r"&.*", "", href_url)
                                if judge_repeat_invest(url_text):
                                    continue
                                tab_2 = page.new_tab()
                                tab_2.get(href_url)
                                # tab_2.get("https://zc-paimai.taobao.com/zc/mn_detail.htm?id=180386&spm=a2129.27076131.puimod-pc-search-list_2004318340.25&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431%2C27076131&track_id=f36ba7d9-e768-4e22-9342-0ee897b09fd4")
                                data_dict["链接"] = url_text
                                tab_2.wait(2)
                                tab_2 = encounter_verify(tab_2)
                                tab_2.wait(2)
                                info_html = tab_2.html
                                info_etree = etree.HTML(info_html)
                                for num in range(1, 16 + 1):
                                    key = info_etree.xpath(
                                        f"//div[@class='notice-detail']/table/tbody/tr[{num}]/td[@class='odd']")
                                    if key:
                                        key_str = "".join(key[0].xpath(".//text()")).strip()
                                        value = info_etree.xpath(
                                            f"//div[@class='notice-detail']/table/tbody/tr[{num}]/td[2]")
                                        value_str = "".join(value[0].xpath(".//text()")).strip()
                                        if key_str == "抵押物":
                                            value_html = ""
                                            for i in value:
                                                value_html += ''.join(
                                                    etree.tostring(i, method='html', encoding='unicode'))
                                            data_dict[key_str] = value_html
                                        else:
                                            data_dict[key_str] = value_str
                                # 获取附件信息
                                annexs = info_etree.xpath(
                                    "//div[@class='notice-detail']//@src | //div[@class='notice-detail']//@href")
                                if annexs:
                                    annex_info = ""
                                    for annex in annexs:
                                        if "https" not in annex[0:5]:
                                            annex_url = "https:" + annex + ","
                                        else:
                                            annex_url = annex + ","
                                        annex_info += annex_url
                                    annex_info = annex_info[:-1]
                                    data_dict["附件"] = annex_info

                                # 上传数据库
                                url = data_dict.get("链接")
                                title = data_dict.get("标题")
                                disposition_subject = data_dict.get("资产处置主体")
                                phone = data_dict.get("咨询电话")
                                reference_value = data_dict.get("参考价值")
                                recruitment_time = data_dict.get("招募时间")
                                type = data_dict.get("资产类型")
                                process = data_dict.get("流程")
                                guarantee_method = data_dict.get("担保方式")
                                total = data_dict.get("债权总额")
                                situation = data_dict.get("债务人情况")
                                guarantor = data_dict.get("保证人")
                                collateral = data_dict.get("抵押物")
                                detail = data_dict.get("公告详情")
                                more_info = data_dict.get("更多信息")
                                supple_mater = data_dict.get("补充材料")
                                original_annex = data_dict.get("附件")
                                up_annex = original_annex
                                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                create_date = datetime.now().strftime('%Y-%m-%d')

                                conn_test = mysql.connector.connect(
                                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                                    user="col2024",
                                    password="Bm_a12a06",
                                    database="col",
                                )
                                cursor_test = conn_test.cursor()
                                # 上传文件
                                insert_sql = "INSERT INTO col_judicial_auctions_investing (url, title, disposition_subject, phone, reference_value, recruitment_time, type, process, guarantee_method, total, situation, guarantor, collateral, detail, more_info, supple_mater, original_annex, up_annex,create_time, create_date, from_queue) VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s)"

                                cursor_test.execute(insert_sql, (
                                    url, title, disposition_subject, phone, reference_value, recruitment_time, type,
                                    process,
                                    guarantee_method, total, situation, guarantor, collateral, detail, more_info,
                                    supple_mater,
                                    original_annex, up_annex, create_time, create_date, from_queue))
                                conn_test.commit()

                                cursor_test.close()
                                conn_test.close()
                                print(data_dict)

                tab_1.close()
        value_end = r.lpop('paimai_list')
        # print(value_end, "结束")
    page.quit()
