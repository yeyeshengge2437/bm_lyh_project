import json
import os
import re
import time
from datetime import datetime
from api_paper import get_image, upload_file, upload_file_by_url
import mysql.connector
import requests
from lxml import html
from lxml import etree
from a_mysql_connection_pool import get_connection
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
# co = co.set_argument('--no-sandbox')
# co = co.headless()
co.set_paths(local_port=9253)


def del_style(content_html):
    tree = etree.HTML(content_html)
    # 删除所有 <style> 标签
    for style_tag in tree.xpath("//style"):
        style_tag.getparent().remove(style_tag)

    # 输出处理后的 HTML
    up_content_html = html.tostring(tree, encoding="unicode")
    return up_content_html


def del_script(content_html):
    tree = etree.HTML(content_html)
    # 删除所有 <style> 标签
    for style_tag in tree.xpath("//script"):
        style_tag.getparent().remove(style_tag)

    # 输出处理后的 HTML
    up_content_html = html.tostring(tree, encoding="unicode")
    return up_content_html


def compress_html(html):
    # 移除 <!-- ... --> 注释（可选）
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

    # 移除换行符(\n)、制表符(\t)、连续空格(保留单个空格)
    html = re.sub(r'\s+', ' ', html)

    # 移除 > 和 < 之间的空格（避免破坏HTML标签结构）
    html = re.sub(r'>\s+<', '><', html)

    html = re.sub(r'<div class="right-list clearfix"><h3>猜你喜欢</h3>.*', '', html)

    return html.strip()


def _execute_batch_update(conn, buffer):
    """执行批量更新"""
    try:
        with conn.cursor() as cursor:
            # 使用 executemany 批量更新
            cursor.executemany(
                "UPDATE col_paper_notice SET content = %s, content_html = %s, update_time = %s WHERE id = %s",
                buffer
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def guanxi():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url, day, update_time  FROM col_paper_notice WHERE paper = '广西交易所集团';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        update_time = i[3]
        if update_time:
            continue
        try:
            url_id = re.findall(r'Detail/(.*?)\.html', page_url)[0]
        except:
            print("!!!!!!!!!!!!!!!!", page_url)
            continue
        headers_time = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Client-Id': 'gxcq',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'http://ljs.gxcq.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            # 'Cookie': 'Hm_lvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1744954682; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1744956119',
        }
        if 'projectToManageDetail' in page_url:
            params = {
                'id': f'{url_id}',
                # 'n': '0.5039649294161339',
            }

            response_ = requests.get(
                'http://ljs.gxcq.com.cn/api/dscq-project/project/detail',
                params=params,
                headers=headers_time,
                verify=False,
            )
            time.sleep(1)
            print(page_url)
            print(url_id)
            print(response_.json())
            title_date = response_.json()["data"]["announcementStartTime"]
            print(title_date)
        else:
            params = {
                'assetsId': f'{url_id}',
                # 'n': '0.5039649294161339',
            }

            response_ = requests.get(
                'http://ljs.gxcq.com.cn/api/dscq-project/assets-detail/normal-detail',
                params=params,
                headers=headers_time,
                verify=False,
            )
            time.sleep(1)
            print(page_url)
            print(url_id)
            title_date = response_.json()["data"]["bidActivity"]["publishDate"]
            print(title_date)
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(
            "UPDATE col_paper_notice SET day = %s, update_time = %s WHERE id = %s",
            (title_date, update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
    cursor.close()
    connection.close()


def heilongjiang_chanjiaosuo():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url, day, update_time, content_html, content  FROM col_paper_notice WHERE paper = '内蒙古产权交易中心_挂牌项目债权';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        day = i[2]
        update_time = i[3]
        content_html = i[4]
        content = i[5]
        tree = html.fromstring(content_html)

        # 删除所有 <style> 标签
        for style_tag in tree.xpath("//style"):
            style_tag.getparent().remove(style_tag)

        # 输出处理后的 HTML
        up_content_html = html.tostring(tree, encoding="unicode")
        update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(
            "UPDATE col_paper_notice SET content_html = %s, update_time = %s WHERE id = %s",
            (up_content_html, update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
    cursor.close()
    connection.close()


def heilongjiang_chanjiaosuo_content():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url, day, update_time, content_html, content  FROM col_paper_notice WHERE paper = '内蒙古产权交易中心_挂牌项目债权';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        day = i[2]
        update_time = i[3]
        content_html = i[4]
        content = i[5]
        tree = etree.HTML(content_html)
        content_str = ''.join(tree.xpath('//text()'))
        print(content_str)

        # # 删除所有 <style> 标签
        # for style_tag in tree.xpath("//style"):
        #     style_tag.getparent().remove(style_tag)
        #
        # # 输出处理后的 HTML
        # up_content_html = html.tostring(tree, encoding="unicode")
        update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(
            "UPDATE col_paper_notice SET content = %s, update_time = %s WHERE id = %s",
            (content_str, update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
    cursor.close()
    connection.close()


def 南方联合产权交易所1():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, update_time, content_html, content  FROM col_paper_notice WHERE paper = '南方联合产权交易所' AND update_time IS NULL LIMIT 10;"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    if not result:
        print('没有需要处理的数据')
        return False
    for i in result:
        target_id = i[0]
        update_time = i[1]
        content_html = i[2]
        content = i[3]
        content_html_str = compress_html(content_html)
        print(f'html修改前长度{len(content_html)}')
        print(f'html修改后长度{len(content_html_str)}')
        tree = etree.HTML(content_html_str)
        content_str = ''.join(tree.xpath('//text()'))
        print(f'内容修改前长度{len(content)}')
        print(f'内容修改后长度{len(content_str)}')
        up_update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(
            "UPDATE col_paper_notice SET content = %s, content_html = %s, update_time = %s WHERE id = %s",
            (content_str, content_html_str, up_update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
        print(f'处理成功:{target_id}')
    cursor.close()
    connection.close()
    return True


def 南方联合产权交易所2():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, update_time, content_html, content  FROM col_paper_notice WHERE paper = '南方联合产权交易所' AND update_time IS NULL LIMIT 10;"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    if not result:
        print('没有需要处理的数据')
        return False
    for i in result:
        target_id = i[0]
        update_time = i[1]
        content_html = i[2]
        content = i[3]
        content_html_str = compress_html(content_html)
        # print(content_html_str)
        tree = etree.HTML(content_html_str)
        body = tree.xpath('//body')[0]  # 获取body元素
        body_html = etree.tostring(body, encoding='unicode')
        up_style_html = del_style(body_html)
        up_script_html = del_script(up_style_html)
        print(up_script_html)
        tree_content = etree.HTML(up_script_html)
        content_str = ''.join(tree_content.xpath('//text()'))
        up_update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(
            "UPDATE col_paper_notice SET content = %s, content_html = %s, update_time = %s WHERE id = %s",
            (content_str, up_script_html, up_update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
        print(f'处理成功:{target_id}')
    cursor.close()
    connection.close()
    return True


def 南方联合产权交易所():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.csuaee.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://www.csuaee.com.cn/searchItem.html?keyword=%E5%80%BA%E6%9D%83',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'language': 'zh-cn',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'Hm_lvt_1aac8492a1c45f4949e13dc855f617ee=1740019778; HMACCOUNT=FDD970C8B3C27398; Hm_lvt_c4f40a0013c2cb0ccb4ad6cf20361123=1740019817; Hm_lpvt_c4f40a0013c2cb0ccb4ad6cf20361123=1740638630; Hm_lpvt_1aac8492a1c45f4949e13dc855f617ee=1740638630',
    }
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url, content  FROM col_paper_notice WHERE paper = '南方联合产权交易所';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    if not result:
        print('没有需要处理的数据')
        return False
    for i in result:
        target_id = i[0]
        page_url = i[1]
        content = i[2]
        print(content)
        if '404 Not Foundnginx/1.24.0' in content:
            print(page_url)
            res_1 = requests.get(page_url, headers=headers)
            time.sleep(2)
            res_1 = res_1.content.decode()
            res_html = etree.HTML(res_1)
            iframes = res_html.xpath("//iframe/@src")
            if not iframes:
                continue
            if 'http' in iframes[0]:
                title_url = page_url

                content_html_str = compress_html(res_1)
                # print(content_html_str)
                tree = etree.HTML(content_html_str)
                body = tree.xpath('//body')[0]  # 获取body元素
                body_html = etree.tostring(body, encoding='unicode')
                up_style_html = del_style(body_html)
                content_html = del_script(up_style_html)
                tree_content = etree.HTML(content_html)
                title_content = ''.join(tree_content.xpath('//text()'))
                cursor.execute(
                    "UPDATE col_paper_notice SET content = %s, content_html = %s WHERE id = %s",
                    (title_content, content_html, target_id)  # 参数按顺序替换 %s
                )
                connection.commit()
                print(f'处理成功:{target_id}')
        else:
            print('无异常')
        # content_html_str = compress_html(content_html)
        # # print(content_html_str)
        # tree = etree.HTML(content_html_str)
        # body = tree.xpath('//body')[0]  # 获取body元素
        # body_html = etree.tostring(body, encoding='unicode')
        # up_style_html = del_style(body_html)
        # up_script_html = del_script(up_style_html)
        # print(up_script_html)
        # tree_content = etree.HTML(up_script_html)
        # content_str = ''.join(tree_content.xpath('//text()'))
        # up_update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # cursor.execute(
        #     "UPDATE col_paper_notice SET content = %s, content_html = %s, update_time = %s WHERE id = %s",
        #     (content_str, up_script_html, up_update_time, target_id)  # 参数按顺序替换 %s
        # )
        # connection.commit()
        # print(f'处理成功:{target_id}')
    cursor.close()
    connection.close()
    return True


# guanxi()
# heilongjiang_chanjiaosuo_content()
# while True:
#     value = 南方联合产权交易所()
#     if not value:
#         break

# 南方联合产权交易所()

def heilongjiang_chanjiaosuo_content1():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, update_time, content_html, content  FROM col_paper_notice WHERE paper = '湖南省联合产权交易所';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        print(1111)
        target_id = i[0]
        update_time = i[1]
        content_html = i[2]
        up_content_html = compress_html(content_html)
        print(up_content_html)
        input('输入数字')
        content = i[3]
        print(target_id, content_html)

        tree = etree.HTML(content_html)

        # 删除所有 <style> 标签
        try:
            for style_tag in tree.xpath("//style"):
                style_tag.getparent().remove(style_tag)
            # 输出处理后的 HTML
            up_content_html = html.tostring(tree, encoding="unicode")
            # update_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            cursor.execute(
                "UPDATE col_paper_notice SET content_html = %s WHERE id = %s",
                (up_content_html, target_id)  # 参数按顺序替换 %s
            )
            connection.commit()
            print(f'处理成功:{target_id}')
        except:
            pass

    cursor.close()
    connection.close()


# heilongjiang_chanjiaosuo_content1()


def qinghai():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url, content_html, page_url  FROM col_paper_notice WHERE paper = '青海省产权交易市场' AND update_time IS NULL;"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        content_html = i[2]
        page_url = i[3]
        # print(content_html)
        # //table[@class='MsoNormalTable']
        content_html_tree = etree.HTML(content_html)
        up_content_html = content_html_tree.xpath('//table[@class="MsoNormalTable"]')
        up_content = ''.join(content_html_tree.xpath('//table[@class="MsoNormalTable"]//text()'))
        try:
            table_html = etree.tostring(up_content_html[0],
                                        encoding='unicode',
                                        pretty_print=True)
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cursor.execute(
                "UPDATE col_paper_notice SET content = %s, content_html = %s, update_time = %s WHERE id = %s",
                (up_content, table_html, update_time, target_id)  # 参数按顺序替换 %s
            )
            connection.commit()
            print(f'处理成功:{target_id}')
        except:
            print(page_url)
            print(content_html)
            # //div[@class='ct']
            input('输入')

    cursor.close()
    connection.close()


# qinghai()

def gansu_jiu():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url, content_html  FROM col_paper_notice WHERE paper = '甘肃省产权交易所（旧址）' AND update_time IS NULL;"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        content_html = i[2]
        up_content_html = del_style(content_html)
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(
            "UPDATE col_paper_notice SET content_html = %s, update_time = %s WHERE id = %s",
            (up_content_html, update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
        print(f'处理成功:{target_id}')

    cursor.close()
    connection.close()


# gansu_jiu()

def jietu():
    page = ChromiumPage(co)
    page.set.load_mode.none()
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url  FROM col_paper_page WHERE paper = '青岛产权交易所' AND update_time IS NULL;"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        print(page_url)
        image = get_image(page, page_url,
                          "xpath=//div[@id='scrollTabCon']", is_to_bottom=True,
                          is_click="xpath=//a[@class='layui-layer-btn0']", is_del_1="xpath=//div[@id='scrollTab']")
        up_img = upload_file(image, "png", "paper")
        print(up_img)
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(
            "UPDATE col_paper_page SET original_img = %s, img_url = %s, update_time = %s WHERE id = %s",
            (up_img, up_img, update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
        print(f'处理成功:{target_id}')
        if os.path.exists(f'{image}.png'):
            os.remove(f'{image}.png')

    cursor.close()
    connection.close()


jietu()

def guangxi():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url  FROM col_paper_notice WHERE paper = '广西交易所集团';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        try:
            url_id = re.findall(r'Detail/(.*?)\.html', page_url)[0]

            headers_time = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Client-Id': 'gxcq',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'http://ljs.gxcq.com.cn/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
                # 'Cookie': 'Hm_lvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1744954682; HMACCOUNT=FDD970C8B3C27398; Hm_lpvt_0ebc0266344b7e1dbda8f61a3a7ee5a1=1744956119',
            }
            params = {
                'assetsId': f'{url_id}',
                # 'n': '0.7465561160908133',
            }

            response_ = requests.get(
                'http://ljs.gxcq.com.cn/api/dscq-project/assets-detail/normal-detail',
                params=params,
                # cookies=cookies,
                headers=headers_time,
                verify=False,
            )
            # print(response_.json())
            title_date = response_.json()["data"]["bidActivity"]["announcementStartTime"]
            title_date = re.findall(r'^(\d{4}-\d{2}-\d{2})', title_date)
            title_date = title_date[0]
            time.sleep(6)
            print(page_url, url_id, title_date)
            update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cursor.execute(
                "UPDATE col_paper_notice SET day = %s, update_time = %s WHERE id = %s",
                (title_date, update_time, target_id)  # 参数按顺序替换 %s
            )
            connection.commit()
            print(f'处理成功:{target_id}')
        except:
            print('1111', page_url)

    cursor.close()
    connection.close()


# guangxi()

def zhejiang():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, content_html  FROM col_paper_notice WHERE paper = '浙江产权交易所';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        content_html = i[1]
        content_html = compress_html(content_html)
        content_html = re.sub(r'<div class="default_detail_title">为您推荐</div>.*', '', content_html)
        print(content_html)
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor.execute(
            "UPDATE col_paper_notice SET content_html = %s, update_time = %s WHERE id = %s",
            (content_html, update_time, target_id)  # 参数按顺序替换 %s
        )
        connection.commit()
        print(f'处理成功:{target_id}')
    cursor.close()
    connection.close()


# zhejiang()


def taizhou():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url  FROM col_paper_notice WHERE paper = '台州市产权交易所';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        pass
    cursor.close()
    connection.close()


# # ["http://www.tzpre.com/attachment/cms/item/2022_04/20_15/5a48a48d3d89036a.doc"]
# ann = "http://www.tzpre.com/attachment/cms/item/2022_04/20_15/5a48a48d3d89036a.doc"
# file_url = upload_file_by_url(ann, "guangxi", "doc")
# print(file_url)
# # ["https://res.debtop.com/col/live/paper/202504/23/202504231046114314325221b34289.doc"]


def jietu_anhui():
    page = ChromiumPage(co)
    page.set.load_mode.none()
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url  FROM col_paper_page WHERE paper = '安徽产权交易中心' AND update_time IS NULL;"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        page_url = i[1]
        print(page_url)
        image = get_image(page, page_url,
                          "xpath=//div[@class='main']", is_to_bottom=True, is_time=10)
        # up_img = upload_file(image, "png", "paper")
        # print(up_img)
        # update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # cursor.execute(
        #     "UPDATE col_paper_page SET original_img = %s, img_url = %s, update_time = %s WHERE id = %s",
        #     (up_img, up_img, update_time, target_id)  # 参数按顺序替换 %s
        # )
        # connection.commit()
        # print(f'处理成功:{target_id}')
        # if os.path.exists(f'{image}.png'):
        #     os.remove(f'{image}.png')

    cursor.close()
    connection.close()


# jietu_anhui()

def fujian():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, original_files, files  FROM col_paper_notice WHERE paper = '江西省产权交易所';"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    for i in result:
        target_id = i[0]
        original_files = i[1]
        files = i[2]
        if original_files:
            original_files_list = json.loads(original_files)
            files_list = []
            original_url_list = []
            for original_file in original_files_list:
                type_file = original_file.split('.')[-1]
                original_file = re.sub('http:', 'https:', original_file)
                up_url = upload_file_by_url(original_file, 'jiangxi', type_file)
                files_list.append(up_url)
                original_url_list.append(original_file)
            files_list = str(files_list).replace("'", '"')
            original_url_list = str(original_url_list).replace("'", '"')
            print(files_list, original_url_list)
            cursor.execute(
                "UPDATE col_paper_notice SET original_files = %s, files = %s WHERE id = %s",
                (original_url_list, files_list, target_id)  # 参数按顺序替换 %s
            )
            connection.commit()
            print(f'处理成功:{target_id}')
    cursor.close()
    connection.close()


# fujian()
