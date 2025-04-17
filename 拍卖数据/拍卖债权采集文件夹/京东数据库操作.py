import json
import re
import random

from api_paimai import upload_file_by_url
from a_mysql_connection_pool import get_connection


def remove_superfluous_data():
    # 连接数据库
    conn = get_connection()
    cursor = conn.cursor()
    # 查询col_judicial_auctions表中京东拍卖的sold_price字段
    cursor.execute("SELECT id, sold_price FROM col_judicial_auctions WHERE url LIKE '%paimai.jd.com%'")
    rows = cursor.fetchall()
    for row in rows:
        id_ = row[0]
        sold_price = row[1]
        if sold_price:
            print(id_, sold_price)
            sold_price = re.sub(r'保证金.*', '', sold_price)
            sold_price = re.sub(r'变卖.*', '', sold_price)
            print(id_, sold_price)
            # 更新数据库
            cursor.execute("UPDATE col_judicial_auctions SET sold_price = %s WHERE id = %s", (sold_price, id_))
            conn.commit()
            print('更新成功')
    cursor.close()
    conn.close()


def annex_update():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, subject_annex, subject_annex_up FROM col_judicial_auctions WHERE url LIKE '%paimai.jd.com%'")
    rows = cursor.fetchall()
    for row in rows:
        id_ = row[0]
        subject_annex = row[1]
        subject_annex_up = row[2]
        if subject_annex:
            if 'res.debtop.com' in subject_annex_up:
                continue
            # 通过,分割
            subject_annex_str = ''
            subject_annex_up_str = ''
            subject_annex_list = subject_annex.split(',')
            for subject_annex_item in subject_annex_list:
                file_name = random.randint(100000, 999999)
                url_type = subject_annex_item.split('.')[-1]
                if url_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z',
                                'png', 'jpg', 'jpeg', "PDF"]:
                    try:
                        file_url = upload_file_by_url(subject_annex_item, f"{file_name}", url_type)
                    except:
                        continue
                    try:
                        subject_annex_up_str += file_url + ','
                    except:
                        subject_annex_up_str += ''
                    try:
                        subject_annex_str += subject_annex_item + ','
                    except:
                        subject_annex_str += ''
            subject_annex_str = str(subject_annex_str[:-1])
            subject_annex_up_str = str(subject_annex_up_str[:-1])
            print(subject_annex_str)
            print(subject_annex_up_str)
            # 更新数据库
            cursor.execute("UPDATE col_judicial_auctions SET subject_annex_up = %s WHERE id = %s", (subject_annex_str, id_))
            conn.commit()
            print('更新成功')
    cursor.close()
    conn.close()


def updata_jd_target_html():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM col_judicial_auctions WHERE url LIKE '%paimai.jd.com%' AND state='已结束'")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def hainan_remove_files():
    # 未完成，删除不了选择的数据
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, original_files, files FROM col_paper_notice WHERE paper='海南联合资产管理有限公司'")
    rows = cursor.fetchall()
    for row in rows:
        id_ = row[0]
        original_files = row[1]
        files = row[2]
        original_files_list = json.loads(original_files)
        for original_file in original_files_list:
            print(original_file)
            if '20160417032739725' in original_file:
                original_files_list.remove(original_file)
            if '20160417032813966' in original_file:
                original_files_list.pop(original_file)

        print(original_files_list)

# hainan_remove_files()
