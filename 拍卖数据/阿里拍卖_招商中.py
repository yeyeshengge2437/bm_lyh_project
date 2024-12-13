import random
import re
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from DrissionPage import ChromiumPage, ChromiumOptions
from lxml import etree
from urllib.parse import urlencode, urljoin

co = ChromiumOptions()
co = co.set_user_data_path(r"D:\chome_data\ali_two")
# co = co.set_argument('--no-sandbox')
# co = co.headless()
co.set_paths(local_port=9154)


def encounter_verify(tab):
    tab.wait(2)
    # 随机0.15到1之间的数
    num = random.uniform(0.15, 0.3)
    if "亲，请拖动下方滑块完成验证" in tab.html:
        # 获取结束位置
        end_loc = tab.ele("xpath=//div[@id='nc_1__scale_text']")
        loc_value = end_loc.rect.corners
        right_up = loc_value[1]
        right_down = loc_value[3]
        tager_x = right_up[0] + random.randint(10, 150)
        tager_y = right_up[1] + right_down[1] // 2
        # input()
        tab.wait(2)
        slider_loc = tab.ele("xpath=//span[@id='nc_1_n1z']")
        print(slider_loc.rect.location)
        tab.actions.hold(slider_loc).move_to((tager_x, tager_y), duration=num).release()
        tab.wait(2)
        if "验证失败" in tab.html:
            tab.ele("验证失败").click(by_js=None)
            if "验证失败" in tab.html:
                tab.ele("验证失败").click(by_js=None)
            if "请按住滑块" in tab.html:
                tab.refresh()
                encounter_verify(tab)
    return tab
# https://zc-paimai.taobao.com/zc/mn_detail.htm?id=180386&spm=a2129.27076131.puimod-pc-search-list_2004318340.25&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431%2C27076131&track_id=f36ba7d9-e768-4e22-9342-0ee897b09fd4
# https://zc-paimai.taobao.com/zc/mn_detail.htm?id=117645&spm=a2129.27076131.puimod-pc-search-list_2004318340.2&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431%2C27076131&track_id=4873899e-9189-4f4a-9b5c-5bb3c254724e

page = ChromiumPage(co)
tab_1 = page.new_tab()
tab_1.get("https://zc-paimai.taobao.com/wow/pm/default/pc/zichansearch?disableNav=YES&page=1&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431,27076131,25287064,27064540&spm=a2129.27064540.puimod-zc-focus-2021_2860107850.category-4-5&fcatV4Ids=[%22206067301%22]&statusOrders=[%226%22]")
tab_1.wait(2)
info_list = tab_1.eles("xpath=//div[@id='guid-2004318340']//div/a")  # /div/div/span[@class='text']
for info in info_list:
    data_dict = {}
    href_text = info.text
    if "同类商品" not in href_text:
        title = info.ele("xpath=/div/div/span[@class='text']")
        if title:
            data_dict["标题"] = title.text
        href_url = info.attr("href")
        url_text = re.sub(r"&.*", "", href_url)
        tab_2 = page.new_tab()
        # tab_2.get(href_url)
        tab_2.get("https://zc-paimai.taobao.com/zc/mn_detail.htm?id=180386&spm=a2129.27076131.puimod-pc-search-list_2004318340.25&pmid=2175852518_1653962822378&pmtk=20140647.0.0.0.27064540.puimod-zc-focus-2021_2860107850.35879&path=27181431%2C27076131&track_id=f36ba7d9-e768-4e22-9342-0ee897b09fd4")
        data_dict["链接"] = url_text
        tab_2.wait(2)
        tab_2 = encounter_verify(tab_2)
        tab_2.wait(2)
        info_html = tab_2.html
        info_etree = etree.HTML(info_html)
        for num in range(1, 16 + 1):
            key = info_etree.xpath(f"//div[@class='notice-detail']/table/tbody/tr[{num}]/td[@class='odd']")
            if key:
                key_str = "".join(key[0].xpath(".//text()")).strip()
                value = info_etree.xpath(f"//div[@class='notice-detail']/table/tbody/tr[{num}]/td[2]")
                value_str = "".join(value[0].xpath(".//text()")).strip()
                if key_str == "抵押物":
                    value_html = ""
                    for i in value:
                        value_html += ''.join(etree.tostring(i, method='html', encoding='unicode'))
                    data_dict[key_str] = value_html
                else:
                    data_dict[key_str] = value_str
        # 获取附件信息
        annexs = info_etree.xpath("//div[@class='notice-detail']//@src | //div[@class='notice-detail']//@href")
        if annexs:
            annex_info = ""
            for annex in annexs:
                if "https" not in annex:
                    annex_url = "https:" + annex + ","
                else:
                    annex_url = annex + ","
                annex_info += annex_url
            annex_info = annex_info[:-1]
            data_dict["附件"] = annex_info

        # 上传数据库
        url = data_dict.get("链接")
        title = data_dict.get("标题")
        disposition_subject = data_dict.get("处置主体")
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


        from_queue = "1233"
        conn_test = mysql.connector.connect(
            host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
            user="col2024",
            password="Bm_a12a06",
            database="col",
        )
        cursor_test = conn_test.cursor()
        # 上传文件
        insert_sql = "INSERT INTO col_judicial_auctions (url, title, disposition_subject, phone, reference_value, recruitment_time, type, process, guarantee_method, total, situation, guarantor, collateral, detail, more_info, supple_mater, original_annex, up_annex,create_time, create_date, from_queue) VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s)"

        cursor_test.execute(insert_sql,(url, title, disposition_subject, phone, reference_value, recruitment_time, type, process, guarantee_method, total, situation, guarantor, collateral, detail, more_info, supple_mater, original_annex, up_annex,create_time, create_date, from_queue))
        conn_test.commit()

        cursor_test.close()
        conn_test.close()
        print(data_dict)
        tab_2.close()
        break



