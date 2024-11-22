import re
import time

from KIMI_free_api import kimitext_free
from deepseek import deepseek_chat
from KIMI import kimi_single_chat
import mysql.connector


def guarantor(model_name=kimi_single_chat):
    # 上传到测试数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col_test",
    )
    cursor_test = conn_test.cursor()

    # 查询数据
    cursor_test.execute(
        "SELECT id, guarantee_new, mortgagor_new, collateral_new, content FROM tmp_paper_collateral1"
    )
    rows = cursor_test.fetchall()
    for id, guarantee_new, mortgagor_new, collateral_new, content in rows:
        print(id, guarantee_new, content)
        if not guarantee_new:
            try:
                a, b, guarantor = model_name(
                    content + "\n\n请从中提取保证人(当担保人没有特殊说明时默认为保证人。保证人之间如果有明确的亲属关系(不要自己推理)，在保证人后面追加()说明与其关系。)主体，单个主体以,分割，不要输出其他无关字段,没有保证人返回'空'。")
                guarantor = re.sub(r'保证人：', '', guarantor)
                guarantor = re.sub(r'保证人:', '', guarantor)
                guarantor = re.sub(r';', ',', guarantor)
                guarantor = re.sub(r'；', ',', guarantor)
                guarantor = re.sub(r'，', ',', guarantor)
                guarantor = re.sub(r"、", ',', guarantor)

                if guarantor[-1] == ',':
                    guarantor = guarantor[:-1]
                if not guarantor:
                    guarantor = "空"
                if guarantor == "某某有限公司,李某某,王某某":
                    guarantor = "空"
                print(guarantor)
                cursor_test1 = conn_test.cursor()
                insert_sql = "UPDATE tmp_paper_collateral1 SET guarantee_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (guarantor, id))
                conn_test.commit()
                # time.sleep(31)
            except Exception as e:
                print(f"------------------发生错误{e}")
                # time.sleep(31)
                continue
        if not mortgagor_new:
            try:
                a, b, mortgagor = model_name(
                    content + "\n\n从中提取抵押人/质押人主体名称（担保人在未说明为抵押人/质押人时不可视为抵押人/质押人，保证人在未说明为抵押人/质押人时不可视为抵押人/质押人。），主体之间以,分割，严格执行。未明确为抵押人/质押人不做推理，不要输出其他无关字段,没有抵押人/质押人返回'空'，严格按照执行。案例：抵押人/质押人:某某有限公司,李某某,王某某;(每项用';'结束)注意：此案例为借鉴数据，请不要引用里面的数据。",
                    temperature=1.0)
                mortgagor = re.sub(r'抵押人/质押人：', '', mortgagor)
                mortgagor = re.sub(r'抵押人/质押人:', '', mortgagor)
                mortgagor = re.sub(r'抵押人：|质押人：', '', mortgagor)
                mortgagor = re.sub(r'抵押人:|质押人:', '', mortgagor)
                mortgagor = re.sub(r';', ',', mortgagor)
                mortgagor = re.sub(r'；', ',', mortgagor)
                mortgagor = re.sub(r'，', ',', mortgagor)
                mortgagor = re.sub(r'、', ',', mortgagor)
                mortgagor = re.sub(r"'", '', mortgagor)
                mortgagor = re.sub(r"’", '', mortgagor)
                if mortgagor[-1] == ',':
                    mortgagor = mortgagor[:-1]
                if not mortgagor:
                    print(1111)
                    mortgagor = "空"
                if mortgagor == "某某有限公司,李某某,王某某":
                    print(2222)
                    mortgagor = "空"

                cursor_test1 = conn_test.cursor()
                insert_sql = "UPDATE tmp_paper_collateral1 SET mortgagor_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (mortgagor, id))
                conn_test.commit()
                # time.sleep(31)
            except Exception as e:
                print(f"--------------发生错误{e}")
                # time.sleep(31)
                continue
        if not collateral_new:
            try:
                a, b, collateral = model_name(
                    content + "\n\n从中提取抵押物/质押物(当担保物没有特殊说明时默认为抵押物/质押物)信息，不要输出其他无关字段,没有抵押物/质押物返回'空'，严格按照执行。案例：抵押物/质押物:位于某处房产,某工厂;(每项用';'结束)注意：此案例为借鉴数据，请不要引用里面的数据。")
                collateral = re.sub(r'抵押物/质押物：', '', collateral)
                collateral = re.sub(r'抵押物/质押物:', '', collateral)
                collateral = re.sub(r'抵押物：|质押物：', '', collateral)
                collateral = re.sub(r'抵押物:|质押物:', '', collateral)
                collateral = re.sub(r';', '', collateral)
                collateral = re.sub(r'；', ',', collateral)
                collateral = re.sub(r'，', ',', collateral)
                if not collateral:
                    collateral = "空"
                if collateral == "位于某处房产,某工厂":
                    collateral = "空"

                cursor_test1 = conn_test.cursor()
                insert_sql = "UPDATE tmp_paper_collateral1 SET collateral_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (collateral, id))
                conn_test.commit()
                # time.sleep(31)
            except Exception as e:
                print(f"-------------------发生错误{e}")
                # time.sleep(31)
                continue

    cursor_test.close()
    conn_test.close()


guarantor()


def count_chinese_chars(text):
    if not text:
        return 0
    return sum(1 for char in text if '\u4e00' <= char <= '\u9fff')


def chang_text(old, new):
    if str(old) == 'nan':
        old = ""
    if str(old) == '无':
        old = ""
    if str(new) == '空':
        new = ""
    if str(new) == 'nan':
        new = ""
    return old, new

def del_abnormal():
    # 上传到测试数据库
    conn_test = mysql.connector.connect(
        host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
        user="col2024",
        password="Bm_a12a06",
        database="col_test",
    )
    cursor_test = conn_test.cursor()

    # 查询数据
    cursor_test.execute(
        "SELECT id,guarantee, guarantee_new,mortgagor, mortgagor_new, collateral,collateral_new, content FROM tmp_paper_collateral1"
    )
    rows = cursor_test.fetchall()
    for id, guarantee, guarantee_new, mortgagor, mortgagor_new, collateral, collateral_new, content in rows:
        guarantee, guarantee_new = chang_text(guarantee, guarantee_new)
        mortgagor, mortgagor_new = chang_text(mortgagor, mortgagor_new)
        collateral, collateral_new = chang_text(collateral, collateral_new)
        if not count_chinese_chars(guarantee) == count_chinese_chars(guarantee_new):
            print("保证人不相等")
            cursor_test.execute("UPDATE tmp_paper_collateral1 SET guarantee_new = %s WHERE id = %s", ('', id))
            conn_test.commit()
        if not count_chinese_chars(mortgagor) == count_chinese_chars(mortgagor_new):
            print("抵押人/质押人不相等")
            cursor_test.execute("UPDATE tmp_paper_collateral1 SET mortgagor_new = %s WHERE id = %s", ('', id))
            conn_test.commit()
        if not count_chinese_chars(collateral) == count_chinese_chars(collateral_new):
            print("抵押物/质押物不相等")
            cursor_test.execute("UPDATE tmp_paper_collateral1 SET collateral_new = %s WHERE id = %s", ('', id))
            conn_test.commit()
    cursor_test.close()
    conn_test.close()


# del_abnormal()
