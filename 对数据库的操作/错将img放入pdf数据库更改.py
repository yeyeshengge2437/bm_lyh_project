
import os
import random
import re
from datetime import datetime

import mysql.connector
import pdfplumber
import requests

produce_url = "http://118.31.45.18:29875"  # 生产环境
# produce_url = "http://121.43.164.84:29775"    # 测试环境
test_url = produce_url

requests.DEFAULT_RETRIES = 3
s = requests.session()
s.keep_alive = False
import mysql.connector
import requests
from lxml import etree
def upload_file_by_url(file_url, file_name, file_type, type="paper", verify=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',

    }
    file_name = file_name + str(random.randint(1, 999999999))
    r = requests.get(file_url, headers=headers, verify=verify)
    if r.status_code != 200:
        return None
    pdf_path = f"{file_name}.{file_type}"
    if not os.path.exists(pdf_path):
        fw = open(pdf_path, 'wb')
        fw.write(r.content)
        fw.close()
    # 上传接口
    fr = open(pdf_path, 'rb')
    file_data = {"file": fr}
    url = produce_url + f"/file/upload/file?type={type}"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    res = requests.post(url=url, headers=headers1, files=file_data)
    result = res.json()
    fr.close()
    os.remove(pdf_path)
    return result.get("value")["file_url"]
# 连接到测试库
conn_test = mysql.connector.connect(
    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
    user="col2024",
    password="Bm_a12a06",
    database="col"
)

cursor_test = conn_test.cursor()

# 查询时间为2024-8-20到2024-8-21之间的数据
cursor_test.execute(
    "select id, page_url, original_pdf, original_img, pdf_url, img_url from col_paper_page where paper = '四川农村日报'")
rows = cursor_test.fetchall()
for id, page_url, original_pdf, original_img, pdf_url, img_url in rows:

    origin_img = original_pdf
    up_img = upload_file_by_url(origin_img, 'sichuan', "jpg", "paper")
    insert_sql = "UPDATE col_paper_page SET original_pdf=%s, original_img=%s,  pdf_url=%s,  img_url=%s WHERE id = %s"
    cursor_test.execute(insert_sql, ('', origin_img, '', up_img, id))
    conn_test.commit()
    print(id, origin_img, up_img)



    # html = etree.HTML(content_html)
    # #
    # title_content = "".join(html.xpath("//div[@class='wznr wow fadeInUp']//text()")).strip()
    # insert_sql = "UPDATE col_paper_notice SET content = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (title_content, id))
    # conn_test.commit()
    # insert_sql = "UPDATE col_paper_notice SET page_url = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (content_url, id))
    # conn_test.commit()

    # delete_sql = "DELETE FROM col_paper_notice WHERE id = %s"
    # cursor_test.execute(delete_sql, (id,))
    # conn_test.commit()




    # title_html = html.xpath("//div[@class='info-lf']/p[@class='info-tit']")
    # info_time = html.xpath("//div[@class='info-cent']/p[@class='info-time tit-16']")
    # content_1 = html.xpath("//div[@class='info-cont tit-16']")
    #
    # content_html = ''
    # for con in title_html:
    #     content_html += etree.tostring(con, encoding='utf-8').decode()
    # for con in info_time:
    #     content_html += etree.tostring(con, encoding='utf-8').decode()
    # for con in content_1:
    #     content_html += etree.tostring(con, encoding='utf-8').decode()
    # insert_sql = "UPDATE col_paper_notice SET content_html = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, (content_html, id))
    # conn_test.commit()

    # content = "山东无棣农村商业银行股份有限公司拟于2024年9月13日通过公开拍卖的方式对合法拥有的以下不良债权进行处置，详情如下：1、借款人吴中尧债权，本金余额0元，欠息合计33617.15元。2、借款人吴中尧债权，本金余额1元，欠息合计120528.03元。现催请上述主从债务人及相关责任人立即履行还款义务，并欢迎符合规定的境内外投资者购买上述债权。以上交易的对象为法人、自然人、其他组织，但农商行内部人员，曾经办上述资产的政法干警、原债务企业的管理人员和参与资产处置工作的律师、会计师等中介机构人员不得购买和变相购买该资产。地址：山东省无棣县海丰十路棣丰支行二楼。电话：0543-6680138监督电话：0543-6360358　特别提示：以上信息仅供参考，相关债权的有关情况请到债权单位进行了解。特此公告。山东无棣农村商业银行股份有限公司2024年9月3日"
    # # img_url_new = upload_file_by_url(original_img, f"{id}", "img", "paper")
    # insert_sql = "UPDATE col_paper_notice SET paper = %s WHERE id = %s"
    # cursor_test.execute(insert_sql, ('浙江省浙商资产管理有限公司', id))
    # conn_test.commit()

cursor_test.close()
conn_test.close()
