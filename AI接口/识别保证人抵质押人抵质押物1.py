import re
import time

from KIMI_free_api import kimitext_free
from deepseek import deepseek_chat
from KIMI import kimi_single_chat
import mysql.connector


def guarantor(model_name=deepseek_chat):
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
        "SELECT id, guarantee_new, mortgagor_new, collateral_new, content FROM tmp_paper_collateral2"
    )
    rows = cursor_test.fetchall()
    for id, guarantee_new, mortgagor_new, collateral_new, content in rows:
        print(id, guarantee_new, content)
        if not guarantee_new:
            try:
                a, b, guarantor = model_name(
                    content + "\n\n请从中提取保证人(包含公司和个人,当担保人没有特殊说明时默认为保证人。保证人之间如有明确亲属关系，在保证人后面追加（）说明。)主体，单个主体以','分割，不要输出其他无关字段,没有保证人返回'空'，严格按照执行。案例：保证人:某某有限公司,李某某,王某某;(每项用';'结束)注意：此案例为借鉴数据，请不要引用里面的数据，不要将其他与保证人无关的主体放在保证人里面，抵押人或质押人不应被视为保证人。")
                guarantor = re.sub(r'保证人：', '', guarantor)
                guarantor = re.sub(r'保证人:', '', guarantor)
                guarantor = re.sub(r';', ',', guarantor)
                guarantor = re.sub(r'；', ',', guarantor)
                guarantor = re.sub(r'，', ',', guarantor)
                guarantor = re.sub(r"\(每项用''结束\)", '', guarantor)
                guarantor = re.sub(r"\(每项用','结束\)", '', guarantor)
                if guarantor[-1] == ',':
                    guarantor = guarantor[:-1]
                if not guarantor:
                    guarantor = "空"
                if guarantor == "某某有限公司,李某某,王某某":
                    guarantor = "空"

                cursor_test1 = conn_test.cursor()
                insert_sql = "UPDATE tmp_paper_collateral2 SET guarantee_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (guarantor, id))
                conn_test.commit()
                # time.sleep(20)
            except:
                print("发生错误")
                continue
        if not mortgagor_new:
            try:
                a, b, mortgagor = model_name(
                    content + "\n\n从中提取抵押人/质押人主体名称（担保人在未说明为抵押人/质押人时不可视为抵押人/质押人，保证人在未说明为抵押人/质押人时不可视为抵押人/质押人。），主体之间以','分割，严格执行。不要输出其他无关字段,没有抵押人/质押人返回'空'，严格按照执行。案例：抵押人/质押人:某某有限公司,李某某,王某某;(每项用';'结束)注意：此案例为借鉴数据，请不要引用里面的数据。",
                    temperature=1.0)
                mortgagor = re.sub(r'抵押人/质押人：', '', mortgagor)
                mortgagor = re.sub(r'抵押人/质押人:', '', mortgagor)
                mortgagor = re.sub(r'抵押人：|质押人：', '', mortgagor)
                mortgagor = re.sub(r'抵押人:|质押人:', '', mortgagor)
                mortgagor = re.sub(r';', ',', mortgagor)
                mortgagor = re.sub(r'；', ',', mortgagor)
                mortgagor = re.sub(r'，', ',', mortgagor)
                if mortgagor[-1] == ',':
                    mortgagor = mortgagor[:-1]
                if not mortgagor:
                    print(1111)
                    mortgagor = "空"
                if mortgagor == "某某有限公司,李某某,王某某":
                    print(2222)
                    mortgagor = "空"

                cursor_test1 = conn_test.cursor()
                insert_sql = "UPDATE tmp_paper_collateral2 SET mortgagor_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (mortgagor, id))
                conn_test.commit()
                # time.sleep(20)
            except:
                print("发生错误")
                continue
        if not collateral_new:
            try:
                a, b, collateral = model_name(
                    content + "\n\n从中提取抵押物/质押物(当担保物没有特殊说明时默认为抵押物/质押物)信息，单个主体以','分割，不要输出其他无关字段,没有抵押物/质押物返回'空'，严格按照执行。案例：抵押物/质押物:位于某处房产,某工厂;(每项用';'结束)注意：此案例为借鉴数据，请不要引用里面的数据，不要将其他与抵押物/质押物无关的主体放在抵押物/质押物里面，抵质押物情况中有主体的也要保存。")
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
                insert_sql = "UPDATE tmp_paper_collateral2 SET collateral_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (collateral, id))
                conn_test.commit()
                # time.sleep(20)
            except:
                print("发生错误")
                continue

    cursor_test.close()
    conn_test.close()


guarantor()
