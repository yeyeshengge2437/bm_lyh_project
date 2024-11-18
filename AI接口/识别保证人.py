import re

from KIMI_free_api import kimitext_free
from deepseek import deepseek_chat
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
        "SELECT id, guarantee_new, mortgagor_new, collateral_new, content FROM tmp_paper_collateral"
    )
    rows = cursor_test.fetchall()
    for id, guarantee_new, mortgagor_new, collateral_new, content in rows:
        if not (guarantee_new and mortgagor_new and collateral_new):
            content = re.sub(r'\n', '', content)
            print(id, guarantee_new, content)
            try:
                a, b, guarantee_new = model_name(
                    content, system_content="请从中提取保证人(包含公司和个人,当担保人没有特殊说明时默认为保证人)， 抵押人/质押人(包含公司和个人)，抵押物/质押物信息，单个主体以','分割，不要输出其他无关字段,没有保证人返回'空'，没有抵押人/质押人返回'空'，没有抵押物/质押物返回'空'，严格按照执行。案例：保证人:某某有限公司,李某某,王某某; 抵押人/质押人:某某公司，某某人; 抵押物/质押物:位于某处房产,某工厂;(每项用';'结束)注意：此案例为借鉴数据，请不要引用里面的数据，不要将其他与保证人无关的主体放在保证人里面。")
                print(guarantee_new)
                guarantor = ''.join(re.findall(r'保证人:(.*?);', guarantee_new))
                mortgage_person = ''.join(re.findall(r'抵押人/质押人:(.*?);', guarantee_new))
                mortgage_goods = ''.join(re.findall(r'抵押物/质押物:(.*?);', guarantee_new))
                if not guarantor:
                    guarantor = "空"
                if not mortgage_person:
                    mortgage_person = "空"
                if not mortgage_goods:
                    mortgage_goods = "空"
                if guarantor == "某某有限公司,李某某,王某某":
                    guarantor = "空"
                if mortgage_person == "某某公司":
                    mortgage_person = "空"
                if mortgage_goods == "位于某处房产,某工厂":
                    mortgage_goods = "空"

                cursor_test1 = conn_test.cursor()
                insert_sql = "UPDATE tmp_paper_collateral SET guarantee_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (guarantor, id))
                conn_test.commit()

                cursor_test1 = conn_test.cursor()
                insert_sql = "UPDATE tmp_paper_collateral SET mortgagor_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (mortgage_person, id))
                conn_test.commit()

                cursor_test1 = conn_test.cursor()
                insert_sql = "UPDATE tmp_paper_collateral SET collateral_new = %s WHERE id = %s"
                cursor_test1.execute(insert_sql, (mortgage_goods, id))
                conn_test.commit()
            except:
                print("发生错误")
                continue

    cursor_test.close()
    conn_test.close()


guarantor()
