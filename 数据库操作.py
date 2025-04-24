import re
import time
from datetime import datetime

import mysql.connector
import requests
from lxml import html
from lxml import etree
from a_mysql_connection_pool import get_connection



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


def 全国产权交易():
    connection = get_connection()
    cursor = connection.cursor()
    sql_search = "SELECT id, page_url, day, update_time, content_html, content  FROM col_paper_notice WHERE paper = '全国产权交易中心' AND update_time IS NULL LIMIT 10;"
    cursor.execute(sql_search)
    result = cursor.fetchall()
    if not result:
        print('没有需要处理的数据')
        return False
    for i in result:
        target_id = i[0]
        page_url = i[1]
        day = i[2]
        update_time = i[3]
        content_html = i[4]
        content = i[5]
        content_html_str = compress_html(content_html)
        print(f'html修改前长度{len(content_html)}')
        print(f'html修改后长度{len(content_html_str)}')
        tree = etree.HTML(content_html_str)
        try:
            content_str = ''.join(tree.xpath('//text()'))
        except:
            content_str = ''
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


# guanxi()
# heilongjiang_chanjiaosuo_content()
while True:
    value = 全国产权交易()
    if not value:
        break

